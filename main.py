from fastapi import FastAPI
from psycopg.types.json import Json
from psycopg_pool import ConnectionPool
import yfinance as yf

from schema.stocks_raw import StockSchema

aapl = yf.Ticker("AAPL")
data = aapl.history(period="1mo")
print(data)


