"""This module displays data for file metadata"""
import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtc
from abf_explorer.abf_logging import make_logger


logger = make_logger(__name__)


class FileInfoPlotControls(qt.QWidget):
    """class for display of info from selected file and controlling plots."""

    sendselections = qtc.pyqtSignal(tuple)
    clearplot = qtc.pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        # VARS
        # layout control widgets
        self.file_info_widget = qt.QWidget()
        self.plot_controls_widget = qt.QWidget()

        # buttons and displays
        self.button_plot_controls_plot = qt.QPushButton("plot")
        self.button_plot_controls_plot.setToolTip(
            "add selected data to the plot ('Tab')"
        )
        self.button_plot_controls_plot.clicked.connect(
            self.get_sweep_and_channel_plotting_opts
        )

        self.button_plot_controls_clear_plot = qt.QPushButton("clear plot")
        self.button_plot_controls_clear_plot.setToolTip("clear plot ('c')")
        self.button_plot_controls_clear_plot.clicked.connect(self.emit_clear_plot)

        self.combobox_plot_controls_sweep_list = qt.QComboBox()
        self.combobox_plot_controls_channel_list = qt.QComboBox()

        self.label_file_info_file_name = qt.QLabel("File name:")
        self.label_file_info_file_name_val = qt.QLabel("")
        self.label_file_info_protocol = qt.QLabel("Protocol:")
        self.label_file_info_protocol_val = qt.QLabel("")
        self.label_file_info_sampling_frequency = qt.QLabel("Sampling Freq. (kHz):")
        self.label_file_info_sampling_frequency_val = qt.QLabel("")

        # layouts
        self.main_layout = qt.QGridLayout()
        self.file_info_layout_form = qt.QFormLayout()
        self.plot_controls_layout = qt.QGridLayout()

        self.file_info_layout_form.addRow(
            self.label_file_info_file_name, self.label_file_info_file_name_val
        )
        self.file_info_layout_form.addRow(
            self.label_file_info_protocol, self.label_file_info_protocol_val
        )
        self.file_info_layout_form.addRow(
            self.label_file_info_sampling_frequency,
            self.label_file_info_sampling_frequency_val,
        )
        self.plot_controls_layout.addWidget(
            self.combobox_plot_controls_sweep_list, 0, 0
        )
        self.plot_controls_layout.addWidget(
            self.combobox_plot_controls_channel_list, 1, 0
        )
        self.plot_controls_layout.addWidget(self.button_plot_controls_plot, 0, 1)
        self.plot_controls_layout.addWidget(self.button_plot_controls_clear_plot, 1, 1)

        self.main_layout.addWidget(
            self.file_info_widget, 0, 0, alignment=qtc.Qt.AlignLeft
        )
        self.main_layout.addWidget(self.plot_controls_widget, 0, 1)

        self.file_info_widget.setLayout(self.file_info_layout_form)
        self.plot_controls_widget.setLayout(self.plot_controls_layout)
        self.setLayout(self.main_layout)

    def update_metadata_vals(self, file_metadata_dict):
        self.label_file_info_file_name_val.setText(
            file_metadata_dict.get("short_filename")
        )
        self.label_file_info_protocol_val.setText(file_metadata_dict.get("protocol"))
        self.label_file_info_sampling_frequency_val.setText(
            file_metadata_dict.get("sampling_frequency_khz")
        )
        self.combobox_plot_controls_sweep_list.clear()
        self.combobox_plot_controls_sweep_list.addItems(
            [
                "sweep " + str(sweep)
                for sweep in range(file_metadata_dict.get("n_sweeps", 0))
            ]
        )
        self.combobox_plot_controls_channel_list.clear()
        self.combobox_plot_controls_channel_list.addItems(
            [
                "channel " + str(sweep)
                for sweep in range(file_metadata_dict.get("n_channels", 0))
            ]
        )
        logger.debug("updated metadata")

    def get_sweep_and_channel_plotting_opts(self):
        sweep_ind = self.combobox_plot_controls_sweep_list.currentIndex()
        channel_ind = self.combobox_plot_controls_channel_list.currentIndex()
        self.sendselections.emit((sweep_ind, channel_ind))
        logger.debug(f"emitting tuple sweep: {sweep_ind}, channel: {channel_ind}")

    def emit_clear_plot(self):
        logger.debug("emitting clear plot")
        self.clearplot.emit(True)
