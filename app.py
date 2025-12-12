# cd "C:\AI PROJECT INFOSYS\PLANT CHATBOT\PlantDocBot"
# python -m venv .venv
# .\.venv\Scripts\Activate.ps1
# Set-ExecutionPolicy RemoteSigned --> on cmd (as admin)
# pip install fastapi uvicorn[standard] python-multipart pytesseract pillow pymupdf sqlalchemy python-dotenv
# pip install streamlit torch torchvision pillow


import streamlit as st
import random

st.title(" Plant Disease Predictor")

# dummy disease classes
diseases = [
    "Leaf Spot",
    "Blight",
    "Rust",
    "Mildew",
    "Healthy Leaf"
]

uploaded_file = st.file_uploader("📥 Upload a leaf image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Leaf Image", use_column_width=True)

    # dummy prediction
    prediction = random.choice(diseases)

    st.success(f" Predicted Disease: **{prediction}**")