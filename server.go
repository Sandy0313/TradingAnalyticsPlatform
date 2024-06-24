package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
)

type StockData struct {
	Ticker string  `json:"ticker"`
	Price  float64 `json:"price"`
}

var stockDatabase = make(map[string]StockData)

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	port := os.Getenv("SERVER_PORT")
	if port == "" {
		log.Fatal("$SERVER_PORT must be set")
	}

	router := mux.NewRouter()

	router.HandleFunc("/stocks", GetStocks).Methods("GET")
	router.HandleFunc("/stock/{ticker}", GetStock).Methods("GET")
	router.HandleFunc("/stock", CreateOrUpdateStock).Methods("POST")
	router.HandleFunc("/stock/{ticker}", DeleteStock).Methods("DELETE")

	log.Printf("Server starting on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, router))
}

func GetStocks(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(stockDatabase)
}

func GetStock(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r) 
	if stock, ok := stockDatabase[params["ticker"]]; ok {
		json.NewEncoder(w).Encode(stock)
	} else {
		w.WriteHeader(http.StatusNotFound)
		json.NewEncoder(w).Encode(&StockData{})
	}
}

func CreateOrUpdateStock(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	var stock StockData
	if err := json.NewDecoder(r.Body).Decode(&stock); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	stockDatabase[stock.Ticker] = stock
	json.NewEncoder(w).Encode(stock)
}

func DeleteStock(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	if _, ok := stockDatabase[params["ticker"]]; ok {
		delete(stockDatabase, params["ticker"])
		w.WriteHeader(http.StatusOK)
	} else {
		w.WriteHeader(http.StatusNotFound)
	}
}