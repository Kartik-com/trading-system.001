import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_alert(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠ Telegram not configured")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Telegram error:", e)
