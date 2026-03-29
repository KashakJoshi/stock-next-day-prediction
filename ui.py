import streamlit as st
import requests
import base64
from datetime import date

# ===== CONFIG =====
st.set_page_config(page_title="AI Stock Predictor", layout="wide")

# ===== CSS (SUPER ATTRACTIVE) =====
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg,
        #020617 0%,
        #020c1b 30%,
        #041a3b 70%,
        #020617 100%
    );
    color: #ffffff;
}

/* Glass cards */
.card {
    background: rgba(255,255,255,0.06);
    padding: 20px;
    border-radius: 16px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

/* Title */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 12px;
    font-size: 18px;
    height: 3em;
    width: 100%;
}

/* Input uppercase */
input {
    text-transform: uppercase;
}

/* Divider */
hr {
    border: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown("<div class='title'>📊 AI Stock Market Predictor 🚀</div>", unsafe_allow_html=True)
st.caption("📈 Predict next-day movement using Machine Learning")

# ===== DATE LIMIT (IMPORTANT FIX) =====
TODAY = date.today()
MIN_DATE = date(2020, 1, 1)   # data available start

# ===== INPUT SECTION =====
col1, col2 = st.columns(2)

with col1:
    search = st.text_input("🔍 Enter Stock (e.g. RELIANCE, TCS, MRF)")
    ticker = search.upper()

    if ticker and not ticker.endswith(".NS"):
        ticker = ticker + ".NS"

    st.caption("💡 NSE format auto-applied (.NS)")

with col2:
    selected_date = st.date_input(
        "📅 Select Date",
        value=TODAY,
        min_value=MIN_DATE,
        max_value=TODAY   # ❌ future disabled
    )

date_str = str(selected_date)

# ===== BUTTON =====
if st.button("🚀 Predict Now"):

    if ticker == "":
        st.warning("⚠ Enter stock ticker first")
    else:

        url = f"http://127.0.0.1:8000/predict?ticker={ticker}&date={date_str}"

        with st.spinner("🔄 Analyzing market patterns..."):

            try:
                response = requests.get(url)
                data = response.json()

                st.markdown("<hr>", unsafe_allow_html=True)

                pred = data["predicted_return"]
                confidence = abs(pred)

                # ===== RESULT SECTION =====
                col1, col2, col3 = st.columns(3)

                # ===== RETURN =====
                with col1:
                    if pred > 0:
                        st.markdown(f"### 📈 Return\n<span style='color:lightgreen;font-size:28px;'>{round(pred,6)}</span>", unsafe_allow_html=True)
                        st.success("BUY SIGNAL 🚀")
                    else:
                        st.markdown(f"### 📉 Return\n<span style='color:red;font-size:28px;'>{round(pred,6)}</span>", unsafe_allow_html=True)
                        st.error("SELL SIGNAL ⚠")

                # ===== PRICES =====
                with col2:
                    st.markdown("###  Prices")
                    st.metric("Current Price", round(data.get("current_price", 0),2))
                    st.metric("Expected Price", round(data.get("expected_price", 0),2))

                # ===== META =====
                with col3:
                    st.markdown("### 📊 Info")
                    st.info(f"📅 Used Date: {data['used_date']}")
                    st.metric("Confidence", round(confidence,6))

                st.markdown("<hr>", unsafe_allow_html=True)

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
                st.error("❌ Server error or invalid stock symbol")