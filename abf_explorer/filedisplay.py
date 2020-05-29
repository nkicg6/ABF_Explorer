import os
import PyQt5.QtWidgets as qt

DEBUG_DIR = "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/passive_membrane_properties_2019-10-26"

class FileDisplay(qt.QWidget):
    """controls display and file handling for file selection"""

    def __init__(self, parent):
        super().__init__(parent=parent)
        # VARS
        self._var_workingDir = DEBUG_DIR # os.path.expanduser("~") # start home, replace with prev dir after selection
        self.var_selected_abf_files_dict = dict

        # button and display
        self.button_select_abf = qt.QPushButton("Choose file")
        self.listbox_file_list = qt.QListWidget()

        # layout
        self.layout = qt.QVBoxLayout()
        self.layout.addWidget(self.button_select_abf)
        self.layout.addWidget(self.listbox_file_list)
        self.setLayout(self.layout)

        # Actions
        self.button_select_abf.clicked.connect(self._choose_directory)

    def _choose_directory(self):
        abf_dir = str(qt.QFileDialog.getExistingDirectory(self, "Select dir",
                                                          self._var_workingDir))
        if not abf_dir:
            return
        self._filter_dir(abf_dir)

    def _filter_dir(self, abf_dir):
        self._var_workingDir = abf_dir
        self.var_selected_abf_files_dict = {f:os.path.join(abf_dir, f) for f in os.listdir(abf_dir) if f.endswith(".abf")}
        self._populate_listbox_file_list()

    def _populate_listbox_file_list(self):
        self.listbox_file_list.clear()
        sorted_keys = sorted(self.var_selected_abf_files_dict.keys())
        for n,f in enumerate(sorted_keys):
            self.listbox_file_list.insertItem(n,f)