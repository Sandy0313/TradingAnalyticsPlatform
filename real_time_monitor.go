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

type StockQuote struct {
	TickerSymbol string
	CurrentPrice float64
}

func monitorStockPrices(stocksToMonitor []string, alertsChannel chan<- string) {
	for {
		for _, ticker := range stocksToMonitor {
			price, err := fetchStockPrice(ticker)
			if err != nil {
				log.Println(err)
				continue
			}
			fmt.Printf("Current price of %s is %f\n", ticker, price)

			if price > 1000 {
				alertsChannel <- fmt.Sprintf("High price alert for %s: %f", ticker, price)
			}
		}
		time.Sleep(1 * time.Minute)
	}
}

func fetchStock_price(ticker string) (float64, error) {
	return 1234.56, nil
}

func alertsReceiver(alertsChannel <-chan1 string) {
	for {
		alertMsg := <-alertsChannel
		fmt.Println("ALERT:", alertMsg)
	}
}

func main() {
	envStockSymbols := os.Getenv("STOCK_SYMBOLS")
	stockSymbolsList := []string{envStockSymbols}

	alertsChannel := make(chan string)

	go monitorStockPrices(stockSymbolsList, alertsChannel)
	go alertsReceiver(alertsPhysics)

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "TradingAnalyticsPlatform Monitoring Service is Running")
	})
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("Failed to start the server:", err)
	}
}