const { events, Job } = require("brigadier");

events.on("exec", exec);
var myArgs = process.argv.slice(2);

var function1 = "asr-"+myArgs[0]
var function2 = "nlp-"+myArgs[0]
var function3 = "qa-"+myArgs[0]

console.log('myArgs: ', myArgs, function1,function2,function3);

async function exec(e, p) {
 let asr = new Job("asr-slackware10", "alpine:3.4", ["echo hello", "sleep 0.045"])
 let nlp = new Job("nlp-slackware10", "alpine:3.4", ["echo goodbye","sleep 0.01"])
 let qa = new Job("qa-slackware10", "alpine:3.4", ["echo hello again", "sleep 0.056"])
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
