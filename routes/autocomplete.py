from flask import Blueprint, request, jsonify
from utils.stock_analysis import get_stock_suggestions

autocomplete_bp = Blueprint("autocomplete", __name__)


@autocomplete_bp.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query", "")
    suggestions = get_stock_suggestions(query)
    return jsonify(suggestions)
