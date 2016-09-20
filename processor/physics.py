# Include third-party libraries.
import esper
import pymunk

# Include local libraries.
from component import wrapper


class PhysicsProcessor(esper.Processor):
    def __init__(self, gravity):
        super().__init__()
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.shapes = {}

    def process(self, dt):
        for entity, (body, shape, position) in self.world.get_components(
                wrapper.Body, wrapper.Shape, wrapper.Position):
            if entity not in self.shapes:
                self.shapes[entity] = self.create_shape(body, shape, position)
                self.space.add(self.shapes[entity].body, self.shapes[entity])
            position.x, position.y = self.shapes[entity].body.position
        self.space.step(dt)

    def create_shape(self, body, shape, position):
        vertices = list(map(list, shape.polygon.vertices))
        if body.moment == 0:
            body.moment = pymunk.moment_for_poly(body.mass, vertices)
        body_object = pymunk.Body(body.mass, body.moment, body.type)
        body_object.position = (position.x, position.y)
        shape_object = pymunk.Poly(body_object, vertices)
        shape_object.elasticity = shape.elasticity
        shape_object.friction = shape.friction
        return shape_object
