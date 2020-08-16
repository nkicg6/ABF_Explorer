"""use pytest-qt for managing qt instances"""
import os
import pytest
import PyQt5.QtWidgets as qt

app = qt.QApplication([])


@pytest.fixture()
def metadata_test_files():
    abf_base_dir = os.path.join("data", "abfs", "metadata-check")
    selected_paths_dict = {
        i: os.path.join(abf_base_dir, i) for i in os.listdir(abf_base_dir)
    }
    abf_metadata_dict = {
        "20101001.abf": {
            "filtered_sweeps": False,
            "full_path": os.path.join(abf_base_dir, "20101001.abf"),
            "mean_sweeps": False,
            "n_channels": 1,
            "n_sweeps": 23,
            "protocol": "cc_01-steps",
            "sampling_frequency_khz": "20.0",
            "short_filename": "20101001",
            "target_sweep": None,
            "error": None,
        },
        "20101006.abf": {
            "filtered_sweeps": False,
            "full_path": os.path.join(abf_base_dir, "20101006.abf"),
            "mean_sweeps": False,
            "n_channels": 1,
            "n_sweeps": 23,
            "protocol": "cc_04-long-steps",
            "sampling_frequency_khz": "20.0",
            "short_filename": "20101006",
            "target_sweep": None,
            "error": None,
        },
    }
    return abf_base_dir, selected_paths_dict, abf_metadata_dict


@pytest.fixture()
def abf_files():
    abf_base_dir = os.path.join("data", "abfs")
    selected_paths_dict = {
        i: os.path.join(abf_base_dir, i)
        for i in os.listdir(abf_base_dir)
        if i.endswith(".abf")
    }
    bad_path = os.path.join(abf_base_dir, "20101002.abf")
    contents = sorted(
        [
            os.path.join(abf_base_dir, f)
            for f in os.listdir(abf_base_dir)
            if f.endswith(".abf")
        ]
    )
    abf_metadata_dict = {
        "20101001.abf": {
            "filtered_sweeps": False,
            "full_path": os.path.join(abf_base_dir, "20101001.abf"),
            "mean_sweeps": False,
            "n_channels": 1,
            "n_sweeps": 23,
            "protocol": "cc_01-steps",
            "sampling_frequency_khz": "20.0",
            "short_filename": "20101001",
            "target_sweep": None,
            "error": None,
        },
        "20101002.abf": {
            "filtered_sweeps": False,
            "full_path": os.path.join(abf_base_dir, "20101002.abf"),
            "mean_sweeps": False,
            "n_channels": 0,
            "n_sweeps": 0,
            "protocol": "",
            "sampling_frequency_khz": "",
            "short_filename": "20101002",
            "target_sweep": None,
            "error": f"cannot read file : {bad_path}. likely pyabf error. exception is : unpack requires a buffer of 253 bytes",
        },
        "20101006.abf": {
            "filtered_sweeps": False,
            "full_path": os.path.join(abf_base_dir, "20101006.abf"),
            "mean_sweeps": False,
            "n_channels": 1,
            "n_sweeps": 23,
            "protocol": "cc_04-long-steps",
            "sampling_frequency_khz": "20.0",
            "short_filename": "20101006",
            "target_sweep": None,
            "error": None,
        },
    }
    return abf_base_dir, selected_paths_dict, abf_metadata_dict, contents


# all_data, all_paths_dict, base_metadata_dir = metadata_test_files
