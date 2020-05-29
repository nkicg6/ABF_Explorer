import os
import PyQt5.QtWidgets as qt

DEBUG_DIR = "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/passive_membrane_properties_2019-10-26"

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
