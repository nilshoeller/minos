package lib

import (
	"time"
)

// performBenchmark performs a benchmark on the matrix multiplication function
// to measure its execution time.
func PerformBenchmark(maxDuration time.Duration) (bool, float64) {
	startTime := time.Now()

	performMatrixMultiplication()

	// Measure how long the computation took
	duration := time.Since(startTime)

	return duration < maxDuration, duration.Seconds()
}
