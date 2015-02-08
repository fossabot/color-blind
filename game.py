from pyglet.gl import *
from pyglet.window import key
import pyglet 
import pymunk
import yaml

config = yaml.load(file('config.yaml', 'r'))
window = pyglet.window.Window(width=config['window']['width'],
                              height=config['window']['height'])
space = pymunk.Space()
space.gravity = (config['gravity']['x'], config['gravity']['y'])
shapes = []


def main():
  setup()
  pyglet.clock.schedule_interval(update, 1 / config['fps'])
  pyglet.app.run()


def setup():
  global config
  global shapes
  for shape in config['shapes']:
      shapes.append(create_shape(tuple(shape['position']),
                                 map(tuple, shape['vertices']), 
                                 shape['elasticity'],
                                 shape['friction']))


def update(dt):
  global space
  space.step(dt)


def create_shape(position, vertices, elasticity, friction):
    global space
    body = pymunk.Body()
    body.position = position
    shape = pymunk.Poly(body, vertices)
    shape.elasticity = elasticity
    shape.friction = friction
    space.add(shape)
    return shape


def draw_rectangle(vertices):
  glBegin(GL_LINE_LOOP)
  for vertex in vertices:
      glVertex2f(vertex[0], vertex[1])
  glEnd()


@window.event
def on_key_press(symbol, modifiers):
  global objects
  if symbol == key.LEFT:
    ball.body.apply_impulse((-50, 0))


@window.event
def on_draw():
  global shapes
  glClear(GL_COLOR_BUFFER_BIT)
  glColor3f(0.9, 0.9, 0.9)
  window.clear()
  for shape in shapes:
    draw_rectangle(shape.verts)


if __name__ == '__main__':
  main()

