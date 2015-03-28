import bunch
import graphics
import physics


def create_shape(properties):
  arguments = properties.body.copy()
  arguments.update(properties.shape)
  return getattr(physics, 'create_' + properties.type)(**arguments)


def draw_shape(shape, properties):
  getattr(graphics, 'draw_' + properties.physics.type)(shape, properties.graphics.color)


def get_shape_points(shape, properties):
  getattr(graphics, 'get_shape_points_' + properties.physics.type)(shape, properties)


def get_shape_points_segment(shape, properties):
  pass


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


def is_in_circle(center, point, radius):
    dx, dy = abs(center[0] - point[0]), abs(center[1] - point[1])
    return dx**2 + dy**2 <= radius**2
  
