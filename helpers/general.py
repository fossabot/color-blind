import bunch
import graphics
import math
import physics


def create_shape(properties):
  arguments = properties.body.copy()
  arguments.update(properties.shape)
  return getattr(physics, 'create_' + properties.type)(**arguments)


def draw_shape(shape, properties):
  getattr(graphics, 'draw_' + properties.physics.type)(shape, properties.graphics.color)


def get_shape_points(shape, properties):
  return globals()['get_shape_points_' + properties.physics.type](shape)


def get_shape_points_segment(shape):
  position, a, b = shape.body.position, shape.a, shape.b
  return [map(sum, zip(position, a)), map(sum, zip(position, b))]


def get_shape_points_poly(shape):
  return shape.get_vertices()


def filter_shapes_in_circle(center, shapes, radius):
  return filter(lambda s: is_in_circle(center, s.shape.body.position, radius), shapes)


# swiss.py


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


def rotate_point(center, point, theta):
  dx, dy = calculate_change(point, center)
  x = (dx * math.cos(theta)) - (dy * math.sin(theta))
  y = (dy * math.cos(theta)) + (dx * math.sin(theta))
  return x + center[0], y + center[1]


def translate_point(center, point, distance):
  distance_old = calculate_distance(center, point)
  x = point[0] + (((point[0] - center[0]) / distance_old) * (distance - distance_old))
  y = point[1] + (((point[1] - center[1]) / distance_old) * (distance - distance_old))
  return x, y


def is_in_range(a, b, radius):
  return all(map(lambda (x, y): abs(x - y) < radius, zip(a, b)))


def is_in_circle(center, point, radius):
    return calculate_distance(center, point) <= radius


def calculate_slope(a, b):
  dx, dy = calculate_change(a, b)
  return dy / dx

def calculate_change(a, b):
  return a[0] - b[0], a[1] - b[1]


def calculate_distance(a, b):
  return math.hypot(*calculate_change(a, b))
  
