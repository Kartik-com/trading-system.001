import os

# Exchange
EXCHANGE_ID = "kraken"

# Strategy Parameters
EMA_FAST = 20
EMA_SLOW = 50
ATR_PERIOD = 14
ATR_MULTIPLIER = 2.0

# Timeframes
TIMEFRAMES = ["15m", "1h"]

# Symbols
SYMBOLS = ["BTC/USDT", "ETH/USDT"]
TOP_COINS = 10

# Telegram (ENV ONLY)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Safety
SCAN_INTERVAL = 60
