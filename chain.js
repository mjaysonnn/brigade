const { events, Job, Group } = require("brigadier")
events.on("exec", () => {
 var asr = new Job("asr", "alpine:3.4", ["echo hello", "sleep 0.01"])
 var imc = new Job("imc", "jashwant/mxnet", ["echo goodbye","sleep 0.1"])
 var img = new Job("img", "alpine:3.4", ["echo hello again", "sleep 0.3"])
 asr.run();
 .then(()=>{ 
    imc.run()
  })
 .then(()=>{
    img.run()
  })*/
//Group.runAll([hello, goodbye]).then( ()=> {
//  helloAgain.run()
})
