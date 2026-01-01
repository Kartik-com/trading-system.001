# backend/indicators.py
import pandas as pd
import numpy as np

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def calculate_ema(series, period):
    return ema(series, period)

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def stoch_rsi(close, period=14):
    rsi_vals = rsi(close, period)
    min_rsi = rsi_vals.rolling(period).min()
    max_rsi = rsi_vals.rolling(period).max()
    return (rsi_vals - min_rsi) / (max_rsi - min_rsi)

def calculate_atr(df, period=14):
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()
