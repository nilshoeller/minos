package gcpfunctions

// Global vars for Google Cloud Storage
const (
	bucketName          = "bsc-implementation-bucket"
	objectName          = "historic-weather-data-1950.csv"
	destinationFileName = "/tmp/historic-weather-data-1950.csv"
)

// Global vars
const (
	retry_url           = "https://europe-west3-bsc-thesis-implementation.cloudfunctions.net/optimizedFunction"
	maxRetries          = 10
	taskExecutionAmount = 10 // how often should we perform LR (for longer execution)
)
