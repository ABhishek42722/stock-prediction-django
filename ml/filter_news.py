from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent         # TODO 1
RAW = ROOT / "data" / "nasdaq_external_data.csv"
OUT = ROOT / "data" / "news_filtered.csv"

TICKERS = [
    # stable large caps
    "AAPL", "MSFT", "JPM", "KO", "PG", "JNJ", "WMT", "XOM", "V", "PEP",
    # growth / tech
    "NVDA", "AMD", "TSLA", "NFLX", "AMZN", "GOOGL", "CRM", "ADBE", "INTC",
    # volatile / high-beta
    "SNAP", "ROKU", "DKNG", "ENPH" ,
]

START = pd.Timestamp("2018-01-01", tz="UTC")
END_EXCLUSIVE = pd.Timestamp("2024-01-01", tz="UTC")

kept = []
for i, chunk in enumerate(pd.read_csv(RAW, usecols=["Date","Stock_symbol","Article_title"], dtype={"Stock_symbol":str}, chunksize=500000)):  # TODO 2
    chunk["Date"] = pd.to_datetime(chunk["Date"], utc=True)
    mask = (chunk["Stock_symbol"].isin(TICKERS))&(chunk["Date"]>=START)&(chunk["Date"]<END_EXCLUSIVE)    # TODO 3
    kept.append(chunk[mask])
    print(f"chunk {i} done")

news = pd.concat(kept,ignore_index=True)   # TODO 4
news.to_csv(OUT, index=False)
print(news.shape)
print(news.head())
print(news["Stock_symbol"].value_counts())