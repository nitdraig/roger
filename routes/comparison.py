from flask import Blueprint, request, jsonify, render_template

comparison_bp = Blueprint("comparison", __name__)


@comparison_bp.route("/compare_stocks", methods=["GET"])
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


@comparison_bp.route("/compare")
def compare_stocks_page():
    return render_template("pages/compare_stocks.html")
