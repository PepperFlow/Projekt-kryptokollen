import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))



import streamlit as st  
from streamlit_autorefresh import st_autorefresh
from sqlalchemy import create_engine
import pandas as pd
from constants import (POSTGRES_DBNAME, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER)
from coin_info import fetch_exchange_rates
from coin_info import crypto_info
 
 
currencies = ["SEK", "NOK", "DKK", "EUR", "USD", "ISK"]
connection_url = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"
 
engine = create_engine(connection_url)
 
def load_data(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
        df = df.set_index("timestamp")
        return df
           
auto_refresh = st_autorefresh(interval=45*1000, limit= 100)
    
def main():
    st.markdown("# Crypto info for cardano")
    
    selected_coin = (st.selectbox("Select cryptocurrency", ("Cardano")))
    
    
    df = load_data("SELECT * FROM cardano;")
    df = df.tail(15)
    
    st.markdown("### Streaming info for Cardano")
    
    currency_code = st.selectbox("Select currency", currencies)
    st.markdown(f"### Price change over time {selected_coin}")
    
    exchange_rate = fetch_exchange_rates(rate=currency_code)
    crypto_info(df, currency_code, exchange_rate)
    
 
 
if __name__ == "__main__":
    main()
 