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

# Include local libraries.
from component import wrapper

# Setup libraries.
capnp.remove_import_hook()
logger = logging.getLogger(__name__)

# Initialise global variables.
CAPNP = {}
COMPONENT = {}
FPS_DISPLAY = None
SETTING = DotMap(yaml.load(open("configuration/settings.yaml", "r")))
WINDOW = pyglet.window.Window(
    width=SETTING.graphics.window.width, height=SETTING.graphics.window.height)
WORLD = None


def setup_logging(path: str, level: int=logging.INFO) -> None:
    """Setup and configure logging environments."""
    if os.path.exists(path):
        with open(path, "r") as handle:
            config = yaml.safe_load(handle.read())
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)


def setup_system() -> None:
    """Setup entities, components, and systems."""
    global CAPNP, WORLD
    CAPNP = DotMap(import_components("component/*.capnp"))
    WORLD = esper.World()
    load_entity('player')


def import_components(glob_path: str) -> Dict[str, object]:
    """Import all of the available components defined in Cap'n Proto."""
    components = {}
    paths = glob.glob(glob_path)
    for path in paths:
        name = os.path.splitext(os.path.basename(path))[0]
        structure = getattr(capnp.load(path), name.capitalize())
        components[name] = structure
    return components


def load_entity(identifier: str) -> None:
    """Load an entity with its components from configuration file."""
    global WORLD
    contents = yaml.load(open("entity/{0}.yaml".format(identifier), "r"))
    entity = WORLD.create_entity()
    for item in contents['components']:
        name, values = list(item.items())[0]
        component = get_component(name, values)
        WORLD.add_component(entity, component)


def get_component(name: str, values: dict={}) -> wrapper.Component:
    """Create an object wrapper around Cap'n Proto component schema."""
    message = CAPNP[name].new_message(**values)
    return getattr(wrapper, name.capitalize())(message)


def setup_graphics() -> None:
    """Setup graphical environment."""
    global FPS_DISPLAY, WINDOW
    FPS_DISPLAY = pyglet.window.FPSDisplay(WINDOW)
    FPS_DISPLAY.label.color = (51, 51, 51, 255)


def update(dt: float) -> None:
    """Update the system based on the delta time."""
    pass


@WINDOW.event
def on_draw() -> None:
    """Draw on the window for each frame."""
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glClearColor(0.5, 0.5, 0.5, 1)
    WINDOW.clear()
    FPS_DISPLAY.draw()

# Start the program execution.
if __name__ == "__main__":
    setup_logging("configuration/logging.yaml")
    setup_system()
    setup_graphics()
    pyglet.clock.schedule_interval(update, 1 / SETTING.graphics.fps)
    pyglet.app.run()
