package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
)

type Stock struct {
	Ticker string  `json:"ticker"`
	Price  float64 `json:"price"`
}

var stocks = make(map[string]Stock)

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	serverPort := os.Getenv("SERVER_PORT")
	if serverPort == "" {
		log.Fatal("$SERVER_PORT must be set")
	}

	router := mux.NewRouter()

	router.HandleFunc("/stocks", RetrieveAllStocks).Methods("GET")
	router.HandleFunc("/stock/{ticker}", RetrieveStock).Methods("GET")
	router.HandleFunc("/stock", AddOrUpdateStock).Methods("POST")
	router.HandleFunc("/stock/{ticker}", RemoveStock).Methods("DELETE")

	log.Printf("Server starting on port %s", serverPort)
	log.Fatal(http.ListenAndServe(":"+serverPort, router))
}

func RetrieveAllStocks(w http.ResponseWriter, _ *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(stocks)
}

func RetrieveStock(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r) 
	if stock, exists := stocks[params["ticker"]]; exists {
		json.NewEncoder(w).Encode(stock)
	} else {
		w.WriteHeader(http.StatusNotFound)
		json.NewEncoder(w).Encode(Stock{})
	}
}

func AddOrUpdateStock(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	var stockInput Stock
	if err := json.NewDecoder(r.Body).Decode(&stockInput); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	stocks[stockInput.Ticker] = stockInput
	json.NewEncoder(w).Encode(stockInput)
}

func RemoveStock(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	if _, exists := stocks[params["ticker"]]; exists {
		delete(stocks, params["ticker"])
		w.WriteHeader(http.StatusOK)
	} else {
		w.WriteHeader(http.StatusNotFound)
	}
}