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
from pyglet import gl

# Setup libraries.
capnp.remove_import_hook()
logger = logging.getLogger(__name__)

# Initialise global variables.
CAPNP = {}
FPS_DISPLAY = None
SETTINGS = DotMap(yaml.load(open('configuration/settings.yaml', 'r')))
WINDOW = pyglet.window.Window(
    width=SETTINGS.graphics.window.width,
    height=SETTINGS.graphics.window.height)


def setup_logging(path: str, level: int=logging.INFO) -> None:
    """Setup and configure logging environments."""
    if os.path.exists(path):
        with open(path, 'r') as handle:
            config = yaml.safe_load(handle.read())
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)


def setup_system() -> None:
    """Setup entities, components, and systems."""
    global CAPNP
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
    FPS_DISPLAY.label.color = (51, 51, 51, 255)


@WINDOW.event
def on_draw() -> None:
    """Draw on the window for each frame."""
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glClearColor(0.5, 0.5, 0.5, 1)
    WINDOW.clear()
    FPS_DISPLAY.draw()
    pyglet.clock.tick()


def update(dt: float) -> None:
    """Update the system based on the delta time."""
    pass

# Start the program execution.
if __name__ == "__main__":
    setup_logging("configuration/logging.yaml")
    setup_system()
    setup_graphics()
    pyglet.clock.schedule_interval(update, 1 / SETTINGS.graphics.fps)
    pyglet.app.run()
