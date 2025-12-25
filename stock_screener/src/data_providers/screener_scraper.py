import requests
from bs4 import BeautifulSoup

def get_screener_data(ticker_symbol):
    # Remove .NS or any suffix after '.' for screener.in
    base_symbol = ticker_symbol.split('.')[0]
    url = f'https://www.screener.in/company/{base_symbol}/consolidated/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract Face Value using the new method
        face_value = None
        ratios_ul = soup.find('ul', id='top-ratios')
        if ratios_ul:
            for li in ratios_ul.find_all('li'):
                name_span = li.find('span', class_='name')
                if name_span and 'Face Value' in name_span.text:
                    number_span = li.find('span', class_='number')
                    if number_span:
                        face_value = number_span.text.strip()
                    break
        # Extract Shareholding Pattern Table
        shareholding_pattern = []
        shareholding_section = soup.find('section', {'id': 'shareholding'})
        if shareholding_section:
            table = shareholding_section.find('table')
            if table:
                for row in table.find_all('tr'):
                    shareholding_pattern.append([
                        cell.text.strip() for cell in row.find_all(['th', 'td'])
                    ])
        return {
            'face_value': face_value,
            'shareholding_pattern': shareholding_pattern
        }, None
    except Exception as e:
        return None, str(e)
