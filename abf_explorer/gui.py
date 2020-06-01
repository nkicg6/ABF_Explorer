# pyqt and graph testing
# https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html
# https://doc.qt.io/qt-5/layout.html
# https://pythonbasics.org/pyqt-grid/
# examples python -m pyqtgraph.examples
# plot item class https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html
# plot customizations for interaction https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html


import sys
import random
import numpy as np
import PyQt5.QtWidgets as qt
from PyQt5 import QtCore, QtGui

from filedisplay import FileDisplay
from fileinfoplotcontrols import FileInfoPlotControls
from plotting import PlotWidget
import plotutils


class ABFExplorer:
    """main abf explorer class contains all widgets and coordinates all actions"""

    def __init__(self, cmdflags):
        self.mainApp = qt.QApplication([])  # command line flags if parsing
        self.mainWindow = qt.QMainWindow()
        self.centralWidget = qt.QWidget()
        self.mainWindow.setCentralWidget(self.centralWidget)
        self.mainWindow.setWindowTitle("ABF explorer v0.1-dev")
        # vars
        self.var_current_selection_short_name = str
        self.var_current_selection_full_path = str
        self.var_current_metadata_map = dict

        # make widgets
        self.plotWidget = PlotWidget(parent=self.centralWidget)
        self.fileExplorerWidget = FileDisplay(parent=self.centralWidget)
        self.fileInfoPlotControlsWidget = FileInfoPlotControls(
            parent=self.centralWidget
        )

        # main widget layout and geometry
        self.mainLayout = qt.QGridLayout()
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 5)
        self.mainLayout.setColumnMinimumWidth(0, 15)
        self.mainLayout.setColumnMinimumWidth(1, 400)

        self.mainLayout.addWidget(self.fileExplorerWidget, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.plotWidget, 0, 1)
        self.mainLayout.addWidget(self.fileInfoPlotControlsWidget, 1, 0, 1, 2)
        self.mainLayout.addWidget(self.fileInfoPlotControlsWidget, 1, 1)
        self.centralWidget.setLayout(self.mainLayout)

        #### events ####

        # file explorer and info actions
        self.fileExplorerWidget.button_select_abf.clicked.connect(
            self.fileExplorerWidget.choose_directory
        )
        self.fileExplorerWidget.listbox_file_list.currentItemChanged.connect(
            self.signal_file_selection_changed
        )

        # ADD ACTIONS HERE
        self.fileInfoPlotControlsWidget.button_plotControls_clear_plot.clicked.connect(
            self.plotWidget.clear_plot
        )
        self.fileInfoPlotControlsWidget.button_plotControls_plot.clicked.connect(
            self.TEMP_gen_data
        )

        # keyboard shortcuts
        self.shortcut_update_plot = qt.QShortcut(
            QtGui.QKeySequence("Tab"),
            self.fileInfoPlotControlsWidget.button_plotControls_plot,
        )
        self.shortcut_clear_plot = qt.QShortcut(
            QtGui.QKeySequence("c"),
            self.fileInfoPlotControlsWidget.button_plotControls_clear_plot,
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

    def signal_file_selection_changed(self, *args):
        # https://doc.qt.io/qt-5/qlistwidget.html#itemActivated
        # signal returns a pointer to the [*selection, *previous selection]
        try:
            print(f"current selection is {args[0].text()}")
            self.var_current_selection_short_name = args[0].text()
            self.var_current_selection_full_path = self.fileExplorerWidget.var_selected_abf_files_dict.get(
                args[0].text(), "NONE"
            )
            self.var_current_metadata_map = plotutils.io_get_metadata(
                self.var_current_selection_full_path
            )

            self.fileInfoPlotControlsWidget.update_metadata_vals(
                self.var_current_metadata_map
            )
        except AttributeError as e:
            print(f"[signal_file_selection_changed] Exception is: \n{e}\n")
            self.var_current_metadata_map = plotutils.metadata_error(e)
            self.fileInfoPlotControlsWidget.update_metadata_vals(
                self.var_current_metadata_map
            )


if __name__ == "__main__":
    ABFExplorer(sys.argv)
    print("Closing")
