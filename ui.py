import streamlit as st
import requests
import base64
from datetime import date

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Stock Predictor", layout="wide")

# ===== PREMIUM CSS =====
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #141E30, #243B55);
    color: white;
}

/* Cards */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

/* Button */
.stButton>button {
    background-color: #00c6ff;
    color: black;
    border-radius: 10px;
    font-weight: bold;
}

/* Input */
input {
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ===== TITLE =====
st.markdown("## 📈 AI Stock Prediction Dashboard")

# ===== SEARCH + DATE =====
col1, col2 = st.columns(2)

popular_stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS",
    "HDFCBANK.NS", "ITC.NS", "SBIN.NS",
    "TATASTEEL.NS", "WIPRO.NS"
]

with col1:
    search = st.text_input("🔍 Search Stock")
    ticker = search.upper()

    if ticker:
        filtered = [s for s in popular_stocks if ticker in s]

        if filtered:
            st.caption("Suggestions:")
            for s in filtered:
                if st.button(s):
                    ticker = s

with col2:
    selected_date = st.date_input("📅 Select Date", date.today())

date_str = str(selected_date)

# ===== VALIDATION =====
if ticker == "":
    st.warning("⚠ Please enter a stock ticker")

# ===== BUTTON =====
if st.button("🚀 Predict Now") and ticker != "":

    url = f"http://127.0.0.1:8000/predict?ticker={ticker}&date={date_str}"

    try:
        response = requests.get(url)
        data = response.json()

        st.divider()

        # ===== RESULT =====
        col1, col2, col3 = st.columns(3)

        pred = data["predicted_return"]

        # ===== RETURN + SIGNAL =====
        with col1:
            if pred > 0:
                st.markdown(f"<h3 style='color:green;'>📈 Return: {pred}</h3>", unsafe_allow_html=True)
                st.success("BUY SIGNAL")
            else:
                st.markdown(f"<h3 style='color:red;'>📉 Return: {pred}</h3>", unsafe_allow_html=True)
                st.error("SELL SIGNAL")

        # ===== PRICE =====
        with col2:
            st.metric("💰 Current Price", data.get("current_price"))
            st.metric("🔮 Expected Price", data.get("expected_price"))

        # ===== DATE =====
        with col3:
            st.info(f"📅 Used Date: {data['used_date']}")

        st.divider()

        # ===== GRAPHS =====
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Full History")
            img1 = base64.b64decode(data["graphs"]["full_graph"])
            st.image(img1)

        with col2:
            st.subheader("📊 Recent + Prediction")
            img2 = base64.b64decode(data["graphs"]["recent_graph"])
            st.image(img2)

    except:
        st.error("❌ Error fetching data. Check ticker or server.")