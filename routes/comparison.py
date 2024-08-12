import openai
import os
from flask import Blueprint, request, jsonify, render_template
from utils.stock_analysis import (
    get_stock_suggestions,
    analyze_stock,
)

openai.api_key = os.getenv("OPENAI_API_KEY")

comparison_bp = Blueprint("comparison", __name__)


@comparison_bp.route("/autocomplete_stocks", methods=["GET"])
def autocomplete_stocks():
    query = request.args.get("query", "")
    suggestions = get_stock_suggestions(query)
    return jsonify(suggestions)


@comparison_bp.route("/compare_stocks", methods=["GET"])
def compare_stocks():
    ticker1 = request.args.get("ticker1")
    ticker2 = request.args.get("ticker2")

    if not ticker1 or not ticker2:
        return jsonify({"error": "Both action symbols are required"}), 400

    try:

        stock1_data = analyze_stock(ticker1)
        stock2_data = analyze_stock(ticker2)

        if not stock1_data or not stock2_data:
            return (
                jsonify({"error": "Could not get data for one or both actions"}),
                500,
            )

        recommendation = "Hold"
        if stock1_data["sharpe_ratio"] > stock2_data["sharpe_ratio"]:
            recommendation = "Buy " + ticker1
        elif stock2_data["sharpe_ratio"] > stock1_data["sharpe_ratio"]:
            recommendation = "Buy " + ticker2

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial advisor, skilled in explaining investment recommendations based on financial metrics.",
                },
                {
                    "role": "user",
                    "content": f"Stock {ticker1} has a Sharpe Ratio of {stock1_data['sharpe_ratio']:.2f} and stock {ticker2} has a Sharpe Ratio of {stock2_data['sharpe_ratio']:.2f}. Which stock should be preferred and why?",
                },
            ],
            max_tokens=100,
        )
        explanation = response["choices"][0]["message"]["content"].strip()

        result = {
            "stock1": {
                "ticker": ticker1,
                "sharpe_ratio": stock1_data.get("sharpe_ratio"),
                "recommendation": stock1_data.get("recommendation"),
                "explanation": stock1_data.get("explanation"),
            },
            "stock2": {
                "ticker": ticker2,
                "sharpe_ratio": stock2_data.get("sharpe_ratio"),
                "recommendation": stock2_data.get("recommendation"),
                "explanation": stock2_data.get("explanation"),
            },
            "comparison_recommendation": recommendation,
            "comparison_explanation": explanation,
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@comparison_bp.route("/compare")
def compare_stocks_page():
    return render_template("pages/compare_stocks.html")
