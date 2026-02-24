from psycopg.types.json import Json
from src.database import pool
import yfinance as yf

df = yf.download("KMI", start="2026-01-02", end="2026-02-24")
for i, row in df.iterrows():
    stock_dict = {
        "ticker": "KMI",
        "price": row[("Close", "KMI")],
        "currency": "USD",
        "date": i.strftime("%Y-%m-%d"),
        "volume": row[("Volume", "KMI")]
    }
    with pool.connection() as conn:
        conn.execute(
            "INSERT INTO stocks_raw (stock) VALUES (%s)",
                     (Json(stock_dict),)
        )
