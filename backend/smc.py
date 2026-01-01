# backend/smc.py

def detect_structure(df):
    highs = df["high"]
    lows = df["low"]

    if highs.iloc[-1] > highs.iloc[-2] and lows.iloc[-1] > lows.iloc[-2]:
        return "BOS"
    if highs.iloc[-1] < highs.iloc[-2] and lows.iloc[-1] < lows.iloc[-2]:
        return "CHoCH"
    return "RANGE"
