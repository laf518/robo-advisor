# app/robo_advisor.py
import requests
import json
import csv
from dotenv import load_dotenv
import pandas
import os
import sys

## Security requirements:
# Create environmental variable for API Key

load_dotenv()
key = os.environ.get("ALPHAVANTAGE_API_KEY")
# breakpoint()
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
# breakpoint()
# Information output
csv_columns = ['Date', '1. open', '2. high', '3. low', '4. close', '5. volume']
# breakpoint()

with open('data/test.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, csv_columns)
    w.writeheader()
    for k, v in time_series.items():
        row = {'Date': k}
        row.update(v)
        w.writerow(row)
        #CREDIT: https://stackoverflow.com/questions/29400631/python-writing-nested-dictionary-to-csv

## Calculation requirements:
# List close, high and low prices

## Starter code:
print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

