import functions
import logging
import pyglet
import pyglet.gl as gl
import pymunk
import yaml


SETTINGS = functions.rebunch(yaml.load(file('settings.yaml', 'r')))
CONFIG = pyglet.gl.Config(
    sample_buffers=SETTINGS.graphics.opengl.sample_buffers,
    samples=SETTINGS.graphics.opengl.samples)
WINDOW = pyglet.window.Window(width=SETTINGS.graphics.window.width,
                              height=SETTINGS.graphics.window.height,
                              config=CONFIG)
FPS = pyglet.clock.ClockDisplay()
SPACE = pymunk.Space()
BINDINGS = functions.rebunch({})
PLAYER = functions.rebunch({})
KEYS_PRESSED = []
SHAPES = []


def main():
    """Setup and initialise the application."""
    setup_bindings()
    setup_graphics()
    setup_physics()
    pyglet.clock.schedule_interval(update, 1 / SETTINGS.graphics.fps)
    pyglet.app.run()


def setup_bindings():
    """Load the key bindings from the configuration file."""
    for state in yaml.load(file(SETTINGS.paths.bindings, 'r'))['states']:
        state = functions.rebunch(state)
        BINDINGS[state.name] = state


def setup_graphics():
    """Setup OpenGL and related graphical utilities."""
    gl.glClearColor(0.1, 0.1, 0.1, 0.1)


def setup_physics():
    """Setup physics engine and initialise the world space."""
    SPACE.gravity = (SETTINGS.physics.gravity.x, SETTINGS.physics.gravity.y)
    objects = []
    for properties in yaml.load(file(SETTINGS.paths.objects, 'r'))['objects']:
        objects.append(functions.rebunch(properties))
    for properties in objects:
        if properties.id == -1:
            logging.warning('attempt to create object with no id set')
        elif properties.id == 0:
            logging.warn(properties)
            body, shape = functions.create_shape(properties.physics)
            #TODO(mraxilus): adde body and shape to world space.
            PLAYER.shape = shape
            PLAYER.properties = properties
        else:
            SHAPES.append(functions.create_shape(properties))


def update(dt):
    """Maintain the game state, inputs, and physical simulation.

    Keyword arguments:
    dt -- the change in time since the previously rendered frame
    """
    if any(k in KEYS_PRESSED for k in BINDINGS.default.movement.left):
        PLAYER.shape.body.apply_impulse((PLAYER.properties.impulse_left, 0))
    if any(k in KEYS_PRESSED for k in BINDINGS.default.movement.right):
        PLAYER.shape.body.apply_impulse((PLAYER.properties.impulse_right, 0))
    if any(k in KEYS_PRESSED for k in BINDINGS.default.movement.jump):
        PLAYER.shape.body.apply_impulse((0, PLAYER.properties.impulse_up))
    SPACE.step(dt)


@WINDOW.event
def on_draw():
    """Clear the window on every frame and draw in game objects."""
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glColor3f(0.2, 0.2, 0.2)
    WINDOW.clear()
    FPS.draw()
    LABEL_0.draw()
    LABEL_1.draw()
    LABEL_2.draw()
    draw_rectangle(PLAYER.shape.verts,
                   PLAYER.shape.body.position,
                   PLAYER.shape.body.angle,
                   [0.8, 0.8, 0.8])
    for shape in SHAPES:
        if shape[0]['type'] == 'poly':
            if 'color' in shape[0]:
                draw_rectangle(shape[1].verts,
                               shape[1].body.position,
                               shape[1].body.angle,
                               choose_color(shape[0]['color']))
            else:
                draw_rectangle(shape[1].verts,
                               shape[1].body.position,
                               shape[1].body.angle)


@WINDOW.event
def on_key_press(symbol, modifiers):
    """Add newly pressed keys to the list of pressed keys."""
    if symbol == BINDINGS.running.movement.emit[0]:
        PLAYER.emit = {
            0: 1,
            1: 2,
            2: 0
        }[PLAYER.emit]
    elif symbol not in KEYS_PRESSED:
        KEYS_PRESSED.append(symbol)


@WINDOW.event
def on_key_release(symbol, modifiers):
    """Remove newly release keys to the list of pressed keys."""
    if symbol in KEYS_PRESSED:
        KEYS_PRESSED.remove(symbol)


if __name__ == '__main__':
    main()
