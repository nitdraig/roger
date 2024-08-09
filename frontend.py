import tkinter as tk
from tkinter import ttk
import requests

class StockAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Analyzer")

        self.label = tk.Label(root, text="Enter Stock Symbol:")
        self.label.pack(padx=10, pady=10)

        self.entry = tk.Entry(root)
        self.entry.pack(padx=10, pady=10)
        self.entry.bind("<KeyRelease>", self.on_key_release)

        self.listbox = tk.Listbox(root)
        self.listbox.pack(padx=10, pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack(padx=10, pady=10)

        self.update_stocks()

    def update_stocks(self):
        response = requests.get("http://127.0.0.1:5000/stocks")
        self.stocks = response.json()

    def on_key_release(self, event):
        search_term = self.entry.get().upper()
        self.listbox.delete(0, tk.END)
        for stock in self.stocks:
            if search_term in stock:
                self.listbox.insert(tk.END, stock)
        if search_term in self.stocks:
            self.show_analysis(search_term)

    def show_analysis(self, ticker):
        response = requests.post("http://127.0.0.1:5000/analyze", json={"ticker": ticker})
        result = response.json()
        if 'error' not in result:
            self.result_label.config(text=f"Ticker: {result['ticker']}\nRecommendation: {result['recommendation']}\nSharpe Ratio: {result['sharpe_ratio']:.2f}")
        else:
            self.result_label.config(text="Error retrieving data.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockAnalyzerApp(root)
    root.mainloop()
