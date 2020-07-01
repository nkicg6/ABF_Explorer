from . import context
import pytest
import PyQt5.QtWidgets as qt
from abf_explorer import gui
from abf_explorer.args import parser

app = qt.QApplication([])


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
