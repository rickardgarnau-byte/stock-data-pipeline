from psycopg.rows import dict_row
from fastapi import FastAPI
from psycopg.types.json import Json
from src.schemas import StockData
from src.database import pool
from src.daily_stats import get_top_gainers as fetch_top_gainers
from src.daily_stats import get_top_volume as fetch_top_volume
from src.daily_stats import get_top_losers as fetch_top_losers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Unusual Volume")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/stocks")
def get_stocks():
    with pool.connection() as conn:
        conn.row_factory = dict_row
        rows = conn.execute("SELECT * FROM stocks_raw").fetchall()
    return rows

@app.post("/stocks")
def insert_stock(stock: StockData):
    with pool.connection() as conn:
        conn.execute(
            "INSERT INTO stocks_raw (stock) VALUES (%s)",
            (Json(stock.model_dump(mode="json")),)
        )
    return {"message": "Stock inserted", "ticker": stock.ticker}



@app.post("/stocks/bulk")
async def add_stocks_bulk(stocks: list[StockData]):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            for stock in stocks:
                cur.execute(
                    "INSERT INTO stocks_raw (stock) VALUES (%s)",
                    (Json(stock.model_dump(mode="json")),)
                )
    return {"inserted": len(stocks)}

@app.get("/top_gainers")
def top_gainers_endpoint():
    return fetch_top_gainers()

@app.get("/top_volume")
def get_top_volume():
    return fetch_top_volume()

@app.get("/top_losers")
def get_top_losers():
    return fetch_top_losers()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)