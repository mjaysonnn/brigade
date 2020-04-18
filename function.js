var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://10.52.3.47:27017/mydb";


var idleContainer = null;
var foundIdle = false;
const arrivalTime = Date.now();
var imagePullPolicy = true;
var containerExist = false;
let jobname = "test";
let name = "test-12345";
console.log(" = Job arrival time is ",arrivalTime, " ", jobname, " ", name);
var toinsertType = jobname;
var toinsertID =  name;
var updated = false;
var inserted = false;

(async function() {
 let client;
 try
 {
 client = await MongoClient.connect(url);
 console.log("Connected correctly to server");

 //if (err) {console.log("job stats insert error " , err.stack);}
 var dbo = client.db("mydb");
 var myobj = { arrivalTime: arrivalTime, ID: toinsertID, type: toinsertType };
 await dbo.collection("job_stats").insertOne(myobj);
 //if (err) throw err;
 console.log("1 job stats document inserted");
 } catch (err) {
 }
 db.close();
 //});
 //})
})();
new Promise((resolve, reject) =>{ MongoClient.connect(url, function(err, db) {
			if (err)  {console.log("containers  error " , err.stack);}
			var dbo = db.db("mydb");
			dbo.collection("containers").count(function (err, count) {
					if (!err && count === 0) {
					var myobj = { createTime: arrivalTime, ID: toinsertID,  idle: "true"}
					dbo.collection("containers").insertOne(myobj, (err, res)=> {
							if (err)  {console.log("containers insert error " , err.stack);}
							{  
							console.log("1 container document inserted"); 
							imagePullPolicy = true;
							//this.runner.spec.containers[0].imagePullPolicy = "Always";
							}
							});
					inserted = true;
					resolve(inserted);
					}
					else if (count > 0)
					{ 
					console.log("containers exists");
					containerExist = true;
					resolve(containerExist);
					}
					db.close();
			})
			//return containerExist;
})
}).then(result =>{
	console.log("in find container exisits .?", result);
	if (containerExist)
	{
	MongoClient.connect(url, function(err, db) {
			if (err)  {console.log("containers  error " , err.stack);}
			var dbo = db.db("mydb");
			var query = {idle: "true"};
			var projection = {
			"ID": 1
			}
			dbo.collection("containers").findOne(query,projection).then((result) => {
					if (result != null) {

					idleContainer = result.ID;
					var options = { "upsert": false };
					console.log("Successfully found document ", idleContainer);
					foundIdle = true;
					dbo.collection("containers").findOneAndUpdate({idle:"true"}, {$set:{idle: "false", ID: toinsertID}}).then((result)=> {
							if (err) 
							console.log(" error updating container idle stats mongodb ", err.stack);
							if (res.value)
							{
							imagePullPolicy = false;
							console.log("1 container updated ", res.value.createTime, res.value.ID, res.value.idle, imagePullPolicy);
							updated = true;
							}})
					}})	
			db.close();
	})
	}

	return updated;
}).then(result => {   

	console.log("inserting new bcoz no match , container exisits .?", idleContainer, result);
	if (!updated && !inserted)
	{
	console.log('No document matches the provided query.');
	var myobj = { createTime: arrivalTime, ID: toinsertID,  idle: "false"}
	MongoClient.connect(url, function(err, db) {
			if (err)  {console.log("updating containers  error " , err.stack);}
			var dbo = db.db("mydb");
			dbo.collection("containers").insertOne(myobj, function(err, res){
					if (err) console.log("container creation error", err.stack)
					if(!err)
					{ 
					console.log("inserting new container ")
					imagePullPolicy = true;
					}
					//this.runner.spec.containers[0].imagePullPolicy = "Always";
					})
			db.close();
			})

	}
	return imagePullPolicy;

}).then(result => {
	if (result)
	{
	console.log("imagePullPolicy is always ", imagePullPolicy);
	this.runner.spec.containers[0].imagePullPolicy = "Always";
	}
	else 
	{
	console.log("imagePullPolicy is Never ", imagePullPolicy);  
	this.runner.spec.containers[0].imagePullPolicy = "Never";
	}
	return imagePullPolicy;
	}) 

/*.then( result =>{
  console.log("in update, container exisits idlecontaier foundidle?", containerExist, idleContainer, foundIdle, result);
  if (containerExist && !result)
  {  
  console.log("attempting to update idle status of container ", idleContainer);
  MongoClient.connect(url, function(err, db) {
  if (err)  {console.log("updating containers  error " , err.stack);}
  var dbo = db.db("mydb");
  dbo.collection("containers").findOneAndUpdate({idle:"true"}, {$set:{idle: "false", ID: toinsertID}}, function(err, res) {
  if (err) 
  console.log(" error updating container idle stats mongodb ", err.stack);
  if (res.value)
  {
  imagePullPolicy = false;
  console.log("1 container updated ", res.value.createTime, res.value.ID, res.value.idle, imagePullPolicy);
  updated = true;
  }
//this.runner.spec.containers[0].imagePullPolicy = "Never";
}) 
db.close();
})
}

return updated;
})*/
