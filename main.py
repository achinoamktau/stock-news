import requests
import html
from twilio.rest import Client
import os
import datetime as dt

STOCK = "TSLA"
COMPANY_NAME = "Tesla INC"

stock_price_key = "your own"   # to generate a key follow the links here
stock_price_END = 'https://www.alphavantage.co/query'

news_key = "your own"
news_END = "https://newsapi.org/v2/everything"

SID_twilio = "your own"
twilio_key ="your own"


def news():
    global news_key, news_END
    params_news = {
        "apiKey": news_key,
        "q": COMPANY_NAME
    }
    response = requests.get(news_END, params=params_news)
    response.raise_for_status()
    data = response.json()["articles"]
    response.close()
    top_three_art = data[:3]
    return top_three_art
    # i = 0      the slicer is much better
    # for article in data:
    #     top_three_art.append(article)
    #     i += 1
    #     if i == 3:
    #         return top_three_art
    # return top_three_art


def formatting(article):
    headline = html.unescape(article["title"])
    brief = html.unescape(article["description"])
    return headline,brief


today = dt.datetime.now()
yesterday = today - dt.timedelta(2)
today = str((today - dt.timedelta(1)).date())
yesterday = str(yesterday.date())

params_price = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": stock_price_key
}
response = requests.get(stock_price_END, params=params_price)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

close_yesterday = float(data_list[1]["4. close"])
close_today = float(data_list[0]["4. close"])
response.close()

percentage = close_yesterday / close_today * 100   # this could have been nicer
percentage = percentage - 100

if abs(percentage) >= 0.5:
    if percentage < 0:
        msg1 = f"{STOCK} is down {percentage}% 📉"
    else:
        msg1 = f"{STOCK} is up {percentage}% 🧿🧿"
    client = Client(SID_twilio, twilio_key)
    articles = news()
    for article in articles:
        head, brief = formatting(article)
        msg = msg1 + f"\nHeadline: {head}\nBrief: {brief}"
        message = client.messages \
            .create(
            from_="TWILO PHONE",
            body=msg,
            to="YOUR_PHONE"
        )





