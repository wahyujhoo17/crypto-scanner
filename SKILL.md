---
name: crypto-scanner
description: >
  Scan Binance crypto markets for MA7/MA25 crossovers (Golden Cross / Death Cross), RSI momentum, volume spikes,
  and support/resistance levels. Generates trade setups with precise Entry, TP1, TP2, SL, and Risk:Reward ratio.
  Use when user asks to scan crypto markets, check pair technical analysis, look for MA crossovers, or evaluate trading setups.
---

Perform crypto market scanning and multi-timeframe technical analysis using Binance public API.

## Workflow

1. **Execute Market Scanner Script**:
   Run the Python script at `scripts/scanner.py` (or full path `~/.config/opencode/skills/crypto-scanner/scripts/scanner.py`):
   - Full market scan: `python3 scripts/scanner.py`
   - Single pair scan: `python3 scripts/scanner.py <SYMBOL>` (e.g. `python3 scripts/scanner.py ZECUSDT`)

2. **Technical Evaluation Criteria**:
   - **Crossover Trigger**: MA7 crosses above MA25 (Golden Cross) or below MA25 (Death Cross) on 1H timeframe.
   - **Trend Confirmation**: Check 4H MA7 vs MA25 trend alignment and structure.
   - **RSI Momentum Guidelines**:
     - Optimal Long: 1H RSI between 50 - 68 (active momentum, not overbought).
     - Overbought Risk: 1H RSI > 70 (do not FOMO at local peaks).
     - Oversold Bounce: 4H RSI < 25 with 1H bullish reversal confirmation.
   - **Volume Verification**: 24h volume must be > $2,000,000 USDT to avoid low liquidity slippage.

3. **Output Response Structure (Match User's Language)**:
   Always respond in the user's language (Indonesian, English, etc.) and structure the response as follows:

   - **Best Scanned Pairs List**: Present top 2-3 scanned pairs matching technical criteria.
   - **Best Momentum Coin Recommendation**:
     - *If valid trade setup exists*:
       **Best Momentum Coin**: `PAIR` (Brief rationale: MA cross, RSI 1H/4H status, volume spike).
       **Position Suggestion [LONG/SHORT] (PAIR)**:
       - **Entry**: $ENTRY_RANGE
       - **TP 1**: $PRICE | **TP 2**: $PRICE
       - **Stop Loss (SL)**: $PRICE (below/above key support or resistance)
     - *If NO strong/safe setup exists*:
       State clearly in user's language: "Currently no pairs meet the ideal criteria for opening a position. Recommended to **WAIT & SEE** because [reason: e.g. market sideways / low volume / extreme RSI without confirmation]."
