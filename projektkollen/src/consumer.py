from quixstreams import Application
from quixstreams.sinks.community.postgresql import PostgreSQLSink
from constants import (
    POSTGRES_USER,
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
)
 

def extract_ada_data(message):
    quote = message["quote"]["USD"]
    return {
        "coin": message["name"],
        "total_supply": message["total_supply"],
        "price_usd": quote["price"],
        "volume": quote["volume_24h"],
        "volume_change": quote["volume_change_24h"],
        "percent_change": quote["percent_change_1h"],
        "percent_change_24h": quote["percent_change_24h"],
        "percent_change_7d": quote["percent_change_7d"],
        "percent_change_30d": quote["percent_change_30d"],
        "updated": message["last_updated"]
    }


def create_postgres_sink():
    sink = PostgreSQLSink(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DBNAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        table_name="cardano",
        schema_auto_update=True,
    )

    return sink




def main():
    app = Application(
        broker_address="localhost:9092",
        consumer_group="ADA_coin_group",
        auto_offset_reset="earliest",
    )
    coin_topic = app.topic(name= "ADA_coins", value_deserializer="json")
    
    sdf = app.dataframe(topic= coin_topic)
    

    sdf = sdf.apply(extract_ada_data)
    
    sdf = sdf.update(lambda row: print(row))
    
    
    postgres_sink = create_postgres_sink()
    sdf.sink(postgres_sink)
    
    app.run()
    
 
if __name__=='__main__':
    main()