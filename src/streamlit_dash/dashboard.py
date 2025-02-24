import sys
import os

sys.path.append("C:\\Users\\Brukare\\Desktop\\github\\Projekt-kryptokollen-main\\src")



import streamlit as st  
from streamlit_autorefresh import st_autorefresh
from sqlalchemy import create_engine
import pandas as pd
from constants.constants import (POSTGRES_DBNAME, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER)
from rates_api import fetch_exchange_rates
from streamlit_dash.coin_info import crypto_info
 
 
currency = ["SEK", "NOK", "DKK", "EUR", "USD", "ISK"]
connection_string = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"
 
engine = create_engine(connection_string)
 
def load_data(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
        df = df.set_index("timestamp")
        return df
           
refresh = st_autorefresh(interval=30 *1000, limit= 100)
    
def main():
    st.markdown("# Crypto currency Cardano")
    
    table = (st.selectbox("Select cryptocurrency", ("Cardano", "Ethereum")))
    
    
    df = load_data("SELECT * FROM cardano;")
    df = df.tail(15)
    
    st.markdown("### Streaming data for Cardano")
    
    currency_code = st.selectbox("Select currency", currency)
    st.markdown(f"### Price change over time  for {table}")
    
    currency_rate = fetch_exchange_rates(rate=currency_code)
    crypto_info(df, currency_code, currency_rate)
    
 
 
if __name__ == "__main__":
    main()
 