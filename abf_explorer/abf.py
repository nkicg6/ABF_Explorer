import os
import numpy as np
import pyabf
from abf_explorer.abf_logging import make_logger

logger = make_logger(__name__)


class Abf(abf_path):
    def __init__():
        logger.debug(f"passed {abf_path}")
        self.abf_path = abf_path
        self.var_plot_data = {
            "short_filename": "",
            "full_path": "",
            "sampling_frequency_khz": "",
            "protocol": "",
            "n_sweeps": 0,
            "n_channels": 0,
            "target_sweep": None,
            "mean_sweeps": False,
            "filtered_sweeps": False,
        }
        validate_path(self.abf_path)

    def _validate_path(path):
        """verify path exists and is an ABF file"""
        if not path.endswith(".abf"):
            logger.warning(f"path must be ABF file, you passed: {path}")
            return self.var_plot_data.copy()
        if not os.path.exists(path):
            logger.warning(f"path: {path} does not exist")
