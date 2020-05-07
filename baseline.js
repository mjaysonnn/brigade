const { events, Job } = require("brigadier");

events.on("exec", exec);

async function exec(e, p) {
 let asr = new Job("asr-baseline", "alpine:3.4", ["echo hello", "sleep 0.045"])
 let nlp = new Job("nlp-baseline", "alpine:3.4", ["echo goodbye","sleep 0.01"])
 let qa = new Job("qa-baseline", "alpine:3.4", ["echo hello again", "time=$(date)" ,"echo $(date -d \"$time\" +\"%s\")", "sleep 0.056", "time=$(date)", "echo $(date -d \"$time\" +\"%s\")"])
 //  let j1 = new Job("j1", "alpine:3.7", ["echo hello"]);
 //   let j2 = new Job("j2", "alpine:3.7", ["echo goodbye"]);
 //   let j3 = new Job("j3", "alpine:3.7", ["echo goodbye"]);

    //asr.args.push(330);
    //asr.args.push(8);
    asr.args="45, 2";
    nlp.args = "10, 2"; 
    qa.args = "56, 2";
    asr.timeout = 9000000;
    nlp.timeout = 9000000;
    qa.timeout = 9000000;
    await asr.run();
    await nlp.run();
    await qa.run();
    console.log("done");
}
