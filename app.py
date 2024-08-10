from flask import Flask, render_template, request, jsonify
from stock_analysis import analyze_stock, get_stock_suggestions
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


# Route for the Landing Page
@app.route("/")
def index():
    return render_template("pages/landing.html")


# Route for the Analyzer Page
@app.route("/analyzer")
def analyzer():
    return render_template("pages/analyzer.html")


# Route for analyzing a stock
@app.route("/analyze", methods=["POST"])
def analyze():
    ticker = request.json.get("ticker")
    if not ticker:
        return jsonify({"error": "Ticker not provided"}), 400

    result = analyze_stock(ticker)
    return jsonify(result)


# Route for autocomplete suggestions
@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query", "")
    suggestions = get_stock_suggestions(query)
    return jsonify(suggestions)


if __name__ == "__main__":
    app.run(debug=True)
