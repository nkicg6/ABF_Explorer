import os
import pytest
import PyQt5.QtWidgets as qt
from abf_explorer import gui
from abf_explorer.args import parser

ABF_DATA_DIR = "data/abfs"
ABF_DATA_DIR_METADATA_CHECK = "data/abfs/metadata-check"


def test_startup_no_startup_dir():
    cmd_args = parser.parse_args([])
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)
    assert explorer.file_explorer_widget.listbox_file_list.count() == 0


def test_startup_non_existent_dir():
    cmd_args = parser.parse_args(["-d" "I_dont_exist"])
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)
    assert (
        explorer.file_explorer_widget.listbox_file_list.item(0).text()
        == "No ABFs found"
    )


def test_startup_real_dir():
    cmd_args = parser.parse_args(["-d", ABF_DATA_DIR])
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)
    assert (
        explorer.file_explorer_widget.listbox_file_list.item(0).text() == "20101001.abf"
    )
    abfs_in_test_dir = sorted(
        [
            os.path.join(ABF_DATA_DIR, f)
            for f in os.listdir(ABF_DATA_DIR)
            if f.endswith(".abf")
        ]
    )
    assert explorer.file_explorer_widget.listbox_file_list.count() == len(
        abfs_in_test_dir
    )


def test_metadata_contents_gui_class(data_files):
    data, all_files_dict = data_files
    cmd_args = parser.parse_args(["-d", ABF_DATA_DIR_METADATA_CHECK])
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)
    assert (
        explorer.file_explorer_widget.listbox_file_list.item(0).text() == "20101001.abf"
    )
    assert explorer.var_current_selection_short_name == "20101001.abf"
    assert explorer.var_selected_abf_files_dict == all_files_dict
    assert explorer.var_current_metadata_dict == data["20101001.abf"]


def test_metadata_contents_file_display_fields():
    cmd_args = parser.parse_args(["-d", ABF_DATA_DIR_METADATA_CHECK])
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)
    test_file_path = os.path.join(ABF_DATA_DIR_METADATA_CHECK, "20101001.abf")
    assert (
        explorer.file_explorer_widget.listbox_file_list.item(0).text() == "20101001.abf"
    )
    assert (
        explorer.file_info_plot_controls_widget.label_file_info_file_name_val.text()
        == "20101001"
    )
    assert (
        explorer.file_info_plot_controls_widget.label_file_info_protocol_val.text()
        == "cc_01-steps"
    )
    assert (
        explorer.file_info_plot_controls_widget.label_file_info_sampling_frequency_val.text()
        == "20.0"
    )


def test_switch_file_updates_display_fields():
    cmd_args = parser.parse_args(["-d", ABF_DATA_DIR_METADATA_CHECK])
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)
    assert (
        explorer.file_explorer_widget.listbox_file_list.item(0).text() == "20101001.abf"
    )
    assert (
        explorer.file_info_plot_controls_widget.label_file_info_file_name_val.text()
        == "20101001"
    )
    assert (
        explorer.file_info_plot_controls_widget.label_file_info_protocol_val.text()
        == "cc_01-steps"
    )
    assert (
        explorer.file_info_plot_controls_widget.label_file_info_sampling_frequency_val.text()
        == "20.0"
    )
    #### CHANGE SELECTION ####
    explorer.file_explorer_widget.listbox_file_list.setCurrentRow(1)
    #### did metadata update? ####
    assert (
        explorer.file_explorer_widget.listbox_file_list.item(1).text() == "20101006.abf"
    )
    assert (
        explorer.file_info_plot_controls_widget.label_file_info_file_name_val.text()
        == "20101006"
    )
    assert (
        explorer.file_info_plot_controls_widget.label_file_info_protocol_val.text()
        == "cc_04-long-steps"
    )
    assert (
        explorer.file_info_plot_controls_widget.label_file_info_sampling_frequency_val.text()
        == "20.0"
    )


