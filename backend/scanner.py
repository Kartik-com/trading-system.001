# backend/scanner.py
import ccxt
import pandas as pd
from config import *
from indicators import ema, stoch_rsi
from smc import detect_structure
from timeframe import is_candle_closed
from alerts import send_alert
from models import Signal

exchange = getattr(ccxt, EXCHANGE)()

def analyze(symbol, timeframe):
    df = pd.DataFrame(
        exchange.fetch_ohlcv(symbol, timeframe, limit=200),
        columns=["ts","open","high","low","close","volume"]
    )

    df["ema20"] = ema(df["close"], 20)
    df["ema50"] = ema(df["close"], 50)
    df["ema200"] = ema(df["close"], 200)
    df["stoch"] = stoch_rsi(df["close"])

    structure = detect_structure(df)

    last = df.iloc[-1]

    if last["close"] > last["ema200"] and structure == "BOS":
        direction = "BUY"
    elif last["close"] < last["ema200"] and structure == "CHoCH":
        direction = "SELL"
    else:
        return None

    sl = last["low"] if direction == "BUY" else last["high"]

    signal = Signal(
        symbol=symbol,
        timeframe=timeframe,
        direction=direction,
        entry=last["close"],
        stop_loss=sl,
        confidence="HIGH",
        structure=structure,
        candle_close=str(pd.to_datetime(last["ts"], unit="ms"))
    )

    return signal

def run_scanner():
    while True:
        for tf in TIMEFRAMES:
            tf_minutes = int(tf.replace("m","").replace("h","")) * (60 if "h" in tf else 1)
            if not is_candle_closed(tf_minutes):
                continue

            for symbol in SYMBOLS:
                try:
                    signal = analyze(symbol, tf)
                    if signal:
                        msg = (
                            f"{'🟢 BUY' if signal.direction=='BUY' else '🔴 SELL'} SIGNAL — {signal.symbol}\n"
                            f"Timeframe: {signal.timeframe}\n"
                            f"Structure: {signal.structure}\n"
                            f"Entry: {signal.entry}\n"
                            f"Stop Loss: {signal.stop_loss}\n"
                            f"Confidence: {signal.confidence}\n"
                            f"Candle Close: {signal.candle_close}"
                        )
                        send_alert(msg)
                except Exception as e:
                    print("Error:", e)
