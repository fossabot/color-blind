# Include standard libraries.
import logging.config

# Setup libraries.
logger = logging.getLogger(__name__)


class Component:
    def __init__(self, parent):
        self.parent = parent

    def __getattr__(self, name):
        try:
            return getattr(self.parent, name)
        except AttributeError:
            logger.error("Attempt to get non-existent attribute from object.")


class Body(Component):
    pass


class Color(Component):
    pass


class Position(Component):
    pass


class Shape(Component):
    pass
