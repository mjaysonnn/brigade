const { events, Job } = require("brigadier");
events.on("exec", () => {
  var job = new Job("test", "jashwant/mxnet:latest");
  job.tasks = [
    "echo Hello",
    "echo World",
    "sleep 10"
  ];

  job.run();
});
