import pyglet.gl as gl


def draw_circle(shape, color):
  position = shape.body.position
  radius = shape.radius
  vertices = [(-radius, -radius),
              (-radius, radius),
              (radius, radius),
              (radius, -radius)]
  gl.glPushMatrix()
  gl.glColor3f(color[0], color[1], color[2])
  gl.glTranslatef(position[0], position[1], 0)
  gl.glBegin(gl.GL_TRIANGLE_STRIP)
  for vertex in vertices[:2] + vertices[:1:-1]:
      gl.glVertex2f(vertex[0], vertex[1])
  gl.glEnd()
  gl.glPopMatrix()


def draw_poly(shape, color):
    """Draw a rectangle using OpenGL based on the provided spacial information.

    Keyword arguments:
    vertices -- points on the rectangle presented in clockwise order
    position -- x and y position to start the operation
    angle -- draw angle in radians (default 0)
    """
    vertices = shape.verts
    position = shape.body.position
    angle = shape.body.angle
    gl.glPushMatrix()
    gl.glColor3f(color[0], color[1], color[2])
    gl.glTranslatef(position[0], position[1], 0)
    gl.glRotatef(angle * 57.3, 0, 0, 1)
    gl.glBegin(gl.GL_TRIANGLE_STRIP)
    for vertex in vertices[:2] + vertices[:1:-1]:
        gl.glVertex2f(vertex[0], vertex[1])
    gl.glEnd()
    gl.glPopMatrix()


def draw_segment(shape, color):
    position = shape.body.position
    a = shape.a
    b = shape.b
    radius = shape.radius
    gl.glPushMatrix()
    gl.glColor3f(color[0], color[1], color[2])
    gl.glTranslatef(position[0], position[1], 0)
    gl.glLineWidth(radius)
    gl.glBegin(gl.GL_LINES)
    gl.glVertex2f(a[0], a[1])
    gl.glVertex2f(b[0], b[1])
    gl.glEnd()
    gl.glPopMatrix()


def draw_line(a, b, color):
    gl.glPushMatrix()
    gl.glColor3f(color[0], color[1], color[2])
    gl.glLineWidth(2)
    gl.glBegin(gl.GL_LINES)
    gl.glVertex2f(a[0], a[1])
    gl.glVertex2f(b[0], b[1])
    gl.glEnd()
    gl.glPopMatrix()

def draw_fan(center, vertices, color):
    gl.glPushMatrix()
    gl.glColor4f(*color)
    gl.glBegin(gl.GL_TRIANGLE_FAN)
    gl.glVertex2f(center[0], center[1])
    for vertex in vertices:
        gl.glVertex2f(vertex[0], vertex[1])
    gl.glEnd()
    gl.glPopMatrix()
