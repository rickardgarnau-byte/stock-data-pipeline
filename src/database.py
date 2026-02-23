from psycopg_pool import ConnectionPool
from dotenv import load_dotenv
import os

load_dotenv() # reads .env from project root
DB_PORT = os.getenv("DB_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DATABASE_URL =f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
pool = ConnectionPool(DATABASE_URL)