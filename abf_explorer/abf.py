import os
import numpy as np
import pyabf
from abf_explorer.abf_logging import make_logger

logger = make_logger(__name__)


class Abf:
    def __init__(self, abf_path):
        logger.debug(f"passed {abf_path}")

        self.var_abf_path = ""
        self._var_abf = None
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
            self.var_abf_path = ""
            return
        if not os.path.exists(path):
            err_str = f"path: {path} does not exist"
            logger.warning(err_str)
            self.error = err_str
            self.var_abf_path = ""
            return
        self.error = None
        self.var_abf_path = path

    def return_metadata(self):
        metadata = self._var_plot_data.copy()
        metadata["short_filename"] = os.path.split(self.var_abf_path)[-1].replace(
            ".abf", ""
        )
        metadata["full_path"] = self.var_abf_path
        if self.error:
            return self._var_plot_data.copy()
        try:
            self._var_abf = pyabf.ABF(self.var_abf_path)
        except Exception as e:
            err_str = f"cannot read file : {metadata['full_path']}. likely pyabf error. exception is : {e}"
            metadata["error"] = err_str
            logger.warning(err_str)
            return metadata
        metadata["sampling_frequency_khz"] = str(self._var_abf.dataRate / 1000)
        metadata["protocol"] = str(self._var_abf.protocol)
        metadata["n_sweeps"] = self._var_abf.sweepCount
        metadata["n_channels"] = self._var_abf.channelCount
        logger.debug(f"{metadata}")
        return metadata

    def _get_sweep_and_channel_data(self, channel, sweep):
        self._var_abf.setSweep(channel=channel, sweep=sweep)
        return (
            self._var_abf.sweepX,
            self._var_abf.sweepY,
            self._var_abf.sweepUnitsX,
            self._var_abf.sweepUnitsY,
        )

    def send_plot_data(self, channel, sweep):
        metadata = self.return_metadata()
        metadata["channel"] = channel
        metadata["sweep"] = sweep
        x, y, x_units, y_units = self._get_sweep_and_channel_data(channel, sweep)
        metadata["x"] = x
        metadata["y"] = y
        metadata["x_units"] = x_units
        metadata["y_units"] = y_units
        metadata["name"] = f"{metadata['short_filename']} sweep-{sweep} ch-{channel}"
