import PyQt5.QtWidgets as qt
from PyQt5 import QtCore


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

    def _update_file_name(self, shortfilename):
        self.label_fileInfo_file_name_val.setText(shortfilename)

    def _update_protocol(self, protocol):
        self.label_fileInfo_protocol_val.setText(protocol)

    def _update_sampling_frequency(self, sampling_frequency):
        self.label_fileInfo_sampling_frequency_val.setText(sampling_frequency)

    def _update_sweep_combobox(self, sweep_n):
        self.combobox_plotControls_sweep_list.clear()
        self.combobox_plotControls_sweep_list.addItems(
            ["sweep " + str(sweep) for sweep in range(sweep_n)]
        )

    def _update_channel_combobox(self, channel_n):
        self.combobox_plotControls_channel_list.clear()
        self.combobox_plotControls_channel_list.addItems(
            ["channel " + str(channel) for channel in range(channel_n)]
        )

    def _get_combobox_selections(self):
        curr_channel_ind = self.combobox_plotControls_channel_list.currentIndex()
        curr_sweep_ind = self.combobox_plotControls_sweep_list.currentIndex()
        return curr_sweep_ind, curr_channel_ind

    def update_metadata_vals(self, file_metadata_dict):
        try:
            self._update_file_name(file_metadata_dict["short_filename"])
            self._update_sampling_frequency(
                file_metadata_dict["sampling_frequency_khz"]
            )
            self._update_protocol(file_metadata_dict["protocol"])
            self._update_sweep_combobox(file_metadata_dict["n_sweeps"])
            self._update_channel_combobox(file_metadata_dict["n_channels"])
        except Exception as e:
            print(f"metadata dict: {file_metadata_dict}\n\nError is {e}")

    def get_sweep_and_channel_plotting_opts(self):
        # RETURNS ALL OPTIONS AND CURRENT SELECTIONS. MUST SET DEFAULT SELECTIONS ON SETUP!
        sweep_ind, channel_ind = self._get_combobox_selections()
        return sweep_ind, channel_ind
