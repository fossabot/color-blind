import pymunk


def add_collision(shape, count):
    shape.collisions += count
    return True


def add_shape(space, body, shape):
  space.add(shape) if body.is_static else space.add(body, shape)


def create_circle(collision_type=None, elasticity=None, friction=None,
                  mass=None, moment=None, offset=None, position=None, 
                  radius=None, **extras):
  if _lacks_moment(mass, moment):
    moment = pymunk.moment_for_circle(mass, 0, radius, offset)
  body = _create_body(mass, moment, position)
  shape = pymunk.Circle(body, radius, offset)
  return _configure_shape(shape, elasticity, friction, collision_type)


def create_poly(collision_type=None, elasticity=None, friction=None, mass=None,
                moment=None, offset=None, position=None, radius=None, 
                vertices=None, **extras):
  if _lacks_moment(mass, moment):
    moment = pymunk.moment_for_poly(mass, vertices, offset)
  body = _create_body(mass, moment, position)
  shape = pymunk.Poly(body, vertices, offset, radius)
  return _configure_shape(shape, elasticity, friction, collision_type)


def create_segment(a=None, b=None, collision_type=None, elasticity=None, 
                   friction=None, mass=None, moment=None, position=None,
                   radius=None, **extras):
  if _lacks_moment(mass, moment):
    moment = pymunk.moment_for_segment(mass, a, b)
  body = _create_body(mass, moment, position)
  shape = pymunk.Segment(body, a, b, radius)
  return _configure_shape(shape, elasticity, friction, collision_type)


def get_intersections(space, center, point):
  intersections = space.segment_query(center, point)
  return sorted(intersections, key=lambda i: i.get_hit_distance())


def _configure_shape(shape, elasticity, friction, collision_type):
  shape.elasticity = elasticity
  shape.friction = friction
  shape.collision_type = collision_type
  return shape


def _create_body(mass, moment, position):
  body = pymunk.Body(mass, moment)
  body.position = position
  return body


def _lacks_moment(mass, moment):
  return mass is not None and moment is None

