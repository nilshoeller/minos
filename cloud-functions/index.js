const benchmark = require("./lib/benchmark");
const instances = require("./lib/instances");
const serverCommunication = require("./lib/server-communication");

// const url = "https://REGION-PROJECT_ID.cloudfunctions.net/myFunction";
const url = "http://localhost:8080/";
// const url =
// "https://us-central1-bsc-thesis-implementation.cloudfunctions.net/optimizationFunction1";

const webhook_url = "http://localhost:3000/webhook";
exports.optimizationFunction = async (req, res) => {
  benchmarkPassed = benchmark.performBenchmark(0.001);

  if (benchmarkPassed) {
    // return res.status(200).send({
    //   status: 200,
    //   message: "Benchmark passed",
    // });

    serverCommunication.sendToWebhook(
      webhook_url,
      JSON.stringify({
        status: 200,
        message: "Benchmark passed",
      })
    );
  } else {
    return await instances.invokeNewInstance(req, res, url, webhook_url); // Try again, passing along the retry count
    // to exit the process gracefully, but have to not wait for a promise
    // process.exit(0);
  }
};
