package gcpfunctions

import (
	"encoding/json"
	"net/http"
	"time"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/google/uuid"
	"github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions/lib"
	"github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions/model"
)

const url = "https://europe-west3-bsc-thesis-implementation.cloudfunctions.net/optimizedFunction"

// const url = "http://localhost:8080/"

const maxRetries = 3

const benchmarkMaxDuration = 5
const downloadingDuration = 10

var benchmarkPassed = false

func init() {
	functions.HTTP("OptimizedFunction", OptimizedFunction)
}

// Handler for the optimization function
func OptimizedFunction(w http.ResponseWriter, r *http.Request) {
	// Decode req-body
	var req model.Request
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

	// Immediate response to the client
	response := model.Response{
		Message: "Request received, processing...",
		TaskID:  req.TaskID,
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)

	// If instance is fast and don't have to perform the benchmark
	if !benchmarkPassed {
		// Concurrently perform the benchmark
		go lib.PerformBenchmark(benchmarkMaxDuration, &benchmarkPassed)
	}
	// Simulate downloading for 10 milliseconds
	time.Sleep(downloadingDuration * time.Millisecond)

	if benchmarkPassed {
		lib.PrintLogs("Benchmark passed", req)
		return
	}

	if req.RetryCount < maxRetries {
		req.RetryCount++
		lib.InvokeNew(url, req)
		return
	}

	lib.PrintLogs("Max retries reached", req)
}
