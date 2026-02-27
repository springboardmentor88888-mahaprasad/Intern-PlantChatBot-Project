import streamlit as st
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from predict import predict_image, predict_symptom

st.title("🌿 Plant Disease Detection Chatbot")

mode = st.radio("Choose input type:", ["Image", "Text"])

if mode == "Image":
    uploaded = st.file_uploader("Upload leaf image", type=["jpg","png"])
    if uploaded:
        st.image(uploaded)
        st.success("Image received (connect CNN model here)")

if mode == "Text":
    text = st.text_area("Describe plant symptoms")
    if st.button("Predict"):
        st.success("Symptom received (connect BERT model here)")
