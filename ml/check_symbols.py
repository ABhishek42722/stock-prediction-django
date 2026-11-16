import pandas as pd 
from pathlib import Path
# Lists every unique Stock_symbol in the FNSPID file and compares it with our 30 planned tickers.
# Found 8,552 symbols, and COIN, META, RIVN, PLTR, UPST, AFRM and MRNA are missing. 
# The old symbol FB exists but has only 433 articles (2020-02-19 to 2020-06-10), too few to use. 

ALL_TICKERS = [
    "AAPL", "MSFT", "JPM", "KO", "PG", "JNJ", "WMT", "XOM", "V", "PEP",
    "NVDA", "AMD", "TSLA", "NFLX", "META", "AMZN", "GOOGL", "CRM", "ADBE", "INTC",
    "PLTR", "COIN", "RIVN", "UPST", "SNAP", "ROKU", "DKNG", "AFRM", "MRNA", "ENPH",
]        

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "nasdaq_external_data.csv"

symbols = set()
for chunk in pd.read_csv(RAW, usecols=["Stock_symbol"], dtype={"Stock_symbol": str}, chunksize=500000):
    symbols.update(chunk["Stock_symbol"].dropna().unique())

print(len(symbols))
print(sorted(set(ALL_TICKERS) - symbols))
print("FB" in symbols)