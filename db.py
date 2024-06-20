import os
import sqlite3
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATABASE_NAME = os.getenv("DATABASE_NAME", "trading_analytics.db")

class DBContextManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
    
    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            return self.conn
        except sqlite3.Error as err:
            logging.error(f"Error connecting to the database: {err}")
            return None
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn is not None:
            self.conn.close()

def define_schema():
    with DBContextManager(DATABASE_NAME) as conn:
        if conn is not None:
            cursor = conn.cursor()
            try:
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
            except sqlite3.Error as err:
                logging.error(f"Error creating table: {err}")

def insert_stock_data(symbol, date, open_price, close_price, high_price, low_price, volume):
    with DBContextZManager(DATABASE_NAME) as conn:
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                INSERT INTO stock_data (symbol, date, open_price, close_price, high_price, low_price, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (symbol, date, open_price, close_price, high_price, low_price, volume))
                conn.commit()
            except sqlite3.Error as err:
                logging.error(f"Error inserting data: {err}")

def read_stock_summary(symbol):
    """Get summary data including the highest, lowest, and average closing prices for a given symbol."""
    with DBContextManager(DATABASE_NAME) as conn:
        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                SELECT MAX(close_price) AS max_close, MIN(close_price) AS min_close, AVG(close_price) AS avg_close
                FROM stock_data
                WHERE symbol = ?
                ''', (symbol,))
                data = cursor.fetchone()
                logging.info(f"Stock Summary: {data}")
                return data
            except sqlite3.Error as err:
                logging.error(f"Error reading stock summary: {err}")
                return None

if __name__ == "__main__":
    define_schema()
    records = [
        ('AAPL', '2023-04-02', 122, 124, 130, 120, 200000),
        ('AAPL', '2023-04-03', 125, 128, 132, 125, 180000)
    ]
    for record in records:
        insert_stock_data(*record)
    read_stock_summary('AAPL')