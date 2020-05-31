# pyqt and graph testing
# https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html
# https://doc.qt.io/qt-5/layout.html
# https://pythonbasics.org/pyqt-grid/
# examples python -m pyqtgraph.examples
# plot item class https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html
# plot customizations for interaction https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html
# TODO! setup file info widget, have text input change when selection changes.

import sys
import random
import numpy as np
import PyQt5.QtWidgets as qt
from PyQt5 import QtCore, QtGui
import pyqtgraph as pg

from filedisplay import FileDisplay
from fileinfoplotcontrols import FileInfoPlotControls

pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

class PlotWidget(pg.GraphicsWindow):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.x = np.linspace(0, 100, 20)
        self.y = np.random.randn(20)
        self.mainPlot = self.addPlot(title="main plot test")

    def update_plot(self, plotdict):
        self.mainPlot.plot(plotdict["x"], plotdict["y"], name=plotdict["name"])
        self.mainPlot.setTitle(plotdict["name"])
        # self.mainPlot.addLegend()
        print("Plotting called")

    def clear_plot(self, e=None):
        self.mainPlot.clear()
        self.mainPlot.setTitle("")
        print(f"cleared plot")


class ABFExplorer:
    """main abf explorer class contains all widgets and coordinates all actions"""

    def __init__(self, cmdflags):
        self.mainApp = qt.QApplication([])  # command line flags if parsing
        self.mainWindow = qt.QMainWindow()
        self.centralWidget = qt.QWidget()
        self.mainWindow.setCentralWidget(self.centralWidget)
        self.mainWindow.setWindowTitle("ABF explorer v0.1-dev")

        # make widgets
        self.plotWidget = PlotWidget(parent=self.centralWidget)
        self.fileExplorerWidget = FileDisplay(parent=self.centralWidget)
        self.fileInfoPlotControlsWidget = FileInfoPlotControls(parent=self.centralWidget)

        # main widget layout and geometry
        self.mainLayout = qt.QGridLayout()
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 5)
        self.mainLayout.setColumnMinimumWidth(0, 15)
        self.mainLayout.setColumnMinimumWidth(1, 400)

        self.mainLayout.addWidget(self.fileExplorerWidget, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.plotWidget, 0, 1)
        self.mainLayout.addWidget(self.fileInfoPlotControlsWidget, 1, 0, 1, 2)
        self.mainLayout.addWidget(self.fileInfoPlotControlsWidget, 1,1)
        self.centralWidget.setLayout(self.mainLayout)


        # events
        self.fileInfoPlotControlsWidget.button_plotControls_clear_plot.clicked.connect(
            self.plotWidget.clear_plot
        )
        self.fileInfoPlotControlsWidget.button_plotControls_plot.clicked.connect(self.TEMP_gen_data)

        # keyboard shortcuts
        self.shortcut_update_plot = qt.QShortcut(
            QtGui.QKeySequence("Tab"), self.fileInfoPlotControlsWidget.button_plotControls_plot
        )
        self.shortcut_clear_plot = qt.QShortcut(
            QtGui.QKeySequence("c"), self.fileInfoPlotControlsWidget.button_plotControls_clear_plot
        )
        self.shortcut_update_plot.activated.connect(self.TEMP_gen_data)
        self.shortcut_clear_plot.activated.connect(self.plotWidget.clear_plot)

        # geometry adn run
        self.mainWindow.setGeometry(50, 50, 900, 600)
        self.mainWindow.show()
        self.mainApp.exec_()

    def TEMP_gen_data(self):
        d = {
            "x": np.random.randn(20),
            "y": np.random.randn(20),
            "name": f"plot item {np.random.randn()}",
        }
        self.plotWidget.update_plot(d)


if __name__ == "__main__":
    ABFExplorer(sys.argv)
    print("Closing")
