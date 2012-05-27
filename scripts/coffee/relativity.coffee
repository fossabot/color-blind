
stats = new Stats()
stats.setMode 0 # 0: fps, 1: ms

# Align top-left.
stats.domElement.style.position = 'absolute'
stats.domElement.style.left     = '150px'
stats.domElement.style.top      = '15px'

document.body.appendChild stats.domElement

canvas = document.getElementById 'c'
ctx    = canvas.getContext '2d'

b2Vec2         = Box2D.Common.Math.b2Vec2
b2BodyDef      = Box2D.Dynamics.b2BodyDef
b2Body         = Box2D.Dynamics.b2Body
b2FixtureDef   = Box2D.Dynamics.b2FixtureDef
b2Fixture      = Box2D.Dynamics.b2Fixture
b2World        = Box2D.Dynamics.b2World
b2MassData     = Box2D.Collision.Shapes.b2MassData
b2PolygonShape = Box2D.Collision.Shapes.b2PolygonShape
b2CircleShape  = Box2D.Collision.Shapes.b2CircleShape
b2DebugDraw    = Box2D.Dynamics.b2DebugDraw

world = {}

init = () ->
  world = new b2World(new b2Vec2(0, 10), true) # gravity, allow sleep

  SCALE = 30

  fixDef = new b2FixtureDef()

  fixDef.density     = 1.0
  fixDef.friction    = 0.5
  fixDef.restitution = 0.75

  bodyDef = new b2BodyDef()

  # Create ground.
  bodyDef.type = b2Body.b2_staticBody

  # Positions the center of the object (not upper left!).
  bodyDef.position.x = (canvas.width / 2) / SCALE
  bodyDef.position.y = 470 / SCALE

  fixDef.shape = new b2PolygonShape()

  # Half width, half height. eg actual height here is 1 unit.
  fixDef.shape.SetAsBox (640 / SCALE) / 2, (10 / SCALE) / 2
  world.CreateBody(bodyDef).CreateFixture(fixDef)

  # Create walls.
  fixDef.shape.SetAsBox (10 / SCALE) / 2, (480 / SCALE) / 2

  # Create left wall.
  bodyDef.position.x = 5 / SCALE
  bodyDef.position.y = (canvas.height / 2) / SCALE
  world.CreateBody(bodyDef).CreateFixture(fixDef)


  # Create right wall.
  bodyDef.position.x = (canvas.width - 5) / SCALE
  bodyDef.position.y = (canvas.height / 2) / SCALE
  world.CreateBody(bodyDef).CreateFixture(fixDef)

  # create some objects
  bodyDef.type = b2Body.b2_dynamicBody

  for i in [0..20]
    if Math.random() > 0.5
           fixDef.shape = new b2PolygonShape()
           fixDef.shape.SetAsBox Math.random() + 0.1, # half width
                                 Math.random() + 0.1 # half height
    else
      fixDef.shape = new b2CircleShape Math.random() + 0.1 # radius

    bodyDef.position.x = Math.random() * 640 / SCALE
    bodyDef.position.y = ((Math.random() * 240) - 100) / SCALE
    world.CreateBody(bodyDef).CreateFixture(fixDef)

  debugDraw = new b2DebugDraw()
  debugDraw.SetSprite document.getElementById('c').getContext('2d')
  debugDraw.SetDrawScale SCALE
  debugDraw.SetFillAlpha 0.3
  debugDraw.SetLineThickness 1.0
  debugDraw.SetFlags b2DebugDraw.e_shapeBit | b2DebugDraw.e_jointBit
  world.SetDebugDraw debugDraw

  setTimeout init, 10000
# init()

update = () ->
  world.Step 1 / 60, 10, 10 # frame-rate, velocity and position iterations
  draw()
  world.ClearForces()

  stats.update()
  requestAnimationFrame update
# update()

draw = () ->
  world.DrawDebugData()
# draw()

init()
requestAnimationFrame update
