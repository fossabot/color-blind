// This file hosts the main game module.  Whenever it makes sense to
// put something in its own module, you can either put it in the dependency
// array for this module (i.e. the way we're using 'game-shim' in th commented
// out version below), or you can call require() directly closer to the
// time you need it.  <http://requirejs.org/> has detailed documentation.
//
//
//
define(function(require) {

  // Toji's game-shim module is included with this template; if you wish to use
  // it, uncomment the require() line below.
  //
  // The reason that this isn't done by default is that the replacement
  // versions of the various APIs that it includes could potentially cause
  // complications or performance issues with other libraries that use these APIs
  // and may have their own strategies for dealing with cross-browser issues.
  // We suggest reviewing the code (in lib/game-shim.js) before enabling it.
  //
  require('game-shim');
  require('stats');

  var stats = new Stats();
  stats.setMode(0); // 0: fps, 1: ms

  // Align top-left
  stats.domElement.style.position = 'absolute';
  stats.domElement.style.left = '0px';
  stats.domElement.style.top = '0px';

  document.body.appendChild(stats.domElement);

  setInterval( function () {
      stats.begin();

      // your code goes here

      stats.end();
  }, 1000 / 60 );

});
