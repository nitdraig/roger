import os
import google.generativeai as genai
import yfinance as yf
import numpy as np
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar la API de Google Gemini usando la variable de entorno
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Configurar el modelo
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

def get_stock_suggestions(query):
    all_stocks = get_sp500_stocks()
    suggestions = [stock for stock in all_stocks if query.upper() in stock]
    return suggestions

def get_explanation(recommendation, sharpe_ratio):
    try:
        chat_session = model.start_chat(
            history=[
                {"role": "system", "content": "You are a financial advisor, skilled in explaining investment recommendations based on financial metrics."}
            ]
        )
        
        # Enviar mensaje con el prompt
        response = chat_session.send_message(f"Given the Sharpe Ratio of {sharpe_ratio}, explain whether the stock should be bought or sold. Recommendation: {recommendation}. Provide a detailed explanation of why this recommendation is made.")
        
        return response.text.strip()
    except Exception as e:
        return f"Error fetching explanation: {str(e)}"

def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1y")

        if df.empty:
            return {"ticker": ticker, "recommendation": "Data not available", "explanation": "No data available", "sharpe_ratio": "N/A"}
        
        df['Return'] = df['Close'].pct_change()
        df.dropna(subset=['Return'], inplace=True)
        
        if df.empty:
            return {"ticker": ticker, "recommendation": "Data not sufficient", "explanation": "Not enough data to calculate Sharpe Ratio", "sharpe_ratio": "N/A"}
        
        mean_return = df['Return'].mean() * 252
        vol = df['Return'].std() * np.sqrt(252)

        if vol == 0:
            return {"ticker": ticker, "recommendation": "No Volatility", "explanation": "Insufficient volatility to calculate Sharpe Ratio", "sharpe_ratio": "N/A"}
        
        sharpe_ratio = mean_return / vol
        recommendation = "Buy" if sharpe_ratio > 1 else "Sell"
        explanation = get_explanation(recommendation, sharpe_ratio)

        return {"ticker": ticker, "sharpe_ratio": sharpe_ratio, "recommendation": recommendation, "explanation": explanation}
    except Exception as e:
        return {"ticker": ticker, "recommendation": "Error", "explanation": str(e), "sharpe_ratio": "N/A"}
