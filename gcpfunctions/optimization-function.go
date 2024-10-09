package gcpfunctions

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/google/uuid"
	"github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions/lib"
	"github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions/model"
)

const maxRetries = 3

const url = "https://europe-west3-bsc-thesis-implementation.cloudfunctions.net/optimizationFunction"

// const url = "http://localhost:8080/"

func init() {
	functions.HTTP("OptimizationFunction", OptimizationFunction)
}

// Handler for the optimization function
func OptimizationFunction(w http.ResponseWriter, r *http.Request) {
	// Decode req-body
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

	// Perform benchmark
	var benchmarkResult model.BenchmarkResult
	benchmarkResult.BenchmarkPassed, benchmarkResult.TimeOfExecution = lib.PerformBenchmark(7)

	// Update total time of execution
	req.TotalTimeOfExecution += benchmarkResult.TimeOfExecution

	if benchmarkResult.BenchmarkPassed {
		lib.PrintLogs("Benchmark passed.", req)

		return
	}

	if req.RetryCount < maxRetries {
		req.RetryCount++
		lib.InvokeNew(url, req)
		return
	}

	lib.PrintLogs("Max retries reached.", req)
}
