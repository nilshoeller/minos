package lib

import (
	"time"
)

// PerformBenchmark performs a micro-benchmark in milliseconds
func PerformBenchmark(maxDuration time.Duration, benchmarkPassed *bool) {
	maxDuration = maxDuration * time.Millisecond

	startTime := time.Now()

	performMatrixMultiplication()

	// Measure how long the computation took
	duration := time.Since(startTime)

	if duration < maxDuration {
		*benchmarkPassed = true
	}

}

// PerformBenchmark performs a micro-benchmark in milliseconds
func PermormBenchmarkReturnDuration() float64 {
	startTime := time.Now()

	performMatrixMultiplication()

	// Measure how long the computation took
	duration := time.Since(startTime)

	return float64(duration.Seconds())
}
