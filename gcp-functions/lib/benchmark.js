const matrixMult = require("./matrix-mult");

module.exports = {
  performBenchmark,
};

/**
 * Performs a benchmark on the matrix multiplication function to measure its execution time.
 *
 * @param {number} maxDuration - The maximum allowable duration for the matrix multiplication
 *                                to be considered a pass.
 * @returns {{ benchmarkPassed: boolean, timeOfExecution: number }} An object containing the
 *          result of the benchmark and the time taken for the execution.
 *          - `benchmarkPassed`: A boolean indicating whether the execution time was less than
 *                                the specified maximum duration.
 *          - `timeOfExecution`: The time taken for the matrix multiplication in milliseconds.
 */
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
