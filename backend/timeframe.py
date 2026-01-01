# backend/timeframe.py
from datetime import datetime

def is_candle_closed(tf_minutes):
    now = datetime.utcnow()
    return now.minute % tf_minutes == 0
