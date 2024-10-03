module.exports = {
  performMatrixMultiplication,
};

/**
 * Performs matrix multiplication on two randomly generated square matrices of a fixed size.
 *
 * @returns {number[][]} The resulting matrix from the multiplication of the two matrices.
 */
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
