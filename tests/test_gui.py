import os
from . import context
import pytest
import PyQt5.QtWidgets as qt
from abf_explorer import gui
from abf_explorer.args import parser

app = qt.QApplication([])

ABF_DATA_DIR = "data/abfs"


def test_startup_no_startup_dir():
    cmd_args = parser.parse_args()
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)
    assert explorer.fileExplorerWidget.listbox_file_list.count() == 0


def test_startup_non_existent_dir():
    cmd_args = parser.parse_args(["-d" "I_dont_exist"])
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)
    assert (
        explorer.fileExplorerWidget.listbox_file_list.item(0).text()
        == "Nothing here..."
    )


def test_startup_real_dir():
    cmd_args = parser.parse_args(["-d", ABF_DATA_DIR])
    explorer = gui.ABFExplorer(startup_dir=cmd_args.startup_dir)
    assert (
        explorer.fileExplorerWidget.listbox_file_list.item(0).text() == "20101001.abf"
    )
    abfs_in_test_dir = sorted(
        [
            os.path.join(ABF_DATA_DIR, f)
            for f in os.listdir(ABF_DATA_DIR)
            if f.endswith(".abf")
        ]
    )
    assert explorer.fileExplorerWidget.listbox_file_list.count() == len(
        abfs_in_test_dir
    )
