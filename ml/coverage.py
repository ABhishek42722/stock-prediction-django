import pandas as pd

# Share of each ticker’s trading days with at least one article.
# Weekend and holiday articles are mapped to the next trading day, 
# articles with no trading day left inside the window are dropped (257 of them), 
# and the window ends at 2023-12-08.
# INTC, AMD and KO have about 90%+ coverage. 
# Thin-coverage for tickers: PG 12.7, AMZN 14.3, JNJ 26.0, MSFT 27.3, GOOGL 28.7, JPM 28.8, AAPL 29.6.
# Last trading day is 2023-12-10, (unreliable dates from Dec 11)

news = pd.read_csv("data/news_filtered.csv", parse_dates=["Date"])

prices = pd.read_csv("data/prices.csv", header=[0, 1], index_col=0, parse_dates=True, skiprows=[2])
prices = prices.loc["2018-01-01":"2023-12-10"]

# Merging news rows to nearest(<) price rows
days = pd.DataFrame({"trade_date": prices.index})
days=days.sort_values("trade_date")
news["Date"]=news["Date"].dt.tz_localize(None)
news = news.sort_values("Date")
n = pd.merge_asof(news, days, left_on="Date", right_on="trade_date",
                  direction="forward", allow_exact_matches=False)
n=n.dropna(subset=["trade_date"])

distinct_days = n.groupby("Stock_symbol")["trade_date"].nunique()     
price_days = prices["Close"].notna().sum()                               
coverage = (( distinct_days / price_days ) * 100).dropna().round(1)      

print(coverage.sort_values(ascending=False))
print(n[n["Date"] == "2023-11-23"][["Date", "trade_date"]])