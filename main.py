# Ilir Bejleri
# Black-Scholes model implementation into live tickers for stocks

import numpy as np
from scipy.stats import norm
import argparse
import requests
from datetime import date
import yfinance as yf
import pandas as pd
from flask import Flask, jsonify
import threading
import time

# Argument Parser Setup
parser = argparse.ArgumentParser()
parser.add_argument('ticker', type=str, help='Stock ticker symbol')
parser.add_argument('years', type=float, help='Number of years (can be fractional)')
parser.add_argument('PutOrCall', type=str, choices=['put', 'call'], help='Specify if option is a put or call')
parser.add_argument('strikePrice', type=float, help='Strike price of the option')

args = parser.parse_args()
ticker = args.ticker
years = args.years
put_or_call = args.PutOrCall.lower()  # Ensure lower case
strikePrice = args.strikePrice

# Debug: Print parsed arguments
print(f'Parsed arguments: ticker={ticker}, years={years}, put_or_call={put_or_call}, strikePrice={strikePrice}')

# FRED API Setup (assuming you have the API key)
api_key = ''  # Add your FRED API key here
series_id = 'DGS1MO'
url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&sort_order=desc&limit=1'

response = requests.get(url)
data = response.json()

if 'observations' in data and len(data['observations']) > 0:
    most_recent_observation = data['observations'][0]
    observation_date = most_recent_observation['date']
    yield_value = most_recent_observation['value']
    interestRate = float(yield_value) / 100.0
    print(f'Interest rate retrieved: {interestRate * 100:.2f}% on {observation_date}')
else:
    print("No data available for the interest rate.")
    interestRate = 0.01  # Fallback interest rate

# Black-Scholes Model Functions
def callBlackScholes(underlyingAssetValue, strikePrice, timeLeft, sigma):
    d1 = (np.log(underlyingAssetValue/strikePrice) + ((interestRate + (sigma**2)/2) * timeLeft)) / (sigma * np.sqrt(timeLeft))
    d2 = d1 - sigma * np.sqrt(timeLeft)
    return underlyingAssetValue * norm.cdf(d1, 0, 1) - strikePrice * np.exp(-interestRate * timeLeft) * norm.cdf(d2, 0, 1)

def putBlackScholes(underlyingAssetValue, strikePrice, timeLeft, sigma):
    d1 = (np.log(underlyingAssetValue/strikePrice) + ((interestRate + (sigma**2)/2) * timeLeft)) / (sigma * np.sqrt(timeLeft))
    d2 = d1 - sigma * np.sqrt(timeLeft)
    return strikePrice * np.exp(-interestRate * timeLeft) * norm.cdf(-d2, 0, 1) - underlyingAssetValue * norm.cdf(-d1, 0, 1)

# Get Current Stock Price
def get_stock_price():
    stock = yf.Ticker(ticker)
    return stock.history(period='1d', interval='1m')['Close'].iloc[-1]

# Calculate Historical Volatility (Sigma)
def calculate_sigma():
    end_date = pd.Timestamp.today()
    start_date = end_date - pd.DateOffset(days=int(years * 365))
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    data['Log Return'] = np.log(data['Close'] / data['Close'].shift(1))
    log_returns = data['Log Return'].dropna()
    sigma = log_returns.std() * np.sqrt(252)
    return sigma

# Flask App Setup
app = Flask(__name__)
current_option_price = None

def update_option_price():
    global current_option_price
    while True:
        stock_price = get_stock_price()
        sigma = calculate_sigma()
        if put_or_call == 'call':
            current_option_price = callBlackScholes(stock_price, strikePrice, years, sigma)
        else:
            current_option_price = putBlackScholes(stock_price, strikePrice, years, sigma)
        
        time.sleep(2)

@app.route('/ticker')
def ticker_route():
    return jsonify({'option_price': current_option_price})

if __name__ == '__main__':
    threading.Thread(target=update_option_price, daemon=True).start()
    app.run(debug=True)
