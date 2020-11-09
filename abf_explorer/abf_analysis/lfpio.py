# LFP io frame
#### DANGER! UNSAFE! TESTING NEEDED! ####
# reaches into parent and plotting stuff. be extra careful.

import json
import os
import PyQt5.QtWidgets as qt
import numpy as np
from abf_explorer.abf_logging import make_logger
from abf_explorer import plotutils

logger = make_logger(__name__)


class LfpIoAnalysis(qt.QWidget):
    def __init__(self, base_ref, init_dict):
        super().__init__()
        logger.debug("initializing")
        self.setWindowTitle("LFP IO Analysis")
        self.parent = None
        self.var_metadata_dict = init_dict.copy()
        self.var_metadata_dict["mean_sweeps"] = True
        self.var_metadata_dict["_lfp_analysis"] = True
        logger.debug(f"init_dict is {self.var_metadata_dict}")
        self.var_offset_initial_stim_ms = 1
        self.var_window_size_ms = 5
        self.var_default_window_x1 = None
        self.var_default_window_x2 = None

        self.var_metadata_dict_plotted = {}

        self.label_peak_direction_label = qt.QLabel("Peak direction:")
        self.combobox_peak_direction_options = qt.QComboBox()
        self.combobox_peak_direction_options.addItems(["-", "+"])
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

        self.button_save_region = qt.QPushButton("Save region...")
        self.button_reset_region = qt.QPushButton("Reset region")

        self.label_status_label = qt.QLabel("Region status:")
        self.label_status_value = qt.QLabel("not saved")

        self.formLayout = qt.QFormLayout()

        self.setGeometry(950, 0, 100, 250)
        self.formLayout.addRow(
            self.label_peak_direction_label, self.combobox_peak_direction_options
        )

        self.formLayout.addRow(self.label_name_label, self.label_name_value)
        # self.formLayout.addRow(self.label_filepath, self.label_filepath_value)
        self.formLayout.addRow(
            self.label_indicies_boundaries_label, self.label_indicies_value
        )
        self.formLayout.addRow(self.label_use_label, self.combobox_use_options)
        self.formLayout.addRow(self.button_reset_region, self.button_save_region)
        self.formLayout.addRow(self.label_status_label, self.label_status_value)

        self.setLayout(self.formLayout)

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

        self.button_reset_region.clicked.connect(self._reset_region)
        self.button_save_region.clicked.connect(self._save_region)

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

    def make_plot_opts(self):
        return plotutils.io_gather_plot_data(self.var_metadata_dict, 0, 0)

    def closeEvent(self, *args):
        logger.debug("")
        self.parent.clear_plot()
        self.parent = None
        self.close()

    def _find_signal_index(self, y):
        y = self.var_metadata_dict_plotted["lfp_stim_data"]
        ind_stim = int(np.where(y > 1)[0])
        logger.debug(f"ind_stim is: {ind_stim}")
        return ind_stim

    def _original_window_indicies(
        self, ind_stim, start_offset_ms, total_len_ms, khz_sampling
    ):
        start = int(ind_stim + (start_offset_ms * khz_sampling))
        stop = int(start + (total_len_ms * khz_sampling))
        return start, stop

    def calculate_original_window_indicies(self, metadata_dict):
        stim_index = self._find_signal_index(metadata_dict["lfp_stim_data"])
        start_ind, stop_ind = self._original_window_indicies(
            stim_index,
            self.var_offset_initial_stim_ms,
            self.var_window_size_ms,
            float(metadata_dict["sampling_frequency_khz"]),
        )
        start_x = metadata_dict["x"][start_ind]
        logger.debug(f"start_x is: {start_x}")
        stop_x = metadata_dict["x"][stop_ind]
        logger.debug(f"stop_x is: {stop_x}")
        return start_x, stop_x

    def _get_peak_direction(self):
        val = self.combobox_peak_direction_options.currentText()
        logger.debug(f"returning current text {val}")
        return val

    def _get_short_file_name_and_path(self):
        short_filename = self.label_name_value.text()
        file_path = self.var_metadata_dict_plotted.get("full_path", "None")
        logger.debug(f"returning: {short_filename}, path is: {file_path}")
        return short_filename, file_path

    def _get_boundaries_as_str(self):
        return self.label_indicies_value.text()

    def _convert_str_boundaries_to_ints(self, str_indicies):
        s1, s2 = str_indicies.split(",")
        return int(s1), int(s2)

    def _get_use_options(self):
        return self.combobox_use_options.currentText()

    def make_export_dict(self):
        export = {}
        short_name, full_path = self._get_short_file_name_and_path()
        str_bounds = self._get_boundaries_as_str()
        low_bound, high_bound = self._convert_str_boundaries_to_ints(str_bounds)

        export["peak_direction"] = self._get_peak_direction()
        export["short_filename"] = short_name
        export["full_path"] = full_path
        export["use_opt"] = self._get_use_options()
        export["start_ind"] = low_bound
        export["stop_ind"] = high_bound
        logger.debug(f"export dict is: {export}")
        return export

    def _start(self):
        logger.debug("")
        # clear plot
        self.parent.clear_plot()
        self.var_metadata_dict_plotted = self.make_plot_opts()
        self.parent.plot_widget.update_plot(self.var_metadata_dict_plotted)
        (
            self.var_default_window_x1,
            self.var_default_window_x2,
        ) = self.calculate_original_window_indicies(self.var_metadata_dict_plotted)
        logger.debug(f"setting plot indicies")
        self.parent.set_linear_selection_region(
            [self.var_default_window_x1, self.var_default_window_x2]
        )
        self.parent.plot_widget.linear_region.sigRegionChangeFinished.connect(
            self.update_linear_region_signal
        )
        new_str = self.fmt_bounds_as_str_indicies(
            [self.var_default_window_x1, self.var_default_window_x2],
            self.var_metadata_dict_plotted,
        )
        self._update_region_label(new_str)
        self.show()

    def update_linear_region_signal(self, *args):
        logger.debug("updating linear region")
        new_region = self._get_new_linear_region_bounds()
        new_str = self.fmt_bounds_as_str_indicies(
            new_region, self.var_metadata_dict_plotted
        )
        self._update_region_label(new_str)

    def fmt_bounds_as_str_indicies(self, vals, metadata):
        x1, x2 = vals
        x1_ind = self._convert_to_indicies(x1, metadata["x"])
        x2_ind = self._convert_to_indicies(x2, metadata["x"])
        return str(x1_ind) + " , " + str(x2_ind)

    def _convert_to_indicies(self, val, real_x):
        logger.debug(f"val passed is {val}\n")
        ind = self._find_nearest(real_x, val)
        logger.debug(f"ind is {ind}")
        return int(ind)

    def _find_nearest(self, array, value):
        # https://stackoverflow.com/a/2566508
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    def _get_new_linear_region_bounds(self):
        return self.parent.get_linear_region_bounds()

    def _update_region_label(self, new_bounds):
        logger.debug(f"setting label to: {new_bounds}")
        self.label_indicies_value.setText(new_bounds)

    def _update_label_saved_status(self):
        self.label_status_value.setText("Saved!")

    def _write_json_file(self, data, path):
        with open(path, "w") as outfile:
            json.dump(data, outfile)
        logger.debug(f"writing json to {path}")

    def _make_save_path(self, orig_path):
        base, name = os.path.split(orig_path)
        new_name = name.replace(".abf", "_io_region.json")
        return os.path.join(base, new_name)

    def _save_region(self, *args):
        logger.debug(f"saving region props")
        export_dict = self.make_export_dict()
        save_path = self._make_save_path(export_dict["full_path"])
        self._write_json_file(export_dict, save_path)
        self._update_label_saved_status()

    def _reset_region(self, *args):
        logger.debug(
            f"resetting region to {self.var_default_window_x1}:{self.var_default_window_x2}"
        )
        self.parent.reset_linear_region(
            [self.var_default_window_x1, self.var_default_window_x2]
        )

    def _show_error(self, message):
        """show if protocol is not correct"""
        self.errorFrame.messagelabel.setText(message)
        self.errorFrame.show()
        logger.debug("")

    def _close_error(self, *args):
        logger.debug("")
        self.errorFrame.close()

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
