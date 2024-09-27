// deploy like this:
// gcloud functions deploy firstTestFunction --no-gen2 --entry-point testFunction --runtime nodejs20 --trigger-http --project bsc-thesis-implementation
exports.testFunction = (req, res) => {
  let message =
    req.query.message ||
    "You didn't specify any message in the message-query parameter";
  res.status(200).send(message);
};

// Problem: i do not have the URL before deploying
const url = "";
// const url = "https://REGION-PROJECT_ID.cloudfunctions.net/myFunction";

exports.optimizationFunction = async (req, res) => {
  const retryCount = req.headers["x-retry-count"] || 0;

  // Log the retry count for debugging purposes
  console.log(`Retry Count: ${retryCount}`);

  const startTime = Date.now();
  const result = performMatrixMultiplication();

  // Microbenchmark: Check how long the computation took
  const duration = Date.now() - startTime;
  const maxDuration = 1000;

  if (duration > maxDuration) {
    const response = await invokeNewInstance(req); // Try again, passing along the retry count
    // return res.status(500).send("Computation took too long, restarting...");
    return res.status(response.status).send(response.message);
  }

  res.status(200).send(`Computation successful. Result: ${result}`);
};

function performMatrixMultiplication() {
  const size = 100;
  const matrixA = Array(size)
    .fill(0)
    .map(() => Array(size).fill(Math.random()));
  const matrixB = Array(size)
    .fill(0)
    .map(() => Array(size).fill(Math.random()));
  const resultMatrix = Array(size)
    .fill(0)
    .map(() => Array(size).fill(0));

  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      for (let k = 0; k < size; k++) {
        resultMatrix[i][j] += matrixA[i][k] * matrixB[k][j];
      }
    }
  }

  return resultMatrix;
}

async function invokeNewInstance(req) {
  const retryCount = req.headers["x-retry-count"] || 0;

  // Ensure we don't retry more than a specific number of times (e.g., 3)
  if (retryCount >= 3) {
    console.log("Max retry limit reached.");
    return {
      status: 500,
      message: "Max retry limit reached, computation failed.",
    };
  }

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-retry-count": parseInt(retryCount) + 1, // Increment retry count
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json(); // Assuming the response is in JSON format
    return { status: 200, message: data.message || "Success" }; // Return success message
  } catch (error) {
    console.error("Error:", error);
    return { status: 500, message: "Error." }; // Handle error
  }
}
