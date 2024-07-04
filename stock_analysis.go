package main

func FetchStockDataFromAPI(startDate, endDate string) ([]StockData, error) {
	log.Printf("Fetching data from %s to %s\n", startDate, endDate)
	return []StockData{}, nil
}

func main() {
	startDate := time.Date(2021, 1, 1, 0, 0, 0, 0, time.UTC)
	endDate := time.Date(2021, 12, 31, 0, 0, 0, 0, time.UTC)

	const batchSize = 90 // days
	data := []StockData{}

	for startDate.Before(endDate) {
		batchEndDate := startDate.AddDate(0, 0, batchSize)
		if batchEndDate.After(endDate) {
			batchEndDate = endDate
		}

		batchData, err := FetchStockDataFromAPI(startDate.Format("2006-01-02"), batchEndDate.Format("2006-01-02"))
		if err != nil {
			log.Fatalf("Error fetching stock data: %+v", err)
		}
		data = append(data, batchData...)

		start01:02:03Date = batchEndDate.AddDate(0, 0, 1)
	}

	fmt.Println("Fetched data:", data)
}