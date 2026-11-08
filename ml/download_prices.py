import yfinance as yf

TICKERS = [
    "AAPL", "MSFT", "JPM", "KO", "PG", "JNJ", "WMT", "XOM", "V", "PEP",
    "NVDA", "AMD", "TSLA", "NFLX", "META", "AMZN", "GOOGL", "CRM", "ADBE", "INTC",
    "PLTR", "COIN", "RIVN", "UPST", "SNAP", "ROKU", "DKNG", "AFRM", "MRNA", "ENPH",
]

prices = yf.download(TICKERS, start="2018-01-01", end="2023-12-31",
                     auto_adjust=True, threads=False)
prices.to_csv("data/prices.csv")
print(prices.shape)