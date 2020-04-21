const { events, Job } = require("brigadier");

events.on("exec", exec);

async function exec(e, p) {
  let asr = new Job("asr", "alpine:3.4", ["echo hello", "sleep 0.01"])
 let imc = new Job("imc", "jashwant/mxnet", ["echo goodbye","sleep 0.1"])
 let img = new Job("img", "alpine:3.4", ["echo hello again", "sleep 0.3"])
 //  let j1 = new Job("j1", "alpine:3.7", ["echo hello"]);
 //   let j2 = new Job("j2", "alpine:3.7", ["echo goodbye"]);
 //   let j3 = new Job("j3", "alpine:3.7", ["echo goodbye"]);

    await asr.run();
    await imc.run();
    await img.run();
    console.log("done");
}
