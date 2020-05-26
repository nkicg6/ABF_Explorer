# pyqt and graph testing
# https://doc.qt.io/qt-5/layout.html
import sys
import random
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
        self.baseWidget.setWindowTitle("abf explorer")
        self.baseWidget.show()
        self.mainApp.exec_()



if __name__ == "__main__":
        Main(sys.argv)
        print("Closing")
