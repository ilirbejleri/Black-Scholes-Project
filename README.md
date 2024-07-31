Ilir Bejleri
Main idea: Create a live ticker for an options price based on a stock's changing price and the model's other factors. As a stock price changes, the ticker will change its price simultaneously. The user can select the stock and option contract details. 


EXUECTION INSTRUCTIONS:
put your FRED API key on line 32 of main.py.
run main.py using the following arguments in this order: TICKER TimeToExpirationInYearsAsFloat CallOrPut StrikePrice
look at port 5000/ticker for the option price

example to get the Black-Scholes price for Apple stock call option expiring in 1 month with a strike price of 235:

python main.py AAPL .08333  call 235


Citations: 
- Concepts and formulas used are taken from the following book:
    Natenberg, Sheldon. Option Volatility & Pricing: Advanced Trading Strategies and Techniques. US: McGraw-Hill, 1994.