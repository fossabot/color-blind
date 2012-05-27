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


SCALE = 30


class Actor
  constructor: (@body, @sprite) ->

  draw: (ctx) ->
    x = @body.GetPosition().x * SCALE
    y = @body.GetPosition().y * SCALE
    angle = @body.GetAngle()

    ctx.save()

    ctx.translate x, y
    ctx.rotate angle
    ctx.drawImage @sprite, -15, -15, 30, 30

    ctx.restore()

  update: () ->

class AssetManager
  constructor: (@downloadQueue = []) ->
    @cache        = {}
    @successCount = 0
    @errorCount   = 0

  downloadAll: (callback) ->
    if @downloadQueue.length is 0
      callback()

    for path in @downloadQueue
      image = new Image()
      that  = @

      image.addEventListener 'load', (() ->
        console.log @src + ' is loaded.'
        @successCount += 1
        # if that.isDone()
        #   callback()
        ), false

      image.addEventListener 'error', (() ->
        @errorCount += 1
        # if that.isDone()
        #   callback()
        ), false

      image.src = path
      @cache[path] = image
    callback()

  getAsset: (path) ->
    @cache[path]

  queueDownload: (path) ->
    @downloadQueue.push path


actor = {}
assetManager = new AssetManager()
canvas = document.getElementById 'game'
ctx    = canvas.getContext '2d'
defs   =
         body:    new b2BodyDef()
         fixture: new b2FixtureDef()
stats  = new Stats()
world  = new b2World(new b2Vec2(5, 10), true) # gravity, allow sleep


# window.addEventListener 'load', init, false

init = () ->
  stats.setMode 0 # 0: fps, 1: ms

  # Align top-left.
  stats.domElement.style.position = 'absolute'
  stats.domElement.style.left     = '150px'
  stats.domElement.style.top      = '15px'

  document.body.appendChild stats.domElement

  assetManager.queueDownload 'assets/images/ball.png'

  assetManager.downloadAll () ->
    setup()
    requestAnimationFrame update
# init()

setup = () ->
  setupWalls()
  setupObjects()

# setup()

setupWalls = () ->
  defs.fixture.density     = 1.0
  defs.fixture.friction    = 1.0
  defs.fixture.restitution = 0.8

  # Create ground.
  defs.body.type = b2Body.b2_staticBody

  # Positions the center of the object (not upper left!).
  defs.body.position.x = (canvas.width / 2) / SCALE
  defs.body.position.y = 470 / SCALE

  defs.fixture.shape = new b2PolygonShape()

  # Half width, half height. eg actual height here is 1 unit.
  defs.fixture.shape.SetAsBox (640 / SCALE) / 2, (10 / SCALE) / 2
  world.CreateBody(defs.body).CreateFixture(defs.fixture)

  # Create walls.
  defs.fixture.shape.SetAsBox (10 / SCALE) / 2, (480 / SCALE) / 2

  # Create left wall.
  defs.body.position.x = 5 / SCALE
  defs.body.position.y = (canvas.height / 2) / SCALE
  world.CreateBody(defs.body).CreateFixture(defs.fixture)


  # Create right wall.
  defs.body.position.x = (canvas.width - 5) / SCALE
  defs.body.position.y = (canvas.height / 2) / SCALE
  world.CreateBody(defs.body).CreateFixture(defs.fixture)
# setupWalls()

setupObjects = () ->
  # create some objects
  defs.body.type = b2Body.b2_dynamicBody

  defs.fixture.shape = new b2CircleShape 30 / SCALE # radius

  defs.body.position.x = Math.random() * 640 / SCALE
  defs.body.position.y = ((Math.random() * 240) - 100) / SCALE
  actorBody = world.CreateBody(defs.body)
  actorBody.CreateFixture(defs.fixture)

  actor = new Actor actorBody, assetManager.getAsset('assets/images/ball.png')

# setupObjects()

update = () ->
  stats.begin()

  world.Step 1 / 60, 10, 10 # frame-rate, velocity and position iterations
  world.ClearForces()

  draw()

  stats.end()
  requestAnimationFrame update
# update()

draw = () ->
  clearCanvas()
  actor.draw(ctx)
# draw()

clearCanvas = () ->
  # // Store the current transformation matrix
  ctx.save()

  # // Use the identity matrix while clearing the canvas
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  # // Restore the transform
  ctx.restore();

init()