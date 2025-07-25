package gcpfunctions

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/google/uuid"
	"github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions/db"
	"github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions/lib"
	"github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions/model"
)

func init() {
	functions.HTTP("BaselineFunction", BaselineFunction)
}

// Handler for the optimization function
func BaselineFunction(w http.ResponseWriter, r *http.Request) {
	// Decode req-body
	var req model.Request
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil && err.Error() != "EOF" {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if req.TaskID == "" {
		req.TaskID = uuid.NewString()
	}

	// Immediate response to the client
	response := model.Response{
		Message: "Request received, processing...",
		TaskID:  req.TaskID,
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)

	startTime := time.Now()
	// Download from cloud storage
	if err := db.DownloadFile(bucketName, objectName, destinationFileName); err != nil {
		fmt.Println("downloading file: ", err)
		return
	}
	duration := time.Since(startTime)
	fmt.Printf("Download-duration: %2.f\n", float64(duration)/float64(time.Millisecond))

	startTimeLR := time.Now()

	maxTemp, minTemp, meanTemp := lib.PerformTask(destinationFileName, taskExecutionAmount)

	durationLR := time.Since(startTimeLR)
	fmt.Printf("LR-duration: %2.f\n", float64(durationLR)/float64(time.Millisecond))

	lib.PrintBaselineLogs("Execution finished", req, maxTemp, minTemp, meanTemp)
}
