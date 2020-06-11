from abf_explorer.args import parser
from abf_explorer.gui import ABFExplorer

if __name__ == "__main__":
    cmd_args = parser.parse_args()
    ABFExplorer(startup_dir=cmd_args.startup_dir)
    print("Closing")
