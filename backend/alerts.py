# backend/alerts.py
import requests
from backend.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_alert(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, json=payload, timeout=10)
