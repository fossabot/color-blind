import bunch
import pymunk


def create_shape(properties):
  print(properties)
  return globals()['create_' + properties.type](properties)


def create_circle(properties):
  moment = properties.body.moment
  if moment is None:
    moment = pymunk.moment_for_circle(properties.body.mass, 
                                      0,
                                      properties.shape.radius,
                                      properties.shape.offset)
  body = pymunk.Body(properties.body.mass, moment)
  body.position = properties.body.position
  shape = pymunk.Circle(body, properties.shape.radius, properties.shape.offset)
  shape.elasticity = properties.shape.elasticity
  shape.friction = properties.shape.friction
  return rebunch({
    'body': body, 
    'shape': shape
  })


def create_poly(properties):
  pass


def create_segment():
  pass


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



def draw_rectangle(vertices, position, angle=0, color=[0.2, 0.2, 0.2]):
    """Draw a rectangle using OpenGL based on the provided spacial information.

    Keyword arguments:
    vertices -- points on the rectangle presented in clockwise order
    position -- x and y position to start the operation
    angle -- draw angle in radians (default 0)
    """
    gl.glPushMatrix()
    gl.glColor3f(color[0], color[1], color[2])
    gl.glTranslatef(position[0], position[1], 0)
    gl.glRotatef(angle * 57.3, 0, 0, 1)
    gl.glBegin(gl.GL_TRIANGLE_STRIP)
    for vertex in vertices[:2] + vertices[:1:-1]:
        gl.glVertex2f(vertex[0], vertex[1])
    gl.glEnd()
    gl.glPopMatrix()
