from pydantic import BaseModel
from typing import Optional
from datetime import date

class StockData(BaseModel):
    ticker: str
    price: float
    currency: str = "USD"
    date: date
    volume: Optional[int] = None