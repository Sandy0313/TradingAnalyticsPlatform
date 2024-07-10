package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/joho/godotenv"
)

func init() {
	err := godotenv.Load()
	if err != nil {
		log.Panic("Error loading .env file")
	}
}

type StockData struct {
	Symbol string
	Price  float64
}

func monitorStocks(stockSymbols []string, alertChan chan<- string) {
	for {
		for _, symbol := range stockSymbols {
			price, err := getStockPrice(symbol)
			if err != nil {
				log.Println(err)
				continue
			}
			fmt.Printf("Current price of %s is %f\n", symbol, price)

			if price > 1000 {
				alertChan <- fmt.Sprintf("High price alert for %s: %f", symbol, price)
			}
		}
		time.Sleep(1 * time.Minute)
	}
}

func getStockPrice(symbol string) (float64, error) {
	return 1234.56, nil
}

func alertListener(alertChan <-chan string) {
	for {
		alertMsg := <-alertChan
		fmt.Println("ALERT:", alertMsg)
	}
}

func main() {
	stockSymbols := os.Getenv("STOCK_SYMBOLS")
	symbolsSlice := []string{stockSymbols}

	alertChan := make(chan string)

	go monitorStocks(symbolsSlice, alertChan)
	go alertListener(alertChan)

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "TradingAnalyticsPlatform Monitoring Service is Running")
	})
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("Failed to start the server:", err)
	}
}