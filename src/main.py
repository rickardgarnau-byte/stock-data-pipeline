from psycopg.rows import dict_row
from fastapi import FastAPI
from psycopg.types.json import Json
from psycopg_pool import ConnectionPool
from schemas import StockData

DATABASE_URL = "postgresql://postgres:benny123@localhost:5440/stock_db"
app = FastAPI(title="Unusual Volume")
pool = ConnectionPool(DATABASE_URL)



@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/stocks")
def insert_stock(stock: StockData):
    with pool.connection() as conn:
        conn.execute(
            "INSERT INTO stocks_raw (stock) VALUES (%s)",
            (Json(stock.model_dump(mode="json")),)
        )
    return {"message": "Stock inserted", "ticker": stock.ticker}

@app.get("/stocks")
def get_stocks():
    with pool.connection() as conn:
        conn.row_factory = dict_row
        rows = conn.execute("SELECT * FROM stocks_raw").fetchall()
    return rows



