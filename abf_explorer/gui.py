"""main GUI interface class"""
# pyqt and graph testing
# https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html
# https://doc.qt.io/qt-5/layout.html
# https://pythonbasics.org/pyqt-grid/
# examples python -m pyqtgraph.examples

import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtc
from PyQt5 import QtGui

import abf_explorer
from abf_explorer.abf_logging import make_logger
from abf_explorer.filedisplay import FileDisplay
from abf_explorer.fileinfoplotcontrols import FileInfoPlotControls
from abf_explorer.plotting import PlotWidget
from abf_explorer import plotutils
from abf_explorer import abf


logger = make_logger(__name__)


class ABFExplorer(qt.QMainWindow):
    """main class contains all widgets and coordinates all actions"""

    # signals
    metadatachanged = qtc.pyqtSignal(dict)
    sendplotdata = qtc.pyqtSignal(dict)

    def __init__(self, startup_dir=""):
        super().__init__()
        self.startup_dir = startup_dir
        self.central_widget = qt.QWidget()
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle(f"ABF Explorer v{abf_explorer.__version__}")
        # TODO menu bar
        # vars
        self.var_current_selection_short_name = ""
        self.var_selected_abf_files_dict = {}

        self.var_current_metadata_dict = {}
        self.var_currently_plotted_data = {}
        self.var_x_units_plotted = ""
        self.var_y_units_plotted = ""

        # make widgets and connect signals
        self._init_plot_widget()
        self._init_file_explorer()
        self._init_file_info_plot_controls()

        # main widget layout and geometry
        self.main_layout = qt.QGridLayout()
        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 5)
        self.main_layout.setColumnMinimumWidth(0, 15)
        self.main_layout.setColumnMinimumWidth(1, 400)

        self.main_layout.addWidget(self.file_explorer_widget, 0, 0, 1, 1)
        self.main_layout.addWidget(self.plot_widget, 0, 1)
        self.main_layout.addWidget(self.file_info_plot_controls_widget, 1, 0, 1, 2)
        self.main_layout.addWidget(self.file_info_plot_controls_widget, 1, 1)
        self.central_widget.setLayout(self.main_layout)

        # keyboard shortcuts

        # geometry and run
        self.setGeometry(50, 50, 900, 600)
        self.show()

    def _init_file_explorer(self):
        logger.debug("Initializing FileDisplay")
        self.file_explorer_widget = FileDisplay(parent=self.central_widget)
        self.file_explorer_widget.dirchanged.connect(
            self.update_current_directory_and_selection
        )

        if self.startup_dir:
            logger.debug(f"startup dir passed: {self.startup_dir}")
            startup_stuff = self.file_explorer_widget.input_dir(self.startup_dir)
            self.update_current_directory_and_selection(startup_stuff)

        self.file_explorer_widget.selectionchanged.connect(
            self.update_current_selection_and_metadata
        )
        return

    def _init_file_info_plot_controls(self):
        logger.debug("Initializing FileInfoPlotControls")
        self.file_info_plot_controls_widget = FileInfoPlotControls(
            parent=self.central_widget
        )

        self.metadatachanged.connect(
            self.file_info_plot_controls_widget.update_metadata_vals
        )
        self.file_info_plot_controls_widget.sendselections.connect(self.send_to_plot)
        self.file_info_plot_controls_widget.clearplot.connect(self.clear_plot)
        self.shortcut_update_plot = qt.QShortcut(
            QtGui.QKeySequence("Tab"), self.central_widget
        )
        self.shortcut_update_plot.activated.connect(
            self.file_info_plot_controls_widget.get_sweep_and_channel_plotting_opts
        )

        self.shortcut_clear_plot = qt.QShortcut(
            QtGui.QKeySequence("c"), self.central_widget
        )
        self.shortcut_clear_plot.activated.connect(
            self.file_info_plot_controls_widget.emit_clear_plot
        )
        self.broadcast_metadata()
        return

    def _init_plot_widget(self):
        logger.debug("Initializing PlotWidget")
        self.plot_widget = PlotWidget(parent=self.central_widget)
        self.sendplotdata.connect(self.plot_widget.update_plot)

    def send_to_plot(self, sweep_and_channel):
        sweep, channel = sweep_and_channel
        logger.debug(f"updating metadata sweep: {sweep} channel: {channel}")
        plot_opts = plotutils.io_gather_plot_data(
            self.var_current_metadata_dict, sweep, channel,
        )

        status, fmt_plot_opts = plotutils.check_fmt_opts(
            self.var_currently_plotted_data, plot_opts, self.var_y_units_plotted,
        )
        if status == "unit_error":
            logger.warning(
                f"Unit mismatch, can't plot '{self.var_y_units_plotted}' on the same axis"
            )
            return
        if status == "unchanged":
            logger.debug("unchanged, continuing")
            return
        if status == "updated":
            logger.debug("updating plot")
            self.var_y_units_plotted = plot_opts["y_units"]
            self.var_currently_plotted_data = fmt_plot_opts
            self.sendplotdata.emit(plot_opts)
            logger.debug(f"emitting {plot_opts}")
            return
        else:
            logger.warning("no paths taken.")

    def broadcast_metadata(self):
        logger.debug("sending metadata")
        self.metadatachanged.emit(self.var_current_metadata_dict.copy())
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
        self.current_selected_object = abf.Abf(item_path)
        self.var_current_metadata_dict = self.current_selected_object.return_metadata()
        logger.debug(f"metadata is: {self.var_current_metadata_dict}")
        return

    def update_current_selection_and_metadata(self, newselection):
        logger.debug(f"updating current selection to {newselection} and metadata")
        self.var_current_selection_short_name = newselection
        item_path = self.var_selected_abf_files_dict.get(
            self.var_current_selection_short_name
        )
        self.current_selected_object = abf.Abf(item_path)
        self.var_current_metadata_dict = self.current_selected_object.return_metadata()
        self.broadcast_metadata()
        return

    def clear_plot(self, *args):
        """clears plot and currently_plotted_items"""
        self.plot_widget.clear_plot()
        self.var_currently_plotted_data = {}
        self.var_y_units_plotted = ""

    def set_linear_selection_region(self, bounds):
        logger.debug("setting linear selection region")
        self.plot_widget.make_linear_region(bounds)

    def get_linear_region_bounds(self):
        logger.debug("returning bounds")
        return list(self.plot_widget.var_linear_region_x_bounds).copy()

    def reset_linear_region(self, bounds):
        logger.debug(f"resetting linear region to {bounds}")
        self.plot_widget.reset_linear_region(bounds)
