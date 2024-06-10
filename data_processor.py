import os
import requests
import pandas as pd
from datetime import datetime

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    time_series_data = data.get('Time Series (Daily)', {})
    df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

    for date, daily_data in time_series_data.items():
        row = {
            'Date': date,
            'Open': daily_data['1. open'],
            'High': daily_data['2. high'],
            'Low': daily_data['3. low'],
            'Close': daily_data['4. close'],
            'Volume': daily_data['5. volume'],
        }
        df = df.append(row, ignore_index=True)

    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    return df

def analyze_trends(stock_dataframe):
    stock_dataframe['SMA_20'] = stock_dataframe['Close'].rolling(window=20).mean()
    stock_dataframe['SMA_50'] = stock_dataframe['Close'].rolling(window=50).mean()

    signal_buy = []
    signal_sell = []
    flag = -1 

    for i in range(len(stock_dataframe)):
        if stock_dataframe['SMA_20'][i] > stock_dataframe['SMA_50'][i] and flag != 1:
            signal_buy.append(stock_dataframe['Close'][i])
            signal_sell.append(float('nan'))
            flag = 1
        elif stock_dataframe['SMA_20'][i] < stock_dataframe['SMA_50'][i] and flag != 0:
            signal_sell.append(stock_dataframe['Close'][i])
            signal_buy.append(float('nan'))
            flag = 0
        else:
            signal_sell.append(float('nan'))
            signal_buy.append(float('nan'))
    
    stock_dataframe['Buy_Signal_Price'] = signal_buy
    stock_dataframe['Sell_Signal_Price'] = signal_sell

    return stock_dataframe

def generate_report(stock_dataframe, symbol):
    report = f"Stock Analysis Report for {symbol}\n"
    report += "---------------------------------\n"
    latest_data = stock_dataframe.iloc[-1]
    report += f"Latest Close Price: {latest_data['Close']}\n"
    report += f"Latest SMA 20: {latest_data['SMA_20']}\n"
    report += f"Latest SMA 50: {latest_data['SMA_50']}\n"
    
    if latest_data['SMA_20'] > latest_data['SMA_50']:
        report += "Recommendation: Potential Buy Signal Detected\n"
    else:
        report += "Recommendation: Potential Sell Signal Detected\n"
    
    trending = "upward" if latest_data['SMA_20'] > latest_data['SMA_50'] else "downward"
    report += f"Overall Trending: {trending}\n"
    
    return report

if __name__ == "__main__":
    symbol = 'AAPL'  
    df = fetch_stock_data(symbol)
    df_analyzed = analyze_trends(df)
    report = generate_report(df_analyzed, symbol)
    print(report)