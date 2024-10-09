package lib

import (
	"time"
)

// PerformBenchmark performs a micro-benchmark in milliseconds
func PerformBenchmark(maxDuration time.Duration) (bool, float64) {
	maxDuration = maxDuration * time.Millisecond

	startTime := time.Now()

	performMatrixMultiplication()

	// Measure how long the computation took
	duration := time.Since(startTime)

	return duration < maxDuration, duration.Seconds()
}
