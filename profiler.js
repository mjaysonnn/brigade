var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://10.52.3.47:27017/mydb";
var idleContainer = null;
var idleCreatetime = null;
var myArgs = process.argv.slice(2);
var mongoProfiler = require('mongodb-profiler');

console.log('myArgs: ', myArgs);
MongoClient.connect(url, function(err, dbo) {
		if (err) throw err;
		console.log("Database created!");
		var db = dbo.db("mydb");
		// Profile ALL events. Do not do this against a production database!
		var profiler = mongoProfiler({ db: db, profile: {
all: true
}});

		// ... or ...

		// Profile all events that take longer than 100ms
		// Good for production
var profiler = mongoProfiler({ db: db, profile: {
slow: 100
}});

// ... or ...

// Passive profiling - does not change the profiling level of the Mongo server
// Good for production
var profiler = mongoProfiler({ db: db });

// Do something with the profiling events
profiler.on("profile", function(profile) {

		// Do something with the profiling information
		// If you want an EXPLAIN PLAN, do this
		profiler.explainProfile(profile, function(err, plan) {
				// For queries, you'll have a plan, otherwise null
				});

		});

// Stop the profiler with `stop`. It will revert the profiler settings
// to the original values
setTimeout(function() {
		profiler.stop();
		}, 10000);
		dbo.close();

});
