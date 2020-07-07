"""use pytest-qt for managing qt instances"""
import pytest
import PyQt5.QtWidgets as qt

app = qt.QApplication([])
