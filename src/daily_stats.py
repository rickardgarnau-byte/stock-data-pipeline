from src.processor import get_stocks


def get_top_gainers():
    df = get_stocks()
    df = df.sort_values(by='date').reset_index(drop=True)
    df["pct_change"] = df.groupby("ticker")["price"].pct_change()
    latest_date = df["date"].max()
    df = df[df["date"] == latest_date]
    df = df.sort_values(by=('pct_change'), ascending=False)
    df["pct_change"] = (df["pct_change"] * 100).round(2)
    df["price"] = df["price"].round(2)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    return df.head(10).to_dict(orient="records")

def get_top_volume():
    df = get_stocks()
    df = df.sort_values(by='date').reset_index(drop=True)
    latest_date = df["date"].max()
    df = df[df["date"] == latest_date]
    df = df.sort_values(by=('volume'), ascending=False)
    df["price"] = df["price"].round(2)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    return df.head(10).to_dict(orient="records")

def get_top_losers():
    df = get_stocks()
    df = df.sort_values(by='date').reset_index(drop=True)
    df["pct_change"] = df.groupby("ticker")["price"].pct_change()
    latest_date = df["date"].max()
    df = df[df["date"] == latest_date]
    df = df.sort_values(by=('pct_change'), ascending=True)
    df["pct_change"] = (df["pct_change"] * 100).round(2)
    df["price"] = df["price"].round(2)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    return df.head(10).to_dict(orient="records")