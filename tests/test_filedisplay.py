import PyQt5.QtWidgets as qt
from abf_explorer import gui
from abf_explorer import filedisplay
from abf_explorer.args import parser


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
    filedisplaywidget = filedisplay.FileDisplay(parent=None)
    assert True


def test_dirchanged_signal():
    dummy = DummyTester()
    dummy.filedisplaywidget = filedisplay.FileDisplay(parent=dummy)
    dummy.filedisplaywidget.dirchanged.connect(dummy.setSelectionAndDict)
    dummy.filedisplaywidget.on_dir_changed("TEST", "_")
    assert dummy.var_current_selection_short_name == "TEST"
    assert dummy.var_selected_abf_files_dict == "_"


def test_dirchanged_startup_signal(metadata_test_files):
    abf_base_dir, selected_paths_dict, abf_metadata_dict = metadata_test_files
    dummy = DummyTester(command_line_dir=abf_base_dir)
    dummy.filedisplaywidget = filedisplay.FileDisplay(parent=dummy)
    dummy.filedisplaywidget.dirchanged.connect(dummy.setSelectionAndDict)
    dummy.filedisplaywidget.input_dir(dummy.kargs["command_line_dir"])
    assert dummy.var_current_selection_short_name == "20101001.abf"
    assert dummy.var_selected_abf_files_dict == selected_paths_dict
    listboxtest = []
    for i in range(dummy.filedisplaywidget.listbox_file_list.count()):
        listboxtest.append(dummy.filedisplaywidget.listbox_file_list.item(i).text())
    assert len(listboxtest) == len(dummy.var_selected_abf_files_dict.keys())


def test_bad_dir_signal():
    dummy = DummyTester(command_line_dir="not/a/dir")
    dummy.filedisplaywidget = filedisplay.FileDisplay(parent=dummy)
    dummy.filedisplaywidget.dirchanged.connect(dummy.setSelectionAndDict)
    dummy.filedisplaywidget.input_dir(dummy.kargs["command_line_dir"])
    assert dummy.var_current_selection_short_name == "No ABFs found"
    assert dummy.var_selected_abf_files_dict == {"No ABFs found": "ABF directory error"}


def test_file_changed_signal(abf_files):
    abf_base_dir, _, _, contents = abf_files
    dummy = DummyTester()
    dummy.filedisplaywidget = filedisplay.FileDisplay(parent=dummy)
    dummy.filedisplaywidget.dirchanged.connect(dummy.setSelectionAndDict)
    dummy.filedisplaywidget.selectionchanged.connect(dummy.setCurrentSelection)
    dummy.filedisplaywidget.input_dir(abf_base_dir)

    assert dummy.var_current_selection_short_name == "20101001.abf"
    dummy.filedisplaywidget.listbox_file_list.setCurrentRow(1)
    assert dummy.var_current_selection_short_name == "20101002.abf"
    dummy.filedisplaywidget.listbox_file_list.setCurrentRow(0)
    assert dummy.var_current_selection_short_name == "20101001.abf"


# TODO: what happens when file changes?
# make sure this works by filling the listbox. Make sure when a user cancels the dialogue it returns with nothing happening (no signal called), this will be a big refactor of choose_directory_button_activated
# other signal is emitted when the selection is changed and emits the new selection
