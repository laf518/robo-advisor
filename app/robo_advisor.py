# app/robo_advisor.py
import requests
import json
import csv
from dotenv import load_dotenv
import pandas
import os
import sys
from datetime import datetime


def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71
# CREDIT: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency

## Security requirements:
# Create environmental variable for API Key

load_dotenv()
key = os.environ.get("ALPHAVANTAGE_API_KEY")
# COMPLETE

## Functionality requirements:
# Information input / validation
"""Create a while loop that sends user input to
the API. If the symbol is invalid, an error should
be returned by the API. Thus if error status = true,
program will return an error message. Otherwise it 
will break out of the WHILE loop.

Use: TIME_SERIES_DAILY function"""
while True:

    quote = input("Please type in the stock symbol for which you are interested: ").upper()
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + quote + "&apikey=" + key

    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    
    validation = list(parsed_response.keys())[0]

    if validation != "Error Message":
        break

    else:
        print("The stock symbol you submitted is invalid. Please try again.")
time_series = parsed_response['Time Series (Daily)']

# Information output
csv_columns = ['Date', '1. open', '2. high', '3. low', '4. close', '5. volume']

with open('data/'+quote+'.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, csv_columns)
    w.writeheader()
    for k, v in time_series.items():
        row = {'Date': k}
        row.update(v)
        w.writerow(row)
        #CREDIT: https://stackoverflow.com/questions/29400631/python-writing-nested-dictionary-to-csv
# COMPLETE

## Calculation requirements:

# List close, high and low prices
now = datetime.now()
date_str = now.strftime("%m/%d/%Y %H:%M:%S")
refresh_date = parsed_response['Meta Data']['3. Last Refreshed']

close_prices = [] #> creates list of the last 100 closing prices
for item in time_series:
    close = float(time_series[item]['4. close'])
    close = to_usd(close)
    close_prices.append(close)
latest_close = close_prices[0]

high_prices = [] #> creates list of the last 100 daily high prices 
for item in time_series:
    high = float(time_series[item]['2. high'])
    high_prices.append(high)
high_prices.sort(reverse = True)
recent_high = to_usd(high_prices[0])

low_prices = [] #> creates list of the last 100 daily low prices
for item in time_series:
    low = float(time_series[item]['3. low'])
    low_prices.append(low)
low_prices.sort()
recent_low = to_usd(low_prices[0])

## Starter code:
print("-------------------------")
print("SELECTED SYMBOL: " + quote)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: " + date_str)
print("-------------------------")
print("LATEST DAY: " + refresh_date)
print("LATEST CLOSE: " + latest_close)
print("RECENT HIGH: " + recent_high)
print("RECENT LOW: " + recent_low)
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

