# ai-trading-assistant
AI-powered trading assistant that analyzes multi-market financial data and generates BUY/SELL signals using technical indicators and interactive candlestick charts.
# 📈 AI Trading Assistant Pro

An AI-powered trading assistant that analyzes financial market data and generates BUY/SELL signals using technical indicators and interactive visualizations.

---

## 🚀 Features

- Multi-market support (US Stocks, Indian Stocks, Forex, Crypto)
- Candlestick charts (Plotly)
- Technical indicators:
  - RSI (Relative Strength Index)
  - SMA (Simple Moving Average)
  - EMA (Exponential Moving Average)
  - MACD (Moving Average Convergence Divergence)
- Volume analysis
- Auto-refresh (live-like tracking)
- Smart ticker detection system

---

## 🧠 How It Works

1. User enters a symbol (e.g., AAPL, RELIANCE, EURUSD, BTC)
2. System detects correct ticker format
3. Fetches historical data using yFinance
4. Calculates indicators using TA library
5. Generates BUY/SELL/HOLD signals
6. Displays interactive charts using Plotly

---

## 🛠️ Tech Stack

- Python
- Streamlit
- yFinance API
- Pandas & NumPy
- TA (Technical Analysis Library)
- Plotly

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py<img width="1920" height="1080" alt="Screenshot (71)" src="https://github.com/user-attachments/assets/4147f282-81c5-431c-84ff-2e22fecce8bb" />
<img width="1920" height="1080" alt="Screenshot (70)" src="https://github.com/user-attachments/assets/4508f6ed-77a2-4f44-97c9-adc242b74466" />
<img width="1920" height="1080" alt="Screenshot (69)" src="https://github.com/user-attachments/assets/063eb8e4-c42f-4f2c-b5e5-bd9d6a8cc5f0" />
<img width="1920" height="1080" alt="Screenshot (68)" src="https://github.com/user-attachments/assets/5d13d27e-e300-40d5-b350-d620bd93743b" />
<img width="1920" height="1080" alt="Screenshot (67)" src="https://github.com/user-attachments/assets/27c323a7-e01b-4bc5-afc3-e34741f71928" />

