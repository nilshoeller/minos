package lib

import (
	"fmt"
	"time"
)

// PerformBenchmark performs a micro-benchmark in milliseconds
func PerformBenchmark(maxDuration time.Duration, benchmarkPassed *bool) {
	startTime := time.Now()

	performMatrixMultiplication()

	// Measure how long the computation took
	duration := time.Since(startTime)

	if duration < maxDuration {
		*benchmarkPassed = true
		fmt.Printf("BM PASSED: %2.f\n", float64(duration)/float64(time.Microsecond))
	} else {
		fmt.Printf("BM: %2.f < %2.f\n", float64(maxDuration)/float64(time.Microsecond), float64(duration)/float64(time.Microsecond))
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
