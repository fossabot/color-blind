import pyglet 
import pymunk

window = pyglet.window.Window(width=1280, height=720)
fps = 60.0
clock = pyglet.clock.Clock(fps_limit=fps)
space = pymunk.Space()
space.gravity = (0.0, -900.0)

@window.event
def on_draw():
  window.clear()
  space.step(1 / fps)
  clock.tick()

if __name__ == '__main__':
  pyglet.app.run()
