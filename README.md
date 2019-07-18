### A minimalistic World of Warcraft addons manager, written in python 3.7.

## Motivation

I needed a lightweight and robust way of syncing my addons periodically. I mainly play on Linux.

## How-to:

#### Install dependencies

python >=3.6 and pip.

#### Write a basic configuration

Create the file `~/.wow_addon_manager.yaml` with the following content:

```
addons:
  # Vendor name that will provide the files. Only curseforge is supported right now.
  curseforge:
  # A list of addon names to be installed. They are present in the main page's URL.
  - deadly-boss-mods  # <= https://www.curseforge.com/wow/addons/deadly-boss-mods
  - details
manager:
  # Tell where the state file will be stored. It contains data about installed addon files.
  state file: ~/.wow_addons_state.yaml
wow:
  # Tell where your WoW Interface/AddOns directory is located.
  addons directory: /some/path/to/World of Warcraft/_retail_/Interface/AddOns/
```

#### Install this module

```
$ pip install git+https://github.com/cowdude/wowaddonmanager.git
[...]

$ python -m wowaddonmanager -h
WoW Addon Manager

Usage:
  manager update
  manager add <addon>
  manager remove <addon>

Options:
  -h --help         Show this screen.
```

#### Install or update any missing modules

`$ python -m wowaddonmanager update`


### Known bugs

- Manually removing an addon from the configuration file, then running an `update` will not delete the addon's files.