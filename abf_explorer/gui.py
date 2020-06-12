# pyqt and graph testing
# https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html
# https://doc.qt.io/qt-5/layout.html
# https://pythonbasics.org/pyqt-grid/
# examples python -m pyqtgraph.examples
# plot item class https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html
# plot customizations for interaction https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html
import numpy as np
import PyQt5.QtWidgets as qt
from PyQt5 import QtCore, QtGui

from .filedisplay import FileDisplay
from .fileinfoplotcontrols import FileInfoPlotControls
from .plotting import PlotWidget
from . import plotutils
from abf_explorer.abf_analysis import regionselection


class ABFExplorer:
    """main abf explorer class contains all widgets and coordinates all actions"""

    def __init__(self, startup_dir=None):
        self.mainApp = qt.QApplication([])  # command line flags if parsing
        print(f"startup_dir is {startup_dir}")
        self.mainWindow = qt.QMainWindow()
        self.centralWidget = qt.QWidget()
        self.mainWindow.setCentralWidget(self.centralWidget)
        self.mainWindow.setWindowTitle("ABF explorer v0.1-dev")
        # menu bar
        self.menuBar = self.mainWindow.menuBar()
        self.menuBarAnalysis = self.menuBar.addMenu("&Analysis")
        self.selectRegionMenuAction = QtGui.QAction("&Select Region", self.mainWindow)
        self.menuBarAnalysis.addAction(self.selectRegionMenuAction)
        # vars
        self.var_current_selection_short_name = ""
        self.var_current_selection_full_path = ""
        self.var_current_metadata_map = {}
        self.var_currently_plotted_data = {}
        self.var_x_units_plotted = ""
        self.var_y_units_plotted = ""

        # make widgets
        self.plotWidget = PlotWidget(parent=self.centralWidget)
        self.fileExplorerWidget = FileDisplay(
            parent=self.centralWidget, startup=startup_dir
        )
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

        #### events ####

        # file explorer and info actions
        self.fileExplorerWidget.button_select_abf.clicked.connect(
            self.fileExplorerWidget.choose_directory
        )
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

        self.selectRegionMenuAction.triggered.connect(self.testprint)

        # keyboard shortcuts
        self.shortcut_update_plot = qt.QShortcut(
            QtGui.QKeySequence("Tab"),
            self.fileInfoPlotControlsWidget.button_plotControls_plot,
        )
        self.shortcut_clear_plot = qt.QShortcut(
            QtGui.QKeySequence("c"),
            self.fileInfoPlotControlsWidget.button_plotControls_clear_plot,
        )
        self.shortcut_update_plot.activated.connect(self.signal_plot_item_called)
        self.shortcut_clear_plot.activated.connect(self.clear_plot)

        # geometry and run
        self.mainWindow.setGeometry(50, 50, 900, 600)
        self.mainWindow.show()
        self.mainApp.exec_()

    def testprint(self):
        print("analysis menu!")

    def clear_plot(self):
        """clears plot and currently_plotted_items"""
        self.plotWidget.clear_plot()
        self.var_currently_plotted_data = {}
        self.var_y_units_plotted = ""

    def signal_file_selection_changed(self, *args):
        """signal when files selection changes. Used to update metadata displayed to user."""
        try:
            print(
                f"[signal_file_selection_changed] current selection is {args[0].text()}"
            )
            self.var_current_selection_short_name = args[0].text()
            self.var_current_selection_full_path = self.fileExplorerWidget.var_selected_abf_files_dict.get(
                args[0].text(), "NONE"
            )
            self.var_current_metadata_map = plotutils.io_get_metadata(
                self.var_current_selection_full_path
            )

            self.fileInfoPlotControlsWidget.update_metadata_vals(
                self.var_current_metadata_map
            )
        except AttributeError as e:
            print(f"[signal_file_selection_changed] Exception is: \n{e}\n")
            self.var_current_metadata_map = plotutils.metadata_error(e)
            self.fileInfoPlotControlsWidget.update_metadata_vals(
                self.var_current_metadata_map
            )

    def signal_plot_item_called(self, *args):
        """called for plotting. Sets vars and gathers data for plot"""

        curr_sel = self.fileExplorerWidget.listbox_file_list.selectedItems()[
            0
        ].text()  # CHANGE FOR MULTIPLE SELECTIONS
        assert (
            curr_sel == self.var_current_selection_short_name
        ), f"[signal_plot_item_called] ERROR, curr_sel {curr_sel} != var {self.var_current_selection_short_name}"

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


# if __name__ == "__main__":
#     testfn()
#     cmd_args = parser.parse_args()
#     ABFExplorer(startup_dir=cmd_args.startup_dir)
#     print("Closing")
