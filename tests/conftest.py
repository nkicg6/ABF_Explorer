"""use pytest-qt for managing qt instances"""
import os
import pytest
import PyQt5.QtWidgets as qt

app = qt.QApplication([])


@pytest.fixture()
def metadata_test_files():
    base_metadata_dir = os.path.join("data", "abfs", "metadata-check")
    all_paths_dict = {
        i: os.path.join(base_metadata_dir, i) for i in os.listdir(base_metadata_dir)
    }
    selected_abf_files_dict = {
        "20101001.abf": {
            "filtered_sweeps": False,
            "full_path": os.path.join(base_metadata_dir, "20101001.abf"),
            "mean_sweeps": False,
            "n_channels": 1,
            "n_sweeps": 23,
            "protocol": "cc_01-steps",
            "sampling_frequency_khz": "20.0",
            "short_filename": "20101001",
            "target_sweep": None,
        },
    }
    return selected_abf_files_dict, all_paths_dict, base_metadata_dir
