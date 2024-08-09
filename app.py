from flask import Flask, render_template, request, jsonify
from stock_analysis import analyze_stock, get_stock_suggestions
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    ticker = request.json.get('ticker')
    if not ticker:
        return jsonify({"error": "Ticker not provided"}), 400

    result = analyze_stock(ticker)
    return jsonify(result)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '')
    suggestions = get_stock_suggestions(query)
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
