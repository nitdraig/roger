import yfinance as yf
import pandas as pd
import numpy as np

# Obtiene una lista de tickers del S&P 500
def get_sp500_stocks():
    # Una lista estática para propósitos de demostración. En un caso real, deberías obtener los tickers de una fuente confiable.
    return [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BRK-B", "UNH", "V", "MA", "HD", "DIS", "PYPL", "NFLX"
        # Agrega aquí todos los tickers reales del S&P 500
    ]

# Analiza una acción y retorna una recomendación
def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1y")
        if df.empty:
            return {"ticker": ticker, "recommendation": "Data not available"}
        
        df['Return'] = df['Close'].pct_change()
        mean_return = df['Return'].mean() * 252
        vol = df['Return'].std() * np.sqrt(252)
        sharpe_ratio = mean_return / vol

        recommendation = "Buy" if sharpe_ratio > 1 else "Sell"
        return {"ticker": ticker, "sharpe_ratio": sharpe_ratio, "recommendation": recommendation}
    except Exception as e:
        return {"ticker": ticker, "recommendation": "Error", "error": str(e)}

# Obtiene sugerencias de acciones basadas en una consulta
def get_stock_suggestions(query):
    all_stocks = get_sp500_stocks()
    suggestions = [stock for stock in all_stocks if query.upper() in stock]
    return suggestions

# Analiza las acciones más interesantes por defecto
def analyze_stocks(stock_symbol=None):
    if stock_symbol:
        return analyze_stock(stock_symbol)
    else:
        default_stocks = ["AAPL", "MSFT", "GOOGL"]
        return [analyze_stock(stock) for stock in default_stocks]
