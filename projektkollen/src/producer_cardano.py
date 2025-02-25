import os
import sys
import time
import json
from pprint import pprint
from quixstreams import Application  
from connect_api import get_latest_coin_data

COIN_SYMBOL = "ADA"

def main():
    app = Application(broker_address="localhost:9092", consumer_group="ADA_coin_group")
    coin_topic = app.topic(name="ADA_coins", value_serializer="json")

    with app.get_producer() as producer:
        while True:
            latest_coin_data = get_latest_coin_data(COIN_SYMBOL)
            
            kafka_payload = coin_topic.serialize(key=latest_coin_data["symbol"], value=latest_coin_data)
            
            print(f"Sending event: key = {kafka_payload.key}, price = {latest_coin_data['quote']['USD']['price']}")
            
            producer.produce(topic=coin_topic.name, key=kafka_payload.key, value=kafka_payload.value)
            
            time.sleep(30)  

if __name__ == "__main__":
    main()
