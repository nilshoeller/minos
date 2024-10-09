package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/nilshoeller/bsc-thesis-implementation/lib"
	"github.com/nilshoeller/bsc-thesis-implementation/model"

	"github.com/GoogleCloudPlatform/functions-framework-go/funcframework"
	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/google/uuid"
)

const maxRetries = 3

const url = "https://us-central1-bsc-thesis-implementation.cloudfunctions.net/optimizationFunctionGo"

// const url = "http://localhost:8080/"

func init() {
	functions.HTTP("OptimizationFunction", OptimizationFunction)
}

// Handler for the optimization function
func OptimizationFunction(w http.ResponseWriter, r *http.Request) {
	var req model.Request

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil && err.Error() != "EOF" {
		fmt.Println("test")
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
	response := model.Response{
		Message: "Request received, processing...",
		TaskID:  req.TaskID,
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)

	var benchmarkResult model.BenchmarkResult

	// Perform benchmark
	benchmarkResult.BenchmarkPassed, benchmarkResult.TimeOfExecution = lib.PerformBenchmark(100 * time.Millisecond)

	if benchmarkResult.BenchmarkPassed {
		fmt.Printf("Benchmark passed for taskId \"%s\" in time (%f).\n", req.TaskID, req.TotalTimeOfExecution)
		return
	}

	if req.RetryCount < maxRetries {
		req.RetryCount++
		req.TotalTimeOfExecution += benchmarkResult.TimeOfExecution
		lib.InvokeNew(url, req.TaskID, req.RetryCount, req.TotalTimeOfExecution, benchmarkResult.TimeOfExecution)
		return
	}
	fmt.Printf("Max retries reached for taskId \"%s\".\n", req.TaskID)
}

// Commands to start local testing
// export FUNCTION_TARGET=OptimizationFunction
// go run main.go
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
