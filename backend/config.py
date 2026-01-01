import os

# Exchange
EXCHANGE = "kraken"

# Timeframes
TIMEFRAMES = ["15m", "1h"]

# Symbols
TOP_COINS = 10

# Telegram (ENV ONLY)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Safety
SCAN_INTERVAL_SECONDS = 60
