import pandas as pd 
#Lists every unique Stock_symbol in the FNSPID file and compares it with our tickers. 
# Found 8,552 symbols; COIN, META, RIVN, PLTR, UPST, AFRM and MRNA are missing. FB exists but only has 433 articles (Feb to Jun 2020).

TICKERS = ["FB"]                  
kept = []
START = pd.Timestamp("2018-01-01", tz="UTC")
END = pd.Timestamp("2023-12-31", tz="UTC")

for i, chunk in enumerate(pd.read_csv("data/nasdaq_external_data.csv", usecols=["Date","Stock_symbol"], chunksize=500000)):          
    chunk["Date"] = pd.to_datetime(chunk["Date"], utc=True)
    mask = chunk["Stock_symbol"].isin(TICKERS) & chunk["Date"].between(START,END)                     # in TICKERS and between START and END
    kept.append(chunk[mask])
    print(f"chunk {i} done")   
news=pd.concat(kept)           
print(len(news))
print(min(news["Date"]))
print(max(news["Date"]))