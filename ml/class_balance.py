import yfinance as yf

TICKERS = [
    # stable large caps
    "AAPL", "MSFT", "JPM", "KO", "PG", "JNJ", "WMT", "XOM", "V", "PEP",
    # growth / tech
    "NVDA", "AMD", "TSLA", "NFLX", "META", "AMZN", "GOOGL", "CRM", "ADBE", "INTC",
    # volatile / high-beta
    "PLTR", "COIN", "RIVN", "UPST", "SNAP", "ROKU", "DKNG", "AFRM", "MRNA", "ENPH",
]
THRESHOLDS = [3, 5, 7, 9]

prices = yf.download(TICKERS, start="2018-01-01", end="2023-12-31", auto_adjust=True)["Close"]
next_day_return = (prices.shift(-1) / prices - 1) * 100

total = next_day_return.notna().sum().sum()
print(f"Total labelled rows: {total}\n")
for t in THRESHOLDS:
    positives = (next_day_return >= t).sum().sum()
    print(f"Rise of at least {t}%: {positives} rows ({positives / total:.2%})")

print("\nPositives at 7% per ticker:")
print((next_day_return >= 7).sum().sort_values(ascending=False))