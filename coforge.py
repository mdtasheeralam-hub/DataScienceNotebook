import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc

# -------------------------
# 1. Load CSV
# -------------------------
df = pd.read_csv("Coforge.csv")

# Convert date column
df["DATE"] = pd.to_datetime(df["DATE"])
df["DATE_NUM"] = mdates.date2num(df["DATE"])

# -------------------------
# 2. Plot HIGH vs LOW Line Graph
# -------------------------
plt.figure(figsize=(12,6))
plt.plot(df["DATE"], df["HIGH"], label="High")
plt.plot(df["DATE"], df["LOW"], label="Low")

plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.title("Daily HIGH and LOW")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()

# Convert OHLC columns to numeric
numeric_cols = ["OPEN", "HIGH", "LOW", "CLOSE"]
for col in numeric_cols:
    df[col] = df[col].astype(str).str.replace(",", "").astype(float)

# -------------------------
# 3. Candlestick Chart (OHLC)
# -------------------------
ohlc = df[["DATE_NUM", "OPEN", "HIGH", "LOW", "CLOSE"]]

plt.figure(figsize=(14,7))
ax = plt.gca()
candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='g', colordown='r')

ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.title("Candlestick Chart (OHLC)")
plt.xlabel("Date")
plt.ylabel("Price")
plt.grid()
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()

# -------------------------
# 4. Moving Averages (20, 50, 200 days)
# -------------------------
df["MA20"] = df["CLOSE"].rolling(20).mean()
df["MA50"] = df["CLOSE"].rolling(50).mean()
df["MA200"] = df["CLOSE"].rolling(200).mean()

plt.figure(figsize=(14,7))
plt.plot(df["DATE"], df["CLOSE"], label="Close Price", linewidth=1)
plt.plot(df["DATE"], df["MA20"], label="MA20")
plt.plot(df["DATE"], df["MA50"], label="MA50")
plt.plot(df["DATE"], df["MA200"], label="MA200")

plt.title("Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.xticks(rotation=45)
plt.show()

# -------------------------
# 5. Volume Chart
# -------------------------
plt.figure(figsize=(14,4))
plt.bar(df["DATE"], df["VOLUME"], width=1)
plt.title("Daily Volume")
plt.xlabel("Date")
plt.ylabel("Volume")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -------------------------
# 6. Trendline (Close Price)
# -------------------------
import numpy as np

x = np.arange(len(df))
y = df["CLOSE"]
coef = np.polyfit(x, y, 1)
trend = coef[0] * x + coef[1]

plt.figure(figsize=(14,7))
plt.plot(df["DATE"], df["CLOSE"], label="Close")
plt.plot(df["DATE"], trend, label="Trendline", color="red", linewidth=2)
plt.title("Trendline Analysis")
plt.legend()
plt.grid()
plt.show()

# -------------------------
# 7. Simple Buy/Sell Signals (MA Crossover)
# -------------------------
df["Signal"] = 0
df["Signal"] = df["MA20"] > df["MA50"]
df["Buy"] = (df["Signal"] == 1) & (df["Signal"].shift(1) == 0)
df["Sell"] = (df["Signal"] == 0) & (df["Signal"].shift(1) == 1)

plt.figure(figsize=(14,7))
plt.plot(df["DATE"], df["CLOSE"], label="Close Price")
plt.plot(df["DATE"], df["MA20"], label="MA20")
plt.plot(df["DATE"], df["MA50"], label="MA50")

plt.scatter(df[df["Buy"]]["DATE"], df[df["Buy"]]["CLOSE"], marker="^", color="green", label="Buy Signal", s=100)
plt.scatter(df[df["Sell"]]["DATE"], df[df["Sell"]]["CLOSE"], marker="v", color="red", label="Sell Signal", s=100)

plt.title("MA Crossover Buy/Sell Signals")
plt.legend()
plt.grid()
plt.show()
