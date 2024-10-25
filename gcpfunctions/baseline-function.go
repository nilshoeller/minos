package gcpfunctions

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/google/uuid"
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

	// Simulate downloading for 10 milliseconds
	time.Sleep(downloadingDuration * time.Millisecond)

	lib.PrintBaselineLogs("Execution finished.", req)

	// download from cloud storage and print document
	bucketName := "test-bucket-myfunction"
	objectName := "test.txt"
	destinationFileName := "/tmp/test-downloaded.txt"

	if err := lib.DownloadFile(bucketName, objectName, destinationFileName); err != nil {
		fmt.Println("downloading file: ", err)
		return
	}

	// Re-open the file to read its content and print it
	fileContent, err := os.ReadFile(destinationFileName)
	if err != nil {
		fmt.Println("os.ReadFile: ", err)
		return
	}

	// Print the file content to the logs
	fmt.Println("File content:\n", string(fileContent))

}
