#Ilir Bejleri

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
from math import exp, sqrt, log
from scipy.stats import norm
import numpy as np
import time

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/derivatives")
async def get_derivatives(ticker: str):
    data = yf.Ticker(ticker)
    try:
        price = data.history(period="1d")["Close"].iloc[-1]
    except:
        return {"error": "Invalid ticker or no price data"}

    S = float(price)     # Spot price
    K = S * 1.05         # Strike price
    T = 1                # 1 year until maturity
    r = 0.05             # Risk-free rate
    sigma = 0.2          # Volatility
    q = 0.01             # Convenience yield / dividend yield

    # Futures Price
    futures = S * exp((r - q) * T)

    # Forward Price (discrete compounding)
    forward = S * ((1 + r) ** T)

    # Black-Scholes European Call and Put
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    call = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    put = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    # Swap fixed leg PV (simplified)
    swap = (S - K) * exp(-r * T)

    return {
        "spot_price": S,
        "futures_price": futures,
        "forward_price": forward,
        "call_option_price": call,
        "put_option_price": put,
        "swap_price": swap,
        "timestamp": time.time()
    }

