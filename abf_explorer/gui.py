# pyqt and graph testing
# https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html
# https://doc.qt.io/qt-5/layout.html
# https://pythonbasics.org/pyqt-grid/
# examples python -m pyqtgraph.examples
# CONVENTIONS!
# if it is a widget, it has widget in the name.

import sys
import random
import numpy as np
import PyQt5.QtWidgets as qt
from PyQt5 import QtCore, QtGui
import pyqtgraph as pg

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class MyWidget(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("abf explorer")
        #self.layout = self.s.QVBoxLayout()
        self.show()


class PlotWidget(pg.GraphicsWindow):
    def __init__(self, parent):
        super().__init__(parent = parent)
        self.x = np.linspace(0,100, 20)
        self.y = np.random.randn(20)
        self.mainPlot = self.addPlot(title="main plot test")

    def plot_points(plotdict):
        self.mainPlot.plot(plotdict['x'], plotdict['y'])

class ABFExplorer:
    def __init__(self, cmdflags):
        self.mainApp = qt.QApplication([]) # command line flags if parsing
        self.mainWindow= qt.QMainWindow()
        self.centralWidget = qt.QWidget()
        self.mainWindow.setCentralWidget(self.centralWidget)

        self.leftSide = qt.QPushButton("Plot")

        self.bottomSide = qt.QLabel()
        self.bottomSide.setText("Bottom side")

        self.plotWidget = PlotWidget(parent=self.centralWidget)
        self.mainWindow.setWindowTitle("abf explorer")
        self.mainLayout = qt.QGridLayout()
        # main widget layout
        self.mainLayout.addWidget(self.leftSide, 0,0)
        self.mainLayout.addWidget(self.plotWidget, 0,1)
        self.mainLayout.addWidget(self.bottomSide, 1,0)
        # another widget
        self.centralWidget.setLayout(self.mainLayout)
        self.mainWindow.setGeometry(50,50,600,400)
        self.mainWindow.show()
        self.mainApp.exec_()

if __name__ == "__main__":
        ABFExplorer(sys.argv)
        print("Closing")
