const benchmark = require("./lib/benchmark");
const instances = require("./lib/instances");
const serverCommunication = require("./lib/server-communication");

// const url = "https://REGION-PROJECT_ID.cloudfunctions.net/myFunction";
const url = "http://localhost:8080/";
// const url =
// "https://us-central1-bsc-thesis-implementation.cloudfunctions.net/optimizationFunction1";

const webhook_url = "http://localhost:3000/webhook";
exports.optimizationFunction = async (req, res) => {
  const { benchmarkPassed, timeOfExecution } = benchmark.performBenchmark(100);

  if (benchmarkPassed) {
    serverCommunication.sendToWebhook(
      webhook_url,
      JSON.stringify({
        status: 200,
        message: "Benchmark passed",
      })
    );
  } else {
    return await instances.invokeNewInstance(req, res, url, webhook_url);
  }
};

const { v4: uuidv4 } = require("uuid"); // For generating UUIDs
const maxRetries = 3;

exports.optimizationFunction2 = async (req, res) => {
  let taskId = req.body.taskId || uuidv4();
  let retryCount = req.body.retryCount || 0;

  // Send 200 OK response immediately, including taskId in the response
  res.status(200).json({
    message: "Request received, processing...",
    taskId: taskId,
    retryCount: retryCount,
  });

  const { benchmarkPassed, timeOfExecution } =
    benchmark.performBenchmark(0.001);

  if (benchmarkPassed) {
    // TODO: save time of execution with the taskId in firestore
    console.log(
      `Benchmark passed for taskId "${taskId}" in time (${timeOfExecution}).`
    );
    return;
  }

  if (retryCount < maxRetries) {
    // Call the same cloud function again
    try {
      await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          taskId: taskId,
          retryCount: retryCount + 1,
        }),
      });
      // .then((response) => response.json())
      // .then((json) => console.log(json));
    } catch (error) {
      console.error(`Error re-invoking function for task ${taskId}:`, error);
    }
    return;
  }

  console.log(`Max retries reached for taskId "${taskId}".`);
};
