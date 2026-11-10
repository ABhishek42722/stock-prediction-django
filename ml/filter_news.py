import pandas as pd

TICKERS = [
        "AAPL", "MSFT", "JPM", "KO", "PG", "JNJ", "WMT", "XOM", "V", "PEP",
        "NVDA", "AMD", "TSLA", "NFLX", "META", "AMZN", "GOOGL", "CRM", "ADBE", "INTC",
        "PLTR", "COIN", "RIVN", "UPST", "SNAP", "ROKU", "DKNG", "AFRM", "MRNA", "ENPH",
    ]                  
START = pd.Timestamp("2018-01-01", tz="UTC")
END = pd.Timestamp("2023-12-31", tz="UTC")

kept = []
for i, chunk in enumerate(pd.read_csv("data/nasdaq_external_data.csv", usecols=["Date","Stock_symbol"], chunksize=500000)):
    chunk["Date"] = pd.to_datetime(chunk["Date"], utc=True)
    mask = chunk["Stock_symbol"].isin(TICKERS) & chunk["Date"].between(START,END)                     # in TICKERS and between START and END
    kept.append(chunk[mask])
    print(f"chunk {i} done")          # so you can see it working

news = pd.concat(kept)
news.to_csv("data/news_filtered.csv", index=False)
print(news["Stock_symbol"].value_counts())