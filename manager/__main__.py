"""WoW Addon Manager

Usage:
  manager update
  manager add <addon>
  manager remove <addon>

Options:
  -h --help         Show this screen.

"""
from docopt import docopt
from . import manager


def main(args):
    manager.init()
    if args["update"]:
        manager.update_addons()
    elif args["add"]:
        addon = args["<addon>"]
        manager.add_addon(addon)
    elif args["remove"]:
        addon = args["<addon>"]
        manager.remove_addon(addon)
    else:
        raise RuntimeError


if __name__ == "__main__":
    args = docopt(__doc__, version="WoW Addon Manager 0.1")
    main(args)
