import os
import numpy as np
import pyabf
from abf_explorer.abf_logging import make_logger

logger = make_logger(__name__)


class Abf:
    def __init__(self, abf_path):
        logger.debug(f"passed {abf_path}")

        self.var_abf_path = None
        self.error = None
        self._var_plot_data = {
            "short_filename": "",
            "full_path": "",
            "sampling_frequency_khz": "",
            "protocol": "",
            "n_sweeps": 0,
            "n_channels": 0,
            "target_sweep": None,
            "mean_sweeps": False,
            "filtered_sweeps": False,
            "error": None,
        }
        self._validate_path(abf_path)

    def _validate_path(self, path):
        """verify path exists and is an ABF file"""

        if not path.endswith(".abf"):
            err_str = f"path: {path} does not end in `.abf`"
            logger.warning(err_str)
            self.error = err_str
            self.var_abf_path = None
            return
        if not os.path.exists(path):
            err_str = f"path: {path} does not exist"
            logger.warning(err_str)
            self.error = err_str
            self.var_abf_path = None
            return
        self.error = None
        self.var_abf_path = path

    def return_metadata(self):
        logger.debug("returning metadata {self.var_metadata}")
        if self.error:
            return self._var_plot_data.copy()
        _abf = pyabf.ABF(self.var_abf_path)
        metadata = self._var_plot_data.copy()
        metadata["short_filename"] = _abf.abfID
        metadata["full_path"] = self.var_abf_path
        metadata["sampling_frequency_khz"] = str(_abf.dataRate / 1000)
        metadata["protocol"] = str(_abf.protocol)
        metadata["n_sweeps"] = _abf.sweepCount
        metadata["n_channels"] = _abf.channelCount
        return metadata

    def send_plot_data(self, channel, sweep):
        pass
