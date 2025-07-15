# app.py

import streamlit as st
import datetime
import random
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ------------- Mock Prediction -------------
def predict_waste(image):
    waste_types = ["Plastic Bottle", "Food Wrapper", "Battery", "Aluminum Can", "Paper", "E-Waste"]
    return random.choice(waste_types)

# ------------- Eco Tips -------------
tips = {
    "Plastic Bottle": "Try using a reusable bottle instead of single-use plastics.",
    "Food Wrapper": "Buy in bulk or use cloth packaging to reduce wrapper waste.",
    "Battery": "Switch to rechargeable batteries to reduce hazardous waste.",
    "Aluminum Can": "Recycle aluminum — it saves 95% of energy vs new production.",
    "Paper": "Avoid unnecessary printing. Go digital!",
    "E-Waste": "Donate or recycle electronics through certified e-waste centers."
}

def get_tip(waste_type):
    return tips.get(waste_type, "Be mindful of your waste and dispose responsibly!")

# ------------- App UI -------------
st.set_page_config(page_title="EcoSnap+", page_icon="♻️")
st.title("♻️ EcoSnap+ — Smart Waste Scanner & Tracker")

# File uploader
uploaded_file = st.file_uploader("📸 Upload a waste image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    # Predict waste type (mock)
    predicted_type = predict_waste(uploaded_file)
    st.success(f"🧠 Detected Waste Type: **{predicted_type}**")

    # Show eco tip
    tip = get_tip(predicted_type)
    st.info(f"🌱 Tip: {tip}")

    # Log the result
    log_path = Path("data/waste_log.txt")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with open(log_path, "a") as log:
        log.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {predicted_type}\n")

# ------------- Dashboard -------------
st.header("📈 Your Weekly Waste Dashboard")

log_path = Path("data/waste_log.txt")
if log_path.exists():
    log_data = []
    with open(log_path, "r") as log:
        for line in log:
            if "-" in line:
                try:
                    timestamp, item = line.strip().split(" - ")
                    log_data.append(item)
                except:
                    continue

    if log_data:
        df = pd.DataFrame(log_data, columns=["Waste Type"])
        waste_counts = df["Waste Type"].value_counts()

        # Show bar chart
        st.subheader("🧾 Waste Type Breakdown")
        st.bar_chart(waste_counts)

        # EcoScore
        harmful_items = ["Plastic Bottle", "Food Wrapper", "Battery", "E-Waste"]
        harm_count = sum(df["Waste Type"].isin(harmful_items))
        total = len(df)
        score = max(0, 100 - int((harm_count / total) * 100))

        st.subheader(f"🌿 Your EcoScore: {score}/100")
        if score > 80:
            st.success("Great job! You're an eco-hero! 🏆")
        elif score > 50:
            st.warning("Good effort! Try reducing plastic and e-waste.")
        else:
            st.error("You can do better! Check the tips above ☝️")

    else:
        st.info("No data yet. Upload a waste image to begin tracking.")
else:
    st.info("Upload a waste image to start building your eco profile.")

# Footer
st.markdown("---")
st.caption("Made for DigiGreen Hackathon 🌍 | Solo Project by [Your Name]")
