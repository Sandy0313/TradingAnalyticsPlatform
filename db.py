import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME", "trading_analytics.db")

def connect_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def define_schema():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_data (
        id INTEGER PRIMARY KEY,
        symbol TEXT NOT NULL,
        date DATE NOT NULL,
        open_price REAL,
        close_price REAL,
        high_price REAL,
        low_price REAL,
        volume INTEGER
    )
    ''')
    conn.commit()
    conn.close()

def insert_stock_data(symbol, date, open_price, close_price, high_price, low_price, volume):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO stock_data (symbol, date, open_price, close_price, high_price, low_price, volume)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (symbol, date, open_price, close_price, high_price, low_price, volume))
    conn.commit()
    conn.close()

def read_stock_data(symbol, start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM stock_data
    WHERE symbol = ? AND date BETWEEN ? AND ?
    ''', (symbol, start_date, end_date))
    data = cursor.fetchall()
    conn.close()
    return data

if __name__ == "__main__":
    define_schema()
    insert_stock_data('AAPL', '2023-04-01', 120, 125, 130, 115, 100000)
    insert_stock'));
