# TODO update when you write the new class method for abf.Abf
import os
import pytest
import PyQt5.QtWidgets as qt
from abf_explorer import gui
from abf_explorer.fileinfoplotcontrols import FileInfoPlotControls


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


def test_update_metadata_vals():
    DATA = {
        "short_filename": "20101001.abf",
        "protocol": "cc01-steps",
        "sampling_frequency_khz": "20.0",
        "n_sweeps": 24,
        "n_channels": 2,
    }
    fileinfoplotcontrols = FileInfoPlotControls(parent=None)
    fileinfoplotcontrols.update_metadata_vals(DATA)
    assert fileinfoplotcontrols.label_file_info_file_name_val.text() == "20101001.abf"
    assert fileinfoplotcontrols.label_file_info_protocol_val.text() == "cc01-steps"
    assert fileinfoplotcontrols.label_file_info_sampling_frequency_val.text() == "20.0"
    assert (
        fileinfoplotcontrols.combobox_plot_controls_sweep_list.count()
        == DATA["n_sweeps"]
    )
    assert (
        fileinfoplotcontrols.combobox_plot_controls_channel_list.count()
        == DATA["n_channels"]
    )


"""
def test_dirchanged_signal():
    dummy = DummyTester()
    dummy.filedisplaywidget = filedisplay.FileDisplay(parent=dummy)
    dummy.filedisplaywidget.dirchanged.connect(dummy.setSelectionAndDict)
    dummy.filedisplaywidget.on_dir_changed("TEST", "_")
    assert dummy.var_current_selection_short_name == "TEST"
    assert dummy.var_selected_abf_files_dict == "_"

"""
