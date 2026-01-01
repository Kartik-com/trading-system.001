import time
import ccxt
import pandas as pd
from datetime import datetime, timezone

# ✅ Correct relative imports (IMPORTANT)
from config import (
    EXCHANGE_ID,
    SYMBOLS,
    TIMEFRAMES,
    EMA_FAST,
    EMA_SLOW,
    ATR_PERIOD,
    ATR_MULTIPLIER,
    SCAN_INTERVAL
)
from indicators import calculate_ema, calculate_atr
from alerts import send_alert


# ---------- Exchange ----------
exchange = getattr(ccxt, EXCHANGE_ID)({
    "enableRateLimit": True
})


# ---------- Helpers ----------
def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def fetch_ohlcv(symbol, timeframe, limit=200):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(
        ohlcv,
        columns=["ts", "open", "high", "low", "close", "volume"]
    )
    df["dt"] = pd.to_datetime(df["ts"], unit="ms")
    return df.set_index("dt")


# ---------- Signal Logic ----------
def detect_signal(df):
    df["ema_fast"] = calculate_ema(df["close"], EMA_FAST)
    df["ema_slow"] = calculate_ema(df["close"], EMA_SLOW)
    df["atr"] = calculate_atr(df, ATR_PERIOD)

    last = df.iloc[-1]
    prev = df.iloc[-2]

    signal = None

    # BUY
    if prev["ema_fast"] < prev["ema_slow"] and last["ema_fast"] > last["ema_slow"]:
        signal = "BUY"

    # SELL
    elif prev["ema_fast"] > prev["ema_slow"] and last["ema_fast"] < last["ema_slow"]:
        signal = "SELL"

    return signal, last


# ---------- Main Scanner ----------
def run_scanner():
    print("🚀 Scanner started")
    send_alert("🚀 Scanner started! Telegram link confirmed.")

    while True:
        try:
            for symbol in SYMBOLS:
                for timeframe in TIMEFRAMES:
                    df = fetch_ohlcv(symbol, timeframe)
                    signal, last = detect_signal(df)

                    if signal:
                        price = float(last["close"])
                        atr = float(last["atr"])

                        stop_loss = (
                            price - ATR_MULTIPLIER * atr
                            if signal == "BUY"
                            else price + ATR_MULTIPLIER * atr
                        )

                        message = (
                            f"{'🟢 BUY' if signal == 'BUY' else '🔴 SELL'} SIGNAL — {symbol}\n"
                            f"Timeframe: {timeframe}\n"
                            f"Entry Price: {price:.4f}\n"
                            f"Stop Loss: {stop_loss:.4f}\n"
                            f"Candle Close: {utc_now()} UTC"
                        )

                        send_alert(message)
                        print(message)

            time.sleep(SCAN_INTERVAL)

        except Exception as e:
            print("Scanner error:", e)
            time.sleep(5)
