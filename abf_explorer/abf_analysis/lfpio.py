# LFP io frame
import PyQt5.QtWidgets as qt


class LFPIOAnalysis(qt.QWidget):
    def __init__(self, init_dict):
        super().__init__()
        self.testLabel = qt.QLabel("TEST!")
        self.testLabel2 = qt.QLabel("TEST area!")
        self.mainLayout = qt.QFormLayout()
        self.setGeometry(950, 0, 100, 250)
        self.mainLayout.addRow(self.testLabel, self.testLabel2)
        self.setLayout(self.mainLayout)
        self.show()
