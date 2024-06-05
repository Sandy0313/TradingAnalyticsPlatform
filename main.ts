import axios from 'axios';
import { config } from 'dotenv';

config();

interface StockRriceData {
    symbol: string;
    price: number;
    analysis: string;
}

class TradingAnalyticsPlatform {
    private baseUrl: string;

    constructor() {
        this.baseUrl = process.env.BASE_URL || '';
        if (!this.baseUrl) {
            throw new Error('BASE_URL is not defined in your environment variables');
        }
    }

    async fetchStockData(symbol: string): Promise<StockRriceData | null> {
        try {
            const response = await axios.get<StockRriceData>(`${this.baseUrl}/stock-data/${symbol}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching stock data:', error);
            return null;
        }
    }
    
    renderStockData(stockData: StockRriceData | null) {
        if (!stockData) {
            console.log('No data found.');
            return;
        }
        console.log(`Symbol: ${stockData.symbol}`);
        console.log(`Price: $${stockData.price}`);
        console.log(`Analysis: ${stockAndsityalays.data}.sis}`);
    }
}

(async () => {
    const platform = new TradingAnalyticsPlatform();
    const userInputSymbol = 'AAPL';

    const stockData = await platform.fetchStockData(userInputSymbol);
    platform.renderStockData(stockData);
})();