package db

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
)

type WeatherResponse struct {
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`
	Timezone  string  `json:"timezone"`
	Daily     struct {
		Temperature2mMax  []float64 `json:"temperature_2m_max"`
		Temperature2mMin  []float64 `json:"temperature_2m_min"`
		Temperature2mMean []float64 `json:"temperature_2m_mean"`
		Time              []string  `json:"time"`
	} `json:"daily"`
}

func callWeatherAPI() WeatherResponse {
	// API URL
	url := "https://archive-api.open-meteo.com/v1/archive?latitude=46.4907&longitude=11.3398&start_date=2000-01-01&end_date=2024-10-28&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean&timezone=Europe%2FBerlin"

	// Make HTTP GET request
	resp, err := http.Get(url)
	if err != nil {
		log.Fatalf("Error making the request: %v", err)
	}
	defer resp.Body.Close()

	// Check if the request was successful
	if resp.StatusCode != http.StatusOK {
		log.Fatalf("Error: received non-200 response code %d", resp.StatusCode)
	}

	// Read the response body
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Error reading response body: %v", err)
	}

	// Parse JSON response
	var weatherData WeatherResponse
	err = json.Unmarshal(body, &weatherData)
	if err != nil {
		log.Fatalf("Error parsing JSON: %v", err)
	}

	return weatherData
}

func getWeatherData() {

	// startTime := time.Now()

	weatherData := callWeatherAPI()

	fmt.Println("Weather Data:")
	fmt.Printf("Latitude: %.4f, Longitude: %.4f\n", weatherData.Latitude, weatherData.Longitude)
	fmt.Println("Timezone:", weatherData.Timezone)

	// for i, date := range weatherData.Daily.Time {
	// 	fmt.Printf("Date: %s - Max Temp: %.2f, Min Temp: %.2f, Mean Temp: %.2f\n",
	// 		date,
	// 		weatherData.Daily.Temperature2mMax[i],
	// 		weatherData.Daily.Temperature2mMin[i],
	// 		weatherData.Daily.Temperature2mMean[i])
	// }

	// duration := time.Since(startTime)
	// fmt.Printf("Duration: %d milliseconds \n", duration.Milliseconds())
}
