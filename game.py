from math import pi, sin, cos
from pyglet.gl import *
import pyglet 
import pymunk

window = pyglet.window.Window(width=1280, height=720)
fps = 60.0
clock = pyglet.clock.Clock(fps_limit=fps)
space = pymunk.Space()
space.gravity = (0.0, -100.0)

ball = None

@window.event
def on_draw():
  global ball
  glClear(GL_COLOR_BUFFER_BIT)
  glColor3f(1, 1, 1)

  window.clear()
  space.step(clock.tick())

  if ball is None:
    ball = add_ball(space)
  draw_ball(ball)
    


def add_ball(space):
  mass = 1
  radius = 14
  inertia = pymunk.moment_for_circle(mass, 0, radius)
  body = pymunk.Body(mass, inertia)
  body.position = window.width // 2, window.height // 2
  shape = pymunk.Circle(body, radius)
  space.add(body, shape)
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
  for i in range((iterations + 1) - 10):
    glVertex2f(x + dx, y + dy)
    dx, dy = ((dx * c) - (dy * s)), ((dy * c) + (dx * s))
  glEnd()


if __name__ == '__main__':
  pyglet.app.run()
