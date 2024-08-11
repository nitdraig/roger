from flask import Flask, render_template, request, jsonify
from stock_analysis import analyze_stock, get_stock_suggestions
from config import Config
import requests

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
    repo_url = app.config["GITHUB_REPO"]
    response = requests.get(repo_url)
    if response.status_code == 200:
        repo_data = response.json()
        stars = repo_data.get("stargazers_count", 0)
        return stars
    else:
        return 0


if __name__ == "__main__":
    app.run(debug=True)
