import os
import sys

# Lägg till projektets root-mapp i sys.path
#sys.path.append(os.path.abspath("../data-platforms-abdirahman-hassan-de24"))
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "C:/Users/Brukare/Desktop/github/data_enginer_trion/src")))



import time
from quixstreams import Application  
import json
from pprint import pprint
from producer.connect_api import get_latest_coin_data
 
TARGET_COIN = "ETH"
 
def main():
    app = Application(broker_address="localhost:9092", consumer_group="ETH_coin_group")
    coins_topic = app.topic(name="ETH_coins", value_serializer="json")
 
    with app.get_producer() as producer:
        while True:
            coin_latest = get_latest_coin_data(TARGET_COIN)
 
            kafka_message = coins_topic.serialize(key=coin_latest["symbol"], value=coin_latest)
 
            print(f"produce event with key = {kafka_message.key}, price = {coin_latest['quote']['USD']['price']}")
 
            producer.produce(topic=coins_topic.name, key=kafka_message.key, value=kafka_message.value)
 
            time.sleep(30)   
 
 
if __name__ == "__main__":
    main()
 