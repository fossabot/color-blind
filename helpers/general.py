import bunch
import graphics
import physics


def create_shape(properties):
  arguments = properties.body.copy()
  arguments.update(properties.shape)
  return getattr(physics, 'create_' + properties.type)(**arguments)


def draw_shape(shape, properties):
  getattr(graphics, 'draw_' + properties.physics.type)(shape, properties)


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

