# pyqt and graph testing
# https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html
# https://doc.qt.io/qt-5/layout.html
# https://pythonbasics.org/pyqt-grid/
import sys
import random
import numpy as np
import PyQt5.QtWidgets as qt
from PyQt5 import QtCore, QtGui
import pyqtgraph as pg


class MyWidget(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("abf explorer")
        #self.layout = self.s.QVBoxLayout()
        self.show()

class Main:
    def __init__(self, cmdflags):
        self.mainApp = qt.QApplication([]) # command line flags if parsing
        self.baseWidget = qt.QWidget()
        self.leftSide = qt.QLabel()
        self.leftSide.setText("Left side")
        self.x = np.linspace(0,100, 20)
        self.y = np.random.randn(20)
        self.plotSide = pg.GraphicsWindow(title="test plot window")
        self.plot = self.plotSide.addPlot(title="plot", x=self.x, y=self.y)
        self.baseWidget.setWindowTitle("abf explorer")
        self.baseLayout = qt.QGridLayout()
        self.baseLayout.addWidget(self.leftSide, 0,0)
        self.baseLayout.addWidget(self.plotSide, 0,1)
        # another widget

        self.baseWidget.setLayout(self.baseLayout)
        self.baseWidget.setGeometry(50,50,600,400)
        self.baseWidget.show()
        self.mainApp.exec_()


if __name__ == "__main__":
        Main(sys.argv)
        print("Closing")
