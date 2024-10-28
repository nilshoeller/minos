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
	fmt.Printf("Retries: %d\n", req.RetryCount)
	fmt.Println(endLogSequence)
}

func PrintBaselineLogs(title string, req model.Request, maxTemp, minTemp, meanTemp float64) {
	fmt.Println(startLogSequence)
	fmt.Println(title)
	fmt.Printf("TaskId: %s\n", req.TaskID)
	fmt.Printf("Predicted MAX temperature: %2.f", maxTemp)
	fmt.Printf("Predicted MIN temperature: %2.f", minTemp)
	fmt.Printf("Predicted MEAN temperature: %2.f", meanTemp)
	fmt.Println(endLogSequence)
}
