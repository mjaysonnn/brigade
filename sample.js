
var Nedb = require('/root/.nvm/versions/node/v8.9.4/lib/node_modules/nedb')
  , planets = new Nedb({ filename: 'data.db', autoload: true });
// Let's insert some data
planets.insert({ name: 'Earth', satellites: 1 }, function (err) {
  planets.insert({ name: 'Mars', satellites: 2 }, function (err) {
    planets.insert({ name: 'Jupiter', satellites: 67 }, function (err) {
      
      // Now we can query it the usual way
      planets.find({ satellites: { $lt: 10 } }, function (err, docs) {
        // docs is an array containing Earth and Mars
      console.log(docs);
	});
    });
  });
});
