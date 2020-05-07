var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://10.52.3.47:27017/mydb";


async function cleanup(name, jobname){

        var  containerID = name;
	var batch_size = 13;
        var batchsize = batch_size;
        var newbatchsize = 8;
        const currentTime = Date.now();
        var found = false;
        client = await MongoClient.connect(url);
        console.log("Connected correctly to server");

 //if (err) {console.log("job stats insert error " , err.stack);}
        var dbo = client.db("mydb");       
        var query = {ID: containerID};
        let result = await dbo.collection("containers").findOne(query);
        
            if (result)
            {
             console.log(result);
            newbatchsize = result.batchsize + 1;
            console.log("queue length is ", result.ID, newbatchsize, result.batchsize, batch_size);
            found = true;
            }
        //}).then(()=>{
            if ( newbatchsize != 1 && newbatchsize <= batch_size){
            console.log("updating the batchsize");
            let updated = await dbo.collection("containers").findOneAndUpdate({ID: containerID},{$set:{idle: "true", ID: containerID, lastUsedTime: currentTime, batchsize:newbatchsize }});
            if (updated.value ){
            console.log("updated result is", updated.value.idle, updated.value.ID, updated.value.batchsize);
            found = true;
            }
            else
              console.log("no container to update ", containerID);
          }
          client.close();
          return found;
  }
cleanup("qa-01e6h53gkt455zzw01a8302380", "asr").then(result=>{
	//imagePolicy = result;
	console.log("all completed ", result);
});
