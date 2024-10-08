package lib

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

// Task represents the structure of the data sent in the POST request.
type Task struct {
	TaskID               string  `json:"taskId"`
	RetryCount           int     `json:"retryCount"`
	TotalTimeOfExecution float64 `json:"totalTimeOfExecution"`
}

// invokeNew re-invokes the function at the specified URL.
func InvokeNew(
	url string,
	taskID string,
	retryCount int,
	totalTimeOfExecution float64,
	timeOfExecution float64,
) error {
	task := Task{
		TaskID:               taskID,
		RetryCount:           retryCount + 1,
		TotalTimeOfExecution: totalTimeOfExecution + timeOfExecution,
	}

	// Serialize the task to JSON.
	body, err := json.Marshal(task)
	if err != nil {
		return fmt.Errorf("failed to marshal task: %w", err)
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
		return fmt.Errorf("failed to invoke function for task %s: %w", taskID, err)
	}
	defer resp.Body.Close()

	// Check if the response is successful.
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("unexpected status code: %d for task %s", resp.StatusCode, taskID)
	}

	return nil
}
