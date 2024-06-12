import os
import requests
import pandas as pd
from datetime import datetime

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code.
        data = response.json()
        time_series_data = data.get('Time Series (Daily)', {})
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:", repr(errh))
        return None
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:", repr(errc))
        return None
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:", repr(errt))
        return None
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred:", repr(err))
        return None

    df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

    try:
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

    except Exception as e:
        print(f"An error occurred while processing the data: {e}")
        return None

    try:
        df['Date'] = pd.to_datetime(df['Date'])
    except Exception as e:
        print(f"Error converting Date column to datetime: {e}")
        return None

    df.sort_values(by='Date', inplace=True)
    return df

def analyze_trends(stock_dataframe):
    if stock_dataframe is None:
        print("No data to analyze")
        return None

    stock_dataframe['SMA_20'] = stock_dataframe['Close'].rolling(window=20).mean()
    stock_dataframe['SMA_50'] = stock_dataframe['Close'].rolling(window=50).mean()

    signal_buy = []
    signal_sell = []
    flag = -1 

    try:
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

    except Exception as e:
        print(f"An error occurred while analyzing trends: {e}")
        return None

    stock_dataframe['Buy_Signal_Price'] = signal_buy
    stock_dataframe['Sell_Signal_Price'] = signal_sell

    return stock_dataframe

def generate_report(stock_dataframe, symbol):
    if stock_dataframe is None:
        return "An error occurred. Unable to generate report."

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
    if df is not None:
        df_analyzed = analyze_trends(df)
        if df_analyzed is not None:
            report = generate_report(df_analyzed, symbol)
            print(report)
        else:
            print("Error in trend analysis. No report generated.")
    else:
        print("Error fetching stock data. No report generated.")