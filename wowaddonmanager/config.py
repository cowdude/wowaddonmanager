import os.path
import yaml

PATH = os.path.expanduser("~/.wow_addon_manager.yaml")
Storage = None


def load(path=PATH):
    global Storage
    with open(path) as f:
        Storage = yaml.safe_load(f)


def save(path=PATH):
    assert Storage is not None
    with open(path, "w") as f:
        yaml.safe_dump(Storage, f)


def get_state_file():
    return os.path.expanduser(Storage["manager"]["state file"])


def get_addons_dir():
    return os.path.expanduser(Storage["wow"]["addons directory"])

