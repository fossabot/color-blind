from math import pi, sin, cos
from pyglet.gl import *
from pyglet.window import key
import pyglet 
import pymunk

window = pyglet.window.Window(width=1280, height=720)
fps = 60.0
space = pymunk.Space()
space.gravity = (0.0, -200.0)
ball, floor = None, None


def update(dt):
  global space
  global keys
  global ball
  ball.body.angular_velocity *= 0.95
  space.step(dt)


@window.event
def on_key_press(symbol, modifiers):
  global ball
  if symbol == key.LEFT:
    ball.body.apply_impulse((-50, 0))
  if symbol == key.RIGHT:
    ball.body.apply_impulse((50, 0))
  if symbol == key.UP:
    ball.body.apply_impulse((0, 200))


@window.event
def on_draw():
  global ball
  global floor
  glClear(GL_COLOR_BUFFER_BIT)
  glColor3f(1, 1, 1)
  window.clear()
  if ball is None:
    ball = add_ball(space)
    floor = add_floor(space)
  draw_ball(ball)
  draw_line((0, 15), (window.width, 15))
  



def add_ball(space):
  mass = 1
  radius = 14
  inertia = pymunk.moment_for_circle(mass, 0, radius)
  body = pymunk.Body(mass, inertia)
  body.position = window.width // 2, window.height // 2
  shape = pymunk.Circle(body, radius)
  shape.friction = 0.1
  shape.elasticity = 0.5
  space.add(body, shape)
  return shape


def add_floor(space):
    body = pymunk.Body()
    body.position = window.width // 2, 0
    shape = pymunk.Segment(body, (-window.width // 2, 0), (window.width // 2, 0), 15)
    shape.elasticity = 0.5
    shape.friction = 0.5
    space.add(shape)
    return shape


def draw_ball(ball):
  draw_circle(ball.body.position.x, ball.body.position.y, ball.radius)


def draw_circle(x, y, radius):
  iterations = int(2 * radius * pi)
  s = sin((2 * pi) / iterations)
  c = cos((2 * pi) / iterations)
  dx, dy = radius, 0

  glBegin(GL_TRIANGLE_FAN)
  glVertex2f(x, y)
  for i in range((iterations + 1) - 2):
    glVertex2f(x + dx, y + dy)
    dx, dy = ((dx * c) - (dy * s)), ((dy * c) + (dx * s))
  glEnd()

def draw_line(a, b):
  glBegin(GL_LINES)
  glVertex2f(a[0], a[1])
  glVertex2f(b[0], b[1])
  glEnd()


if __name__ == '__main__':
  pyglet.clock.schedule_interval(update, 1 / fps)
  pyglet.app.run()
