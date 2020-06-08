import os
import PyQt5.QtWidgets as qt

# https://doc.qt.io/qtforpython/overviews/qtwidgets-tutorials-addressbook-part1-example.html#part-1-designing-the-user-interface
# TODO! signal changes. Print new file on change. This may need to be set in the main controller class? Alternatively, could add a listener to a VAR here for the main class to watch and take action.


class FileDisplay(qt.QWidget):
    """controls display and file handling for file selection"""

    def __init__(self, parent, startup):
        super().__init__(parent=parent)
        # VARS
        self._var_workingDir = os.path.expanduser(
            "~"
        )  # start home, replace with prev dir after selection
        self.var_selected_abf_files_dict = dict

        # button and display
        self.button_select_abf = qt.QPushButton("Choose file")
        self.listbox_file_list = qt.QListWidget()

        # layout
        self.layout = qt.QVBoxLayout()
        self.layout.addWidget(self.button_select_abf)
        self.layout.addWidget(self.listbox_file_list)
        self.setLayout(self.layout)
        self.startup_dir(startup)

        # Actions

    def startup_dir(self, startup):
        if startup is not None:
            if not os.path.exists(startup):
                print(f"[STARTUP ERROR] provided startup dir does not exist {startup}")
                return
            self._filter_dir(startup)

    def choose_directory(self):
        abf_dir = str(
            qt.QFileDialog.getExistingDirectory(
                self, "Select dir", self._var_workingDir
            )
        )
        if not abf_dir:
            print("[DEBUG] _choose_directory failed")
            return
        self._filter_dir(abf_dir)

    def _filter_dir(self, abf_dir):
        self._var_workingDir = abf_dir
        self.var_selected_abf_files_dict = {
            f: os.path.join(abf_dir, f)
            for f in os.listdir(abf_dir)
            if f.endswith(".abf")
        }
        self._populate_listbox_file_list()

    def _populate_listbox_file_list(self):
        self.listbox_file_list.clear()
        sorted_keys = sorted(self.var_selected_abf_files_dict.keys())
        if len(sorted_keys) == 0:
            self.listbox_file_list.insertItem(0, "No ABFs found")
            return
        for n, f in enumerate(sorted_keys):
            self.listbox_file_list.insertItem(n, f)
        default_selection = self.listbox_file_list.item(0)
        self.listbox_file_list.setCurrentItem(default_selection)
