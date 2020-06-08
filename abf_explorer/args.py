# command line options and parsing
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d",
    "--startup-dir",
    dest="startup_dir",
    help="Load ABFs from this directory upon startup.",
)
