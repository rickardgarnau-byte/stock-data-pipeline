from psycopg.types.json import Json
from src.database import pool
import yfinance as yf
import schedule
import time


tickers = ['AAPL','ADBE','AMZN','BAC','IBM','MSFT','INTC','GOOGL','NFLX','NVDA','QCOM','WFC','BA','C','JPM','TSLA','INSM','TSM','KMI','ISRG','GEV','NBIS','SNOW','DLO','UBER','HIMS','V','PYPL','LMND','MA','AXP','MELI','ACN','DDOG','ONDS','NU','RIG','PLTR','PATH','SNAP','ORCL','BMNR','HOOD','FIG','AMD','PFE','MU','NOW','CRWV','CPNG','U','SNDK','AVGO','NKE','CRWD','CRM','RKLB','FCX','ASTS','SHOP','CPRT','DIS','GTLB','TEAM','MRVL','BE','LUMN','ANET','LUNR','NET','TXN','SBUX']


def fetch_data():
    for ticker in tickers:
        df = yf.download(ticker, period="5d", interval="1m", progress=False)

        if df.empty:
            continue

        last_row = df.iloc[-1:]

        for i, row in last_row.iterrows():
            stock_dict = {
                "ticker": ticker,
                "price": float(row[("Close", ticker)]),
                "currency": "USD",
                "date": i.strftime("%Y-%m-%d %H:%M"),
                "volume": int(row[("Volume", ticker)])
            }
            with pool.connection() as conn:
                conn.execute(
                    "INSERT INTO stocks_raw (stock) VALUES (%s) ON CONFLICT DO NOTHING",
                    (Json(stock_dict),)
                )

fetch_data()

schedule.every().day.at("15:30").do(fetch_data)

while True:
    schedule.run_pending()
    time.sleep(1)
