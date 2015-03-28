import helpers
import logging
import pyglet
import pyglet.gl as gl
import pymunk
import time
import yaml


SETTINGS = helpers.rebunch(yaml.load(file('config/settings.yaml', 'r')))
CONFIG = pyglet.gl.Config(
    sample_buffers=SETTINGS.graphics.opengl.sample_buffers,
    samples=SETTINGS.graphics.opengl.samples)
WINDOW = pyglet.window.Window(width=SETTINGS.graphics.window.width,
                              height=SETTINGS.graphics.window.height,
                              config=CONFIG)
FPS = pyglet.clock.ClockDisplay()
SPACE = pymunk.Space()
BINDINGS = helpers.rebunch({})
KEYS_PRESSED = helpers.rebunch({})
SHAPES = helpers.rebunch({})


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
        state = helpers.rebunch(state)
        BINDINGS[state.name] = state


def setup_graphics():
    """Setup OpenGL and related graphical utilities."""
    gl.glClearColor(*SETTINGS.graphics.background)


def setup_physics():
    """Setup physics engine and initialise the world space."""
    SPACE.gravity = SETTINGS.physics.gravity
    objects = []
    for properties in yaml.load(file(SETTINGS.paths.objects, 'r'))['objects']:
        objects.append(helpers.rebunch(properties))
    for properties in objects:
        if properties.id == -1:
            logging.warning('attempt to create object with no id set')
        else:
            shape = helpers.create_shape(properties.physics)
            helpers.add_shape(SPACE, shape.body, shape)
            SHAPES[properties.id] = helpers.rebunch({
                'shape': shape,
                'properties': properties,
                'collisions': 0
            })
    SPACE.add_collision_handler(0, 1, 
            begin=lambda *x: helpers.add_collision(SHAPES[0], 1),
            separate=lambda *x: helpers.add_collision(SHAPES[0], -1))


def update(dt):
    """Maintain the game state, inputs, and physical simulation.

    Keyword arguments:
    dt -- the change in time since the previously rendered frame
    """
    duration = helpers.get_pressed_duration(KEYS_PRESSED,
                                            BINDINGS.default.actions.left) 
    if duration is not None and SHAPES[0].collisions > 0:
        SHAPES[0].shape.body.apply_impulse(
            (SHAPES[0].properties.physics.impulse.left, 0),
            (0, SHAPES[0].shape.radius))
    duration = helpers.get_pressed_duration(KEYS_PRESSED,
                                            BINDINGS.default.actions.right) 
    if duration is not None and SHAPES[0].collisions > 0:
        SHAPES[0].shape.body.apply_impulse(
            (SHAPES[0].properties.physics.impulse.right, 0),
            (0, SHAPES[0].shape.radius))
    duration = helpers.get_pressed_duration(KEYS_PRESSED, BINDINGS.default.actions.jump) 
    if duration is not None and SHAPES[0].collisions > 0:
        SHAPES[0].shape.body.apply_impulse(
            (0, SHAPES[0].properties.physics.impulse.up))

    SHAPES[0].shape.body.angular_velocity *= SETTINGS.physics.damping
    SPACE.step(dt)


@WINDOW.event
def on_draw():
    """Clear the window on every frame and draw in game objects."""
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glColor4f(*SETTINGS.graphics.background)
    WINDOW.clear()
    FPS.draw()
    for id_, shape in SHAPES.items():
        helpers.draw_shape(shape.shape, shape.properties)


@WINDOW.event
def on_key_press(symbol, modifiers):
    """Add newly pressed keys to the list of pressed keys."""
    KEYS_PRESSED[symbol] = time.time()


@WINDOW.event
def on_key_release(symbol, modifiers):
    """Remove newly release keys to the list of pressed keys."""
    KEYS_PRESSED[symbol] = None


if __name__ == '__main__':
    main()

