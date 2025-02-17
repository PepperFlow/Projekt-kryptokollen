import time
from API import fetch_crypto

INTERVAL = 30  # intervallet 30-60 sekunder

def run_producer():
    """Hämtar kryptodata från CoinMarketCap-API:t
    och skriver ut resultatet i terminalen var 30:e sekund."""
    print("Hämtar kryptodata.")
    
    while True:
        data = fetch_crypto("BTC")  # Det går bra att byta valuta
        if data:
            print(f"Hämtad data: {data}")
        else:
            print("Misslyckades med att hämta data.")
        
        time.sleep(INTERVAL)

if __name__ == "__main__":
    run_producer()
