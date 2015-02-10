from pyglet.gl import *
from pyglet.window import key
import pyglet 
import pymunk
import yaml

setting = yaml.load(file('settings.yaml', 'r'))
config = pyglet.gl.Config(sample_buffers=setting['opengl']['sample_buffers'],
                          samples=setting['opengl']['samples'])
window = pyglet.window.Window(width=setting['window']['width'],
                              height=setting['window']['height'],
                              config=config)
fps = pyglet.clock.ClockDisplay()
space = pymunk.Space()
space.gravity = (setting['gravity']['x'], setting['gravity']['y'])
shapes = []


def main():
  setup()
  pyglet.clock.schedule_interval(update, 1 / setting['fps'])
  pyglet.clock.set_fps_limit(setting['fps'])
  pyglet.app.run()


def setup():
  global setting
  global shapes
  glClearColor(0.1, 0.1, 0.1, 0.1)
  for properties in setting['shapes']:
      shapes.append(create_shape(properties))


def update(dt):
  global space
  space.step(dt)


def create_shape(properties):
    return {
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
    print(vertices[0])
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
  if angle > 0: print(angle)
  glRotatef(angle, 0, 0, 1)
  glBegin(GL_TRIANGLE_STRIP)
  for vertex in vertices[:2] + vertices[:1:-1]:
      glVertex2f(vertex[0], vertex[1])
  glEnd()
  glPopMatrix()


@window.event
def on_draw():
  global shapes
  glClear(GL_COLOR_BUFFER_BIT)
  glColor3f(0.9, 0.9, 0.9)
  window.clear()
  fps.draw()
  for shape in shapes:
      if shape[0] == 'poly':
          draw_rectangle(shape[1].verts,
                         shape[1].body.position, 
                         shape[1].body.angle)


@window.event
def on_key_press(symbol, modifiers):
  global objects
  if symbol == key.LEFT:
    ball.body.apply_impulse((-50, 0))


if __name__ == '__main__':
  main()

