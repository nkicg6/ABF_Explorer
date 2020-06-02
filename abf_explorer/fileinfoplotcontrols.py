import PyQt5.QtWidgets as qt


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
        self.label_fileInfo_file_name = qt.QLabel("File name:")
        self.label_fileInfo_file_name_val = qt.QLabel("")
        self.label_fileInfo_protocol = qt.QLabel("Protocol:")
        self.label_fileInfo_protocol_val = qt.QLabel("")
        self.label_fileInfo_sampling_frequency = qt.QLabel("Sampling Freq. (kHz):")
        self.label_fileInfo_sampling_frequency_val = qt.QLabel("")

        # layouts
        self.mainLayout = qt.QGridLayout()
        self.fileInfoLayoutForm = qt.QFormLayout()
        self.plotControlsLayout = qt.QVBoxLayout()

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

        self.plotControlsLayout.addWidget(self.button_plotControls_plot)
        self.plotControlsLayout.addWidget(self.button_plotControls_clear_plot)

        self.mainLayout.addWidget(self.fileInfoWidget, 0, 0)
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

    def update_metadata_vals(self, file_metadata_dict):
        try:
            self._update_file_name(file_metadata_dict["short_filename"])
            self._update_sampling_frequency(
                file_metadata_dict["sampling_frequency_khz"]
            )
            self._update_protocol(file_metadata_dict["protocol"])
        except Exception as e:
            print(f"metadata dict: {file_metadata_dict}\n\nError is {e}")
