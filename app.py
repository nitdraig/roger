from flask import Flask, render_template, request, jsonify
from stock_analysis import analyze_stock, get_stock_suggestions
from config import Config
import requests
import os
from dotenv import load_dotenv
from textblob import TextBlob


load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

app = Flask(__name__)
app.config.from_object(Config)


# Route for the Landing Page
@app.route("/")
def index():
    stars = get_github_stars()
    return render_template("pages/landing.html", stars=stars)


# Route for the Analyzer Page
@app.route("/analyzer")
def analyzer():
    return render_template("pages/analyzer.html")


# Route for analyzing a stock
@app.route("/analyze", methods=["POST"])
def analyze():
    ticker = request.json.get("ticker")
    if not ticker or not isinstance(ticker, str) or len(ticker) < 1:
        return jsonify({"error": "Invalid ticker provided"}), 400

    try:
        result = analyze_stock(ticker)
        if not result:
            return jsonify({"error": "Unable to analyze stock"}), 500
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route for autocomplete suggestions
@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query", "")
    suggestions = get_stock_suggestions(query)
    return jsonify(suggestions)


@app.route("/github-stars", methods=["GET"])
def get_github_stars():
    repo_url = "https://api.github.com/repos/nitdraig/roger"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(repo_url, headers=headers)
    print(f"GitHub API Status: {response.status_code}")
    if response.status_code == 200:
        repo_data = response.json()
        stars = repo_data.get("stargazers_count", 0)
        return stars
    else:
        return 0


# Route for the Investment Calculator Page


@app.route("/investment-calculator", methods=["GET", "POST"])
def investment_calculator():
    if request.method == "POST":

        initial_investment = float(request.form.get("initial-investment"))
        interest_rate = float(request.form.get("interest-rate")) / 100
        years = int(request.form.get("years"))

        future_value = initial_investment * (1 + interest_rate) ** years

        return render_template(
            "pages/investment_calculator.html", future_value=future_value
        )

    return render_template("pages/investment_calculator.html")


@app.route("/sp500_sentiment", methods=["GET"])
def sp500_sentiment():
    try:
        url = f"https://newsapi.org/v2/everything?q=S&P%20500&apiKey={NEWSAPI_KEY}"
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": "Error fetching news"}), 500

        news_data = response.json()
        articles = news_data.get("articles", [])

        if not articles:
            return jsonify({"error": "No news articles found"}), 404

        sentiment_score = 0
        total_articles = len(articles)

        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")
            text = (title or "") + " " + (description or "")
            blob = TextBlob(text)
            sentiment_score += blob.sentiment.polarity

        average_sentiment = sentiment_score / total_articles

        sentiment = "neutral"
        if average_sentiment > 0:
            sentiment = "positive"
        elif average_sentiment < 0:
            sentiment = "negative"

        result = {
            "average_sentiment": average_sentiment,
            "sentiment": sentiment,
            "total_articles": total_articles,
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/sp500_sentiment_analyzer")
def sp500_sentiment_analyzer():
    return render_template("pages/sp500_sentiment_analyzer.html")


@app.route("/compare_stocks", methods=["GET"])
def compare_stocks():
    ticker1 = request.args.get("ticker1")
    ticker2 = request.args.get("ticker2")

    if not ticker1 or not ticker2:
        return jsonify({"error": "Both action symbols are required"}), 400

    try:

        stock1_data = get_stock_data(ticker1)
        stock2_data = get_stock_data(ticker2)

        if not stock1_data or not stock2_data:
            return (
                jsonify({"error": "Could not get data for one or both actions"}),
                500,
            )

        result = {
            "stock1": {
                "performance": stock1_data.get("performance", "Unknown"),
                "current_value": stock1_data.get("current_value", "Unknown"),
            },
            "stock2": {
                "performance": stock2_data.get("performance", "Unknown"),
                "current_value": stock2_data.get("current_value", "Unknown"),
            },
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_stock_data(ticker):

    return {
        "performance": "Performance example",
        "current_value": "Current value example",
    }


@app.route("/compare")
def compare_stocks_page():
    return render_template("pages/compare_stocks.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
