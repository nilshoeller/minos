package model

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
	TimeOfExecution float64
}
