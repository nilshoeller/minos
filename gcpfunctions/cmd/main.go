package main

import (
	"fmt"
	"log"
	"os"

	"github.com/GoogleCloudPlatform/functions-framework-go/funcframework"
	_ "github.com/nilshoeller/bsc-thesis-implementation/gcpfunctions"
)

// Commands to start local testing:
// export FUNCTION_TARGET=OptimizationFunction
// go run main.go
func main() {
	// Use PORT environment variable, or default to 8080.
	port := "8080"
	if envPort := os.Getenv("PORT"); envPort != "" {
		port = envPort
	}
	// Print server running message before starting the server
	fmt.Printf("Server running on localhost:%s\n", port)

	if err := funcframework.Start(port); err != nil {
		log.Fatalf("funcframework.Start: %v\n", err)
	}
}
