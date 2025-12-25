import yfinance as yf

def get_ticker_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        market_cap = info.get('marketCap')
        week_52_high = info.get('fiftyTwoWeekHigh')
        week_52_low = info.get('fiftyTwoWeekLow')
        hist = ticker.history(period='max')
        all_time_high = hist['High'].max() if not hist.empty else None
        all_time_low = hist['Low'].min() if not hist.empty else None
        pe_ratio = info.get('trailingPE')
        sector_pe = info.get('forwardPE')
        return {
            'market_cap': market_cap,
            'week_52_high': week_52_high,
            'week_52_low': week_52_low,
            'all_time_high': all_time_high,
            'all_time_low': all_time_low,
            'pe_ratio': pe_ratio,
            'sector_pe': sector_pe,
        }, None
    except Exception as e:
        return None, str(e)
