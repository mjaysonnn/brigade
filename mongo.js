var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://10.52.3.47:27017/mydb";
var idleContainer = null;
var idleCreatetime = null;
var myArgs = process.argv.slice(2);
console.log('myArgs: ', myArgs);
MongoClient.connect(url, function(err, db) {
		if (err) throw err;
		console.log("Database created!");
		var dbo = db.db("mydb");
		dbo.setProfilingLevel('all', function(err, db) {
                                if (err) { console.log(err.message,"******");throw err;}
		})
		db.close();
		});

switch (myArgs[0]) {
	case 'profile':
		console.log(myArgs[0], 'profile');
		MongoClient.connect(url, function(err, db) {
				if (err) throw err;
				var dbo = db.db("mydb");
				dbo.collections("containers").profilingInfo(function(err, infos) {
				  console.log(infos);
				})
				db.close();
			});
		break;
		MongoClient.connect(url, function(err, db) {
				if (err) throw err;
				var dbo = db.db("mydb");
				var myobj = { name: "Company Inc", address: "Highway 37" };
				dbo.collection("customers").insertOne(myobj, function(err, res) {
						if (err) throw err;
						console.log("1 document inserted");
						db.close();
						});
				});
		MongoClient.connect(url, function(err, db) {
				if (err) throw err;
				var dbo = db.db("mydb");
				var query = { address: "23 Meyer Hill Dr" };
				dbo.collection("customers").find(query).toArray(function(err, result) {
						if (err) throw err;
						console.log(result[0].name);
						db.close();
						});
				});
		break;
		case 'count':
		console.log(myArgs[0], 'find count of all jobs');
		MongoClient.connect(url, function(err, db) {
				if (err) { console.log("err.stack" , err.stack) ; throw err;}
				var dbo = db.db("mydb");
				dbo.collection("containers").count()
				.then( result => {
					console.log("num containers is ", result);
				})
				dbo.collection("job_stats").count()
				.then( result => {
					console.log("num jobs is ", result);
				})
	
						
				db.close();
				});
		break;

	case 'find':
		console.log(myArgs[0], 'findall in job and container');
		/*MongoClient.connect(url, function(err, db) {
				if (err) { console.log("err.stack" , err.stack) ; throw err;}
				var dbo = db.db("mydb");
				dbo.collection("job_stats").find().toArray(function(err, result) {
						if (err) throw err;
						result.forEach( element =>{
						console.log(element.ID);
						});
				});
				db.close();
				});*/
		MongoClient.connect(url, function(err, db) {
				if (err){ console.log("err.stack" , err.stack);throw err;}
				var dbo = db.db("mydb");
				dbo.collection("containers").find().toArray(function(err, result) {
						if (err) throw err;
						console.log(result);
						});
				db.close();
				});	
		break;


	case 'findone':
		console.log(myArgs[0], 'find first matching idle  container');
		MongoClient.connect(url, function(err, db) {
				if (err)  {console.log("updating containers  error " , err.stack);}
				var dbo = db.db("mydb");
				query = {idle: "true"};
				const projection = {
				"ID": 1,
				"createTime": 1
				}
				dbo.collection("containers").findOne(query,projection).then((result) => {
						if (result) {
						console.log("Successfully found document ", result.ID, " ", result.lastUsedTime);
						idleContainer = result.ID;
						idleCreatetime = result.createTime;
						} else {
						console.log('No document matches the provided query.');
						}
						})
				db.close();
				});

		break;

	case 'update':
		console.log(myArgs[0], 'updating idle to true');
		MongoClient.connect(url, function(err, db) {
				if (err)  {console.log("updating containers  error " , err.stack);}
				var dbo = db.db("mydb");
				var myquery = { ID: idleContainer };
				var newvalues = { $set: {idle: "False" }};
				dbo.collection("containers").findOneAndUpdate({"idle": "false"}, {$set: {"idle": "true", "ID": "test-01e5zhvw7vh5k41ayp18n1wskt"}}, function(err, result) {
						if (err) { console.log("findoneupdate error ", err.stack);
						throw err; }
						if (result.value)
						console.log("result is ", result.value.createTime, result.value.ID, result.value.idle);
						});


				db.close(); 
				});
		break;
	case 'delete':
		console.log(myArgs[0], 'deleting all containers');
		MongoClient.connect(url, function(err, db) {
				if (err)  {console.log("deleting containers  error " , err.stack);}
				var dbo = db.db("mydb");
				dbo.collection("containers").remove( { } )
				dbo.collection("job_stats").remove( { } )
				console.log("deleted all containers ");
				db.close(); 
				});
		break;

	case 'update-batch':
	var containerID = "asr-01e6h53gkt455zzw01a8302380";
	var batch_size = 8;
	var newbatchsize = 0;
	var currentTime = Date.now();
	MongoClient.connect(url, function(err, db) {
        if (err)  {console.log("updating containers  error " , err.stack);}
        var dbo = db.db("mydb");
        var query = {ID: containerID};
        dbo.collection("containers").findOne(query, (err, result) => {
        if (err) { console.log("findone idle true error ", err.stack);
            throw err; }
            if (result)
            {
             console.log(result);
            newbatchsize = result.batchsize + 1;
            console.log("queue length is ", result.ID, newbatchsize, result.batchsize, batch_size);
            }
          }).then(() => {
        //}).then(()=>{
          if ( newbatchsize != 1 && newbatchsize <= batch_size){
            console.log("updating the batchsize");
            var dbo = db.db("mydb");
            dbo.collection("containers").findOneAndUpdate({ID: containerID},{$set:{idle: "true", ID: containerID, lastUsedTime: currentTime, batchsize:newbatchsize }}, 
            function(err, result) {
            if (err) { console.log("findoneupdate idle true error ", err.stack);
            throw err; }
            if (result.value)
            console.log("updated result is", result.value.idle, result.value.ID, result.value.batchsize);
            else
              console.log("no container to update ", containerID);
            });
            db.close();
	}
	});  
	})         	
	break;


	default:
		console.log('Sorry, that is not something I know how to do. enter test,find,findone,update');
}


