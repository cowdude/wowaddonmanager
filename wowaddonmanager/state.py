import yaml
from . import config

State = None


def store_addon(addon, md5, filelist):
    State["installed"][addon] = {"md5": md5, "files": [x.filename for x in filelist]}


def drop_addon(addon):
    del State["installed"][addon]


def load():
    global State
    path = config.get_state_file()
    try:
        with open(path) as f:
            State = yaml.safe_load(f)
    except FileNotFoundError:
        pass

    if not State:
        State = {"installed": {}}


def save():
    path = config.get_state_file()
    with open(path, "w") as f:
        yaml.safe_dump(State, f)


def get_addon(addon):
    return State["installed"][addon]
