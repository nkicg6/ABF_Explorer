# LFP io frame
#### DANGER! UNSAFE! TESTING NEEDED! ####
# reaches into parent and plotting stuff. be extra careful.
# TODO Add linear region

import PyQt5.QtWidgets as qt
from abf_logging import make_logger
import plotutils

logger = make_logger(__name__)


class LFPIOAnalysis(qt.QWidget):
    def __init__(self, base_ref, init_dict):
        super().__init__()
        logger.debug("initializing")
        self.parent = None
        self.var_metadata_dict = init_dict.copy()
        self.var_metadata_dict["mean_sweeps"] = True
        self.var_metadata_dict_plotting = {}

        self.label_peak_direction_label = qt.QLabel("Peak direction:")
        self.combobox_peak_direction_options = qt.QComboBox()
        self.combobox_peak_direction_options.addItems(["+", "-"])
        self.label_name_label = qt.QLabel("file:")
        self.label_name_value = qt.QLabel(
            self.var_metadata_dict.get("short_filename", "")
        )
        # self.label_filepath = qt.QLabel("path:")
        # self.label_filepath_value = qt.QLabel(self.var_metadata_dict.get('full_path', ""))
        self.label_indicies_boundaries_label = qt.QLabel("boundaries:")
        self.label_indicies_value = qt.QLabel("")
        self.label_use_label = qt.QLabel("Use?")
        self.combobox_use_options = qt.QComboBox()
        self.combobox_use_options.addItems(["Yes", "Maybe", "No"])

        self.mainLayout = qt.QFormLayout()
        self.setGeometry(950, 0, 100, 250)
        self.mainLayout.addRow(
            self.label_peak_direction_label, self.combobox_peak_direction_options
        )

        self.mainLayout.addRow(self.label_name_label, self.label_name_value)
        # self.mainLayout.addRow(self.label_filepath, self.label_filepath_value)
        self.mainLayout.addRow(
            self.label_indicies_boundaries_label, self.label_indicies_value
        )
        self.mainLayout.addRow(self.label_use_label, self.combobox_use_options)

        self.setLayout(self.mainLayout)

        self.errorFrame = qt.QWidget()
        self.errorFrame.messagelabel = qt.QLabel()
        self.errorFrameLayout = qt.QVBoxLayout()
        self.errorFrame.closeButton = qt.QPushButton("Close")
        self.errorFrameLayout.addWidget(self.errorFrame.messagelabel)
        self.errorFrameLayout.addWidget(self.errorFrame.closeButton)
        self.errorFrame.setLayout(self.errorFrameLayout)
        self.errorFrame.closeButton.clicked.connect(self._close_error)
        # start
        self.validate_dict_and_start(self.var_metadata_dict, base_ref)

    def validate_dict_and_start(self, d, base_ref):
        status, message = self._check_protocol(d["protocol"])
        if status == "Not-valid":
            logger.debug("File selection NOT valid")
            logger.warning("File selection NOT valid")
            self._show_error(message)
        if status == "Valid":
            logger.debug("File selection valid")
            self.parent = base_ref
            self._start()

    def _check_protocol(self, protocol):
        if protocol != "single-pulse-averaged":
            logger.warning(
                f"only single-puse-averaged accepted, you passed: {protocol}"
            )
            return (
                "Not-valid",
                f"only single-puse-averaged accepted, you passed: {protocol}",
            )
        else:
            return ("Valid", "Valid")

    def make_plot_opts(self):
        return plotutils.io_gather_plot_data(self.var_metadata_dict, 0, 0)

    def _start(self):
        logger.debug("")
        # clear plot
        self.parent.clear_plot()
        self.var_metadata_dict_plotted = self.make_plot_opts()
        self.parent.plotWidget.update_plot(self.var_metadata_dict_plotted)
        # place ref region
        self.show()

    def closeEvent(self, *args):
        logger.debug("")
        self.parent.clear_plot()
        self.parent = None
        self.close()

    def _show_error(self, message):
        """show if protocol is not correct"""
        self.errorFrame.messagelabel.setText(message)
        self.errorFrame.show()
        logger.debug("")

    def _close_error(self, *args):
        logger.debug("")
        self.errorFrame.close()
