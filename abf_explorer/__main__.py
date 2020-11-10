import os
import sys

import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtc
from abf_explorer.args import parser
from abf_explorer.gui import ABFExplorer
from abf_explorer.abf_logging import make_logger

logger = make_logger(__name__)

qt.QApplication.setAttribute(qtc.Qt.AA_EnableHighDpiScaling, True)


def main():
    """main for gui entrypoint"""
    cmd_args = parser.parse_args()
    app = qt.QApplication([])
    explorer = ABFExplorer(startup_dir=cmd_args.startup_dir)
    sys.exit(app.exec_())


if __name__ == "__main__":
    logger.debug("Starting ABF_Explorer")
    main()
