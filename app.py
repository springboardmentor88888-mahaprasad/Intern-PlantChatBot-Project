"""
Plant Disease Predictor 🌱

How to Run This Application:
1.Install Virtual Environment
python -m venv .venv
2. Activate virtual environment
   venv\\Scripts\\activate

3. Install required packages
   pip install streamlit

4. Run the application
   streamlit run app.py

Expected Output:
- Streamlit web application opens in browser
- Title displayed: Plant Disease Predictor
- Option to upload a leaf image (jpg / jpeg / png)
- After uploading an image, a predicted disease is displayed
"""

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
