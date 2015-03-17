import bunch
import pyglet.gl as gl
import pymunk


def add_shape(space, body, shape):
  if body.is_static:
    space.add(shape)
  else:
    space.add(body, shape)


def create_shape(properties):
  arguments = properties.body.copy()
  arguments.update(properties.shape)
  return globals()['create_' + properties.type](**arguments)


def create_circle(collision_type=None, elasticity=None, friction=None,
                  mass=None, moment=None, offset=None, position=None, 
                  radius=None, **extras):
  if mass is not None and  moment is None:
    moment = pymunk.moment_for_circle(mass, 0, radius, offset)
  body = pymunk.Body(mass, moment)
  body.position = position
  shape = pymunk.Circle(body, radius, offset)
  shape.elasticity = elasticity
  shape.friction = friction
  shape.collision_type = collision_type
  return shape


def create_poly(collision_type=None, elasticity=None, friction=None, mass=None,
                moment=None, offset=None, position=None, radius=None, 
                vertices=None, **extras):
  if mass is not None and moment is None:
    moment = pymunk.moment_for_poly(mass, vertices, offset)
  body = pymunk.Body(mass, moment)
  body.position = position
  shape = pymunk.Poly(body, vertices, offset, radius)
  shape.elasticity = elasticity
  shape.friction = friction
  shape.collision_type = collision_type
  return shape


def create_segment(a=None, b=None, collision_type=None, elasticity=None, 
                   friction=None, mass=None, moment=None, position=None,
                   radius=None, **extras):
  if mass is not None and moment is None:
    moment = pymunk.moment_for_segment(mass, a, b)
  body = pymunk.Body(mass, moment)
  body.position = position
  shape = pymunk.Segment(body, a, b, radius)
  shape.elasticity = elasticity
  shape.friction = friction
  shape.collision_type = collision_type
  return shape


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

