#!/usr/bin/env python3

# Include standard libraries.
import glob
import os
from typing import Dict, Tuple, List, Any, Union

# Include third-party libraries.
import capnp
import esper
import pyglet
import pymunk
import yaml

# Setup libraries.
capnp.remove_import_hook()
capnps = {}

# Define types.


def load_components(glob_path: str) -> Dict[str, object]:
    components = {}
    paths = glob.glob(glob_path)
    for path in paths:
        name = os.path.splitext(os.path.basename(path))[0]
        components[name] = capnp.load(path)
    return components


def setup_globals() -> None:
    global capnps
    capnps = load_components("component/*.capnp")
    body = capnps['body'].Body.new_message()


if __name__ == "__main__":
    setup_globals()

