from pydantic import BaseModel
from datetime import date

class StockSchema(BaseModel):
    ticker: str
    price: float
    currency: str
    date: date
    volume: int