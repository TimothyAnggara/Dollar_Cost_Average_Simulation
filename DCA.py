# Import Dependencies
import time
import secret
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame

API_KEY = secret.API_KEY
SECRET_KEY = secret.SECRET_KEY
rest_api = tradeapi.REST(API_KEY, SECRET_KEY,'https://paper-api.alpaca.markets')

# Define crypto, start, and end dates
crypto = "ETHUSD"
num_of_years = 1
start_date = dt.datetime.today() - dt.timedelta(int(365 * num_of_years))
end_date = dt.datetime.today()

# Retrieve historical pricing for crypto
data = rest_api.get_crypto_bars(crypto, TimeFrame.Day, start_date.date(), end_date.date(), exchanges=['CBSE']).df
data_price = data['close']

# Get current price for crypto
def get_current_price(crypto):
    price = (rest_api.get_crypto_bars(crypto, TimeFrame.Minute, exchanges=["CBSE"])).df["close"][-1]
    return price

def place_buy_order(quantity, crypto):
    rest_api.submit_order(symbol=crypto, qty=quantity, type="market", side="buy", time_in_force="day")
    return

# Function to place orders when dollar cost averaging
def dollar_cost_average(crypto, position_size):
    try:
        currentPrice = float(get_current_price(crypto))
        print(f"\nThe current price for {crypto} is {currentPrice}")

        cash = float(get_cash_balance())
        print(f"The current cash balance available is {cash}")

        if cash > position_size:
            quantity = float(round(position_size / currentPrice, 3))
            print(f"{crypto} Buy Quantity: {quantity}")
            place_buy_order(quantity, crypto)

            time.sleep(1)
            print(f"The new cash balance is {get_cash_balance()}")
        else:
            print("Insufficient funds for full position")

            quantity = float(round((cash / currentPrice) * 0.95, 3))
            print(f"{crypto} Buy Quantity: {quantity}")
            place_buy_order(quantity, crypto)

            time.sleep(1)
            print(f"The new cash balance is {get_cash_balance()}")

        return {"Success": True}

    except Exception as e:
        print(e)
        return {"Success": False}

# User input for timeframe, position sizing, cryptocurrency
timeframe = input("Enter DCA time frame (day, week, month): " )
position_size = float(input("Enter many dollars you want to buy of crypto per interval: "))
crypto = 'ETHUSD'

timeframe_to_seconds = {
    "day": 86400,
    "week": 604800,
    "month": 2629746
}

print(f"You have chosen to dollar cost average {position_size} of {crypto} every {timeframe}")

# Set up while statement to run DCA bot
while True:
    dollar_cost_average(crypto, position_size)
    time.sleep(timeframe_to_seconds[timeframe.lower()])