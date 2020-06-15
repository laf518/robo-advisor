# app/robo_advisor.py
import requests
import json
import csv
from dotenv import load_dotenv
import statistics as stat
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

## Functionality requirements:
# Information input / validation
"""
Create a while loop that sends user input to
the API. If the symbol is invalid, an error should
be returned by the API. Thus if error status = true,
program will return an error message. Otherwise it 
will break out of the WHILE loop.

Use: TIME_SERIES_DAILY function
"""
while True:

    quote = input("Please type in the stock symbol for which you are interested: ").upper()
    
    # Check validitity of user inputted stock symbol:
    if type(quote) != str or len(quote) > 5:
        print("Hmmm, something is wrong with your stock symbol. Please ensure your input is accurate and contains only letters.")
        continue

    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + quote + "&apikey=" + key

    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    
    validation = list(parsed_response.keys())[0]

    # Check for error message returned by API:
    if validation != "Error Message":
        break

    else:
        again = input("The stock symbol you submitted is invalid. Would you like to try again? (y/n): ").upper()
        if again == 'Y':
            continue
        elif again == 'N':
            print("Leaving program...")
            exit()
        else:
            print("Invalid input. Please try again.")
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

## Calculation requirements:

# List close, high and low prices
now = datetime.now()
date_str = now.strftime("%m/%d/%Y %H:%M:%S")
refresh_date = parsed_response['Meta Data']['3. Last Refreshed']

close_prices = [] #> creates list of the last 100 closing prices
for item in time_series:
    close = float(time_series[item]['4. close'])
    close_prices.append(close)
latest_close = to_usd(close_prices[0])

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

## Recommendation:
"""
Dictionary of recommendations to include 'recommendation' and reason 'keys'.
The recommendations will be based on the z-score of the current price relative
to the normalized 100-day closing prices.
"""
recommendations = {
   "sb": {"rec": "Strong Buy!", "reason": "Current price is over 2 standard deviations less than the average closing price for the past 100 days."},
    "b": {"rec": "Buy!", "reason": "Current price is within 1 to 2 standard deviations less than the average closing price for the past 100 days."},
    "h": {"rec": "Hold!", "reason": "Current price is within 1 standard deviation from the average closing price for the past 100 days."},
    "s": {"rec": "Sell!", "reason": "Current price is within 1 to 2 standard deviations greater than the average closing price for the past 100 days."},
    "ss": {"rec": "Strong Sell!", "reason": "Current price is over 2 standard deviations greter than the average closing price for the past 100 days."}
}

current_price = close_prices[0]

avg_close = stat.mean(close_prices)
stdev_close = stat.pstdev(close_prices)

z_score = round((current_price - avg_close) / stdev_close, 2)

if z_score > 2: 
    advice = recommendations['ss']
elif z_score >= 1:
    advice = recommendations['s']
elif z_score >= -1:
    advice = recommendations['h']
elif z_score >= -2:
    advice = recommendations['b']
elif z_score < -2: 
    advice = recommendations['sb']

rec = advice['rec']
reason = advice['reason']

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
print("RECOMMENDATION: " + rec)
print("RECOMMENDATION REASON: " + reason)
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

