#!/usr/bin/env python3

from datetime import datetime
from time import time
from pathlib import Path
import re
import json


def print_with_timestamp(text):
    print(f"\033[1m{get_iso_time()}:\033[0m {text}")


def get_iso_time(time_in_seconds=None, include_ms=True, remove_colons=False):
    if time_in_seconds:
        time_value = datetime.utcfromtimestamp(time_in_seconds).isoformat()
    else:
        time_value = datetime.utcnow().isoformat()
    if remove_colons:
        time_value = time_value.replace(":", "_")
    return time_value + "Z" if include_ms else time_value[:-7] + "Z"


def get_epoch():
    return int(time())


def extend_filename(original_name, new_suffix, new_ending=None):
    path = Path(original_name)
    if new_ending:
        return "{0}_{2}{1}".format(Path.joinpath(path.parent, path.stem),
                                   new_ending,
                                   new_suffix)
    else:
        return "{0}_{2}{1}".format(Path.joinpath(path.parent, path.stem),
                                   path.suffix,
                                   new_suffix)


def remove_ansi_escapes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub("", text)


def save_labeled_dataset(data, new_filename):
    print(f"Saving labeled dataset to new file {new_filename}.")
    with open(new_filename, "w") as file:
        for entry in data:
            json.dump(entry, file)
            file.write("\n")


def apply_label_to_event(event, label):
    event["misuse"] = label
