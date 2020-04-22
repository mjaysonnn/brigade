var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://10.52.3.47:27017/mydb";


var idleContainer = null;
var foundIdle = false;
const arrivalTime = Date.now();
var imagePullPolicy = true;
var imagePolicy = false;
var containerExist = false;
let jobname = "test";
var imageForcePull = "";
let name = "test-12345";
console.log(" = Job arrival time is ",arrivalTime, " ", jobname, " ", name);
var toinsertType = jobname;
var toinsertID =  name;
var updated = false;
var inserted = false;
var canProceed =  true;
async function f() {
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
let count = await dbo.collection("containers").count();
console.log("container count is ", count);
if (count === 0) {
	var myobj = { createTime: arrivalTime, ID: toinsertID,  idle: "true"}
	await dbo.collection("containers").insertOne(myobj);
	console.log("1 container document inserted"); 
	imagePullPolicy = true;
	inserted = true;
 	}
 else
 {
 	var query = {idle: "true"};
			let container = await dbo.collection("containers").findOne(query)
			if (container != null){

					idleContainer = container.ID;
					var options = { "upsert": false };
					console.log("Successfully found document ", idleContainer);
					foundIdle = true;
					let updtatedContainer = await dbo.collection("containers").findOneAndUpdate({idle:"true"}, {$set:{idle: "false", ID: toinsertID}})
					imagePullPolicy = false;
					console.log("1 container updated ", updtatedContainer.value.createTime, updtatedContainer.value.ID, updtatedContainer.value.idle, imagePullPolicy);
					updated = true;
			}
			else{
				console.log('No document matches the provided query.');
				var myobj = { createTime: arrivalTime, ID: toinsertID,  idle: "false"}

				await dbo.collection("containers").insertOne(myobj);
			
				console.log("inserting new container ")
				imagePullPolicy = true;
			}
					//this.runner.spec.containers[0].imagePullPolicy = "Always";
	}
	if (imagePullPolicy)
	{
	console.log("imagePullPolicy is always ", imagePullPolicy);
	//this.runner.spec.containers[0].imagePullPolicy = "Always";
	}
	else 
	{
	console.log("imagePullPolicy is Never ", imagePullPolicy);  
	//this.runner.spec.containers[0].imagePullPolicy = "Never";
	}
	 client.close();
	 canProceed = false;
return imagePullPolicy

 //});
 //})
}

f().then(result=>{
	imagePolicy = result;
	console.log("all completed ", result);
});
function waitForIt(){
        if (canProceed) {
            console.log("waiting for new runnerpod to be created ");
            setTimeout(function(){waitForIt()},100);
        } else {
if (imagePolicy)
          {
          imageForcePull = "Always";
          }
          else{
          imageForcePull = "Never";
          console.log("all completed ", imagePolicy, imageForcePull);

          }
      };}
 waitForIt();
 


