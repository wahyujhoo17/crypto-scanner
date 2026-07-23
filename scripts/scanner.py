#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import ssl
import sys

def get_ssl_context():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()

ctx = get_ssl_context()

def get_klines(symbol, interval='1h', limit=50):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        print(f"Binance HTTP error for {symbol}: {error.code}", file=sys.stderr)
        return []
    except urllib.error.URLError as error:
        print(f"Network error for {symbol}: {error.reason}", file=sys.stderr)
        return []
    except json.JSONDecodeError:
        print(f"Invalid JSON response from Binance for {symbol}", file=sys.stderr)
        return []
    except Exception as error:
        print(f"Unexpected error fetching {symbol}: {error}", file=sys.stderr)
        return []

def calculate_wilder_rsi(closes, period=14):
    if len(closes) <= period:
        return 50.0

    changes = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    gains = [max(c, 0) for c in changes]
    losses = [max(-c, 0) for c in changes]

    # Initial SMA for first period
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    # Wilder's Smoothing for remaining data
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 1)

def scan_markets(min_volume=2000000, target_symbol=None):
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            tickers = json.loads(response.read().decode())
    except Exception as error:
        print(f"Failed to fetch market tickers: {error}", file=sys.stderr)
        return []

    if target_symbol:
        pairs = [t for t in tickers if t['symbol'].upper() == target_symbol.upper()]
    else:
        pairs = sorted([t for t in tickers if t['symbol'].endswith('USDT') and float(t['quoteVolume']) >= min_volume],
                       key=lambda x: float(x['quoteVolume']), reverse=True)

    results = []

    for t in pairs[:100]:
        sym = t['symbol']
        raw_k1h = get_klines(sym, '1h', 50)
        raw_k4h = get_klines(sym, '4h', 50)
        
        # Use last closed candles to avoid incomplete active candle distortion
        k1h = raw_k1h[:-1] if len(raw_k1h) > 1 else raw_k1h
        k4h = raw_k4h[:-1] if len(raw_k4h) > 1 else raw_k4h

        if len(k1h) < 30 or len(k4h) < 30:
            continue

        c1 = [float(x[4]) for x in k1h]
        c4 = [float(x[4]) for x in k4h]
        v1 = [float(x[5]) for x in k1h]

        m7_1h_curr, m25_1h_curr = sum(c1[-7:]) / 7, sum(c1[-25:]) / 25
        m7_1h_prev, m25_1h_prev = sum(c1[-8:-1]) / 7, sum(c1[-26:-1]) / 25

        m7_4h_curr, m25_4h_curr = sum(c4[-7:]) / 7, sum(c4[-25:]) / 25
        m7_4h_prev, m25_4h_prev = sum(c4[-8:-1]) / 7, sum(c4[-26:-1]) / 25

        # Wilder's RSI Calculation on closed candles
        rsi1 = calculate_wilder_rsi(c1)
        rsi4 = calculate_wilder_rsi(c4)

        # Volume Ratio Calculation (comparing last closed candle to 20-candle MA)
        avg_vol_20 = sum(v1[-21:-1]) / 20 if len(v1) >= 21 else sum(v1[:-1]) / max(len(v1[:-1]), 1)
        vol_ratio = round(v1[-1] / avg_vol_20, 2) if avg_vol_20 > 0 else 0.0
        volume_spike = vol_ratio >= 1.5

        cross_1h_bull = (m7_1h_prev <= m25_1h_prev and m7_1h_curr > m25_1h_curr)
        cross_1h_bear = (m7_1h_prev >= m25_1h_prev and m7_1h_curr < m25_1h_curr)
        cross_4h_bull = (m7_4h_prev <= m25_4h_prev and m7_4h_curr > m25_4h_curr)

        high_24h = max([float(x[2]) for x in k1h[-24:]])
        low_24h = min([float(x[3]) for x in k1h[-24:]])
        curr_price = c1[-1]

        # Calculate TP, SL, and Risk:Reward Validation
        tp1 = round(high_24h, 4)
        tp2 = round(high_24h * 1.025, 4)
        sl = round(max(low_24h, m25_1h_curr * 0.99), 4) if low_24h < curr_price else round(curr_price * 0.98, 4)

        # Ensure SL is strictly below current price
        if sl >= curr_price:
            sl = round(curr_price * 0.98, 4)

        risk = round(curr_price - sl, 4)
        reward_tp1 = round(tp1 - curr_price, 4)
        reward_tp2 = round(tp2 - curr_price, 4)

        rr_tp1 = round(reward_tp1 / risk, 2) if risk > 0 else 0.0
        rr_tp2 = round(reward_tp2 / risk, 2) if risk > 0 else 0.0

        # Enforce 4H Trend Alignment + 1H Golden Cross / Bullish RSI
        valid_long = (
            tp1 > curr_price and
            sl < curr_price and
            risk > 0 and
            rr_tp1 >= 1.5 and
            m7_4h_curr > m25_4h_curr and
            45 <= rsi1 <= 68 and
            (cross_1h_bull or m7_1h_curr > m25_1h_curr)
        )

        entry_low = round(min(m7_1h_curr, curr_price), 4)
        entry_high = round(max(m7_1h_curr, curr_price), 4)

        results.append({
            'symbol': sym,
            'price': curr_price,
            'high_24h': high_24h,
            'low_24h': low_24h,
            'rsi_1h': rsi1,
            'rsi_4h': rsi4,
            'volume_ratio': vol_ratio,
            'volume_spike': volume_spike,
            'cross_1h_bull': cross_1h_bull,
            'cross_1h_bear': cross_1h_bear,
            'cross_4h_bull': cross_4h_bull,
            'm7_gt_m25_1h': m7_1h_curr > m25_1h_curr,
            'm7_gt_m25_4h': m7_4h_curr > m25_4h_curr,
            'volume_24h': float(t['quoteVolume']),
            'valid_long': valid_long,
            'setup': {
                'entry_range': f"${entry_low} - ${entry_high}",
                'tp1': tp1,
                'tp2': tp2,
                'sl': sl,
                'risk': risk,
                'reward_tp1': reward_tp1,
                'reward_tp2': reward_tp2,
                'rr_tp1': rr_tp1,
                'rr_tp2': rr_tp2
            } if valid_long else None
        })

    return results

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else None
    res = scan_markets(target_symbol=target)
    print(json.dumps(res, indent=2))
