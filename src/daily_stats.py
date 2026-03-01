import pandas as pd
from src.processor import get_stocks
from datetime import date, timedelta
import yfinance as yf

tickers = ['AAPL','ADBE','AMZN','BAC','IBM','MSFT','INTC','GOOGL','NFLX','NVDA','QCOM','WFC','BA','C','JPM','TSLA','INSM','TSM','KMI','ISRG','GEV','NBIS','SNOW','DLO','UBER','HIMS','V','PYPL','LMND','MA','AXP','MELI','ACN','DDOG','ONDS','NU','RIG','PLTR','PATH','SNAP','ORCL','BMNR','HOOD','FIG','AMD','PFE','MU','NOW','CRWV','CPNG','U','SNDK','AVGO','NKE','CRWD','CRM','RKLB','FCX','ASTS','SHOP','CPRT','DIS','GTLB','TEAM','MRVL','BE','LUMN','ANET','LUNR','NET','TXN','SBUX']

def get_prev_close():
    yesterday = date.today() - timedelta(days=1)
    two_days_ago = date.today() - timedelta(days=2)
    df = yf.download(tickers, start=two_days_ago, end=date.today(), progress=False)["Close"]
    return df.iloc[-1]

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

    result = result.sort_values(by="pct_change", ascending=True)
    return result.head(10).to_dict(orient="records")

def get_top_volume():
    df = get_stocks()
    df = df.sort_values(by='date').reset_index(drop=True)
    today = date.today()
    df = df[df["date"].dt.date == today]
    latest_date = df["date"].max()
    df = df[df["date"] == latest_date]
    df = df.sort_values(by='volume', ascending=False)
    df["price"] = df["price"].round(2)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d %H:%M")

    return df.head(10).to_dict(orient="records")


portfolio = ['TSM', 'GEV', 'ENR.DE', 'KMI', 'INSM', 'ISRG']

def get_prev_close_portfolio():
    df = yf.download(portfolio, period="1d", interval="1m")["Close"]
    current_price = df.iloc[-1]
    return current_price


def get_portfolio():
    today = date.today()
    yesterday = today - timedelta(days=1)
    current = yf.download(portfolio, period="1d", interval="1m")["Close"].iloc[-1]
    prev_close = yf.download(portfolio, start=yesterday, end=today, progress=False)["Close"].iloc[-1]

    pct_change = ((current - prev_close) / prev_close * 100).round(2)

    result = pd.DataFrame({
        "ticker": current.index,
        "price": current.values.round(2),
        "pct_change": pct_change.values.round(2),
        "currency": "USD"
    })

    result = result.sort_values(by="pct_change", ascending=False)
    return result.to_dict(orient="records")

print(get_portfolio())