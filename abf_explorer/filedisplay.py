import os
import PyQt5.QtWidgets as qt

# https://doc.qt.io/qtforpython/overviews/qtwidgets-tutorials-addressbook-part1-example.html#part-1-designing-the-user-interface
# TODO! signal changes. Print new file on change. This may need to be set in the main controller class? Alternatively, could add a listener to a VAR here for the main class to watch and take action.


class FileDisplay(qt.QWidget):
    """controls display and file handling for file selection"""

    def __init__(self, parent):
        super().__init__(parent=parent)
        # VARS
        self._var_workingDir = os.path.expanduser(
            "~"
        )  # start home, replace with prev dir after selection

        # button and display
        self.button_select_abf = qt.QPushButton("Choose file")
        self.listbox_file_list = qt.QListWidget()

        # layout
        self.layout = qt.QVBoxLayout()
        self.layout.addWidget(self.button_select_abf)
        self.layout.addWidget(self.listbox_file_list)
        self.setLayout(self.layout)

        # Actions

    def choose_directory(self):
        abf_dir = str(
            qt.QFileDialog.getExistingDirectory(
                self, "Select dir", self._var_workingDir
            )
        )
        if not abf_dir:
            print("[DEBUG] _choose_directory failed")
            return
        selected_abf_files_dict, current_selection = self.filter_and_select(abf_dir)
        return selected_abf_files_dict, current_selection

    def filter_and_select(self, directory):
        if not os.path.exists(directory):
            print("[filter_and_select] dir does not exist: {directory}")
            return
        selected_abf_files_dict = self._filter_dir(directory)
        current_selection = self._populate_listbox_file_list(selected_abf_files_dict)
        return selected_abf_files_dict, current_selection

    def _filter_dir(self, abf_dir):
        self._var_workingDir = abf_dir
        selected_abf_files_dict = {
            f: os.path.join(abf_dir, f)
            for f in os.listdir(abf_dir)
            if f.endswith(".abf")
        }
        return selected_abf_files_dict

    def _populate_listbox_file_list(self, selected_abf_files_dict):
        self.listbox_file_list.clear()
        sorted_keys = sorted(selected_abf_files_dict.keys())
        if len(sorted_keys) == 0:
            self.listbox_file_list.insertItem(0, "No ABFs found")
            return

        for n, f in enumerate(sorted_keys):
            self.listbox_file_list.insertItem(n, f)
        default_selection = self.listbox_file_list.item(0)
        self.listbox_file_list.setCurrentItem(default_selection)
        return self.listbox_file_list.selectedItems()[0].text()

    def get_current_selection(self):
        return self.listbox_file_list.selectedItems()[0].text()
