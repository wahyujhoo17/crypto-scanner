# 🚀 Crypto Market Scanner Skill for Claude Code & OpenCode

> **Instant technical analysis and real-time Binance market scanning directly inside your AI coding assistant.**

`crypto-scanner` is an autonomous AI agent skill designed for **Claude Code**, **OpenCode**, and compatible LLM CLI tools. It scans 100+ Binance USDT pairs in real-time to detect high-probability technical setups, Golden Crosses, RSI momentum divergences, and volume breakouts—delivering actionable trade plans with calculated **Entry, Take Profits (TP), Stop Losses (SL), and Risk-to-Reward ratios**.

---

## 🔥 Key Benefits & Features

- **⚡ Real-Time Binance Data**: Queries live 24h ticker and candle data across 100+ top-volume USDT pairs using Binance's public REST API (no API key required).
- **📊 Multi-Timeframe Confluence**: Analyzes 1H execution candles alongside 4H macro trend alignment to eliminate false breakout traps.
- **🎯 Precise Technical Indicators**:
  - **Moving Averages**: 1H & 4H MA7 / MA25 crossover detection (Golden Cross & Death Cross).
  - **RSI Momentum Scoring**: Filters out overbought (RSI > 70) FOMO entries while identifying sweet-spot momentum (RSI 50–68) and oversold bounces (4H RSI < 25).
  - **Liquidity Filter**: Excludes low-volume pairs (< $2M 24h volume) to protect against slippage.
- **🛡️ Capital Preservation First ("WAIT & SEE")**: Unlike generic bots that force trades, this skill explicitly advises **WAIT & SEE** when market conditions are choppy, low-volume, or unsafe.
- **🌐 Multilingual Output**: Automatically responds in your spoken language (English, Indonesian, Spanish, etc.) while executing prompt logic in high-precision English.

---

## 📁 Repository Structure

```text
crypto-scanner/
├── SKILL.md                 # Main agent skill instructions & workflow
├── README.md                # Skill documentation & installation guide
├── LICENSE                  # MIT License
├── scripts/
│   └── scanner.py           # Core Python market scanner & indicator engine
├── examples/
│   ├── input.md             # Example prompt queries
│   └── expected-output.md   # Sample AI trade analysis output
└── references/              # Technical indicator reference documentation
```

---

## ⚡ Quick Installation

### Option 1: For Claude Code (`~/.claude/skills/`)

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/wahyujhoo17/crypto-scanner.git ~/.claude/skills/crypto-scanner
```

### Option 2: For OpenCode (`~/.config/opencode/skills/`)

```bash
mkdir -p ~/.config/opencode/skills
git clone https://github.com/wahyujhoo17/crypto-scanner.git ~/.config/opencode/skills/crypto-scanner
```

---

## 💡 How to Use

Simply ask your AI assistant naturally in CLI mode:

### 1. Scan Full Market
> *"Scan Binance crypto market for the best MA crossover setups."*  
> *"Cek market crypto mana pair yang sedang bagus untuk open posisi."*

### 2. Analyze Specific Coin
> *"Analyze ZECUSDT on 1H and 4H timeframes and provide a trade setup."*  
> *"Bagaimana kondisi teknikal KAITOUSDT saat ini?"*

---

## 📈 Example Output

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

Distributed under the **MIT License**. See `LICENSE` for more details.

---

⭐ **If you find this skill helpful, give it a star on GitHub!**
