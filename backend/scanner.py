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
    start_msg = (
        f"🚀 **Scanner started!**\n"
        f"Exchange: {EXCHANGE_ID.upper()}\n"
        f"Symbols: {', '.join(SYMBOLS)}\n"
        f"Timeframes: {', '.join(TIMEFRAMES)}\n"
        f"Interval: {SCAN_INTERVAL}s"
    )
    print(start_msg.replace("**", "")) # Print without markdown for console
    send_alert(start_msg)

    # For heartbeat track
    last_heartbeat = time.time()
    heartbeat_interval = 4 * 3600 # 4 hours

    while True:
        try:
            current_time = time.time()
            
            # Periodic Heartbeat
            if current_time - last_heartbeat >= heartbeat_interval:
                send_alert(f"💓 **Heartbeat**: Scanner is active and monitoring {len(SYMBOLS)} symbols.")
                last_heartbeat = current_time

            for symbol in SYMBOLS:
                for timeframe in TIMEFRAMES:
                    print(f"🔍 [{utc_now()}] Scanning {symbol} on {timeframe}...")
                    df = fetch_ohlcv(symbol, timeframe)
                    
                    if df.empty or len(df) < 2:
                        continue
                        
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
                        print("✅", message.replace("\n", " "))

            time.sleep(SCAN_INTERVAL)

        except Exception as e:
            error_msg = f"❌ Scanner error: {e}"
            print(error_msg)
            # Only send persistent errors? Let's just log for now to avoid spam
            time.sleep(10)
