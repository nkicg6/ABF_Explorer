# pyqt and graph testing
# https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html
# https://doc.qt.io/qt-5/layout.html
# https://pythonbasics.org/pyqt-grid/
# examples python -m pyqtgraph.examples
# plot item class https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html
# plot customizations for interaction https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html

import os
import numpy as np
import PyQt5.QtWidgets as qt
from PyQt5 import QtCore, QtGui

from abf_logging import make_logger
from filedisplay import FileDisplay
from fileinfoplotcontrols import FileInfoPlotControls
from plotting import PlotWidget
import plotutils
from abf_analysis import lfpio as lfp


logger = make_logger(__name__)


class ABFExplorer:
    """main abf explorer class contains all widgets and coordinates all actions"""

    def __init__(self, startup_dir=""):
        self.mainApp = qt.QApplication([])  # command line flags if parsing
        logger.debug(f"Startup dir is {startup_dir}")
        self.mainWindow = qt.QMainWindow()
        self.centralWidget = qt.QWidget()
        self.mainWindow.setCentralWidget(self.centralWidget)
        self.mainWindow.setWindowTitle("ABF explorer v0.1-dev")
        # menu bar
        self.menuBar = self.mainWindow.menuBar()
        self.menuBarAnalysis = self.menuBar.addMenu("&Analysis")
        self.selectLFPIOMenuAction = QtGui.QAction("&LFP IO region", self.mainWindow)
        self.menuBarAnalysis.addAction(self.selectLFPIOMenuAction)
        self.selectLFPRefractoryMenuAction = QtGui.QAction(
            "&LFP refractory periods", self.mainWindow
        )
        self.menuBarAnalysis.addAction(self.selectLFPRefractoryMenuAction)
        self.selectLFP83HzMenuAction = QtGui.QAction("&LFP 83Hz", self.mainWindow)
        self.menuBarAnalysis.addAction(self.selectLFP83HzMenuAction)

        # vars
        self.var_current_selection_short_name = ""
        self.var_current_selection_full_path = ""
        self.var_selected_abf_files_dict = {}

        self.var_current_metadata_dict = {}
        self.var_currently_plotted_data = {}
        self.var_x_units_plotted = ""
        self.var_y_units_plotted = ""

        # make widgets
        self.plotWidget = PlotWidget(parent=self.centralWidget)
        self.fileExplorerWidget = FileDisplay(parent=self.centralWidget)
        self.fileInfoPlotControlsWidget = FileInfoPlotControls(
            parent=self.centralWidget
        )

        # main widget layout and geometry
        self.mainLayout = qt.QGridLayout()
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 5)
        self.mainLayout.setColumnMinimumWidth(0, 15)
        self.mainLayout.setColumnMinimumWidth(1, 400)

        self.mainLayout.addWidget(self.fileExplorerWidget, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.plotWidget, 0, 1)
        self.mainLayout.addWidget(self.fileInfoPlotControlsWidget, 1, 0, 1, 2)
        self.mainLayout.addWidget(self.fileInfoPlotControlsWidget, 1, 1)
        self.centralWidget.setLayout(self.mainLayout)

        # pass command line args here
        if startup_dir:
            # must run before currentItemChanged is registered
            logger.debug(f"startup directory passed to choose_directory: {startup_dir}")
            self.choose_directory(startup_dir)

        #### events ####

        # file explorer and info actions
        self.fileExplorerWidget.button_select_abf.clicked.connect(self.choose_directory)

        self.fileExplorerWidget.listbox_file_list.currentItemChanged.connect(
            self.signal_file_selection_changed
        )

        # ADD ACTIONS HERE
        self.fileInfoPlotControlsWidget.button_plotControls_clear_plot.clicked.connect(
            self.clear_plot
        )
        self.fileInfoPlotControlsWidget.button_plotControls_plot.clicked.connect(
            self.signal_plot_item_called,
        )
        # analysis actions
        self.selectLFPIOMenuAction.triggered.connect(self.lfp_io_analysis_frame)
        self.selectLFPRefractoryMenuAction.triggered.connect(
            self.lfp_refractory_analysis_frame
        )
        self.selectLFP83HzMenuAction.triggered.connect(self.lfp_83Hz_analysis_frame)

        # keyboard shortcuts
        self.shortcut_update_plot = qt.QShortcut(
            QtGui.QKeySequence("Tab"), self.centralWidget
        )
        self.shortcut_update_plot.activated.connect(self.signal_plot_item_called)

        self.shortcut_lfp_io = qt.QShortcut(
            QtGui.QKeySequence("Ctrl+i"), self.centralWidget
        )
        self.shortcut_lfp_io.activated.connect(self.lfp_io_analysis_frame)

        self.shortcut_clear_plot = qt.QShortcut(
            QtGui.QKeySequence("c"), self.centralWidget
        )
        self.shortcut_clear_plot.activated.connect(self.clear_plot)

        # geometry and run
        self.mainWindow.setGeometry(50, 50, 900, 600)
        self.mainWindow.show()

        self.mainApp.exec_()

    def lfp_io_analysis_frame(self):
        logger.debug("raise IO frame")
        self.LFPIOWindow = lfp.LFPIOAnalysis()

    def lfp_refractory_analysis_frame(self):
        logger.debug("Raise refractory!")

    def lfp_83Hz_analysis_frame(self):
        logger.debug("Raise 83Hz")

    def clear_plot(self):
        """clears plot and currently_plotted_items"""
        self.plotWidget.clear_plot()
        self.var_currently_plotted_data = {}
        self.var_y_units_plotted = ""

    def choose_directory(self, command_line_dir=""):
        """gets data from selected directory. file connected to filedisplay.choose_directory_button_activated"""
        if command_line_dir in ("", False):
            command_line_dir = ""
        logger.debug(f"command_line_dir: {command_line_dir}")
        (
            current_selection,
            selected_file_dict,
        ) = self.fileExplorerWidget.choose_directory_button_activated(command_line_dir)
        self.var_current_selection_short_name = current_selection
        logger.debug(f"setting current_selection: {current_selection}")
        logger.debug("setting current_selection_dict: not printed")
        self.var_current_selection_full_path = selected_file_dict.get(
            current_selection, None
        )
        logger.debug(
            f"setting current_selection_full_path to: {selected_file_dict.get(current_selection, None)}"
        )
        self.var_selected_abf_files_dict = selected_file_dict
        self._update_metadata_vals()

    def signal_file_selection_changed(self, *args):
        """signal when files selection changes. Used to update metadata displayed to user."""
        try:
            # first arg in signal is new selection, second is previous selection
            arg = [arg.text() for arg in args]
        except Exception as e:
            logger.warning(f"signal conversion exception: {e}")
            return
        current_selection = arg[0]
        self.var_current_selection_short_name = current_selection
        logger.debug(f"current selection is: {current_selection}")
        self.var_current_selection_full_path = self.var_selected_abf_files_dict.get(
            current_selection, None
        )
        logger.debug(f"full path is: {self.var_current_selection_full_path}")
        self._update_metadata_vals()

    def _update_metadata_vals(self):
        self.current_metadata_dict = plotutils.io_get_metadata(
            self.var_current_selection_full_path
        )
        logger.debug(f"current metadata is: {self.current_metadata_dict}")
        self.fileInfoPlotControlsWidget.update_metadata_vals(self.current_metadata_dict)

    def signal_plot_item_called(self, *args):
        """called for plotting. Sets vars and gathers data for plot"""
        curr_sel = self.var_current_selection
        assert (
            curr_sel == self.var_current_selection_short_name
        ), f"[signal_plot_item_called] ERROR, curr_sel '{curr_sel}' != var {self.var_current_selection_short_name}"

        print(f"[signal_plot_item_called] current selection is {curr_sel}")
        if not curr_sel:
            print("[signal_plot_item_called] Nothing selected, continuing")
            return None
        (
            sweep_ind,
            channel_ind,
        ) = self.fileInfoPlotControlsWidget.get_sweep_and_channel_plotting_opts()
        plot_opts = plotutils.io_gather_plot_data(
            self.var_current_metadata_map,
            sweep_ind,
            channel_ind,
            mean_sweeps=False,
            filtered_sweeps=False,
        )
        status, fmt_plot_opts = plotutils.check_fmt_opts(
            self.var_currently_plotted_data, plot_opts, self.var_y_units_plotted,
        )
        if status == "unit_error":
            print(
                f"Unit mismatch, can't reasonably plot '{self.var_y_units_plotted}' together on the same axis"
            )
        if status == "unchanged":
            print("[signal_plot_item_called] unchanged, continuing")
            return
        if status == "updated":
            print("[signal_plot_item_called] updating plot")
            self.var_y_units_plotted = plot_opts["y_units"]
            self.var_currently_plotted_data = fmt_plot_opts
            self.plotWidget.update_plot(plot_opts)
            return
        else:
            print("[signal_plot_item_called] problem, no paths taken.")
