import pandas as pd
from database import pool
from psycopg.rows import dict_row

def fetch_stocks():
    with pool.connection() as conn:
        conn.row_factory = dict_row
        rows = conn.execute("SELECT * FROM stocks_raw").fetchall()
        df = pd.DataFrame(rows)
        return df

def get_stocks() -> pd.DataFrame:
    df = fetch_stocks()
    df_expanded = pd.json_normalize(df["stock"])



    df_expanded["ticker"] = df_expanded["ticker"].astype("string")
    df_expanded["ticker"] = df_expanded["ticker"].str.strip()
    df_expanded["ticker"] = df_expanded["ticker"].str.upper()
    df_expanded["ticker"] = df_expanded["ticker"].str.replace(" ", "").str.replace("_", "-")
    df_expanded = df_expanded[df_expanded["ticker"].str.strip() != ""]

    df_expanded["price"] = pd.to_numeric(df_expanded["price"], errors="coerce")
    df_expanded = df_expanded[df_expanded["price"] > 0]


    df_expanded["currency"] = df_expanded["currency"].astype("string")
    df_expanded["currency"] = df_expanded["currency"].str.strip()
    df_expanded["currency"] = df_expanded["currency"].str.upper()

    df_expanded["date"] = pd.to_datetime(df_expanded["date"], errors="coerce", yearfirst=True)
    df_expanded = df_expanded[df_expanded["date"].notna()]
    df_expanded = df_expanded.drop_duplicates(subset=["ticker", "date"])
    df_expanded.to_csv("stocks_cleaned.csv", index=False)
    return df_expanded

if __name__ == "__main__":
    df = get_stocks()
    print(df)