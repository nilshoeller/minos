const matrixMult = require("./matrix-mult");

module.exports = {
  performBenchmark,
};

function performBenchmark(maxDuration) {
  const startTime = Date.now();

  matrixMult.performMatrixMultiplication();

  // Microbenchmark: Check how long the computation took
  const duration = Date.now() - startTime;

  return {
    benchmarkPassed: duration < maxDuration,
    timeOfExecution: duration,
  };
}
