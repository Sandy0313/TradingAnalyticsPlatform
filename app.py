from flask import Flask, request, jsonify
import os
import requests
import json
from dotenv import load_dotenv
import sqlite3

load_dotenv()

app = Flask(__name__)

def db_connection():
    conn = None
    db_file = os.getenv("DATABASE_PATH")
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/fetch_stock_data', methods=['GET'])
def fetch_stock_data():
    stock_symbol = request.args.get('symbol')
    api_key = os.getenv("API_KEY")
    base_url = "https://api.example.com/stock_data"
    
    try:
        response = requests.get(f"{base_url}?symbol={stock_symbol}&apikey={api_key}")
        stock_data = response.json()
        return jsonify(stock_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze_data', methods=['POST'])
def analyze_data():
    data = request.json
    try:
        analyzed_data = {"average": sum(data.values())/len(data)}
        return jsonify(analyzed_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analysis_results', methods=['POST'])
def analysis_results():
    analysis_id = request.json.get('analysis_id')
    conn = db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT result FROM analysis WHERE id=?", (analysis_id,))
        result = cursor.fetchone()
        return jsonify({"analysis_result": result[0]}), 200
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)