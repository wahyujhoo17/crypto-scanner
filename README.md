# 🚀 Universal Crypto Market Scanner AI Skill

> **Real-time Binance crypto scanner & technical analysis engine for ANY AI Assistant, Coding Agent, or LLM CLI.**

`crypto-scanner` is a universal AI skill designed to equip **any AI coding agent or assistant** (Claude Code, OpenCode, Cursor, Windsurf, Codex, Aider, custom LLM agents) with real-time crypto technical analysis capabilities. It scans 100+ Binance USDT pairs live to detect high-probability trade setups, Golden Crosses, RSI momentum, and volume breakouts—delivering actionable trade plans complete with calculated **Entry, Take Profit (TP), Stop Loss (SL), and Risk-to-Reward (R:R) ratios**.

---

## 🔥 Key Features & Benefits

- **⚡ Universal Compatibility**: Works seamlessly with any AI agent framework, LLM CLI, or agentic coding environment.
- **📈 Real-Time Binance Data**: Connects directly to Binance public REST APIs (no API key required) to fetch 24h tickers and OHLCV klines across 100+ top USDT pairs.
- **📊 Multi-Timeframe Confluence**: Combines 1H execution signals with 4H macro trend verification to eliminate false breakout traps.
- **🎯 Precision Technical Indicators**:
  - **Moving Averages**: 1H & 4H MA7 vs MA25 Golden Cross & Death Cross detection.
  - **RSI Momentum Filtering**: Pinpoints sweet-spot momentum (RSI 50–68), flags overbought FOMO risk (RSI > 70), and identifies oversold reversal opportunities (4H RSI < 25).
  - **Liquidity Guard**: Automatically filters out low-volume pairs (< $2M 24h volume) to protect against slippage.
- **🛡️ Capital Protection ("WAIT & SEE")**: Explicitly recommends **WAIT & SEE** when market conditions are choppy, low-volume, or ambiguous.
- **🌐 Multilingual Responses**: Adapts output language to match user queries (English, Indonesian, Spanish, etc.) while maintaining strict underlying logic.

---

## 📁 Repository Structure

```text
crypto-scanner/
├── SKILL.md                 # Universal AI agent skill prompt & guidelines
├── README.md                # General skill documentation & setup guide
├── LICENSE                  # MIT License
├── scripts/
│   └── scanner.py           # Core Python market scanner & indicator engine
├── examples/
│   ├── input.md             # Sample user prompts
│   └── expected-output.md   # Sample trade analysis output
└── references/              # Technical analysis & indicator reference material
```

---

## ⚡ Setup & Integration

### For Agent Skill Folders (Claude Code, OpenCode, etc.)

```bash
# General / Universal Skills Directory
git clone https://github.com/wahyujhoo17/crypto-scanner.git ~/.agents/skills/crypto-scanner

# For Claude Code
git clone https://github.com/wahyujhoo17/crypto-scanner.git ~/.claude/skills/crypto-scanner

# For OpenCode
git clone https://github.com/wahyujhoo17/crypto-scanner.git ~/.config/opencode/skills/crypto-scanner
```

### For Standalone Execution / Custom Agents

Run the scanner directly from terminal or integrate into custom Python workflows:

```bash
# Scan full market (Top 100 USDT pairs)
python3 scripts/scanner.py

# Analyze a specific trading pair
python3 scripts/scanner.py ZECUSDT
```

---

## 💡 Usage Examples

Simply prompt your AI assistant naturally:

- *"Scan the crypto market for the best MA crossover setups."*
- *"Cek pasar crypto mana pair yang paling potensial untuk open posisi."*
- *"Analyze ZECUSDT on 1H and 4H timeframes and provide a trade setup."*

---

## 📈 Sample AI Trade Output

```text
Top Scanned Pairs:
1. JTO/USDT - 1H Golden Cross (MA7 > MA25), RSI 1H: 64.2, RSI 4H: 59.8 (High Volume)
2. NEAR/USDT - 1H Bullish Momentum, RSI 1H: 68.1, RSI 4H: 42.5

⭐ Best Momentum Recommendation: JTO/USDT
Fresh 1H Golden Cross confirmed with healthy RSI alignment (no overbought risk) and strong volume support.

Position Suggestion [LONG] (JTO/USDT):
• Entry Range : $0.620 – $0.628
• Take Profit 1: $0.640
• Take Profit 2: $0.655
• Stop Loss   : $0.608 (Below MA25 support)
• Risk:Reward : 1:3.2
```

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for details.

---

⭐ **If you find this skill helpful, give it a star on GitHub!**
