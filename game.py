import functions
import logging
import pyglet
import pyglet.gl as gl
import pymunk
import time
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
KEYS_PRESSED = functions.rebunch({})
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
    gl.glClearColor(*SETTINGS.graphics.background)


def setup_physics():
    """Setup physics engine and initialise the world space."""
    SPACE.gravity = SETTINGS.physics.gravity
    objects = []
    for properties in yaml.load(file(SETTINGS.paths.objects, 'r'))['objects']:
        objects.append(functions.rebunch(properties))
    for properties in objects:
        if properties.id == -1:
            logging.warning('attempt to create object with no id set')
        elif properties.id == 0:
            #TODO(mraxilus): remove, can identify player by id.
            shape = functions.create_shape(properties.physics)
            functions.add_shape(SPACE, shape.body, shape)
            PLAYER.shape = shape
            PLAYER.properties = properties
            PLAYER.shape.body.velocity_limit = SETTINGS.physics.limit
            PLAYER.collisions = 0
        else:
            shape = functions.create_shape(properties.physics)
            functions.add_shape(SPACE, shape.body, shape)
            SHAPES.append(functions.rebunch({
                'shape': shape,
                'properties': properties
            }))
    SPACE.add_collision_handler(0, 1, 
            begin=lambda *x: add_collision(PLAYER, 1),
            separate=lambda *x: add_collision(PLAYER, -1))


def add_collision(object_, count):
    object_.collisions += count
    return True


def update(dt):
    """Maintain the game state, inputs, and physical simulation.

    Keyword arguments:
    dt -- the change in time since the previously rendered frame
    """
    if is_key_pressed(KEYS_PRESSED, BINDINGS.default.actions.left): 
        PLAYER.shape.body.apply_impulse(
            (PLAYER.properties.physics.impulse.left, 0),
            (0, PLAYER.shape.radius))
    if is_key_pressed(KEYS_PRESSED, BINDINGS.default.actions.right): 
        PLAYER.shape.body.apply_impulse(
            (PLAYER.properties.physics.impulse.right, 0),
            (0, PLAYER.shape.radius))
    duration = get_duration(KEYS_PRESSED, BINDINGS.default.actions.jump) 
    if duration is not None and PLAYER.collisions > 0:
        PLAYER.shape.body.apply_impulse(
            (0, PLAYER.properties.physics.impulse.up))

    PLAYER.shape.body.angular_velocity *= SETTINGS.physics.damping
    queries = SPACE.segment_query(PLAYER.shape.body.position, (1280, 720))
    queries = sorted(queries, key=lambda x: x.t)
    if queries is not None:
        print(queries[1].get_hit_point())
    SPACE.step(dt)


def is_key_pressed(keys_pressed, symbol):
    return symbol in keys_pressed.keys() and keys_pressed[symbol] is not None


def get_duration(keys_pressed, symbol):
    duration = None
    for key, time_start in keys_pressed.items():
        if key == symbol and time_start is not None: 
            duration = time.time() - time_start
    return duration


@WINDOW.event
def on_draw():
    """Clear the window on every frame and draw in game objects."""
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glColor4f(*SETTINGS.graphics.background)
    WINDOW.clear()
    FPS.draw()
    functions.draw_shape(PLAYER.shape, PLAYER.properties)
    for shape in SHAPES:
        functions.draw_shape(shape.shape, shape.properties)


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

