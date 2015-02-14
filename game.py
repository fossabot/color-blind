from pyglet.gl import *
from pyglet.window import key
import bunch
import pyglet 
import pymunk
import yaml

settings = yaml.load(file('settings.yaml', 'r'))
config = pyglet.gl.Config(sample_buffers=settings['opengl']['sample_buffers'], 
                          samples=settings['opengl']['samples'])
window = pyglet.window.Window(width=settings['window']['width'],
                              height=settings['window']['height'],
                              config=config)
fps = pyglet.clock.ClockDisplay()
space = pymunk.Space()
player = {'movement': None}
shapes = []


def main():
  setup_graphics()
  setup_physics()
  pyglet.clock.schedule_interval(update, 1/settings['fps'])
  pyglet.app.run()


def setup_graphics():
  glClearColor(0.1, 0.1, 0.1, 0.1)


def setup_physics():
  space.gravity = (settings['gravity']['x'], settings['gravity']['y'])
  objects = yaml.load(file(settings['paths']['objects'], 'r'))['objects']
  for properties in (o['object'] for o in objects):
    print(properties)
    if properties['type'] == 'player':
      player['shape'] = create_shape(properties)
      player['shape'][1].body.velocity_limit = properties['velocity_limit']
    else:
      shapes.append(create_shape(properties))


def update(dt):
  if player['movement'] == 'left':
      player['shape'][1].body.apply_impulse((-10, 0))
  if player['movement'] == 'right':
      player['shape'][1].body.apply_impulse((10, 0))
  space.step(dt)


def create_shape(properties):
    return {
        'player': lambda: create_poly(properties),
        'poly': lambda: create_poly(properties),
        'segment': lambda: create_segment(properties)
    }[properties['type']]()


def create_segment(properties):
    global space
    moment = None 
    vertices = map(tuple, properties['vertices'])
    if properties['mass'] is not None:
        moment = pymunk.moment_for_segment(properties['mass'], 
                                           vertices[0],
                                           vertices[1])
    body = pymunk.Body(properties['mass'], moment)
    body.position = tuple(properties['position'])
    shape = pymunk.Segment(body, vertices[0], vertices[1], float(properties['radius']))
    shape.elasticity = properties['elasticity']
    shape.friction = properties['friction']
    if properties['mass'] is None:
        space.add(shape)
    else:
        space.add(body, shape)
    return properties['type'], shape


def create_poly(properties):
    global space
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
        space.add(shape)
    else:
        space.add(body, shape)
    return properties['type'], shape


def draw_rectangle(vertices, position, angle=0):
  glPushMatrix()
  glTranslatef(position[0], position[1], 0)
  glRotatef(angle * 57.3, 0, 0, 1)
  glBegin(GL_TRIANGLE_STRIP)
  for vertex in vertices[:2] + vertices[:1:-1]:
      glVertex2f(vertex[0], vertex[1])
  glEnd()
  glPopMatrix()


@window.event
def on_draw():
  global player
  global shapes
  glClear(GL_COLOR_BUFFER_BIT)
  glColor3f(0.9, 0.9, 0.9)
  window.clear()
  fps.draw()
  draw_rectangle(player['shape'][1].verts,
                 player['shape'][1].body.position, 
                 player['shape'][1].body.angle)
  for shape in shapes:
      if shape[0] == 'poly':
          draw_rectangle(shape[1].verts,
                         shape[1].body.position, 
                         shape[1].body.angle)


@window.event
def on_key_press(symbol, modifiers):
  global objects
  if symbol == key.LEFT:
    player['movement'] = 'left'
  if symbol == key.RIGHT:
    player['movement'] = 'right'
  if symbol == key.UP:
    player['shape'][1].body.apply_impulse((0, 300))

@window.event
def on_key_release(symbol, modifiers):
  if symbol == key.LEFT:
    player['movement'] = None
  if symbol == key.RIGHT:
    player['movement'] = None

if __name__ == '__main__':
  main()

