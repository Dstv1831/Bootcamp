import requests
from datetime import *
from twilio.rest import Client
import os

KEY_STOCKS = os.environ.get("KEY_STOCKS")
KEY_NEWS = os.environ.get("KEY_NEWS")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")


def format_message(headline, content, percent):
    if percent < 0:
        # returns the absolute value of the number
        percent = abs(percent)
        msg = f"  BTC :🔻{round(percent)}% \nHeadline: {headline} \nBrief: {content}"
    else:
        percent = abs(percent)
        msg = f"  BTC :🔺{round(percent)}% \nHeadline: {headline} \nBrief: {content}"

    return msg


param_stock = {
    "function": "DIGITAL_CURRENCY_DAILY",
    "symbol": "BTC",
    "market": "USD",
    "apikey": KEY_STOCKS,
}

resp_stock = requests.get(url="https://www.alphavantage.co/query", params=param_stock)
resp_stock.raise_for_status()
data_stock = resp_stock.json()

today = datetime.today().date()
yesterday = (datetime.today() - timedelta(days=1)).date()

bit_today = float(data_stock["Time Series (Digital Currency Daily)"][f"{today}"]["1. open"])
bit_yesterday = float(data_stock["Time Series (Digital Currency Daily)"][f"{yesterday}"]["1. open"])
percentage = 100 - (bit_today * 100 / bit_yesterday)


if percentage >= 3:
    param_news = {
        "q": "Bitcoin Ethereum",
        "from": "2024-05-23",
        "sortBy": "relevancy",
        "apikey": KEY_NEWS,
    }
    resp_news = requests.get(url="https://newsapi.org/v2/everything", params=param_news)
    resp_news.raise_for_status()
    data_news = resp_news.json()
    news = []
    for n in range(3):
        title = data_news['articles'][n]['title']
        description = data_news['articles'][n]['description']
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=format_message(headline=title,content=description,percent=percentage),
            from_='+18436066048',
            to='+61414531124'
        )
