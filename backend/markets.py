# backend/markets.py
import ccxt

def get_top_coins(limit=10):
    exchange = ccxt.binance()
    tickers = exchange.fetch_tickers()
    sorted_pairs = sorted(
        tickers.items(),
        key=lambda x: x[1]["quoteVolume"] or 0,
        reverse=True
    )
    return [pair for pair, _ in sorted_pairs if pair.endswith("/USDT")][:limit]
