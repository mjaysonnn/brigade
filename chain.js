const { events, Job, Group } = require("brigadier")
events.on("exec", () => {
 var hello = new Job("asr", "alpine:3.4", ["echo hello", "sleep 0.01"])
 var goodbye = new Job("imc", "alpine:3.4", ["echo goodbye","sleep 0.1"])
 var helloAgain = new Job("img", "alpine:3.4", ["echo hello again", "sleep 0.3"])
Group.runAll([hello, goodbye]).then( ()=> {
  helloAgain.run()
 })
})
