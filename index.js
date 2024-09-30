// deploy like this:
// gcloud functions deploy firstTestFunction --no-gen2 --entry-point testFunction --runtime nodejs20 --trigger-http --project bsc-thesis-implementation
exports.testFunction = (req, res) => {
  let message =
    req.query.message ||
    "You didn't specify any message in the message-query parameter";
  res.status(200).send(message);
};

// Problem: i do not have the URL before deploying
// const url = "https://REGION-PROJECT_ID.cloudfunctions.net/myFunction";
// const url = "http://localhost:8080/";
const url =
  "https://us-central1-bsc-thesis-implementation.cloudfunctions.net/optimizationFunction1";

exports.optimizationFunction = async (req, res) => {
  const retryCount = req.headers["x-retry-count"] || 0;

  // Log the retry count for debugging purposes
  console.log(`Retry Count: ${retryCount}`);

  const startTime = Date.now();
  const result = performMatrixMultiplication();

  // Microbenchmark: Check how long the computation took
  const duration = Date.now() - startTime;
  const maxDuration = 100;

  if (duration > maxDuration) {
    const response = await invokeNewInstance(req); // Try again, passing along the retry count
    // return res.status(500).send("Computation took too long, restarting...");
    return res.status(response.status).send({
      status: response.status,
      message: response.message,
    });
  }

  // res.status(200).send(`Computation successful. Result: ${result}`);
  res.status(200).send({
    status: 200,
    message: "Computation successful",
  });
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
      let errorMessage = `HTTP error! Status: ${response.status}`;

      try {
        const errorData = await response.json();
        errorMessage = errorData.message || errorMessage;
      } catch (parseError) {
        console.error("Failed to parse error response:", parseError);
      }

      return {
        status: response.status,
        message: errorMessage,
      };
    }

    let data = await response.json();
    return {
      status: data.status,
      message: data.message || "Success",
    };
  } catch (error) {
    console.error("Error:", error);
    return {
      status: 500,
      message: "Failed invoking new instance: " + error.message,
    };
  }
}
