import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # hack for absolute imports/tests for now..
import PyQt5.QtWidgets as qt
from .args import parser
from .gui import ABFExplorer
from .abf_logging import make_logger

logger = make_logger(__name__)


def main():
    cmd_args = parser.parse_args()
    app = qt.QApplication([])
    explorer = ABFExplorer(startup_dir=cmd_args.startup_dir)
    sys.exit(app.exec_())


if __name__ == "__main__":
    logger.debug("Starting ABF_Explorer")
    main()
