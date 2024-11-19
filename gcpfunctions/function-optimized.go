package gcpfunctions

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/google/uuid"
	"github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions/db"
	"github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions/lib"
	"github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions/model"
)

const url = "https://europe-west3-bsc-thesis-implementation.cloudfunctions.net/optimizedFunction"

const maxRetries = 3

// med: 0.004192012 Seconds
var benchmarkMaxDuration = 3880 * time.Microsecond // = 4.2 Milliseconds

var benchmarkPassed = false

func init() {
	functions.HTTP("OptimizedFunction", OptimizedFunction)
}

// Handler for the optimization function
func OptimizedFunction(w http.ResponseWriter, r *http.Request) {
	// Extract maxBenchmark parameter
	benchmarkMaxDurationParam := r.URL.Query().Get("maxBenchmarkDuration")

	if benchmarkMaxDurationParam != "" {
		parsedDuration, err := time.ParseDuration(benchmarkMaxDurationParam)
		if err != nil {
			fmt.Printf("Invalid maxBenchmark value: %v\n", err)
		} else {
			benchmarkMaxDuration = parsedDuration
		}
	}

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

	// Create a wait group
	wg := new(sync.WaitGroup)
	wg.Add(1)
	// currently no error handling because of goroutine, maybe channels would work
	startTime := time.Now()
	go db.DownloadFileWaitGroupWrapper(bucketName, objectName, destinationFileName, wg)

	// If we already know instance is fast -> don't have to perform the benchmark
	if !benchmarkPassed {
		// Concurrently perform the benchmark
		lib.PerformBenchmark(benchmarkMaxDuration, &benchmarkPassed)
	} else {
		fmt.Println("Fast instance")
	}

	if benchmarkPassed {
		// Ensure download completes
		wg.Wait()
		duration := time.Since(startTime)
		fmt.Printf("Download-duration: %2.f\n", float64(duration)/float64(time.Millisecond))

		startTimeLR := time.Now()

		maxTemp, minTemp, meanTemp := lib.ReadCsvAndPerformLR(destinationFileName)
		maxTemp, minTemp, meanTemp = lib.ReadCsvAndPerformLR(destinationFileName)
		maxTemp, minTemp, meanTemp = lib.ReadCsvAndPerformLR(destinationFileName)

		durationLR := time.Since(startTimeLR)
		fmt.Printf("LR-duration: %2.f\n", float64(durationLR)/float64(time.Millisecond))

		lib.PrintLogsOptimized("Execution finished", req, maxTemp, minTemp, meanTemp)
		return
	}

	if req.RetryCount < maxRetries {
		req.RetryCount++
		// Construct the URL with the maxBenchmark parameter
		newInstanceURL := fmt.Sprintf("%s?maxBenchmarkDuration=%s", url, benchmarkMaxDuration.String())
		lib.InvokeNew(newInstanceURL, req)
		// After invoking new instance crash current slow instance
		fmt.Println("Crashing instance")
		os.Exit(0)
	}

	lib.PrintLogs("Max retries reached", req)
	return
}
