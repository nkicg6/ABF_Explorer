import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtc
from abf_explorer.abf_logging import make_logger


logger = make_logger(__name__)


class FileInfoPlotControls(qt.QWidget):
    """class for display of info from selected file and controlling plots. Most complex class."""

    def __init__(self, parent):
        super().__init__(parent=parent)
        # VARS
        # layout control widgets
        self.fileInfoWidget = qt.QWidget()
        self.plotControlsWidget = qt.QWidget()

        # buttons and displays
        self.button_plotControls_plot = qt.QPushButton("plot")
        self.button_plotControls_clear_plot = qt.QPushButton("clear plot")
        self.button_plotControls_plot.setToolTip(
            "add selected data to the plot ('Tab')"
        )
        self.button_plotControls_clear_plot.setToolTip("clear plot ('c')")

        self.combobox_plotControls_sweep_list = qt.QComboBox()
        self.combobox_plotControls_channel_list = qt.QComboBox()

        self.label_fileInfo_file_name = qt.QLabel("File name:")
        self.label_fileInfo_file_name_val = qt.QLabel("")
        self.label_fileInfo_protocol = qt.QLabel("Protocol:")
        self.label_fileInfo_protocol_val = qt.QLabel("")
        self.label_fileInfo_sampling_frequency = qt.QLabel("Sampling Freq. (kHz):")
        self.label_fileInfo_sampling_frequency_val = qt.QLabel("")

        # layouts
        self.mainLayout = qt.QGridLayout()
        self.fileInfoLayoutForm = qt.QFormLayout()
        self.plotControlsLayout = qt.QGridLayout()

        self.fileInfoLayoutForm.addRow(
            self.label_fileInfo_file_name, self.label_fileInfo_file_name_val
        )
        self.fileInfoLayoutForm.addRow(
            self.label_fileInfo_protocol, self.label_fileInfo_protocol_val
        )
        self.fileInfoLayoutForm.addRow(
            self.label_fileInfo_sampling_frequency,
            self.label_fileInfo_sampling_frequency_val,
        )
        self.plotControlsLayout.addWidget(self.combobox_plotControls_sweep_list, 0, 0)
        self.plotControlsLayout.addWidget(self.combobox_plotControls_channel_list, 1, 0)
        self.plotControlsLayout.addWidget(self.button_plotControls_plot, 0, 1)
        self.plotControlsLayout.addWidget(self.button_plotControls_clear_plot, 1, 1)

        self.mainLayout.addWidget(
            self.fileInfoWidget, 0, 0, alignment=QtCore.Qt.AlignLeft
        )
        self.mainLayout.addWidget(self.plotControlsWidget, 0, 1)

        self.fileInfoWidget.setLayout(self.fileInfoLayoutForm)
        self.plotControlsWidget.setLayout(self.plotControlsLayout)
        self.setLayout(self.mainLayout)

    def update_metadata_vals(self, file_metadata_dict):
        self.label_fileInfo_file_name_val.setText(
            file_metadata_dict.get("short_filename")
        )
        self.label_fileInfo_protocol_val.setText(file_metadata_dict.get("protocol"))
        self.label_fileInfo_sampling_frequency_val.setText(
            file_metadata_dict.get("sampling_frequency_khz")
        )
        self.combobox_plotControls_sweep_list.clear()
        self.combobox_plotControls_sweep_list.addItems(
            [
                "sweep " + str(sweep)
                for sweep in range(file_metadata_dict.get("n_sweeps"))
            ]
        )
        self.combobox_plotControls_channel_list.clear()
        self.combobox_plotControls_sweep_list.addItems(
            [
                "channel " + str(sweep)
                for sweep in range(file_metadata_dict.get("n_channels"))
            ]
        )
        logger.debug("updated metadata")

    def get_sweep_and_channel_plotting_opts(self):
        sweep_ind = self.combobox_plotControls_sweep_list.currentIndex()
        channel_ind = self.combobox_plotControls_channel_list.currentIndex()
        logger.debug(f"sweep: {sweep_ind}, channel: {channel_ind}")
        return sweep_ind, channel_ind
