import streamlit as st
from millify import millify
from projektkollen.src.charts import line_chart
import matplotlib.pyplot as plt

from requests import Session, Timeout, TooManyRedirects
import requests  
import json
 
def crypto_info(df, currency_code, currency_rate=1):
    price_chart = line_chart(x= df.index, y= (df["price_usd"] * currency_rate), title= f"price {currency_code}")
    st.pyplot(price_chart)
    column_1, column_2, column_3 = st.columns(3)
    column_4, column_5, column_6 = st.columns(3)
    column_1.metric(
        "Volume",
        millify((df["volume"].tail(1) * currency_rate), precision= 2),
        f"{millify(df['volume_change'].tail(1))}%",
        border=True,)
    column_2.metric(
        "price change 1h",
        f"{millify((df['price_usd'].tail(1) * currency_rate), precision = 2)}{currency_code}",
        f"{millify(df['percent_change'].tail(1), precision = 2)}%",
        border=True)
    column_3.metric(
        "Price change 24h",
        f"{millify((df['price_usd'].tail(1) * currency_rate), precision= 2)}{currency_code}",
        f"{millify(df['percent_change_24h'].tail(1))}%",
        border=True)
    column_4.metric(
        "Total supply",
        f"{millify(df['total_supply'].tail(1), precision= 2)}",
        border=True)
    
    cols = st.columns(2)
    with cols[0]:
        st.subheader("Volume Change Trend")
        volume_chart = line_chart(x= df.index, y= (df["volume_change"] * currency_rate), title= f"price {currency_code}")
        st.pyplot(volume_chart)
    with cols[1]:
        st.subheader("Percentage Change Trend")
        percent_chart = line_chart(x=df.index, y=df["percent_change"], title="1h Percent Change (%)")
        st.pyplot(percent_chart)


def fetch_exchange_rates(base_currency="USD", rate ="SEK"):
   
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    
    session = Session()
    
    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()       
        return data["rates"][rate]
    except requests.exceptions.RequestException as e:
        print(f"Failed to obtain exchange rate: {e}")
        return None
    