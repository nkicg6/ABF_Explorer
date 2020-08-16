"""use pytest-qt for managing qt instances"""
import os
import pytest
import PyQt5.QtWidgets as qt

app = qt.QApplication([])


@pytest.fixture()
def data_files():
    base_path = os.path.join("data", "abfs", "metadata-check")
    all_paths = {i: os.path.join(base_path, i) for i in os.listdir(base_path)}
    selected_abf_files_dict = {
        "20101001.abf": {
            "filtered_sweeps": False,
            "full_path": os.path.join(base_path, "20101001.abf"),
            "mean_sweeps": False,
            "n_channels": 1,
            "n_sweeps": 23,
            "protocol": "cc_01-steps",
            "sampling_frequency_khz": "20.0",
            "short_filename": "20101001",
            "target_sweep": None,
        },
    }
    return selected_abf_files_dict, all_paths
