import PyQt5.QtWidgets as qt

class FileInfoPlotControls(qt.QWidget):
    """class for display of info from selected file and controlling plots. Most complex class."""
    def __init__(self, parent):
        super().__init__(parent=parent)
        # VARS
        # extra layout
        self.fileInfoWidget = qt.QWidget()
        self.plotControlsWidget = qt.QWidget()

        # buttons and displays
        self.button_plotControls_plot = qt.QPushButton("plot")
        self.button_plotControls_clear_plot = qt.QPushButton("clear plot")
        self.button_plotControls_plot.setToolTip("add selected data to the plot ('Tab')")
        self.button_plotControls_clear_plot.setToolTip("clear plot ('c')")

        # layouts
        self.mainLayout = qt.QGridLayout()
        self.fileInfoLayout = qt.QVBoxLayout()#qt.QFormLayout()
        self.plotControlsLayout = qt.QVBoxLayout()

        self.fileInfoLayout.addWidget(qt.QLabel("TEST"))
        self.plotControlsLayout.addWidget(self.button_plotControls_plot)
        self.plotControlsLayout.addWidget(self.button_plotControls_clear_plot)

        self.mainLayout.addWidget(self.fileInfoWidget, 0,0)
        self.mainLayout.addWidget(self.plotControlsWidget, 0,1)


        self.fileInfoWidget.setLayout(self.fileInfoLayout)
        self.plotControlsWidget.setLayout(self.plotControlsLayout)
        self.setLayout(self.mainLayout)
