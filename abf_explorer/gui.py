# pyqt and graph testing
# https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html
# https://doc.qt.io/qt-5/layout.html
# https://pythonbasics.org/pyqt-grid/
# examples python -m pyqtgraph.examples
import os
import numpy as np
import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtc
from PyQt5 import QtGui

from abf_explorer.abf_logging import make_logger
from abf_explorer.filedisplay import FileDisplay
from abf_explorer.fileinfoplotcontrols import FileInfoPlotControls
from abf_explorer.plotting import PlotWidget
from abf_explorer import plotutils
from abf_explorer.abf_analysis import lfpio as lfp


logger = make_logger(__name__)


class ABFExplorer(qt.QMainWindow):
    """main abf explorer class contains all widgets and coordinates all actions"""

    # signals
    metadatachanged = qtc.pyqtSignal(dict)

    def __init__(self, startup_dir=""):
        super().__init__()
        self.startup_dir = startup_dir
        self.centralWidget = qt.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle("ABF explorer v0.1-dev")
        # menu bar
        self.menuBar = self.menuBar()
        self.menuBarAnalysis = self.menuBar.addMenu("&Analysis")
        self.selectLFPIOMenuAction = QtGui.QAction("&LFP IO region", self)
        self.menuBarAnalysis.addAction(self.selectLFPIOMenuAction)
        self.selectLFPRefractoryMenuAction = QtGui.QAction(
            "&LFP refractory periods", self
        )
        self.menuBarAnalysis.addAction(self.selectLFPRefractoryMenuAction)
        self.selectLFP83HzMenuAction = QtGui.QAction("&LFP 83Hz", self)
        self.menuBarAnalysis.addAction(self.selectLFP83HzMenuAction)

        # analysis windows
        self.LFPIOWindow = None

        # vars
        self.var_current_selection_short_name = ""
        self.var_selected_abf_files_dict = {}

        self.var_current_metadata_dict = {}
        self.var_currently_plotted_data = {}
        self.var_x_units_plotted = ""
        self.var_y_units_plotted = ""

        # make widgets and connect signals
        self.plotWidget = PlotWidget(parent=self.centralWidget)
        self._init_file_explorer()
        self._init_file_info_plot_controls()

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

        #### events ####

        # ADD ACTIONS HERE

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
        self.setGeometry(50, 50, 900, 600)
        self.show()

    def _init_file_explorer(self):
        logger.debug("Initializing FileDisplay")
        self.fileExplorerWidget = FileDisplay(parent=self.centralWidget)
        self.fileExplorerWidget.dirchanged.connect(
            self.update_current_directory_and_selection
        )

        if self.startup_dir:
            logger.debug(f"startup dir passed: {self.startup_dir}")
            self.fileExplorerWidget.input_dir(self.startup_dir)

        self.fileExplorerWidget.selectionchanged.connect(
            self.update_current_selection_and_metadata
        )
        return

    def _init_file_info_plot_controls(self):
        logger.debug("Initializing FileInfoPlotControls")
        self.fileInfoPlotControlsWidget = FileInfoPlotControls(
            parent=self.centralWidget
        )
        self.fileInfoPlotControlsWidget.button_plotControls_clear_plot.clicked.connect(
            self.clear_plot
        )
        self.fileInfoPlotControlsWidget.button_plotControls_plot.clicked.connect(
            self.signal_plot_item_called,
        )
        return

    def update_current_directory_and_selection(self, item: tuple):
        current, all_dict = item
        logger.debug(f"setting with selection {current}")
        self.var_current_selection_short_name = current
        logger.debug("setting abf_dict")
        self.var_selected_abf_files_dict = all_dict
        logger.debug("updating metadata")
        item_path = self.var_selected_abf_files_dict.get(
            self.var_current_selection_short_name
        )
        self.var_current_metadata_dict = plotutils.io_get_metadata(item_path)
        logger.debug(f"metadata is: {self.var_current_metadata_dict}")
        return

    def update_current_selection_and_metadata(self, newselection):
        logger.debug(f"updating current selection to {newselection} and metadata")
        self.var_current_selection_short_name = newselection
        item_path = self.var_selected_abf_files_dict.get(
            self.var_current_selection_short_name
        )
        self.var_current_metadata_dict = plotutils.io_get_metadata(item_path)
        return

    def lfp_io_analysis_frame(self):
        logger.debug("raise IO frame")
        self.LFPIOWindow = lfp.LFPIOAnalysis(self, self.var_current_metadata_dict)

    def lfp_refractory_analysis_frame(self):
        logger.debug("Raise refractory!")
        return

    def lfp_83Hz_analysis_frame(self):
        logger.debug("Raise 83Hz")
        return

    def clear_plot(self):
        """clears plot and currently_plotted_items"""
        self.plotWidget.clear_plot()
        self.var_currently_plotted_data = {}
        self.var_y_units_plotted = ""
        return

    def _validate_selection_for_plotting(self):
        valid_current_selection = self.fileExplorerWidget.get_current_selection()
        if not valid_current_selection:
            logger.warning(
                f"No valid current selection found: {valid_current_selection}. Raising AssertionError"
            )
            raise (
                AssertionError(
                    f"No valid current selection found: {valid_current_selection}"
                )
            )
        if self.var_current_selection_short_name != valid_current_selection:
            logger.warning(
                f"{self.var_current_selection} != {valid_current_selection}. Raising AssertionError"
            )
            raise (
                AssertionError(
                    f"{self.var_current_selection} != {valid_current_selection}"
                )
            )
        return

    def signal_plot_item_called(self, *args):
        """called for plotting. Sets vars and gathers data for plot"""
        try:
            self._validate_selection_for_plotting()
        except AssertionError as e:
            logger.exception(e)
            logger.debug("returning due to a validation error")
            return

        (
            sweep_ind,
            channel_ind,
        ) = self.fileInfoPlotControlsWidget.get_sweep_and_channel_plotting_opts()
        logger.debug(
            f"metadata passed to gather data: {self.var_current_metadata_dict}"
        )

        plot_opts = plotutils.io_gather_plot_data(
            self.var_current_metadata_dict, sweep_ind, channel_ind,
        )

        status, fmt_plot_opts = plotutils.check_fmt_opts(
            self.var_currently_plotted_data, plot_opts, self.var_y_units_plotted,
        )
        if status == "unit_error":
            logger.warning(
                f"Unit mismatch, can't reasonably plot '{self.var_y_units_plotted}' together on the same axis"
            )
            return
        if status == "unchanged":
            logger.debug(f"unchanged, continuing")
            return
        if status == "updated":
            logger.debug("updating plot")
            self.var_y_units_plotted = plot_opts["y_units"]
            self.var_currently_plotted_data = fmt_plot_opts
            self.plotWidget.update_plot(plot_opts)
            return
        else:
            logger.warning("problem, no paths taken.")

    def set_linear_selection_region(self, bounds):
        logger.debug("setting linear selection region")
        self.plotWidget.make_linear_region(bounds)

    def get_linear_region_bounds(self):
        logger.debug("returning bounds")
        return list(self.plotWidget.var_linear_region_x_bounds).copy()

    def reset_linear_region(self, bounds):
        logger.debug(f"resetting linear region to {bounds}")
        self.plotWidget.reset_linear_region(bounds)
