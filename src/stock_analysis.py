import pandas as pd

percental_diff = pd.read_csv('../data/cleaned_data.csv')

# ---- % Change ----
percental_diff = percental_diff.sort_values(by='date').reset_index(drop=True)
percental_diff["pct_change"] = percental_diff.groupby("ticker")["price"].pct_change()
percental_diff['pct_change'] = percental_diff['pct_change'].round(2) * 100
print(percental_diff)

# ---- Mean price ----
mean_price = percental_diff.groupby("ticker")["price"].mean()
print(f"Mean price: {mean_price}")


# ---- Volatility ----
percental_diff['vola'] = percental_diff.groupby("ticker")["price"].rolling(window=2).std().reset_index(level=0, drop=True)
print(percental_diff['vola'])

# ---- Volume ----
most_volume = percental_diff["high_volume"].groupby("ticker")["volume"].max()
print(f"Most active: {most_volume}")