# Stock Screener Streamlit App

This application is a simple stock screener built using [Streamlit](https://streamlit.io/) and [yfinance](https://github.com/ranaroussi/yfinance). It allows users to quickly fetch and view key financial data for any stock ticker supported by Yahoo Finance.

## Features
- Enter any stock ticker symbol (e.g., `RELIANCE.NS`) in the text box.
- Instantly view:
  - Market Capitalization
  - 52 Week High & Low
  - All Time High & Low
  - Script P/E (Price to Earnings Ratio)
  - Sector P/E (if available)
  - Face Value (if available)
- Error handling for invalid or unavailable ticker symbols.

## How It Works
1. The app provides a text input box for the user to enter a stock ticker symbol.
2. On entering a symbol, the app fetches data using the `yfinance` library.
3. The results are displayed interactively on the page, including market cap, price ranges, and valuation metrics.

## How to Run
1. Make sure you have Python installed.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app from the `stock_screener` directory or from the project root:
   ```bash
   streamlit run stock_screener/app.py
   ```
4. Open the local URL provided by Streamlit in your browser.

## Requirements
- Python 3.7+
- Packages listed in `requirements.txt` (including `yfinance`, `streamlit`, `pandas`, `numpy`, etc.)

## Notes
- The app relies on Yahoo Finance data, which may occasionally be unavailable or incomplete for some tickers.
- For Indian stocks, use the `.NS` suffix (e.g., `RELIANCE.NS`).

---

Feel free to extend this app with more features or customizations as needed!
