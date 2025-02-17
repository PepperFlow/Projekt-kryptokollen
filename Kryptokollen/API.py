import requests

API_KEY = "84be434e-da03-4a52-8164-b832787660d8"
BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

def fetch_crypto(symbol="BTC"):
    """Hämtar kryptodata från CoinMarketCap API."""
    try:
        response = requests.get(
            BASE_URL,
            headers={"X-CMC_PRO_API_KEY": API_KEY},
            params={"symbol": symbol}
        )
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        print(f"API-fel: {e}")
        return None
