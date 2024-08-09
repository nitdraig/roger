from flask import Flask, render_template, request, jsonify
from analysis import analyze_stock, get_stock_suggestions

app = Flask(__name__)

@app.route('/')
def index():
    # Mostrar recomendaciones por defecto al cargar la página
    recommendations = [analyze_stock(ticker) for ticker in ['AAPL', 'MSFT', 'GOOGL']]
    return render_template('index.html', recommendations=recommendations)

@app.route('/search', methods=['POST'])
def search():
    stock_symbol = request.form.get('stock_symbol')
    if stock_symbol:
        recommendation = analyze_stock(stock_symbol)
        return render_template('recommendations.html', recommendation=recommendation)
    return render_template('index.html', recommendations=[])

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '')
    suggestions = get_stock_suggestions(query)
    return jsonify(suggestions)
if __name__ == '__main__':
    app.run(debug=True)
