import streamlit as st
import random
from PIL import Image

st.title("🌿 Plant Disease Predictor")

diseases = [
    "Leaf Spot",
    "Blight",
    "Rust",
    "Mildew",
    "Healthy Leaf"
]

uploaded_file = st.file_uploader(
    "📥 Upload a leaf image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Leaf Image", use_column_width=True)

    prediction = random.choice(diseases)
    st.success(f"✅ Predicted Disease: **{prediction}**")
