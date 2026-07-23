#!/usr/bin/env python3
import urllib.request
import json
import ssl
import sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_klines(symbol, interval='1h', limit=50):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        res = urllib.request.urlopen(req, context=ctx)
        return json.loads(res.read().decode())
    except:
        return []

def calculate_rsi(closes, period=14):
    if len(closes) <= period:
        return 50.0
    gains = [max(closes[i] - closes[i-1], 0) for i in range(1, len(closes))]
    losses = [max(closes[i-1] - closes[i], 0) for i in range(1, len(closes))]
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100.0
    return round(100 - (100 / (1 + (avg_gain / avg_loss))), 1)

def scan_markets(min_volume=2000000, target_symbol=None):
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req, context=ctx)
    tickers = json.loads(res.read().decode())

    if target_symbol:
        pairs = [t for t in tickers if t['symbol'].upper() == target_symbol.upper()]
    else:
        pairs = sorted([t for t in tickers if t['symbol'].endswith('USDT') and float(t['quoteVolume']) >= min_volume],
                       key=lambda x: float(x['quoteVolume']), reverse=True)

    results = []

    for t in pairs[:100]:
        sym = t['symbol']
        k1h = get_klines(sym, '1h', 50)
        k4h = get_klines(sym, '4h', 50)
        
        if len(k1h) < 30 or len(k4h) < 30:
            continue

        c1 = [float(x[4]) for x in k1h]
        c4 = [float(x[4]) for x in k4h]
        h1 = [float(x[2]) for x in k1h]
        l1 = [float(x[3]) for x in k1h]

        m7_1h_curr, m25_1h_curr = sum(c1[-7:]) / 7, sum(c1[-25:]) / 25
        m7_1h_prev, m25_1h_prev = sum(c1[-8:-1]) / 7, sum(c1[-26:-1]) / 25

        m7_4h_curr, m25_4h_curr = sum(c4[-7:]) / 7, sum(c4[-25:]) / 25
        m7_4h_prev, m25_4h_prev = sum(c4[-8:-1]) / 7, sum(c4[-26:-1]) / 25

        rsi1 = calculate_rsi(c1)
        rsi4 = calculate_rsi(c4)

        cross_1h_bull = (m7_1h_prev <= m25_1h_prev and m7_1h_curr > m25_1h_curr)
        cross_1h_bear = (m7_1h_prev >= m25_1h_prev and m7_1h_curr < m25_1h_curr)
        cross_4h_bull = (m7_4h_prev <= m25_4h_prev and m7_4h_curr > m25_4h_curr)

        high_24h = max([float(x[2]) for x in k1h[-24:]])
        low_24h = min([float(x[3]) for x in k1h[-24:]])
        curr_price = c1[-1]

        # Calculate trade setup levels if bullish momentum
        tp1 = round(high_24h, 4)
        tp2 = round(high_24h * 1.025, 4)
        sl = round(min(low_24h, m25_1h_curr * 0.99), 4)

        results.append({
            'symbol': sym,
            'price': curr_price,
            'high_24h': high_24h,
            'low_24h': low_24h,
            'rsi_1h': rsi1,
            'rsi_4h': rsi4,
            'cross_1h_bull': cross_1h_bull,
            'cross_1h_bear': cross_1h_bear,
            'cross_4h_bull': cross_4h_bull,
            'm7_gt_m25_1h': m7_1h_curr > m25_1h_curr,
            'm7_gt_m25_4h': m7_4h_curr > m25_4h_curr,
            'volume_24h': float(t['quoteVolume']),
            'setup': {
                'entry_range': f"${round(m7_1h_curr, 4)} - ${curr_price}",
                'tp1': tp1,
                'tp2': tp2,
                'sl': sl
            }
        })

    return results

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else None
    res = scan_markets(target_symbol=target)
    print(json.dumps(res, indent=2))
