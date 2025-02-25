from quixstreams import Application
from quixstreams.sinks.community.postgresql import PostgreSQLSink
from constants import (
    POSTGRES_USER,
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
)

def transform_ada_data(record):
    market_data = record["quote"]["USD"]
    return {
        "currency": record["name"],
        "total_supply": record["total_supply"],
        "price_usd": market_data["price"],
        "trade_volume": market_data["volume_24h"],
        "volume_shift": market_data["volume_change_24h"],
        "hourly_change": market_data["percent_change_1h"],
        "daily_change": market_data["percent_change_24h"],
        "weekly_change": market_data["percent_change_7d"],
        "monthly_change": market_data["percent_change_30d"],
        "last_updated": record["last_updated"]
    }

def setup_postgres_sink():
    return PostgreSQLSink(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DBNAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        table_name="cardano",
        schema_auto_update=True,
    )

def start_application():
    app = Application(
        broker_address="localhost:9092",
        consumer_group="ADA_data_group",
        auto_offset_reset="earliest",
    )
    ada_topic = app.topic(name="ADA_stream", value_deserializer="json")
    
    data_stream = app.dataframe(topic=ada_topic)
    
    data_stream = data_stream.apply(transform_ada_data)
    
    data_stream = data_stream.update(lambda entry: print(entry))
    
    database_sink = setup_postgres_sink()
    data_stream.sink(database_sink)
    
    app.run()

if __name__ == "__main__":
    start_application()