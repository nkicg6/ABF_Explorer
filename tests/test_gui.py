import os
import pytest
import PyQt5.QtWidgets as qt
from abf_explorer import gui
from abf_explorer.args import parser


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


def test_startup_real_dir(abf_files):
    abf_base_dir, _, _, contents = abf_files
    cmd_args = parser.parse_args(["-d", abf_base_dir])
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)
    assert explorer.file_explorer_widget.listbox_file_list.count() == len(contents)


def test_metadata_contents_gui_class(metadata_test_files):
    abf_base_dir, selected_paths_dict, abf_metadata_dict = metadata_test_files
    cmd_args = parser.parse_args(["-d", abf_base_dir])
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)
    assert (
        explorer.file_explorer_widget.listbox_file_list.item(0).text() == "20101001.abf"
    )
    assert explorer.var_current_selection_short_name == "20101001.abf"
    assert explorer.var_selected_abf_files_dict == selected_paths_dict
    assert explorer.var_current_metadata_dict == abf_metadata_dict["20101001.abf"]


def test_metadata_contents_file_display_fields(metadata_test_files):
    abf_base_dir, selected_paths_dict, abf_metadata_dict = metadata_test_files
    cmd_args = parser.parse_args(["-d", abf_base_dir])
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


def test_switch_file_updates_display_fields(metadata_test_files):
    abf_base_dir, selected_paths_dict, abf_metadata_dict = metadata_test_files
    cmd_args = parser.parse_args(["-d", abf_base_dir])
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


def test_metadata_contents_gui_class_changes_on_selection(metadata_test_files):
    abf_base_dir, selected_paths_dict, abf_metadata_dict = metadata_test_files
    cmd_args = parser.parse_args(["-d", abf_base_dir])
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)

    assert (
        explorer.file_explorer_widget.listbox_file_list.item(0).text() == "20101001.abf"
    )
    assert explorer.var_current_selection_short_name == "20101001.abf"
    assert explorer.var_selected_abf_files_dict == selected_paths_dict
    assert explorer.var_current_metadata_dict == abf_metadata_dict["20101001.abf"]
    #### CHANGE SELECTION ####
    explorer.file_explorer_widget.listbox_file_list.setCurrentRow(1)
    #### did metadata update? ####
    assert explorer.var_current_selection_short_name == "20101006.abf"
    assert explorer.var_selected_abf_files_dict == selected_paths_dict
    assert explorer.var_current_metadata_dict == abf_metadata_dict["20101006.abf"]


def test_metadata_contents_gui_class_bad_file(abf_files):
    abf_base_dir, selected_paths_dict, abf_metadata_dict, contents = abf_files
    cmd_args = parser.parse_args(["-d", abf_base_dir])
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)
    assert (
        explorer.file_explorer_widget.listbox_file_list.item(0).text() == "20101001.abf"
    )
    assert (
        explorer.file_explorer_widget.listbox_file_list.selectedItems()[0].text()
        == "20101001.abf"
    )
    assert explorer.var_current_selection_short_name == "20101001.abf"
    assert explorer.var_selected_abf_files_dict == selected_paths_dict
    assert explorer.var_current_metadata_dict == abf_metadata_dict["20101001.abf"]
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
    assert explorer.var_selected_abf_files_dict == selected_paths_dict
    assert explorer.var_current_metadata_dict == abf_metadata_dict["20101002.abf"]
