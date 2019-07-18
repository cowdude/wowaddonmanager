import requests
import tempfile
from zipfile import ZipFile
import re
import hashlib
import os.path
import shutil

from . import vendors, config, state
import concurrent.futures


def ensure_safe_to_extract(zf: ZipFile):
    """
    Raises if the zip file contains non alphanumeric root directories.
    Used to detect out of cwd extraction attacks
    """
    for entry in zf.filelist:
        name = entry.filename
        if not name or not re.match(r"[a-zA-Z0-9]", name[0]):
            raise RuntimeError("Zip file %r may be harmful. Aborting" % name)


def md5sum(filename, blocksize=65536):
    "Computes the hex representation of the md5 hash for a given file path"
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()


def check_hash(filename, check):
    "For a given file path, ensures that it matches the given `check` md5 hash"
    result = md5sum(filename)
    if result.lower() != check.lower():
        raise RuntimeError("MD5 hash mismatch: %s != %s" % (result, check))


def unzip(src, dst):
    "Extract the zip file located at `src` path in `dst` path."
    with ZipFile(src, "r") as zf:
        ensure_safe_to_extract(zf)
        zf.extractall(dst)
        return zf.filelist


def install(addon, url, md5, dst):
    "Download and install an addon - internal function"
    print("Downloading: %s" % url)
    req = requests.get(url, allow_redirects=True)
    req.raise_for_status()
    with tempfile.TemporaryDirectory() as tmpdir:
        path = "%s/tmp.zip" % tmpdir
        with open(path, "wb") as f:
            for chunk in req.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print("Checking integrity...")
        check_hash(path, md5)

        delete_addon_files(addon)

        print("Extracting...")
        filelist = unzip(path, dst)
        return filelist


def delete_addon_files(addon):
    "Attempts to cleanup old addon files"
    addons_dir = config.get_addons_dir()
    try:
        info = state.get_addon(addon)
    except KeyError:
        pass
    else:
        filelist = info["files"]
        rootdirs = {f.split(os.path.sep, 1)[0] for f in filelist}
        print("Deleting files of %r" % addon)
        for d in rootdirs:
            path = os.path.join(addons_dir, d)
            print(" - %s" % path)
            shutil.rmtree(path, ignore_errors=True)


def update_addon(addon, vendor="curseforge"):
    addons_dir = config.get_addons_dir()
    api = getattr(vendors, vendor)
    print("%s/%s" % (vendor, addon))
    url, md5 = api.get_info(addon)

    try:
        info = state.get_addon(addon)
    except KeyError:
        info = None

    if not info or info["md5"] != md5:
        filelist = install(addon, url, md5, addons_dir)
        return md5, filelist
    else:
        return None, None


def update_addons():
    addons_dir = config.get_addons_dir()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        print("Looking for updates...")
        print()
        params = [
            (vendor, addon)
            for vendor, addons in config.Storage["addons"].items()
            for addon in addons
        ]
        futures = [
            (a, executor.submit(update_addon, addon=a, vendor=v)) for (v, a) in params
        ]

    print()
    print("Saving state...")
    for addon, future in futures:
        md5, filelist = future.result()
        if md5:
            print("Updated: %s" % addon)
            state.store_addon(addon, md5, filelist)
    state.save()


def add_addon(addon, vendor="curseforge"):
    "Adds the given addon to the user config"
    addon_config = config.Storage["addons"]
    if vendor not in addon_config:
        addon_config[vendor] = []
    print("Adding addon %r" % addon)
    addon_config[vendor] = list(set(addon_config[vendor]) | {addon})
    config.save()


def remove_addon(addon, vendor="curseforge"):
    "Removes the given addon from the user config, delete any installed files, and update the state"
    addons_dir = config.get_addons_dir()
    addon_config = config.Storage["addons"]

    if vendor in addon_config and addon in addon_config[vendor]:
        print("Removing addon %r from config" % addon)
        addon_config[vendor] = [x for x in addon_config[vendor] if x != addon]
        config.save()

    delete_addon_files(addon)

    print("Updating state...")
    try:
        state.drop_addon(addon)
    except KeyError:
        print("Warning: addon was not found in state file: %r" % addon)
    else:
        state.save()


def init():
    config.load()
    state.load()
