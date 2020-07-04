import os
from . import context
import pytest
import PyQt5.QtWidgets as qt
from abf_explorer import gui
from abf_explorer.fileinfoplotcontrols import FileInfoPlotControls

app = qt.QApplication([])

ABF_DATA_DIR = "data/abfs"
ABF_DATA_DIR_METADATA_CHECK = "data/abfs/metadata-check"


class DefaultParent(qt.QWidget):
    def __init__(self):
        super().__init__()

    pass


class DummyTester(qt.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.var_current_selection_short_name = ""
        self.var_selected_abf_files_dict = ""
        self.kargs = kwargs

    def setSelectionAndDict(self, thing):
        self.var_current_selection_short_name = thing[0]
        self.var_selected_abf_files_dict = thing[-1]

    def setCurrentSelection(self, thing):
        self.var_current_selection_short_name = thing


def test_startup():
    fileinfoplotcontrols = FileInfoPlotControls(parent=None)


"""
def test_dirchanged_signal():
    dummy = DummyTester()
    dummy.filedisplaywidget = filedisplay.FileDisplay(parent=dummy)
    dummy.filedisplaywidget.dirchanged.connect(dummy.setSelectionAndDict)
    dummy.filedisplaywidget.onDirChanged("TEST", "_")
    assert dummy.var_current_selection_short_name == "TEST"
    assert dummy.var_selected_abf_files_dict == "_"
"""
