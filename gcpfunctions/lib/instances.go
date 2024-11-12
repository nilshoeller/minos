package lib

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"sync"

	"github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions/model"
)

func InvokeNewWaitGroupWrapper(url string, body_information model.Request, wg *sync.WaitGroup) {
	defer wg.Done()
	err := InvokeNew(url, body_information)
	if err != nil {
		fmt.Println("Error in InvokeNew:", err)
	}
}

// invokeNew re-invokes the function at the specified URL.
func InvokeNew(
	url string,
	body_information model.Request,
) error {

	// Serialize the task to JSON.
	body, err := json.Marshal(body_information)
	if err != nil {
		return fmt.Errorf("failed to marshal body_information: %w", err)
	}

	// Create a new POST request.
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(body))
	if err != nil {
		return fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Content-Type", "application/json")

	// Send the request.
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("failed to invoke function for task %s: %w", body_information.TaskID, err)
	}
	defer resp.Body.Close()

	// Check if the response is successful.
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("unexpected status code: %d for task %s", resp.StatusCode, body_information.TaskID)
	}

	fmt.Println("Finished invoking new instance.")
	return nil
}
