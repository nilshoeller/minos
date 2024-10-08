package main

import (
	"bsc-thesis-implementation/lib"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/google/uuid"

	"github.com/GoogleCloudPlatform/functions-framework-go/funcframework"
)

func init() {
	functions.HTTP("OptimizationFunction", OptimizationFunction)
}

const maxRetries = 3

// const url = "https://us-central1-bsc-thesis-implementation.cloudfunctions.net/optimizationFunction1"
const url = "http://localhost:8080/"

// Response structure for the initial HTTP response
type Response struct {
	Message string `json:"message"`
	TaskID  string `json:"taskId"`
}

// Request structure for the incoming HTTP request
type Request struct {
	TaskID               string  `json:"taskId,omitempty"`
	RetryCount           int     `json:"retryCount,omitempty"`
	TotalTimeOfExecution float64 `json:"totalTimeOfExecution,omitempty"`
}

// BenchmarkResult structure to hold the result of the benchmarking
type BenchmarkResult struct {
	BenchmarkPassed bool
	TimeOfExecution time.Duration
}

// Handler for the optimization function
func OptimizationFunction(w http.ResponseWriter, r *http.Request) {
	var req Request

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil && err.Error() != "EOF" {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if req.TaskID == "" {
		req.TaskID = uuid.NewString()
	}
	if req.RetryCount < 0 {
		req.RetryCount = 0
	}
	if req.TotalTimeOfExecution < 0 {
		req.TotalTimeOfExecution = 0
	}

	// Immediate response to the client
	response := Response{
		Message: "Request received, processing...",
		TaskID:  req.TaskID,
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)

	// Perform benchmark
	benchmarkPassed, timeOfExecution := lib.PerformBenchmark(100 * time.Millisecond)

	if benchmarkPassed {
		fmt.Printf("Benchmark passed for taskId \"%s\" in time (%f).\n", req.TaskID, req.TotalTimeOfExecution)
		return
	}

	if req.RetryCount < maxRetries {
		req.RetryCount++
		req.TotalTimeOfExecution += timeOfExecution
		lib.InvokeNew(url, req.TaskID, req.RetryCount, req.TotalTimeOfExecution, timeOfExecution)
		return
	}
	fmt.Printf("Max retries reached for taskId \"%s\".\n", req.TaskID)
}

func main() {
	// Use PORT environment variable, or default to 8080.
	port := "8080"
	if envPort := os.Getenv("PORT"); envPort != "" {
		port = envPort
	}
	// Print server running message before starting the server
	fmt.Printf("Server running on localhost:%s\n", port)

	if err := funcframework.Start(port); err != nil {
		log.Fatalf("funcframework.Start: %v\n", err)
	}
}
