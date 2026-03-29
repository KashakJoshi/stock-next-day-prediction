import streamlit as st
import requests
import base64

st.title("📈 Stock Prediction App")

ticker = st.text_input("Enter Stock Ticker", "RELIANCE.NS")
date = st.text_input("Enter Date (YYYY-MM-DD)", "2025-01-10")

if st.button("Predict"):

    url = f"http://127.0.0.1:8000/predict?ticker={ticker}&date={date}"
    response = requests.get(url)
    data = response.json()

    st.subheader("Prediction Result")
    st.write("Predicted Return:", data["predicted_return"])
    st.write("Used Date:", data["used_date"])

    # ===== SHOW GRAPHS =====
    st.subheader("📊 Full History Graph")
    img1 = base64.b64decode(data["graphs"]["full_graph"])
    st.image(img1)

    st.subheader("📊 Recent + Prediction Graph")
    img2 = base64.b64decode(data["graphs"]["recent_graph"])
    st.image(img2)