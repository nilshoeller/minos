const matrixMult = require("./lib/matrix-mult");
const instances = require("./lib/instances");

// const url = "https://REGION-PROJECT_ID.cloudfunctions.net/myFunction";
// const url = "http://localhost:8080/";
const url =
  "https://us-central1-bsc-thesis-implementation.cloudfunctions.net/optimizationFunction1";

exports.optimizationFunction = async (req, res) => {
  const startTime = Date.now();
  const result = matrixMult.performMatrixMultiplication();

  // Microbenchmark: Check how long the computation took
  const duration = Date.now() - startTime;
  const maxDuration = 100;

  if (duration > maxDuration) {
    let retryCount = req.headers["retry-count"] || 0;
    const response = await instances.invokeNewInstance(retryCount, url); // Try again, passing along the retry count

    return res.status(response.status).send({
      status: response.status,
      message: response.message,
    });
  }

  res.status(200).send({
    status: 200,
    message: "Computation successful",
  });
};
