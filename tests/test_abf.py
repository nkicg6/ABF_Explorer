import os
import pytest
from abf_explorer.abf import Abf

ABF_DATA_DIR_METADATA_CHECK = "data/abfs/metadata-check"


def test_path_init():
    non_abf_ending = "i/do/not/exist.fake"
    does_not_exist = "i/do/not/exist.abf"
    real_path = os.path.join(ABF_DATA_DIR_METADATA_CHECK, "20101001.abf")
    abf_obj = Abf(non_abf_ending)
    assert abf_obj.error == f"path: {non_abf_ending} does not end in `.abf`"
    assert abf_obj.var_abf_path == ""
    abf_obj = Abf(does_not_exist)
    assert abf_obj.error == f"path: {does_not_exist} does not exist"
    assert abf_obj.var_abf_path == ""
    abf_obj = Abf(real_path)
    assert abf_obj.error == None
    assert abf_obj.var_abf_path == real_path


def test_send_metadata():
    does_not_exist = "i/do/not/exist.abf"
    real_path = os.path.join(ABF_DATA_DIR_METADATA_CHECK, "20101001.abf")
    truth_20101001 = {
        "short_filename": "20101001",
        "full_path": real_path,
        "sampling_frequency_khz": "20.0",
        "protocol": "cc_01-steps",
        "n_sweeps": 23,
        "n_channels": 1,
        "target_sweep": None,
        "mean_sweeps": False,
        "filtered_sweeps": False,
        "error": None,
    }
    abf_obj = Abf(does_not_exist)
    assert abf_obj.return_metadata() == abf_obj._var_plot_data
    abf_obj = Abf(real_path)
    assert abf_obj.return_metadata() == truth_20101001
