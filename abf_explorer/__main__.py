from args import parser
from gui import ABFExplorer


def main():
    cmd_args = parser.parse_args()
    ABFExplorer(startup_dir=cmd_args.startup_dir)
    print("Closing")


if __name__ == "__main__":
    main()
