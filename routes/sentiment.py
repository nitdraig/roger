from flask import Blueprint, jsonify, render_template
import requests
from textblob import TextBlob
import os
from dotenv import load_dotenv

load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

sentiment_bp = Blueprint("sentiment", __name__)


@sentiment_bp.route("/sp500_sentiment", methods=["GET"])
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


@sentiment_bp.route("/sp500_sentiment_analyzer")
def sp500_sentiment_analyzer():
    return render_template("pages/sp500_sentiment_analyzer.html")
