package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
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
				var alertMsg strings.Builder
				alertMsg.WriteString("High price alert for ")
				alertMsg.WriteString(ticker)
				alertMsg.WriteString(fmt.Sprintf(": %.2f", price))
				alertsChannel <- alertMsg.String()
			}
		}
		time.Sleep(1 * time.Minute)
	}
}

func fetchStockPrice(ticker string) (float64, error) {
	return 1234.56, nil
}

func receiveAlerts(alertsChannel <-chan string) {
	for alertMsg := range alertsChannel {
		fmt.Println("ALERT:", alertMsg)
	}
}

func main() {
	envStockSymbols := os.Getenv("STOCK_SYMBOLS")
	stockSymbolsList := strings.Split(envStockSymbols, ",")

	alertsChannel := make(chan string, 10)

	go monitorStocks(stockSymbolsList, alertsChannel)
	go receiveAlerts(alertsChannel)

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "TradingAnalyticsPlatform Monitoring Service is Running")
	})
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("Failed to start the server:", err)
	}
}