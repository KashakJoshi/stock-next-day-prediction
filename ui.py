import streamlit as st
import requests
import base64
from datetime import date

# ===== CONFIG =====
st.set_page_config(page_title="Stock AI", layout="wide")

# ===== NEW LIGHT PREMIUM THEME =====
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(120deg, #f8fafc, #e0f2fe);
    color: #0f172a;
}

/* HEADER */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
}
.subtitle {
    text-align: center;
    color: #475569;
    margin-bottom: 30px;
}

/* INPUT */
input {
    text-transform: uppercase;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    color: white;
    border-radius: 12px;
    height: 45px;
    font-weight: 600;
}

/* CARD */
.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    text-align: center;
}

/* GREEN */
.green {
    border-left: 6px solid #10b981;
}

/* RED */
.red {
    border-left: 6px solid #ef4444;
}

/* TEXT */
.big {
    font-size: 32px;
    font-weight: 700;
}
.small {
    color: #64748b;
}

/* SECTION */
.section {
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown("<div class='title'>🚀 Smart Stock AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-powered stock prediction dashboard</div>", unsafe_allow_html=True)

# ===== DATE LIMIT =====
TODAY = date.today()
MIN_DATE = date(2020, 1, 1)

# ===== INPUT =====
col1, col2 = st.columns([2,1])

with col1:
    search = st.text_input("🔍 Enter Stock (RELIANCE, TCS, MRF)")
    ticker = search.upper()
    if ticker and not ticker.endswith(".NS"):
        ticker += ".NS"

with col2:
    selected_date = st.date_input(
        "📅 Select Date",
        value=TODAY,
        min_value=MIN_DATE,
        max_value=TODAY
    )

date_str = str(selected_date)

# ===== BUTTON =====
if st.button("Predict"):

    if ticker == "":
        st.warning("Enter stock ticker")
    else:

        url = f"http://127.0.0.1:8000/predict?ticker={ticker}&date={date_str}"

        with st.spinner("Analyzing data..."):

            try:
                res = requests.get(url)
                data = res.json()

                pred = data["predicted_return"]
                percent = pred * 100
                confidence = abs(pred)

                current_price = data.get("current_price", 0)
                expected_price = data.get("expected_price", 0)

                # SIGNAL
                if pred > 0:
                    color = "green"
                    signal = "BUY 📈"
                else:
                    color = "red"
                    signal = "SELL 📉"

                st.markdown("<div class='section'></div>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)

                # ===== SIGNAL CARD =====
                with col1:
                    st.markdown(f"""
                    <div class="card {color}">
                        <div class="small">Signal</div>
                        <div class="big">{signal}</div>
                        <div class="small">{round(percent,3)}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                # ===== PRICE CARD =====
                with col2:
                    st.markdown(f"""
                    <div class="card">
                        <div class="small">Current Price</div>
                        <div class="big">₹ {round(current_price,2)}</div>
                        <div class="small">Expected: ₹ {round(expected_price,2)}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # ===== CONFIDENCE CARD =====
                with col3:
                    st.markdown(f"""
                    <div class="card">
                        <div class="small">Confidence</div>
                        <div class="big">{round(confidence,6)}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.progress(min(confidence * 100, 100))

                st.markdown("<div class='section'></div>", unsafe_allow_html=True)

                # ===== GRAPHS =====
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 📊 Market History")
                    img1 = base64.b64decode(data["graphs"]["full_graph"])
                    st.image(img1)

                with col2:
                    st.markdown("### 📊 Prediction Trend")
                    img2 = base64.b64decode(data["graphs"]["recent_graph"])
                    st.image(img2)

            except:
                st.error("Error fetching data")