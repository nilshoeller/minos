package gcpfunctions

import (
	"encoding/json"
	"net/http"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/google/uuid"
	"github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions/lib"
	"github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions/model"
)

func init() {
	functions.HTTP("ExecuteBenchmark", ExecuteBenchmark)
}

// Handler for the execute benchmark
func ExecuteBenchmark(w http.ResponseWriter, r *http.Request) {
	// Decode req-body
	var req model.Request
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil && err.Error() != "EOF" {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if req.TaskID == "" {
		req.TaskID = uuid.NewString()
	}

	benchmarkDuration := lib.PermormBenchmarkReturnDuration()
	// Immediate response to the client
	response := model.BenchmarkResponse{
		Message:  "Performed benchmark.",
		Duration: benchmarkDuration,
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}
