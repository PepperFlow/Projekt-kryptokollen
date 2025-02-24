from dotenv import load_dotenv
import os
 
load_dotenv()
 
API_KEY = os.getenv("API_KEY")
 
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DBNAME = os.getenv("POSTGRES_DB")
 


