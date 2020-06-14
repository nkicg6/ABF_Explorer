# import logging
from args import parser
from gui import ABFExplorer
from abf_logging import make_logger

logger = make_logger(__name__)


def main():
    print("main")
    cmd_args = parser.parse_args()
    ABFExplorer(startup_dir=cmd_args.startup_dir)


if __name__ == "__main__":
    logger.debug("Starting ABF_Explorer")
    main()
    logger.debug("ABF_Explorer Closing...")
