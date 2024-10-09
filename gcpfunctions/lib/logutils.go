package lib

import (
	"fmt"

	"github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions/model"
)

const startLogSequence = "=== START LOG ==="
const endLogSequence = "=== END LOG ==="

// Prints the logs with a recogniseable start and end sequence
func PrintLogs(title string, req model.Request) {
	fmt.Println(startLogSequence)
	fmt.Println(title)
	fmt.Printf("TaskId: %s\n", req.TaskID)
	fmt.Printf("Time: %f\n", req.TotalTimeOfExecution)
	fmt.Printf("Retries: %d\n", req.RetryCount)
	fmt.Println(endLogSequence)
}
