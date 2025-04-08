Ilir Bejleri
Main idea: Create a live ticker for an options price based on a stock's changing price and the model's other factors. As a stock price changes, the ticker will change its price simultaneously. Any ticker symbol on yahoo finance including commodities. 

REQUIRED PROGRAMS:
    pip install fastapi uvicorn numpy scipy
    pip install --upgrade yfinance

EXUECTION INSTRUCTIONS:
Run
    uvicorn main:app --reload


Citations: 
- Concepts and formulas used are taken from the following book:
    Natenberg, Sheldon. Option Volatility & Pricing: Advanced Trading Strategies and Techniques. US: McGraw-Hill, 1994.
