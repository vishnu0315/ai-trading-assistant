import streamlit as st
import yfinance as yf
import pandas as pd
import time

from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, EMAIndicator, MACD
import plotly.graph_objects as go

# --------------------------
# CONFIG
# --------------------------
st.set_page_config(page_title="AI Trading Assistant Pro", layout="wide")
st.title("📈 AI Trading Assistant Pro (Stable Version)")

# --------------------------
# SIDEBAR
# --------------------------
st.sidebar.header("⚙️ Settings")

market = st.sidebar.selectbox(
    "Select Market",
    ["Auto Detect", "US Stock", "Indian Stock", "Forex", "Crypto"]
)

symbol = st.sidebar.text_input("Enter Symbol", "AAPL").upper().strip()

refresh_rate = st.sidebar.slider("Auto Refresh (seconds)", 5, 60, 10)

# --------------------------
# SMART TICKER GENERATION
# --------------------------
def generate_ticker_variants(symbol, market):
    symbol = symbol.upper().strip()

    if market == "US Stock":
        return [symbol]

    elif market == "Indian Stock":
        return [f"{symbol}.NS", f"{symbol}.BO"]

    elif market == "Forex":
        return [f"{symbol}=X"]

    elif market == "Crypto":
        return [f"{symbol}-USD"]

    # AUTO DETECT (SAFE ORDER)
    variants = []

    # 1. Try as US stock
    variants.append(symbol)

    # 2. Forex (EURUSD → EURUSD=X)
    if len(symbol) == 6 and symbol.isalpha():
        variants.append(f"{symbol}=X")

    # 3. Crypto (BTC → BTC-USD)
    if len(symbol) <= 5:
        variants.append(f"{symbol}-USD")

    # 4. Indian stocks
    if len(symbol) <= 10:
        variants.append(f"{symbol}.NS")
        variants.append(f"{symbol}.BO")

    return variants


# --------------------------
# FETCH DATA
# --------------------------
@st.cache_data
def fetch_data(symbol, market):
    variants = generate_ticker_variants(symbol, market)

    for ticker in variants:
        try:
            data = yf.download(ticker, period="6mo", interval="1d")

            # Fix multi-index issue
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            if not data.empty and "Close" in data.columns:
                return data, ticker

        except:
            continue

    return None, None


data, used_ticker = fetch_data(symbol, market)

# --------------------------
# ERROR HANDLING
# --------------------------
if data is None:
    st.error("❌ No data found. Try: AAPL, RELIANCE, EURUSD, BTC")
    st.stop()

st.success(f"✅ Using ticker: {used_ticker}")

# --------------------------
# INDICATORS
# --------------------------
try:
    data["Close"] = data["Close"].astype(float)

    data["RSI"] = RSIIndicator(data["Close"]).rsi()
    data["SMA_20"] = SMAIndicator(data["Close"], window=20).sma_indicator()
    data["EMA_20"] = EMAIndicator(data["Close"], window=20).ema_indicator()

    macd = MACD(data["Close"])
    data["MACD"] = macd.macd()
    data["MACD_SIGNAL"] = macd.macd_signal()

except Exception as e:
    st.error(f"Indicator Error: {e}")
    st.stop()

latest = data.iloc[-1]

# --------------------------
# SIGNAL LOGIC
# --------------------------
signal = "HOLD"

if latest["RSI"] < 30:
    signal = "BUY"
elif latest["RSI"] > 70:
    signal = "SELL"

# --------------------------
# METRICS
# --------------------------
st.subheader(f"📊 {used_ticker} Analysis")

col1, col2, col3 = st.columns(3)
col1.metric("Price", f"{latest['Close']:.2f}")
col2.metric("RSI", f"{latest['RSI']:.2f}")
col3.metric("Signal", signal)

# --------------------------
# CANDLESTICK CHART
# --------------------------
st.write("### 🕯️ Candlestick Chart")

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=data.index,
    open=data["Open"],
    high=data["High"],
    low=data["Low"],
    close=data["Close"],
    name="Candles"
))

fig.add_trace(go.Scatter(x=data.index, y=data["SMA_20"], name="SMA 20"))
fig.add_trace(go.Scatter(x=data.index, y=data["EMA_20"], name="EMA 20"))

fig.update_layout(xaxis_rangeslider_visible=False)

st.plotly_chart(fig, use_container_width=True)

# --------------------------
# VOLUME
# --------------------------
st.write("### 📊 Volume")

vol_fig = go.Figure()
vol_fig.add_trace(go.Bar(x=data.index, y=data["Volume"], name="Volume"))

st.plotly_chart(vol_fig, use_container_width=True)

# --------------------------
# RSI
# --------------------------
st.write("### 📉 RSI")

rsi_fig = go.Figure()
rsi_fig.add_trace(go.Scatter(x=data.index, y=data["RSI"], name="RSI"))
rsi_fig.add_hline(y=70)
rsi_fig.add_hline(y=30)

st.plotly_chart(rsi_fig, use_container_width=True)

# --------------------------
# MACD
# --------------------------
st.write("### 📊 MACD")

macd_fig = go.Figure()
macd_fig.add_trace(go.Scatter(x=data.index, y=data["MACD"], name="MACD"))
macd_fig.add_trace(go.Scatter(x=data.index, y=data["MACD_SIGNAL"], name="Signal"))

st.plotly_chart(macd_fig, use_container_width=True)

# --------------------------
# STRATEGY
# --------------------------
st.write("### 🧠 Strategy")
st.write("""
- RSI < 30 → BUY (Oversold)  
- RSI > 70 → SELL (Overbought)  
- SMA & EMA → Trend direction  
- MACD → Momentum confirmation  
""")

# --------------------------
# RAW DATA
# --------------------------
with st.expander("🔍 Show Raw Data"):
    st.write(data.tail())

# --------------------------
# AUTO REFRESH (LIVE EFFECT)
# --------------------------
time.sleep(refresh_rate)
st.rerun()