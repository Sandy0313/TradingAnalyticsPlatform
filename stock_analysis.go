package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"log"
	"math"
	"os"
	"strconv"
	"time"
)

var env map[string]string

func init() {
	env = make(map[string]string)
	env["DATA_FILE_PATH"] = "path/to/your/data.csv"
}

type StockData struct {
	Date     time.Time
	Open     float64
	High     float64
	Low      float64
	Close    float64
	Volume   int64
	AdjClose float64
}

func LoadStockData(filePath string) ([]StockData, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	r := csv.NewReader(file)
	_, err = r.Read() // Skip header
	if err != nil {
		return nil, err
	}

	return parseCSVRecordsToStockData(r)
}

func parseCSVRecordsToStockData(r *csv.Reader) ([]StockData, error) {
	var records []StockData

	for {
		record, err := r.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, err
		}

		data, err := parseRecordToStockData(record)
		if err != nil {
			return nil, err // Consider logging or collecting errors here instead of returning immediately
		}

		records = append(records, data)
	}

	return records, nil
}

func parseRecordToStockData(record []string) (StockData, error) {
	date, err := time.Parse("2006-01-02", record[0])
	if err != nil {
		return StockData{}, err
	}
	open, err := strconv.ParseFloat(record[1], 64)
	high, err := strconv.ParseFloat(record[2], 64)
	low, err := strconv.ParseFloat(record[3], 64)
	close, err := strconv.ParseFloat(record[4], 64)
	volume, err := strconv.ParseInt(record[5], 10, 64)
	adjClose, err := strconv.ParseFloat(record[6], 64)
	if err != nil {
		return StockData{}, err // This returns the last error, consider aggregating errors if needed
	}

	return StockData{Date: date, Open: open, High: high, Low: low, Close: close, Volume: volume, AdjClose: adjClose}, nil
}

func CalculateMovingAverage(data []StockData, period int) ([]float64, error) {
	if period <= 0 || period > len(data) {
		return nil, fmt.Errorf("invalid period")
	}

	var movingAverages []float64

	for i := period; i <= len(data); i++ {
		sum := calculateSumForPeriod(data[i-period : i])
		movingAverages = append(movingAverages, sum/float64(period))
	}

	return movingAverages, nil
}

func calculateSumForPeriod(data []StockData) float64 {
	sum := 0.0
	for _, d := range data {
		sum += d.Close
	}
	return sum
}

func CalculateVolatility(data []StockData) ([]float64, error) {
	if len(data) <= 1 {
		return nil, fmt.Errorf("not enough data")
	}

	return calculateVolatilities(data), nil
}

func calculateVolatilities(data []StockData) []float64 {
	var volatilities []float64

	for i := 1; i < len(data); i++ {
		volatility := (data[i].High - data[i].Low) / data[i-1].Close * 100
		volatilities = append(volatilities, volatility)
	}

	return volatilities
}

func GenerateRealTimeAnalysis(data []StockData) {
	log.Println("Real-time analysis not implemented")
}

func main() {
	dataFilePath := env["DATA_FILE_PATH"]
	if dataFilePath == "" {
		log.Fatal("DATA_FILE_PATH env variable is not set")
	}

	data, err := LoadStockData(dataFilePath)
	if err != nil {
		log.Fatalf("Error loading stock data: %+v", err)
	}

	movingAverages, err := CalculateMovingAverage(data, 20)
	if err != nil {
		log.Fatalf("Error calculating moving averages: %+v", err)
	}
	fmt.Println("20-day moving averages:", movingAverages)

	volatilities, err := CalculateVolatility(data)
	if err != nil {
		log.Fatalf("Error calculating volatilities: %+v", err)
	}
	fmt.Println("Volatilities:", volatilities)

	GenerateRealTimeAnalysis(data)
}