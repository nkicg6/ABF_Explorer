import os
import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtc
from abf_explorer.abf_logging import make_logger

# https://doc.qt.io/qtforpython/overviews/qtwidgets-tutorials-addressbook-part1-example.html#part-1-designing-the-user-interface
# TODO! signal changes. Print new file on change. This may need to be set in the main controller class? Alternatively, could add a listener to a VAR here for the main class to watch and take action.

logger = make_logger(__name__)


class FileDisplay(qt.QWidget):
    """controls display and file handling for file selection"""

    # signals
    dirchanged = qtc.pyqtSignal(tuple)
    selectionchanged = qtc.pyqtSignal(str)

    def __init__(self, parent, command_line_dir=""):
        super().__init__(parent=parent)
        # VARS
        self._var_workingDir = os.path.expanduser(
            "~"
        )  # start home, replace with prev dir after selection
        # button and display
        self.button_select_abf = qt.QPushButton("Choose folder")
        self.button_select_abf.clicked.connect(self.choose_directory_button_activated)

        self.listbox_file_list = qt.QListWidget()

        # layout
        self.layout = qt.QVBoxLayout()
        self.layout.addWidget(self.button_select_abf)
        self.layout.addWidget(self.listbox_file_list)
        self.setLayout(self.layout)

        # Actions

        if command_line_dir:
            self.input_dir(command_line_dir)

    def input_dir(self, path):
        current_dicts = self._filter_and_make_dict(path)
        current_selection = self._populate_listbox_file_list(current_dicts)
        self.onDirChanged(current_selection, current_dicts)

    def onDirChanged(self, current_selection, current_dicts):
        logger.debug(f"emitting tuple {(current_selection, current_dicts)}")
        self.dirchanged.emit((current_selection, current_dicts))

    def onSelectionChanged(self):
        pass

    def choose_directory_button_activated(self) -> tuple:
        """sets file listbox and returns current selection and shortname:full-path dict.
        activated when button pushed. Checks for valid files (abf only now), sets the listbox with the file paths
        :param command_line_dir: a string passed from --startup-dir or -d upon app startup, defaults to None.
        :return: a tuple of current_selection and a dictionary where keys are the base file name and vals are the full paths to the files.
        """
        selected_dir = self._choose_directory_button_action()
        # case when button is cancelled.
        if selected_dir is None:
            logger.debug("button action likely cancelled by user.")
            logger.warning("button action likely cancelled by user.")
            self.onDirChanged(None, None)
            return
        self.onDirChanged(self.input_dir(selected_dir))
        return

    def get_current_selection(self) -> str:
        """returns currently selected item from listbox"""
        current_selection = self.listbox_file_list.selectedItems()[0].text()
        if not isinstance(current_selection, str):
            logger.warning(
                f"current selection is not a string, it is type: {type(current_selection)}, id: {current_selection}"
            )
            return None
        logger.debug(f"current selection is: {current_selection}")
        return current_selection

    def _choose_directory_button_action(self):
        logger.debug("Qt dir chooser")
        selected_directory = str(
            qt.QFileDialog.getExistingDirectory(
                self, "Select dir", self._var_workingDir
            )
        )
        if not selected_directory:
            logger.warning(
                f"Failed. selected_directory var is: {selected_directory}. likely cancelled by user"
            )
            return None
        return selected_directory

    def _filter_and_make_dict(self, directory):
        if not directory:
            logger.warning(f"Invalid directory: {directory}")
            return {"No ABFs found": "ABF directory error"}
        if not os.path.exists(directory):
            logger.warning(f"Directory does not exist: {directory}")
            return {"No ABFs found": "ABF directory error"}
        logger.debug(f"setting working dir to {directory}")
        self._var_workingDir = directory
        abfs = [abf for abf in os.listdir(directory) if abf.endswith("abf")]
        if len(abfs) < 1:
            logger.warning(f"No ABFs found in: {directory}")
            return {"Nothing here...": "Bad directory"}
        current_dicts = {f: os.path.join(directory, f) for f in abfs}
        return current_dicts

    def _populate_listbox_file_list(self, selected_abf_files_dict):
        self.listbox_file_list.clear()
        sorted_keys = sorted(selected_abf_files_dict.keys())
        for n, f in enumerate(sorted_keys):
            self.listbox_file_list.insertItem(n, f)
        default_selection = self.listbox_file_list.item(0)
        self.listbox_file_list.setCurrentItem(default_selection)
        return sorted_keys[0]
