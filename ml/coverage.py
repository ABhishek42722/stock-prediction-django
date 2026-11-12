import pandas as pd

# Share of each ticker’s trading days with at least one article. 
# Weekend and holiday news (9,941 articles, 8.3%) is dropped. 
# INTC, AMD and KO have about 90%+ coverage. 
# PG (12%), AMZN (15%) and JNJ, MSFT, GOOGL, JPM and AAPL (under 30%) are thin.

news = pd.read_csv("data/news_filtered.csv", parse_dates=["Date"])
news["Day"] = news["Date"].dt.date

prices = pd.read_csv("data/prices.csv", header=[0, 1], index_col=0, parse_dates=True, skiprows=[2])

trading_days = set(prices.index.date)
news_td = news[news["Day"].isin(trading_days)]  
distinct_days = news_td.groupby("Stock_symbol")["Day"].nunique()     
price_days = prices["Close"].notna().sum()                               
coverage = (( distinct_days / price_days ) * 100).dropna().round(1)            
print(coverage.sort_values(ascending=False))
print("Articles dropped due to falling on non-trading days: ",len(news)-len(news_td))