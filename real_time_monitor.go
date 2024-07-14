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

// StockQuote represents the price quote for a stock
type StockQuote struct {
	TickerSymbol string
	CurrentPrice float64
}

// monitorStocks checks the stock prices and sends alerts if price conditions are met
func monitorStocks(stocksToMonitor []string, alertsChannel chan<- string) {
	for {
		for _, ticker := range stocksToMonitor {
			price, err := fetchStockPrice(ticker)
			if err != nil {
				log.Printf("Error fetching price for %s: %v\n", ticker, err)
				continue
			}
			fmt.Printf("Current price of %s is %.2f\n", ticker, price)

			if price > 1000 {
				alertsChannel <- fmt.Sprintf("High price alert for %s: %.2f", ticker, price)
			}
		}
		time.Sleep(1 * time.Minute)
	}
}

// fetchStockPrice simulates fetching the current stock price
// Note: Integrate with a real API for actual stock prices
func fetchStockPrice(ticker string) (float64, error) {
	// Placeholder implementation
	return 1234.56, nil
}

// receiveAlerts listens for alerts and prints them
func receiveAlerts(alertsChannel <-chan string) {
	for {
		alertMsg := <-alertsChannel
		fmt.Println("ALERT:", alertMsg)
	}
}

func main() {
	envStockSymbols := os.Getenv("STOCK_SYMBOLS")
	// Assuming STOCK_SYMBOLS are comma-separated, split into a slice
	stockSymbolsList := strings.Split(envStockSymbols, ",")

	alertsChannel := make(chan string)

	go monitorStocks(stockSymbolsList, alertsChannel)
	go receiveAlerts(alertsChannel)

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "TradingAnalyticsPlatform Monitoring Service is Running")
	})
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("Failed to start the server:", err)
	}
}