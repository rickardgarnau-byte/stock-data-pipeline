from psycopg.types.json import Json
from src.database import pool
import yfinance as yf
import schedule
import time


tickers = ['AAPL','ADBE','AMZN','BAC','IBM','MSFT','INTC','GOOGL','NFLX','NVDA','QCOM','WFC','BA','C','JPM','TSLA','INSM','TSM','KMI','ISRG','GEV','NBIS','SNOW','DLO','UBER','HIMS','V','PYPL','LMND','MA','AXP','MELI','ACN','DDOG','ONDS','NU','RIG','PLTR','PATH','SNAP','ORCL','BMNR','HOOD','FIG','AMD','PFE','MU','NOW','CRWV','CPNG','U','SNDK','AVGO','NKE','CRWD','CRM','RKLB','FCX','ASTS','SHOP','CPRT','DIS','GTLB','TEAM','MRVL','BE','LUMN','ANET','LUNR','NET','TXN','SBUX']

def fetch_data():
    for ticker in tickers:
        df = yf.download(ticker, start="2026-02-23", end="2026-03-24")
        for i, row in df.iterrows():
            stock_dict = {
                "ticker": ticker,
                "price": row[("Close", ticker)],
                "currency": "USD",
                "date": i.strftime("%Y-%m-%d"),
                "volume": row[("Volume", ticker)]
        }
            with pool.connection() as conn:
                conn.execute(
                    "INSERT INTO stocks_raw (stock) VALUES (%s)",
                    (Json(stock_dict),)
                )

schedule.every().day.at("15:55").do(fetch_data)
while True:
    schedule.run_pending()
    time.sleep(1)