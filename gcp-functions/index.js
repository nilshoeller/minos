const benchmark = require("./lib/benchmark");
const instances = require("./lib/instances");
const { v4: uuidv4 } = require("uuid"); // For generating UUIDs

// const url = "https://REGION-PROJECT_ID.cloudfunctions.net/myFunction";
const url =
  "https://us-central1-bsc-thesis-implementation.cloudfunctions.net/optimizationFunction1";
// const url = "http://localhost:8080/";

const maxRetries = 3;

/**
 * Cloud Function that processes a request for optimization and benchmarks its execution.
 *
 * @param {Object} req - The HTTP request object containing data related to the invocation.
 * @param {Object} req.body - The body of the request containing task information.
 * @param {string} [req.body.taskId] - The ID of the current task. If not provided, a new ID will be generated.
 * @param {number} [req.body.retryCount] - The number of times the task has been retried. Defaults to 0 if not provided.
 * @param {number} [req.body.totalTimeOfExecution] - The total time of execution accumulated across retries. Defaults to 0 if not provided.
 *
 * @returns {void} Responds to the HTTP request with a status of 200 and a message indicating that the request has been received.
 */
exports.optimizationFunction = async (req, res) => {
  let taskId = req.body.taskId || uuidv4();
  let retryCount = req.body.retryCount || 0;
  let totalTimeOfExecution = req.body.totalTimeOfExecution || 0;

  // Send 200 OK response immediately, including taskId in the response
  res.status(200).json({
    message: "Request received, processing...",
    taskId: taskId,
  });

  let { benchmarkPassed, timeOfExecution } = benchmark.performBenchmark(100);

  if (benchmarkPassed) {
    // TODO: save time of total execution and the taskId in firestore
    console.log(
      `Benchmark passed for taskId "${taskId}" in time (${totalTimeOfExecution}).`
    );
    return;
  }

  if (retryCount < maxRetries) {
    // Make call to another instance of the same cloud function
    instances.invokeNew(
      url,
      taskId,
      retryCount,
      totalTimeOfExecution,
      timeOfExecution
    );
    return;
  }

  // TODO: save in firestore, that max retries were reached
  console.log(`Max retries reached for taskId "${taskId}".`);
};
