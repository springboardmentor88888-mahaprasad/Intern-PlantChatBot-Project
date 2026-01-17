import streamlit as st
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import os

from backend.treatments import get_treatment
from backend.chatbot import text_diagnosis

# ---------------- CONFIG ----------------
BASE_DIR = os.getcwd()

MODEL_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "model",
    "plant_disease_resnet50.pth"
)

IMG_SIZE = 224
NUM_CLASSES = 15  # 🔴 must match your app classes

# 🔴 DEFINE CLASS NAMES (ORDER MUST MATCH TRAINING)
class_names = [
    "Apple Scab",
    "Apple Black Rot",
    "Apple Cedar Rust",
    "Corn Gray Leaf Spot",
    "Corn Common Rust",
    "Corn Healthy",
    "Grape Black Rot",
    "Grape Esca",
    "Grape Healthy",
    "Potato Early Blight",
    "Potato Late Blight",
    "Potato Healthy",
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Tomato Healthy"
]

st.set_page_config(
    page_title="PlantDocBot",
    page_icon="🌿",
    layout="centered"
)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"Model file not found at: {MODEL_PATH}")
        st.stop()

    checkpoint = torch.load(MODEL_PATH, map_location="cpu")

    model = models.resnet50(pretrained=False)
    model.fc = nn.Linear(2048, NUM_CLASSES)

    state_dict = checkpoint["model_state_dict"]

    # 🔥 REMOVE FC LAYER WEIGHTS (size mismatch fix)
    state_dict.pop("fc.weight", None)
    state_dict.pop("fc.bias", None)

    model.load_state_dict(state_dict, strict=False)
    model.eval()

    return model

model = load_model()

# ---------------- IMAGE TRANSFORM ----------------
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ---------------- UI ----------------
st.title("🌿 PlantDocBot – AI Plant Disease Diagnosis")
st.write(
    "Upload a plant leaf image **or** describe plant symptoms to get AI-based diagnosis and treatment."
)

# ---------------- IMAGE INPUT ----------------
uploaded_file = st.file_uploader(
    "📷 Upload a plant leaf image",
    type=["jpg", "jpeg", "png"]
)

# ---------------- TEXT INPUT ----------------
st.markdown("---")
st.subheader("💬 Describe Plant Symptoms (Chatbot)")

user_text = st.text_area(
    "Example: yellow leaves with brown spots, wilting plant, holes in leaves"
)

# ---------------- IMAGE DIAGNOSIS ----------------
image_disease = None
image_confidence = None

if uploaded_file:
    if uploaded_file.size > 3 * 1024 * 1024:
        st.error("⚠️ Image too large. Upload image smaller than 3MB.")
        st.stop()

    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Leaf Image", width=350)

    img_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1)[0]

    topk = min(3, len(class_names))
    top_preds = torch.topk(probs, topk)

    st.subheader("🔍 Image-based Predictions")
    for i in range(topk):
        label = class_names[top_preds.indices[i].item()]
        conf = top_preds.values[i].item() * 100
        st.write(f"{i+1}. **{label}** — {conf:.2f}%")

    pred_idx = torch.argmax(probs).item()
    image_disease = class_names[pred_idx]
    image_confidence = probs[pred_idx].item()

    if image_confidence >= 0.25:
        st.success(f"🌿 Image Diagnosis: **{image_disease}**")
        st.info(f"Confidence: **{image_confidence * 100:.2f}%**")
    else:
        st.warning("⚠️ Image diagnosis confidence is low.")

# ---------------- TEXT DIAGNOSIS ----------------
text_disease = None

if user_text.strip():
    text_disease = text_diagnosis(user_text)
    st.subheader("🧠 Text-based Diagnosis")
    st.success(f"Possible Disease: **{text_disease}**")

# ---------------- FINAL RECOMMENDATION ----------------
if image_disease or text_disease:
    st.markdown("### ✅ Final Recommendation")

    final_disease = (
        image_disease
        if image_confidence and image_confidence >= 0.25
        else text_disease
    )

    treatment = get_treatment(final_disease)

    st.write(f"**Final Disease Decision:** {final_disease}")
    st.warning(f"💊 **Recommended Treatment:** {treatment}")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🌿 PlantDocBot | Image + Chatbot based AI Plant Disease Diagnosis")
