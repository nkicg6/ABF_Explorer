import os
import PyQt5.QtWidgets as qt
from abf_logging import make_logger

# https://doc.qt.io/qtforpython/overviews/qtwidgets-tutorials-addressbook-part1-example.html#part-1-designing-the-user-interface
# TODO! signal changes. Print new file on change. This may need to be set in the main controller class? Alternatively, could add a listener to a VAR here for the main class to watch and take action.

logger = make_logger(__name__)


class FileDisplay(qt.QWidget):
    """controls display and file handling for file selection"""

    def __init__(self, parent):
        super().__init__(parent=parent)
        # VARS
        self._var_workingDir = os.path.expanduser(
            "~"
        )  # start home, replace with prev dir after selection

        # button and display
        self.button_select_abf = qt.QPushButton("Choose folder")
        self.listbox_file_list = qt.QListWidget()

        # layout
        self.layout = qt.QVBoxLayout()
        self.layout.addWidget(self.button_select_abf)
        self.layout.addWidget(self.listbox_file_list)
        self.setLayout(self.layout)

        # Actions

    def choose_directory_button_activated(self, command_line_dir: str = "") -> tuple:
        """sets file listbox and returns current selection and shortname:full-path dict.
        activated when button pushed or on startup with command line --startup-dir or -d. Checks for valid files (abf only now), sets the listbox with the file paths, and returns a tuple of
        returns a tuple with current_selection and a dictionary of
        :param command_line_dir: a string passed from --startup-dir or -d upon app startup, defaults to None.
        :return: a tuple of current_selection and a dictionary where keys are the base file name and vals are the full paths to the files.
        """
        if command_line_dir == "" or command_line_dir == False:
            logger.debug("no command_line_dir passed, opening file dialogue")
            selected_dir = self._choose_directory_button_action()
        if command_line_dir != "":
            logger.debug("command_line_dir passed, continuing with command line dir")
            selected_dir = command_line_dir
        # case when button is cancelled.
        if selected_dir is None:
            logger.debug("button action likely cancelled by user.")
            logger.warning("button action likely cancelled by user.")
            return (None, None)
        selected_file_dict = self._filter_and_make_dict(selected_dir)
        current_selection = self._populate_listbox_file_list(selected_file_dict)
        return (current_selection, selected_file_dict)

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
            return {"Nothing here...": "Bad directory"}
        if not os.path.exists(directory):
            logger.warning(f"Directory does not exist: {directory}")
            return {"Nothing here...": "Bad directory"}
        logger.debug(f"setting working dir to {directory}")
        self._var_workingDir = directory
        abfs = [abf for abf in os.listdir(directory) if abf.endswith("abf")]
        if len(abfs) < 1:
            logger.warning(f"No ABFs found in: {directory}")
            return {"No ABFs found": "No ABFs"}
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
