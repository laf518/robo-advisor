# Robo Advisor
This program asks the user to input a valid stock quote and returns a recommendation based on the stock's current price and historical data.  The program validates the user input and prints the stock's most recent data to include latest closing price, maximum intraday price, and minimum intraday price over the last 100 days.  An algorithm then evaluates the stock's current price and compares it to the 100 day historical data to provide a recommendation of strong sell, sell, hold, buy, or strong buy. 
## Getting Started
---
This program requires Python  version 3.7.  Required third party packages are provided below and are also listed in the *requirements.txt* document included in this repository.
### Prerequisites
* Required third party packages include:
    * *requests*
    * *python-dotenv*
* User must register with Alpha Vantage.  Registration process is available at the following link: https://www.alphavantage.co/support/#api-key
### Installing
* The user will be required to clone the repository located at the following hyperlink: https://github.com/laf518/robo-advisor. 
* After cloning the repository, the user must create a local *.env* file and save it in the *app* folder. The user will then save the following information in the *.env* file:
>ALPHAVANTAGE_API_KEY="[*insert Alpha Vantage user key here*]"
* Once the user has finished setting up their local repository, they must navigate to the *app* folder and run the following code within their virtual Python environment to install the required third party packages:
>`pip install -r requirements.txt`
## Deployment
---
The program will prompt the user for a valid stock symbol.  The input is not required to follow a specific capitalization format however, the symbol must be accurate to obtain the stock information and recommendation.  The program will return data for the desired stock along with a recommendation based on a normalized interpretation of the 100 day historical data.

### Errors:
* User will receive an error message if the input provided contains any non-alphabetic characters or if the length of the input is greater than 5 total characters. *User will be prompted to input the stock symbol again.*
* If Alpha Vantage is not able to find information on the provided stock symbol, the following error message will appear "*The stock symbol you submitted is invalid. Would you like to try again? (y/n)*". *User must select 'y' or 'n', any other input will not be accepted.*
## Author
---
* **Luke Fellin** - *Programming in Python and Fundamentals of Software Development: **NYU Stern School of Business**, Summer 2020*