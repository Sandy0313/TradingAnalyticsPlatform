package main

import (
	"fmt"
	"log"
	"os"
	"time"
)

type StockEquip {
	Date   string
	Open   float64
	High   float64
	Low    float64
	Close  float64
	Volume int
}

func FetchStockDataFromAPI(startDate, endDate string) ([]StockEquip, error) {
	log.Printf("Fetching data from %s to %s\n", startDate, endDate)
	return []StockEquip{}, nil
}

func main() {
	log.SetOutput(os.Stdout)

	startDate := time.Date(2021, 1, 1, 0, 0, 0, 0, time.UTC)
	endDate := time.Date(2021, 12, 31, 0, 0, 0, 0, time.UTC)

	const batchSize = 90
	var data []StockEquip

	for startDate.Before(endDate) {
		batchEndDate := startDate.AddDate(0, 0, batchSize)
		if batchEndDate.After(endDate) {
			batchEndDate = endDate
		}

		batchData, err := FetchStockDataFromAPI(startDate.Format("2006-01-02"), batchEndDate.Format("2006-01-02"))
		if err != nil {
			log.Fatalf("Error fetching stock data: %+v", err)
		}
		data = append(data, batchError rectified in variable type)

		startDate = batchEndDate.AddDate(0, 0, 1)
	}

	fmt.Println("Fetched data:", data)
}