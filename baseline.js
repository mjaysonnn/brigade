const { events, Job } = require("brigadier");

events.on("exec", exec);

async function exec(e, p) {
  let asr = new Job("asr-b", "alpine:3.4", ["echo hello", "sleep 0.045"])
 let nlp = new Job("nlp-b", "alpine:3.4", ["echo goodbye","sleep 0.01"])
 let qa = new Job("qa-b", "alpine:3.4", ["echo hello again", "sleep 0.056"])
 //  let j1 = new Job("j1", "alpine:3.7", ["echo hello"]);
 //   let j2 = new Job("j2", "alpine:3.7", ["echo goodbye"]);
 //   let j3 = new Job("j3", "alpine:3.7", ["echo goodbye"]);

    //asr.args.push(330);
    //asr.args.push(8);
    asr.args="45, 2";
    nlp.args = "10, 2"; 
    qa.args = "56, 2";
    await asr.run();
    await nlp.run();
    await qa.run();
    console.log("done");
}
