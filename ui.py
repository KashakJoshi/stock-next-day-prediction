import streamlit as st
import requests
import base64

st.title("📈 Stock Prediction App")

# ===== INPUT =====
ticker = st.text_input("Enter Stock Ticker", "RELIANCE.NS")
date = st.text_input("Enter Date (YYYY-MM-DD)", "2025-01-10")

# ===== BUTTON =====
if st.button("Predict"):

    url = f"http://127.0.0.1:8000/predict?ticker={ticker}&date={date}"
    response = requests.get(url)
    data = response.json()

    # ===== RESULT =====
    st.subheader("Prediction Result")

    pred = data["predicted_return"]

    # 🎨 Colored Return
    if pred > 0:
        st.markdown(f"### 🟢 Predicted Return: `{pred}`")
    else:
        st.markdown(f"### 🔴 Predicted Return: `{pred}`")

    # 🎯 SIGNAL
    if pred > 0:
        st.success("📈 UP Signal (Buy)")
    else:
        st.error("📉 DOWN Signal (Sell)")

    # 📅 Date
    st.write("📅 Used Date:", data["used_date"])

    # 💰 Prices
    st.write("💰 Current Price:", data["current_price"])
    st.write("🔮 Expected Price:", data["expected_price"])

    # ===== GRAPHS =====
    st.subheader("📊 Full History Graph")
    img1 = base64.b64decode(data["graphs"]["full_graph"])
    st.image(img1)

    st.subheader("📊 Recent + Prediction Graph")
    img2 = base64.b64decode(data["graphs"]["recent_graph"])
    st.image(img2)