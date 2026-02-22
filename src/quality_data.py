import pandas as pd

missing_df = pd.read_csv("stocks_cleaned.csv")
rejected_df = pd.read_csv("stocks_cleaned.csv")

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
any_flagged = flagged_ticker | flagged_price | flagged_currency | flagged_date
df_flagged = missing_df[any_flagged]
df_flagged.to_csv("flagged_data.csv", index=False)

rejected_ticker = rejected_df["ticker"].isna()
rejected_price = (
    (rejected_df["price"] == 0) |
    (rejected_df["price"] > 50000) |
    (rejected_df["price"] < 0)
)
rejected_currency = (rejected_df["currency"].astype(str).str.strip().str.len() != 3) & rejected_df["currency"].notna()
rejected_date = pd.to_datetime(rejected_df["date"], errors="coerce").isna() & rejected_df["date"].notna()
any_rejected = rejected_ticker | rejected_price | rejected_currency | rejected_date
df_rejected = rejected_df[any_rejected]
df_rejected.to_csv("rejected_data.csv", index=False)