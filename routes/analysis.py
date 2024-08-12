from flask import Blueprint, render_template, request, jsonify
from utils.stock_analysis import analyze_stock, get_stock_suggestions

analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.route("/analyzer")
def analyzer():
    return render_template("pages/analyzer.html")


@analysis_bp.route("/analyze", methods=["POST"])
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


@analysis_bp.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query", "")
    suggestions = get_stock_suggestions(query)
    return jsonify(suggestions)
