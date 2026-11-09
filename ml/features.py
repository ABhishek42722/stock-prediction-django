import pandas as pd

raw = pd.read_csv("data/prices.csv", header=[0, 1], index_col=0, parse_dates=True)
close = raw["Close"]


def rsi(series, window=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window).mean()
    loss = (-delta.clip(upper=0)).rolling(window).mean()
    return 100 - 100 / (1 + gain / loss)


ema12 = close.ewm(span=12, adjust=False).mean()
ema26 = close.ewm(span=26, adjust=False).mean()
macd = ema12 - ema26
macd_signal = macd.ewm(span=9, adjust=False).mean()

features = pd.DataFrame({
    "rsi": rsi(close).stack(),
    "macd": (macd / close).stack(),
    "macd_signal": (macd_signal / close).stack(),
    "dist_ma10": (close / close.rolling(10).mean() - 1).stack(),
    "dist_ma20": (close / close.rolling(20).mean() - 1).stack(),
    "dist_ma50": (close / close.rolling(50).mean() - 1).stack(),
    "volatility20": close.pct_change().rolling(20).std().stack(),
    "label_return": ((close.shift(-1) / close - 1) * 100).stack(),
})
features = features.dropna()
features.index.names = ["date", "ticker"]

print(features.shape)
print(features.head())
features.to_csv("data/features.csv")