import os
import sys

import PyQt5.QtWidgets as qt
from .args import parser
from .gui import ABFExplorer
from .abf_logging import make_logger

logger = make_logger(__name__)

# this is a this is a this is a this is a this is a this is a this is a this is a this is a


def main():
    """main for gui entrypoint"""
    cmd_args = parser.parse_args()
    app = qt.QApplication([])
    explorer = ABFExplorer(startup_dir=cmd_args.startup_dir)
    sys.exit(app.exec_())


if __name__ == "__main__":
    logger.debug("Starting ABF_Explorer")
    main()
