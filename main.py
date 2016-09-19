#!/usr/bin/env python3

# Include standard libraries.
import glob
import logging.config
import os
from typing import Dict, Tuple, List, Any, Union

# Include third-party libraries.
import capnp
import esper
import pyglet
import pymunk
import yaml
from dotmap import DotMap

# Setup libraries.
capnp.remove_import_hook()
logger = logging.getLogger(__name__)

# Initialise global variables.
CAPNP = {}
FPS_DISPLAY = None
SETTINGS = DotMap(yaml.load(open('configuration/settings.yaml', 'r')))
WINDOW = pyglet.window.Window(width=SETTINGS.graphics.window.width,
                              height=SETTINGS.graphics.window.height)


def setup_logging(path: str, level: int=logging.INFO) -> None:
    if os.path.exists(path):
        with open(path, 'r') as handle:
            config = yaml.safe_load(handle.read())
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)



def setup_system() -> None:
    """Setup entities, components, and systems."""
    global CAPNP
    logger.info("Setting up system.")
    CAPNP = import_components("component/*.capnp")


def import_components(glob_path: str) -> Dict[str, object]:
    """Import all of the available components defined in Cap'n Proto."""
    components = {}
    paths = glob.glob(glob_path)
    for path in paths:
        name = os.path.splitext(os.path.basename(path))[0]
        components[name] = capnp.load(path)
    return components


def setup_graphics() -> None:
    """Setup graphical environment."""
    global FPS_DISPLAY, WINDOW
    FPS_DISPLAY = pyglet.window.FPSDisplay(WINDOW)


@WINDOW.event
def on_draw():
    WINDOW.clear()
    FPS_DISPLAY.draw()


# Start the program execution.
if __name__ == "__main__":
    setup_logging("configuration/logging.yaml")
    setup_system()
    setup_graphics()
    pyglet.app.run()

