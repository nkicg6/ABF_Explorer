# pyqt and graph testing
# https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html
# https://doc.qt.io/qt-5/layout.html
# https://pythonbasics.org/pyqt-grid/
# examples python -m pyqtgraph.examples
# plot item class https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html
# plot customizations for interaction https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html
# TODO! choose file widget, more buttons to bottom placeholder.

# CONVENTIONS!
# if it is a widget, it has widget in the name.

import os
import sys
import random
import numpy as np
import PyQt5.QtWidgets as qt
from PyQt5 import QtCore, QtGui
import pyqtgraph as pg

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
DEBUG_DIR = "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/passive_membrane_properties_2019-10-26"

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

    def clear_plot(self, e=None):
        self.mainPlot.clear()
        print(f"cleared plot")


class PlotControls(qt.QWidget):
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


class FileDisplay(qt.QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.layout = qt.QVBoxLayout()
        self._workingDir = DEBUG_DIR # os.path.expanduser("~") # start home, replace with prev dir after selection
        self.selected_abf_files_dict = dict
        self.button_select_abf = qt.QPushButton("Choose file")
        self.tempButton1 = qt.QPushButton("Another button")
        self.layout.addWidget(self.button_select_abf)
        self.layout.addWidget(self.tempButton1)
        self.setLayout(self.layout)
        # file button
        self.button_select_abf.clicked.connect(self._choose_directory)

    def _choose_directory(self):
        abf_dir = str(qt.QFileDialog.getExistingDirectory(self, "Select dir", self._workingDir))
        if not abf_dir:
            return
        self._filter_dir(abf_dir)

    def _filter_dir(self, abf_dir):
        self._workingDir = abf_dir
        self.selected_abf_files_dict = {f:os.path.join(abf_dir, f) for f in os.listdir(abf_dir) if f.endswith(".abf")}
        print(self.selected_abf_files_dict.keys())


class ABFExplorer:
    """main abf explorer class contains all widgets and coordinates all actions"""
    def __init__(self, cmdflags):
        self.mainApp = qt.QApplication([]) # command line flags if parsing
        self.mainWindow= qt.QMainWindow()
        self.centralWidget = qt.QWidget()
        self.mainWindow.setCentralWidget(self.centralWidget)
        self.mainWindow.setWindowTitle("ABF explorer v0.0-dev")

        # make widgets
        self.plotControlWidget= PlotControls(parent=self.centralWidget)
        self.plotWidget = PlotWidget(parent=self.centralWidget)
        self.fileExplorerWidget = FileDisplay(parent=self.centralWidget)

        # main widget layout
        self.mainLayout = qt.QGridLayout()
        self.mainLayout.addWidget(self.fileExplorerWidget, 0,0)
        self.mainLayout.addWidget(self.plotWidget, 0,1)
        self.mainLayout.addWidget(self.plotControlWidget, 1,0)
        self.centralWidget.setLayout(self.mainLayout)

        # events
        self.plotControlWidget.button_clear_plot.clicked.connect(self.plotWidget.clear_plot)
        self.plotControlWidget.button_plot.clicked.connect(self.TEMP_gen_data)

        # keyboard shortcuts
        self.shortcut_update_plot = qt.QShortcut(QtGui.QKeySequence("Tab"),
                                                 self.plotControlWidget.button_plot)
        self.shortcut_clear_plot = qt.QShortcut(QtGui.QKeySequence("c"),
                                                self.plotControlWidget.button_clear_plot)
        self.shortcut_update_plot.activated.connect(self.TEMP_gen_data)
        self.shortcut_clear_plot.activated.connect(self.plotWidget.clear_plot)

        # geometry adn run
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
