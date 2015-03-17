import pymunk


def add_collision(object_, count):
    object_.collisions += count
    return True


def add_shape(space, body, shape):
  if body.is_static:
    space.add(shape)
  else:
    space.add(body, shape)


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

