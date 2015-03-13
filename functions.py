import bunch
import pyglet.gl as gl
import pymunk


def add_shape(space, body, shape):
  if body.is_static:
    space.add(shape)
  else:
    space.add(body, shape)
  return shape


def create_shape(properties):
  return globals()['create_' + properties.type](properties)


def create_circle(properties):
  moment = properties.body.moment
  if properties.body.mass is not None and  moment is None:
    moment = pymunk.moment_for_circle(properties.body.mass, 
                                      0,
                                      properties.shape.radius,
                                      properties.shape.offset)
  body = pymunk.Body(properties.body.mass, moment)
  body.position = properties.body.position
  shape = pymunk.Circle(body, properties.shape.radius, properties.shape.offset)
  shape.elasticity = properties.shape.elasticity
  shape.friction = properties.shape.friction
  shape.collision_type = properties.shape.collision_type
  return body, shape


def create_poly(properties):
  moment = properties.body.moment
  if properties.body.mass is not None and moment is None:
    moment = pymunk.moment_for_poly(properties.body.mass, 
                                    properties.shape.vertices,
                                    properties.shape.offset)
  body = pymunk.Body(properties.body.mass, moment)
  body.position = properties.body.position
  shape = pymunk.Poly(body,
                      properties.shape.vertices,
                      properties.shape.offset,
                      properties.shape.radius)
  shape.elasticity = properties.shape.elasticity
  shape.friction = properties.shape.friction
  shape.collision_type = properties.shape.collision_type
  return body, shape


def create_segment(properties):
  moment = properties.body.moment
  if properties.body.mass is not None and moment is None:
    moment = pymunk.moment_for_segment(properties.body.mass, 
                                      properties.shape.a,
                                      properties.shape.b)
  body = pymunk.Body(properties.body.mass, moment)
  body.position = properties.body.position
  shape = pymunk.Segment(body,
                         properties.shape.a,
                         properties.shape.b,
                         properties.shape.radius)
  shape.elasticity = properties.shape.elasticity
  shape.friction = properties.shape.friction
  shape.collision_type = properties.shape.collision_type
  return body, shape


def draw_shape(shape, properties):
  globals()['draw_' + properties.physics.type](shape, properties)


def draw_segment(shape, properties):
    position = shape.body.position
    a = shape.a
    b = shape.b
    radius = shape.radius
    color = properties.graphics.color
    gl.glPushMatrix()
    gl.glColor3f(color[0], color[1], color[2])
    gl.glTranslatef(position[0], position[1], 0)
    gl.glLineWidth(radius)
    gl.glBegin(gl.GL_LINES)
    gl.glVertex2f(a[0], a[1])
    gl.glVertex2f(b[0], b[1])
    gl.glEnd()
    gl.glPopMatrix()


def draw_circle(shape, properties):
  position = shape.body.position
  radius = shape.radius
  color = properties.graphics.color
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


def draw_poly(shape, properties):
    """Draw a rectangle using OpenGL based on the provided spacial information.

    Keyword arguments:
    vertices -- points on the rectangle presented in clockwise order
    position -- x and y position to start the operation
    angle -- draw angle in radians (default 0)
    """
    vertices = shape.verts
    position = shape.body.position
    angle = shape.body.angle
    color = properties.graphics.color
    gl.glPushMatrix()
    gl.glColor3f(color[0], color[1], color[2])
    gl.glTranslatef(position[0], position[1], 0)
    gl.glRotatef(angle * 57.3, 0, 0, 1)
    gl.glBegin(gl.GL_TRIANGLE_STRIP)
    for vertex in vertices[:2] + vertices[:1:-1]:
        gl.glVertex2f(vertex[0], vertex[1])
    gl.glEnd()
    gl.glPopMatrix()


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

