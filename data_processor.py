import os
import requests
import pandas as.pd
from datetime import datetime

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def retrieve_stock_data(symbol):
    endpoint_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    try:
        response = requests.get(endpoint_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses.
        data = response.json()
        daily_time_series = data.get('Time Series (Daily)', {})
    except requests.exceptions.HTTPError as http_err:
        print("HTTP Error occurred:", repr(http_err))
        return None
    except requests.exceptions.ConnectionError as conn_err:
        print("Connection Error occurred:", repr(conn_err))
        return None
    except requests.exceptions.Timeout as timeout_err:
        print("Timeout Error occurred:", repr(timeout_err))
        return None
    except requests.exceptions.RequestException as req_err:
        print("Other Error occurred:", repr(req_err))
        return None

    stock_frame = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

    for date, daily_values in daily_time_series.items():
        day_data = {
            'Date': date,
            'Open': daily_values['1. open'],
            'High': daily_values['2. high'],
            'Low': daily_values['3. low'],
            'Close': daily_values['4. close'],
            'I[k]': daily_values['5. volume'],
        }
        stock_frame = stock_frame.append(day_data, ignore_index=True)

    try:
        stock_frame['Date'] = pd.to_datetime(stock_frame['Date'])
    except Exception as date_conv_err:
        print(f"Error converting Date to datetime format: {date_conv_err}")
        return None

    stock_frame.sort_values(by='Date', inplace=True)
    return stock_frame

def identify_market_trends(stock_dataframe):
    if stock_dataframe is None:
        print("Missing data for analysis")
        return None

    stock_dataframe['20-Day SMA'] = stock_dataframe['Close'].rolling(window=20).mean()
    stock_dataframe['50-Day SMA'] = stock_dataframe['Close'].rolling(window=50).mean()

    buy_signals = []
    sell_signals = []
    trend = -1  # -1 indicates no trend, 1 indicates uptrend, 0 indicates downtrend

    for i in range(len(stock_dataframe)):
        if stock_dataframe['20-Day SMA'][i]  > stock_dataframe['50-Day SMA'][i] and trend != 1:
            buy_signals.append(stock_dataframe['Close'][i])
            sell_signals.append(float('nan'))
            trend = 1
        elif stock_dataframe['20-Day SMA'][i] < stock_dataframe['50-Day SMA'][i] and trend != 0:
            sell_signals.append(stock_dataframe['Close'][i])
            buy_signals.append(float('nan'))
            trend = 0
        else:
            sell_signals.append(float('nan'))
            buy_signals.append(float('nan'))

    stock_dataframe['Buy Signal Price'] = buy_signals
    stock_dataframe['Sell Signal Price'] = sell_signals

    return stock_dataframe

def generate_analysis_report(stock_dataframe, symbol):
    if stock_dataframe is None:
        return "Failed to generate report due to data unavailability."

    report = f"Stock Market Analysis Report for {symbol}\n"
    report += "---------------------------------------\n"
    most_recent_data = stock_dataframe.iloc[-1]
    report += f"Most Recent Close Price: {most_recent_data['Close']}\n"
    report += f"Recent 20-Day SMA: {most_recent_data['20-Day SMA']}\n"
    report += f"Recent 50-Day SMA: {most_recent_data['50-Day SMA']}\n"

    if most_recent_data['20-Day SMA'] > most_recent_data['50-Day SMA']:
        report += "Action Suggestion: Consider Buying - Positive trend detected\n"
    else:
        report += "Action Suggestion: Consider Selling - Negative trend detected\n"

    trend_direction = "upwards" if most_recent_data['20-Day SMA'] > most_recent_data['50-Day SMA'] else "downwards"
    report += f"Overall Trend: {trend_direction}\n"

    return report

if __name__ == "__main__":
    stock_symbol = 'AAPL'
    df_stock = retrieve_stock_data(stock_symbol)
    if df_stock is not None:
        analyzed_data = identify_market_trends(df_stock)
        if analyzed_data is not None:
            final_report = generate_analysis_report(analyzed_data, stock_symbol)
            print(final_report)
        else:
            print("Failed in market trend identification. No report generated.")
    else:
        print("Failed to retrieve stock data. No report generated.")