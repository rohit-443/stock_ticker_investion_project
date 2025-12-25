import json
import requests
from typing import Optional

# Load API keys from the user's secret file
with open(r"C:\Users\Rohit Jonnadula\secret_key.txt", "r") as file:
    json_str = json.load(file)
    GEMINI_API_KEY = json_str.get("gemini")
    SERPAPI_KEY = json_str.get("serpapi")

def get_tickertape_url(ticker_symbol: str, serpapi_key: str) -> Optional[str]:
    """
    Get exact Tickertape.in URL for NSE ticker using SerpAPI
    """
    search_queries = [
        f'site:tickertape.in "{ticker_symbol}" stock',
        f'site:tickertape.in/stocks/ {ticker_symbol}',
        f'{ticker_symbol} site:tickertape.in',
        f'{ticker_symbol} NSE tickertape',
    ]
    params_base = {
        "engine": "google",
        "api_key": serpapi_key,
        "num": 10
    }
    for query in search_queries:
        params = params_base.copy()
        params["q"] = query
        try:
            response = requests.get("https://serpapi.com/search", params=params)
            results = response.json()
            for result in results.get("organic_results", []):
                url = result.get("link", "")
                if ("tickertape.in" in url and 
                    "/stocks/" in url and 
                    (ticker_symbol.lower() in url.lower() or 
                    ticker_symbol.upper() in result.get("title", "").upper())):
                    return url
        except Exception as e:
            print(f"Error: {e}")
    return None

def get_sector_pe_from_tickertape(ticker_symbol: str) -> Optional[float]:
    """
    Get sector P/E from Tickertape using SerpAPI to find the correct URL.
    """
    url = get_tickertape_url(ticker_symbol, SERPAPI_KEY)
    if not url:
        return None
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            # Example: parse sector P/E from the HTML (update selector as needed)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, 'html.parser')
            # This selector may need to be updated based on Tickertape's structure
            pe_elem = soup.find('span', string=lambda s: s and 'Sector PE' in s)
            if pe_elem:
                # Try to find the value next to the label
                value_elem = pe_elem.find_next('span')
                if value_elem:
                    try:
                        return float(value_elem.text.strip().replace(',', ''))
                    except Exception:
                        pass
        return None
    except Exception as e:
        print(f"Error scraping Tickertape: {e}")
        return None
