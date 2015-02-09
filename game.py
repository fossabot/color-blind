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
  for shape in setting['shapes']:
      moment = None 
      vertices = map(tuple, shape['vertices'])
      if shape['mass'] is not None:
          moment = pymunk.moment_for_poly(shape['mass'], vertices)
      shapes.append(create_shape(shape['mass'],
                                 moment,
                                 tuple(shape['position']),
                                 vertices,
                                 shape['elasticity'],
                                 shape['friction']))


def update(dt):
  global space
  space.step(dt)


def create_shape(mass, moment, position, vertices, elasticity, friction):
    global space
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Poly(body, vertices)
    shape.elasticity = elasticity
    shape.friction = friction
    if mass is None:
        space.add(shape)
    else:
        space.add(body, shape)
    return shape


def draw_rectangle(vertices, position, angle=0):
  glPushMatrix()
  glTranslatef(position[0], position[1], 0)
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
      draw_rectangle(shape.verts, shape.body.position, shape.body.angle)


@window.event
def on_key_press(symbol, modifiers):
  global objects
  if symbol == key.LEFT:
    ball.body.apply_impulse((-50, 0))


if __name__ == '__main__':
  main()

