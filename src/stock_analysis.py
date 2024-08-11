import yfinance as yf
import openai
import os
import pandas as pd
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

cached_sp500_stocks = {}


def get_sp500_stocks():
    global cached_sp500_stocks
    if cached_sp500_stocks:
        return cached_sp500_stocks

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    sp500_table = pd.read_html(url)[0]

    sp500_stocks = {}
    for _, row in sp500_table.iterrows():
        ticker = row["Symbol"]
        company_name = row["Security"]
        sp500_stocks[ticker] = company_name

    cached_sp500_stocks = sp500_stocks

    with open("sp500_stocks.json", "w") as f:
        json.dump(sp500_stocks, f)

    return sp500_stocks


def get_stock_suggestions(query):
    sp500_stocks = get_sp500_stocks()
    query = query.lower()
    suggestions = []

    for symbol, name in sp500_stocks.items():
        if query in symbol.lower() or query in name.lower():
            suggestions.append({"symbol": symbol, "name": name})

    return suggestions


def analyze_stock(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y")

    if df.empty:
        return {"error": "No data available"}

    df["Return"] = df["Close"].pct_change()
    mean_return = df["Return"].mean() * 252
    vol = df["Return"].std() * (252**0.5)
    sharpe_ratio = mean_return / vol

    recommendation = (
        "Buy" if sharpe_ratio > 1 else "Sell" if sharpe_ratio < 0.5 else "Hold"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a financial advisor, skilled in explaining investment recommendations based on financial metrics.",
            },
            {
                "role": "user",
                "content": f"The stock {ticker} has a Sharpe Ratio of {sharpe_ratio:.2f}. Should it be bought, sold, or held? Explain why. Not more than 100 words.",
            },
        ],
        max_tokens=100,
    )
    explanation = response["choices"][0]["message"]["content"].strip()

    return {
        "ticker": ticker,
        "sharpe_ratio": sharpe_ratio,
        "recommendation": recommendation,
        "explanation": explanation,
    }
