import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

st.title("🌿 Plant Disease Predictor")

# Load model
model = load_model("models/plant_disease_model.h5")

# Class names (EDIT if needed)
class_names = [
    "Tomato___Late_blight",
    "Tomato___Early_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Bacterial_spot",
    "Tomato___YellowLeaf__Curl_Virus",
    "Tomato___mosaic_virus",
    "Tomato___healthy"
]

uploaded_file = st.file_uploader("Upload a leaf image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Convert uploaded file into PIL image
    img = Image.open(uploaded_file)

    # Show the uploaded image
    st.image(img, use_container_width=True)

    # Preprocess image
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    predictions = model.predict(img_array)
    class_idx = np.argmax(predictions)
    confidence = predictions[0][class_idx]

    st.success(f"Prediction: **{class_names[class_idx]}**")
    st.info(f"Confidence: **{confidence*100:.2f}%**")