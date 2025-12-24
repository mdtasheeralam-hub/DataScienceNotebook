import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# 1. Load & Clean Data
# -------------------------
df = pd.read_csv("Coforge1.csv")
df["DATE"] = pd.to_datetime(df["DATE"])
df["CLOSE"] = df["CLOSE"].astype(str).str.replace(",", "").astype(float)

df = df.sort_values("DATE")
df.set_index("DATE", inplace=True)

# -------------------------
# 2. Statistical Window
# -------------------------
window = 20   # 20-day statistical range
k = 2         # 2 standard deviations

mean = df["CLOSE"].rolling(window).mean()
std = df["CLOSE"].rolling(window).std()

upper_band = mean + k * std
lower_band = mean - k * std

# -------------------------
# 3. Plot Statistical Bands
# -------------------------
plt.figure(figsize=(12,6))
plt.plot(df.index, df["CLOSE"], label="Close Price")
plt.plot(mean.index, mean, label="Mean (20-day)")
plt.plot(upper_band.index, upper_band, label="Upper Band (μ + 2σ)")
plt.plot(lower_band.index, lower_band, label="Lower Band (μ − 2σ)")

plt.title("Coforge Statistical Price Range (Mean ± 2σ)")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# -------------------------
# 4. Latest Statistical Levels
# -------------------------
print("Latest Mean:", round(mean.dropna().iloc[-1], 2))
print("Upper Range:", round(upper_band.dropna().iloc[-1], 2))
print("Lower Range:", round(lower_band.dropna().iloc[-1], 2))
