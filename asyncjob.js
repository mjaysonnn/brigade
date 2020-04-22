const { events, Job } = require("brigadier");

events.on("exec", exec);

async function exec(e, p) {
  let asr = new Job("asr", "alpine:3.4", ["echo hello", "sleep 0.045"])
 let nlp = new Job("nlp", "alpine:3.4", ["echo goodbye","sleep 0.01"])
 let qa = new Job("qa", "alpine:3.4", ["echo hello again", "sleep 0.056"])
 //  let j1 = new Job("j1", "alpine:3.7", ["echo hello"]);
 //   let j2 = new Job("j2", "alpine:3.7", ["echo goodbye"]);
 //   let j3 = new Job("j3", "alpine:3.7", ["echo goodbye"]);

    //asr.args.push(330);
    //asr.args.push(8);
    asr.args="45, 8";
    nlp.args = "10, 8"; 
    qa.args = "56, 8";
    await asr.run();
    await nlp.run();
    await qa.run();
    console.log("done");
}
