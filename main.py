import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "UJB943K4G45GUP0D"
NEWS_API_KEY = "949bb4872a8745f38d0294b39a8d43f6"
TWILIO_SID = "AC2fe173a11dbd88b6545fd994bfa1fc2f"
TWILIO_AUTH_TOKEN = "33776b2b8e89dcbac4f5f84087419075"

# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_param = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
response = requests.get(STOCK_ENDPOINT, params=stock_param)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

# Get the day before yesterday's closing stock price

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
if difference > 0:
    up_down = "📈"
else:
    up_down = "📉"

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)

# If TODO4 percentage is greater than 5 then print("Get News").
news_param = {
    "apiKey": NEWS_API_KEY,
    "qInTitle": STOCK_NAME

}

if abs(diff_percent) >= 4:
    res = requests.get(NEWS_ENDPOINT, params=news_param)
    articles = res.json()["articles"]

three_articles = articles[:3]
print(three_articles)

news = [f"{STOCK_NAME}: {up_down} {diff_percent}%\nHeadline: {articles['title']}. \nBrief: {articles['description']}"
        for articles in three_articles]

# Send each article as a separate message via Twilio.

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
for article in news:
    message = client.messages.create(
        body=article,
        from_="+13862515225",
        to="+15199978465",
    )
