const benchmark = require("./lib/benchmark");
const instances = require("./lib/instances");

// const url = "https://REGION-PROJECT_ID.cloudfunctions.net/myFunction";
const url = "http://localhost:8080/";
// const url =
// "https://us-central1-bsc-thesis-implementation.cloudfunctions.net/optimizationFunction1";

exports.optimizationFunction = async (req, res) => {
  benchmarkPassed = benchmark.performBenchmark(0.1);

  if (benchmarkPassed) {
    return res.status(200).send({
      status: 200,
      message: "Benchmark passed",
    });
  } else {
    return await instances.invokeNewInstance(req, res, url); // Try again, passing along the retry count
    // to exit the process gracefully, but have to not wait for a promise
    process.exit(0);
  }
};
