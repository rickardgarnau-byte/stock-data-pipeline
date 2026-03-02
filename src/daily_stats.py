import pandas as pd
from src.processor import get_stocks
from datetime import date, timedelta
import yfinance as yf

tickers = ['AAPL','ADBE','AMZN','BAC','IBM','MSFT','INTC','GOOGL','NFLX','NVDA','QCOM','WFC','BA','C','JPM','TSLA','INSM','TSM','KMI','ISRG','GEV','NBIS','SNOW','DLO','UBER','HIMS','V','PYPL','LMND','MA','AXP','MELI','ACN','DDOG','ONDS','NU','RIG','PLTR','PATH','SNAP','ORCL','BMNR','HOOD','FIG','AMD','PFE','MU','NOW','CRWV','CPNG','U','SNDK','AVGO','NKE','CRWD','CRM','RKLB','FCX','ASTS','SHOP','CPRT','DIS','GTLB','TEAM','MRVL','BE','LUMN','ANET','LUNR','NET','TXN','SBUX']

def get_prev_close():
    yesterday = date.today() - timedelta(days=1)
    two_days_ago = date.today() - timedelta(days=2)
    df = yf.download(tickers, period="5d", progress=False)["Close"]
    return df.iloc[-2]



def get_top_gainers():
    df = get_stocks()
    df = df.sort_values(by='date').reset_index(drop=True)
    today = date.today()
    df = df[df["date"].dt.date == today]

    prev_close = get_prev_close()
    last_price = df.groupby("ticker")["price"].last()
    pct_change = ((last_price - prev_close) / prev_close * 100).round(2)

    result = last_price.reset_index()
    result.columns = ["ticker", "price"]
    result["pct_change"] = result["ticker"].map(pct_change)
    result["price"] = result["price"].round(2)
    result["date"] = df.groupby("ticker")["date"].last().values
    result["currency"] = "USD"
    result["volume"] = df.groupby("ticker")["volume"].last().values

    result = result.dropna()
    result = result.sort_values(by="pct_change", ascending=False)
    return result.head(10).to_dict(orient="records")

def get_top_losers():
    df = get_stocks()
    df = df.sort_values(by='date').reset_index(drop=True)
    today = date.today()
    df = df[df["date"].dt.date == today]

    prev_close = get_prev_close()
    last_price = df.groupby("ticker")["price"].last()
    pct_change = ((last_price - prev_close) / prev_close * 100).round(2)

    result = last_price.reset_index()
    result.columns = ["ticker", "price"]
    result["pct_change"] = result["ticker"].map(pct_change)
    result["price"] = result["price"].round(2)
    result["date"] = df.groupby("ticker")["date"].last().values
    result["currency"] = "USD"
    result["volume"] = df.groupby("ticker")["volume"].last().values

    result = result.dropna()
    result = result.sort_values(by="pct_change", ascending=True)
    return result.head(10).to_dict(orient="records")


def get_top_volume():
    df = get_stocks()
    df = df.sort_values(by='date').reset_index(drop=True)
    today = date.today()

    df = df[df["date"].dt.date == today]
    if df.empty:
        return []

    result = df.sort_values('date').groupby('ticker').tail(1).copy()
    result = result.sort_values(by='volume', ascending=False)
    result["price"] = result["price"].round(2)
    result["date"] = result["date"].dt.strftime("%Y-%m-%d %H:%M")
    result["currency"] = "USD"

    return result.head(10).to_dict(orient="records")


portfolio = ['TSM', 'GEV', 'ENR.DE', 'KMI', 'INSM', 'ISRG']

def get_prev_close_portfolio():
    df = yf.download(portfolio, period="1d", interval="1m")["Close"]
    current_price = df.iloc[-1]
    return current_price


def get_portfolio():
    today = date.today()
    yesterday = today - timedelta(days=1)
    current = yf.download(portfolio, period="5d", interval="1m")["Close"].iloc[-1]
    prev_close = yf.download(portfolio, period="5d", progress=False)["Close"].iloc[-2]

    pct_change = ((current - prev_close) / prev_close * 100).round(2)

    result = pd.DataFrame({
        "ticker": current.index,
        "price": current.values.round(2),
        "pct_change": pct_change.reindex(current.index).values.round(2),
        "currency": "USD"
    })
    result = result.dropna()
    result = result.sort_values(by="pct_change", ascending=False)
    return result.to_dict(orient="records")