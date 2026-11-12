import pandas as pd

TICKERS = [
    # stable large caps
    "AAPL", "MSFT", "JPM", "KO", "PG", "JNJ", "WMT", "XOM", "V", "PEP",
    # growth / tech
    "NVDA", "AMD", "TSLA", "NFLX", "AMZN", "GOOGL", "CRM", "ADBE", "INTC",
    # volatile / high-beta
    "SNAP", "ROKU", "DKNG", "ENPH"
]
THRESHOLDS = [3, 5, 7, 9]

prices = pd.read_csv("data/prices.csv", header=[0, 1], index_col=0, parse_dates=True,skiprows=[2])
close=prices["Close"][TICKERS].loc["2018-01-01":"2023-12-31"]
next_day_return = (close.shift(-1) / close - 1) * 100

total = next_day_return.notna().sum().sum()
print(f"Total labelled rows: {total}\n")
for t in THRESHOLDS:
    positives = (next_day_return >= t).sum().sum()
    print(f"Rise of at least {t}%: {positives} rows ({positives / total:.2%})")

print("\nPositives at 3% per ticker:")
print((next_day_return >= 3).sum().sort_values(ascending=False))
print("\nPositives at 5% per ticker:")
print((next_day_return >= 5).sum().sort_values(ascending=False))
print("\nPositives at 7% per ticker:")
print((next_day_return >= 7).sum().sort_values(ascending=False))
print("\nPositives at 9% per ticker:")
print((next_day_return >= 9).sum().sort_values(ascending=False))