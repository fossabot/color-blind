import bunch
import pyglet
import pyglet.gl as gl
import pymunk
import yaml


def rebunch(dictionary):
    """Recursively convert a dictionary to a bunch.

    Keyword arguments:
    dictionary -- the dictionary to covert into a bunch
    """
    if isinstance(dictionary, dict):
        dictionary = bunch.Bunch(dictionary)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                value = rebunch(value)
            dictionary[key] = value
    return dictionary


SETTINGS = rebunch(yaml.load(file('settings.yaml', 'r')))
CONFIG = pyglet.gl.Config(sample_buffers=SETTINGS.opengl.sample_buffers,
                          samples=SETTINGS.opengl.samples)
WINDOW = pyglet.window.Window(width=SETTINGS.window.width,
                              height=SETTINGS.window.height,
                              config=CONFIG)
FPS = pyglet.clock.ClockDisplay()
SPACE = pymunk.Space()
BINDINGS = rebunch({})
PLAYER = rebunch({})
SHAPES = []
KEYS_PRESSED = []


def main():
    """Setup and initialise the application."""
    setup_bindings()
    setup_graphics()
    setup_physics()
    pyglet.clock.schedule_interval(update, 1 / SETTINGS.fps)
    pyglet.app.run()


def setup_bindings():
    """Load the key bindings from the configuration file."""
    for state in yaml.load(file(SETTINGS.paths.bindings, 'r'))['states']:
        state = rebunch(state['state'])
        BINDINGS[state.name] = state


def setup_graphics():
    """Setup OpenGL and related graphical utilities."""
    gl.glClearColor(0.1, 0.1, 0.1, 0.1)


def setup_physics():
    """Setup physics engine and initialise the world space."""
    SPACE.gravity = (SETTINGS.gravity.x, SETTINGS.gravity.y)
    objects = []
    for properties in yaml.load(file(SETTINGS.paths.objects, 'r'))['objects']:
        objects.append(rebunch(properties['object']))
    for properties in objects:
        if properties.type == 'player':
            PLAYER.shape = create_shape(properties)[1]
            PLAYER.shape.body.velocity_limit = properties['velocity_limit']
            PLAYER.properties = properties
        else:
            SHAPES.append(create_shape(properties))


def update(dt):
    """Maintain the game state, inputs, and physical simulation.

    Keyword arguments:
    dt -- the change in time since the previously rendered frame
    """
    if any(k in KEYS_PRESSED for k in BINDINGS.running.movement.left):
        PLAYER.shape.body.apply_impulse((PLAYER.properties.impulse_left, 0))
    if any(k in KEYS_PRESSED for k in BINDINGS.running.movement.right):
        PLAYER.shape.body.apply_impulse((PLAYER.properties.impulse_right, 0))
    if any(k in KEYS_PRESSED for k in BINDINGS.running.movement.jump):
        PLAYER.shape.body.apply_impulse((0, PLAYER.properties.impulse_up))
    SPACE.step(dt)


def create_shape(properties):
    """Delegate the creation of a physical shape to the appropriate function.

    Keyword arguments:
    properties -- the physical informational traits of a shape
    """
    return {
        'player': lambda: create_poly(properties),
        'poly': lambda: create_poly(properties),
        'segment': lambda: create_segment(properties)
    }[properties['type']]()


def create_segment(properties):
    """Create a physical segment based on configuration properties.

    Keyword arguments:
    properties -- the physical informational traits of a shape
    """
    moment = None
    vertices = map(tuple, properties['vertices'])
    if properties['mass'] is not None:
        moment = pymunk.moment_for_segment(properties['mass'],
                                           vertices[0],
                                           vertices[1])
    body = pymunk.Body(properties['mass'], moment)
    body.position = tuple(properties['position'])
    shape = pymunk.Segment(body,
                           vertices[0],
                           vertices[1],
                           float(properties['radius']))
    shape.elasticity = properties['elasticity']
    shape.friction = properties['friction']
    if properties['mass'] is None:
        SPACE.add(shape)
    else:
        SPACE.add(body, shape)
    return properties['type'], shape


def create_poly(properties):
    """Create a physical polygon based on configuration properties.

    Keyword arguments:
    properties -- the physical informational traits of a shape
    """
    moment = None
    vertices = map(tuple, properties['vertices'])
    if properties['mass'] is not None:
        moment = pymunk.moment_for_poly(properties['mass'], vertices)
    body = pymunk.Body(properties['mass'], moment)
    body.position = tuple(properties['position'])
    shape = pymunk.Poly(body, vertices)
    shape.elasticity = properties['elasticity']
    shape.friction = properties['friction']
    if properties['mass'] is None:
        SPACE.add(shape)
    else:
        SPACE.add(body, shape)
    return properties['type'], shape


def draw_rectangle(vertices, position, angle=0):
    """Draw a rectangle using OpenGL based on the provided spacial information.

    Keyword arguments:
    vertices -- points on the rectangle presented in clockwise order
    position -- x and y position to start the operation
    angle -- draw angle in radians (default 0)
    """
    gl.glPushMatrix()
    gl.glTranslatef(position[0], position[1], 0)
    gl.glRotatef(angle * 57.3, 0, 0, 1)
    gl.glBegin(gl.GL_TRIANGLE_STRIP)
    for vertex in vertices[:2] + vertices[:1:-1]:
        gl.glVertex2f(vertex[0], vertex[1])
    gl.glEnd()
    gl.glPopMatrix()


@WINDOW.event
def on_draw():
    """Clear the window on every frame and draw in game objects."""
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glColor3f(0.9, 0.9, 0.9)
    WINDOW.clear()
    FPS.draw()
    draw_rectangle(PLAYER.shape.verts,
                   PLAYER.shape.body.position,
                   PLAYER.shape.body.angle)
    for shape in SHAPES:
        if shape[0] == 'poly':
            draw_rectangle(shape[1].verts,
                           shape[1].body.position,
                           shape[1].body.angle)


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
