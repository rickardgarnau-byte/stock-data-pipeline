import pandas as pd

missing_df = pd.read_csv("stocks_cleaned.csv")


flagged_ticker = (
        (missing_df["ticker"].isna()) |
        (missing_df["ticker"] == "")
)

flagged_price = (
        (missing_df["price"].isna()) |
        (missing_df["price"] > 10000) |
        (missing_df["price"] < 0)
)

flagged_currency = (
        (missing_df["currency"].isna()) |
        (missing_df["currency"] == "")
)

flagged_date = (
        (missing_df["date"].isna()) |
        (missing_df["date"] == "")
)

any_flagged = (
    flagged_ticker |
    flagged_price |
    flagged_currency |
    flagged_date
)

df_flagged = missing_df[any_flagged]
df_flagged.to_csv("any_flagged.csv", index=False)