def test_metadata_contents_gui_class_changes_on_selection():
    cmd_args = parser.parse_args(["-d", ABF_DATA_DIR_METADATA_CHECK])
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)
    test_file_path1 = os.path.join(ABF_DATA_DIR_METADATA_CHECK, "20101001.abf")
    test_file_path2 = os.path.join(ABF_DATA_DIR_METADATA_CHECK, "20101006.abf")
    selected_abf_files_dict1 = {
        "20101001.abf": test_file_path1,
        "20101006.abf": test_file_path2,
    }

    current_metadata_dict1 = {
        "filtered_sweeps": False,
        "full_path": test_file_path1,
        "mean_sweeps": False,
        "n_channels": 1,
        "n_sweeps": 23,
        "protocol": "cc_01-steps",
        "sampling_frequency_khz": "20.0",
        "short_filename": "20101001",
        "target_sweep": None,
        # "error": None,
    }
    current_metadata_dict2 = {
        "filtered_sweeps": False,
        "full_path": test_file_path2,
        "mean_sweeps": False,
        "n_channels": 1,
        "n_sweeps": 23,
        "protocol": "cc_04-long-steps",
        "sampling_frequency_khz": "20.0",
        "short_filename": "20101006",
        "target_sweep": None,
        "error": None,
    }
    assert (
        explorer.file_explorer_widget.listbox_file_list.item(0).text() == "20101001.abf"
    )
    assert explorer.var_current_selection_short_name == "20101001.abf"
    assert explorer.var_selected_abf_files_dict == selected_abf_files_dict1
    assert explorer.var_current_metadata_dict == current_metadata_dict1
    #### CHANGE SELECTION ####
    explorer.file_explorer_widget.listbox_file_list.setCurrentRow(1)
    #### did metadata update? ####
    assert explorer.var_current_selection_short_name == "20101006.abf"
    assert explorer.var_selected_abf_files_dict == selected_abf_files_dict1
    assert explorer.var_current_metadata_dict == current_metadata_dict2


def test_metadata_contents_gui_class_bad_file():
    cmd_args = parser.parse_args(["-d", ABF_DATA_DIR])
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)
    selected_abf_files_dict = {
        f: os.path.join(ABF_DATA_DIR, f)
        for f in os.listdir(ABF_DATA_DIR)
        if f.endswith(".abf")
    }
    test_file_path1 = os.path.join(ABF_DATA_DIR, "20101001.abf")
    test_bad_file_path = os.path.join(ABF_DATA_DIR, "20101002.abf")
    test_file_path2 = os.path.join(ABF_DATA_DIR, "20101006.abf")

    current_metadata_dict1 = {
        "filtered_sweeps": False,
        "full_path": test_file_path1,
        "mean_sweeps": False,
        "n_channels": 1,
        "n_sweeps": 23,
        "protocol": "cc_01-steps",
        "sampling_frequency_khz": "20.0",
        "short_filename": "20101001",
        "target_sweep": None,
    }
    current_metadata_dict_bad_file = {
        "filtered_sweeps": False,
        "full_path": test_bad_file_path,
        "mean_sweeps": False,
        "n_channels": 0,
        "n_sweeps": 0,
        "protocol": "",
        "sampling_frequency_khz": "",
        "short_filename": "20101002",
        "target_sweep": None,
        "error": None,
    }

    assert (
        explorer.file_explorer_widget.listbox_file_list.item(0).text() == "20101001.abf"
    )
    assert (
        explorer.file_explorer_widget.listbox_file_list.selectedItems()[0].text()
        == "20101001.abf"
    )
    assert explorer.var_current_selection_short_name == "20101001.abf"
    assert explorer.var_selected_abf_files_dict == selected_abf_files_dict
    assert explorer.var_current_metadata_dict == current_metadata_dict1
    #### CHANGE SELECTION ####
    explorer.file_explorer_widget.listbox_file_list.setCurrentRow(1)
    #### did metadata update? ####
    assert (
        explorer.file_explorer_widget.listbox_file_list.item(1).text() == "20101002.abf"
    )
    assert (
        explorer.file_explorer_widget.listbox_file_list.selectedItems()[0].text()
        == "20101002.abf"
    )
    assert explorer.var_current_selection_short_name == "20101002.abf"
    assert explorer.var_selected_abf_files_dict == selected_abf_files_dict
    assert explorer.var_current_metadata_dict == current_metadata_dict_bad_file
