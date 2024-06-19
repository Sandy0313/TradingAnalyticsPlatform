import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME", "trading_analytics.db")

def connect_db():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except sqlite3.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

def define_schema():
    conn = connect_db()
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
            print(f"Error creating table: {err}")
        finally:
            conn.close()

def insert_stock_data(symbol, date, open_price, close_price, high_price, low_price, volume):
    conn = connect_db()
    if conn is not_none:
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO stock_data (symbol, date, open_price, close_price, high_price, low_price, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (symbol, date, open_price, close_price, high_price, low_price, volume))
            conn.commit()
        except sqlite3.Error as err:
            print(f"Error inserting data: {err}")
        finally:
            conn.close()

def bulk_insert_stock_data(records):
    """
    records: List of tuples containing stock data records
    """
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.executemany('''
            INSERT INTO stock_data (symbol, date, open_price, close_price, high_price, low_price, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', records)
            conn.commit()
        except sqlite3.Error as err:
            print(f"Error during bulk insert: {err}")
        finally:
            conn.close()

def update_stock_data(symbol, date, open_price, close_price, high_price, low_price, volume):
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute('''
            UPDATE stock_data
            SET open_price = ?, close_price = ?, high_price = ?, low_price = ?, volume = ?
            WHERE symbol = ? AND date = ?
            ''', (open_price, close_price, high_price, low_price, volume, symbol, date))
            conn.commit()
        except sqlite3.Error as err:
            print(f"Error updating stock data: {err}")
        finally:
            conn.close()

def delete_stock_data(symbol, date):
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute('''
            DELETE FROM stock_data
            WHERE symbol = ? AND date = ?
            ''', (symbol, date))
            conn.commit()
        except sqlite3.Error as err:
            print(f"Error deleting stock data: {err}")
        finally:
            conn.close()

def read_stock_data(symbol, start_date, end_date):
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute('''
            SELECT * FROM stock_data
            WHERE symbol = ? AND date BETWEEN ? AND ?
            ''', (symbol, start_date, end_date))
            data = cursor.fetchall()
        except sqlite3.Error as err:
            print(f"Error reading stock data: {err}")
            data = []
        finally:
            conn.close()
        return data

if __name__ == "__main__":
    define_schema()
    # Example of bulk insertion
    records = [
        ('AAPL', '2023-04-02', 122, 124, 130, 120, 200000),
        ('AAPL', '2023-04-03', 125, 128, 132, 125, 180000)
    ]
    bulk_insert_stock_data(records)
    # Example of updating stock data
    update_stock_data('AAPL', '2023-04-02', 121, 123, 129, 119, 195000)
    # Example of deleting stock data
    delete_stock_data('AAPL', '2023-04-01')