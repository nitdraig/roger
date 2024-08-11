# ROGER

ROGER is a fast and efficient stock consultant designed to help you make informed decisions about buying, selling, or holding stocks in the S&P 500. By leveraging real-time financial data and AI-powered insights, ROGER provides quick recommendations along with brief explanations for each action.

## Features

- **Real-Time Data**: Access up-to-date stock prices and financial metrics for companies in the S&P 500.
- **AI-Powered Recommendations**: Get suggestions on whether to buy, sell, or hold a stock based on technical analysis and AI-generated insights.
- **Autocomplete Search**: Quickly find the stock you're interested in by typing the company name or ticker symbol.
- **Detailed Explanations**: Understand the reasoning behind each recommendation with AI-generated explanations.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/nitdraig/roger.git
   cd roger
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add your API keys:

   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000/`.
2. Start typing the name or ticker symbol of an S&P 500 company in the search box.
3. Select the stock from the autocomplete suggestions.
4. View the recommendation (Buy, Sell, Hold) along with a brief explanation.

## Technology Stack

- **Backend**: Flask (Python)
- **Data Source**: Yahoo Finance (`yfinance` library)
- **AI Engine**: OpenAI GPT (via `openai` library)
- **Frontend**: HTML, CSS, JavaScript (for dynamic search and autocompletion)
- **Other**: Pandas (for data processing), JSON (for caching stock data)

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## License

This project is licensed under the GPL v3.0 - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please feel free to reach out at agustind@duck.com
