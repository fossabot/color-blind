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
                              config=CONFIG,
                              resizable=True)
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
            #TODO(mraxilus): remove, can identify player by id.
            body, shape = functions.create_shape(properties.physics)
            shape = functions.add_shape(SPACE, body, shape)
            PLAYER.shape = shape
            PLAYER.properties = properties
            PLAYER.shape.body.velocity_limit = SETTINGS.physics.limit
            PLAYER.shape.body.inertia = pymunk.inf
        else:
            body, shape = functions.create_shape(properties.physics)
            shape = functions.add_shape(SPACE, body, shape)
            SHAPES.append(functions.rebunch({
                'shape': shape,
                'properties': properties
            }))


def update(dt):
    """Maintain the game state, inputs, and physical simulation.

    Keyword arguments:
    dt -- the change in time since the previously rendered frame
    """
    if any(k in KEYS_PRESSED for k in BINDINGS.default.actions.left):
        PLAYER.shape.body.apply_impulse(
            (PLAYER.properties.physics.impulse.left, 0))
    if any(k in KEYS_PRESSED for k in BINDINGS.default.actions.right):
        PLAYER.shape.body.apply_impulse(
            (PLAYER.properties.physics.impulse.right, 0))
    if any(k in KEYS_PRESSED for k in BINDINGS.default.actions.jump):
        PLAYER.shape.body.apply_impulse(
            (0, PLAYER.properties.physics.impulse.up))
    SPACE.step(dt)


@WINDOW.event
def on_draw():
    """Clear the window on every frame and draw in game objects."""
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glColor3f(0.2, 0.2, 0.2)
    WINDOW.clear()
    FPS.draw()
    functions.draw_circle(PLAYER.shape.body.position,
                          PLAYER.shape.radius,
                          PLAYER.properties.graphics.color)
    for shape in SHAPES:
        if shape.properties.physics.type == 'poly':
            functions.draw_rectangle(shape.shape.verts,
                                     shape.shape.body.position,
                                     shape.shape.body.angle,
                                     [0.8, 0.8, 0.8])
        elif shape.properties.physics.type == 'segment':
            functions.draw_segment(shape.shape.body.position,
                                   shape.shape.a,
                                   shape.shape.b,
                                   shape.shape.radius,
                                   [0.8, 0.8, 0.8])


@WINDOW.event
def on_key_press(symbol, modifiers):
    """Add newly pressed keys to the list of pressed keys."""
    if symbol not in KEYS_PRESSED:
        KEYS_PRESSED.append(symbol)


@WINDOW.event
def on_key_release(symbol, modifiers):
    """Remove newly release keys to the list of pressed keys."""
    if symbol in KEYS_PRESSED:
        KEYS_PRESSED.remove(symbol)


if __name__ == '__main__':
    main()
