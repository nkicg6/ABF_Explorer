# pyqt and graph testing
# https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html
# https://doc.qt.io/qt-5/layout.html
# https://pythonbasics.org/pyqt-grid/
# examples python -m pyqtgraph.examples
# plot item class https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html
# plot customizations for interaction https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html
# TODO! Make the sample buttons work.
# TODO! add keyboard shortcuts to activate those fns too

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

class PlotWidget(pg.GraphicsWindow):
    def __init__(self, parent):
        super().__init__(parent = parent)
        self.x = np.linspace(0,100, 20)
        self.y = np.random.randn(20)
        self.mainPlot = self.addPlot(title="main plot test")

    def update_plot(self, plotdict):
        self.mainPlot.plot(plotdict['x'], plotdict['y'],
                           name=plotdict['name'])
        self.mainPlot.setTitle(plotdict['name'])
        #self.mainPlot.addLegend()
        print("Plotting called")

    def clear_plot(self, e):
        self.mainPlot.clear()
        print(f"cleared plot")


class FileDisplay(qt.QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.button_plot = qt.QPushButton("plot")
        self.button_plot.setToolTip("add selected data to the plot ('Tab')")
        self.button_clear_plot = qt.QPushButton("clear plot")
        self.button_clear_plot.setToolTip("clear plot ('c')")
        self.layout = qt.QGridLayout()
        self.layout.addWidget(self.button_plot, 0, 0)
        self.layout.addWidget(self.button_clear_plot, 1, 0)
        self.setLayout(self.layout)


class ABFExplorer:
    def __init__(self, cmdflags):
        self.mainApp = qt.QApplication([]) # command line flags if parsing
        self.mainWindow= qt.QMainWindow()
        self.centralWidget = qt.QWidget()
        self.mainWindow.setCentralWidget(self.centralWidget)

        self.leftSide = FileDisplay(parent=self.centralWidget)


        self.bottomSide = qt.QLabel()
        self.bottomSide.setText("Bottom side")

        self.plotWidget = PlotWidget(parent=self.centralWidget)
        self.mainWindow.setWindowTitle("abf explorer")
        self.mainLayout = qt.QGridLayout()
        # main widget layout
        self.mainLayout.addWidget(self.leftSide, 0,0)
        self.mainLayout.addWidget(self.plotWidget, 0,1)
        self.mainLayout.addWidget(self.bottomSide, 1,0)

        # event driven
        self.leftSide.button_clear_plot.clicked.connect(self.plotWidget.clear_plot)
        self.leftSide.button_plot.clicked.connect(self.TEMP_gen_data)
        # another widget
        self.centralWidget.setLayout(self.mainLayout)
        self.mainWindow.setGeometry(50,50,600,400)
        self.mainWindow.show()
        self.mainApp.exec_()

    def TEMP_gen_data(self):
        d = {'x':np.random.randn(20), 'y':np.random.randn(20),
             'name':f'plot item {np.random.randn()}'}
        self.plotWidget.update_plot(d)

if __name__ == "__main__":
        ABFExplorer(sys.argv)
        print("Closing")
