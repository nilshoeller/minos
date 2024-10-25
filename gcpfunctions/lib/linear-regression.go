package lib

import (
	"encoding/csv"
	"log"
	"os"
	"strconv"
	"time"

	"gonum.org/v1/gonum/stat"
)

func daysElapsedSince(startDate string, dateStr string) (float64, error) {
	start, _ := time.Parse("2006-01-02", startDate)
	date, err := time.Parse("2006-01-02", dateStr)
	if err != nil {
		return 0, err
	}
	return date.Sub(start).Hours() / 24, nil
}

func readCSV(file *os.File) ([]float64, []float64, []float64, []float64) {
	reader := csv.NewReader(file)

	// Read data headers
	headers, err := reader.Read()
	if err != nil {
		log.Fatalf("Error reading weather data headers: %v", err)
	}

	// Validate headers
	if len(headers) != 4 {
		log.Fatal("CSV format mismatch or unexpected headers.")
	}

	// Extract temperature data and convert dates to days since start
	var days, tempMax, tempMin, tempMean []float64
	startDate := "1950-01-01"

	for {
		record, err := reader.Read()
		if err != nil {
			break // End of file
		}

		day, err := daysElapsedSince(startDate, record[0])
		if err != nil {
			log.Fatal(err)
		}
		currTempMax, err := strconv.ParseFloat(record[1], 64)
		if err != nil {
			log.Fatal(err)
		}
		currTempMin, err := strconv.ParseFloat(record[2], 64)
		if err != nil {
			log.Fatal(err)
		}
		currTempMean, err := strconv.ParseFloat(record[3], 64)
		if err != nil {
			log.Fatal(err)
		}

		days = append(days, day)
		tempMax = append(tempMax, currTempMax)
		tempMin = append(tempMin, currTempMin)
		tempMean = append(tempMean, currTempMean)
	}

	return days, tempMax, tempMin, tempMin
}

func performLinearRegression(days, temp []float64, text string) {
	// Perform linear regression
	b, a := stat.LinearRegression(days, temp, nil, false)

	nextDay := days[len(days)-1] + 1

	// Predict temperature for the next day
	predictedTemp := a*nextDay + b
	log.Printf("%s: %.2f°C\n", text, predictedTemp)
}

func ReadCsvAndPerformLR(destFileName string) {
	// Open CSV file
	file, err := os.Open(destFileName)
	if err != nil {
		log.Fatal(err)
	}

	days, tempMax, tempMin, tempMean := readCSV(file)
	file.Close()

	performLinearRegression(days, tempMax, "Predicted MAX temperature for next day")
	performLinearRegression(days, tempMin, "Predicted MIN temperature for next day")
	performLinearRegression(days, tempMean, "Predicted MEAN temperature for next day")
}
