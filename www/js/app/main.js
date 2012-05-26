define(function(require) {
  var stats, canvas, ctx, world;

  require('game-shim');
  require('stats');
  require('jquery');
  require('box2d/javascript/Box2D/box2d');


  stats = new Stats();
  stats.setMode(0); // 0: fps, 1: ms

  // Align top-left
  stats.domElement.style.position = 'absolute';
  stats.domElement.style.left = '0px';
  stats.domElement.style.top = '0px';

  document.body.appendChild(stats.domElement);

  canvas = document.getElementById('c');
  ctx = canvas.getContext('2d');

  function init() {
      var bodyDef, debugDraw, fixDef, SCALE;

      world = new b2World(
              new b2Vec2(0, -10), // gravity
              true // allow sleep
     );

     SCALE = 30;

     fixDef = new b2FixtureDef();

     fixDef.density     = 1.0;
     fixDef.friction    = 0.5;
     fixDef.restitution = 0.75;

     bodyDef = new b2BodyDef();

     // create ground
     bodyDef.type = b2Body.b2_staticBody;

     // positions the center of the object (not upper left!)
     bodyDef.position.x = canvas.width / 2 / SCALE;
     bodyDef.position.y = 7 / SCALE;

     fixDef.shape = new b2PolygonShape();

     // half width, half height. eg actual height here is 1 unit
     fixDef.shape.SetAsBox((600 / SCALE) / 2, (10 / SCALE) / 2);
     world.CreateBody(bodyDef).CreateFixture(fixDef);

     // create some objects
     bodyDef.type = b2Body.b2_dynamicBody;

     for (var i = 0; i < 20; i++) {
         if (Math.random() > 0.5) {
             fixDef.shape = new b2PolygonShape();
             fixDef.shape.SetAsBox(
                     Math.random() + 0.1, // half width
                     Math.random() + 0.1 // half height
            );
        } else {
            fixDef.shape = new b2CircleShape(
                    Math.random() + 0.1 // radius
            );
        }

        bodyDef.position.x = Math.random() * 20;
        bodyDef.position.y = Math.random() * 20;
        world.CreateBody(bodyDef).CreateFixture(fixDef);
    }

    debugDraw = new b2DebugDraw();
    debugDraw.SetSprite(document.getElementById('c').getContext('2d'));
    debugDraw.SetDrawScale(SCALE);
    debugDraw.SetFillAlpha(0.3);
    debugDraw.SetLineThickness(1.0);
    debugDraw.SetFlags(b2DebugDraw.e_shapeBit | b2DebugDraw.e_jointBit);
    world.SetDebugDraw(debugDraw);

    setTimeout(init, 10000);
  }


  function update() {
      world.Step(
              1 / 60, // frame-rate
              10, // velocity iterations
              10 // position iterations
      );
      world.DrawDebugData();
      world.ClearForces();

      stats.update();
      requestAnimationFrame(update);
 }; // update()

 init();
 requestAnimationFrame(update);
});

