import axios from 'axios';
import { config } from 'dotenv';

config();

interface StockData {
    symbol: string;
    price: number;
    analysis: string;
}

class TradingAnalyticsPlatform {
    private baseUrl: string;

    constructor() {
        if (!process.env.BASE_URL) {
            throw new Error('BASE_URL is not defined in your environment variables');
        }
        this.baseUrl = process.env.BASE_URL;
    }

    async fetchStockData(symbol: string): Promise<StockData | null> {
        try {
            const response = await axios.get<StockData>(`${this.baseUrl}/stock-data/${symbol}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching stock data:', error);
            return null;
        }
    }
    
    renderStockData(stockData: StockData) {
        if (!stockData) {
            console.log('No data found.');
            return;
        }
        console.log(`Symbol: ${stockData.symbol}`);
        console.log(`Price: $${stockData.price}`);
        console.log(`Analysis: ${stockData.analysis}`);
    }
}

(async () => {
    const platform = new TradingAnalyticsPlatform();
    const userInputSymbol = 'AAPL';

    const stockData = await platform.fetchStockData(userInputSymbol);
    platform.renderStockData(stockData);
})();