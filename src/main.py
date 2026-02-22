from psycopg.rows import dict_row
from fastapi import FastAPI
from psycopg.types.json import Json
from src.schemas import StockData
from src.database import pool

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

