import streamlit as st
import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image

# ---------------- CONFIG ----------------
MODEL_PATH = "models/plant_disease_resnet50.pth"
IMG_SIZE = 224

# ---------------- LOAD MODEL ----------------
def load_model():
    checkpoint = torch.load(MODEL_PATH, map_location="cpu")

    class_names = checkpoint["class_names"]
    num_classes = len(class_names)

    model = models.resnet50(pretrained=False)

    state_dict = checkpoint["model_state_dict"]
    state_dict.pop("fc.weight")
    state_dict.pop("fc.bias")

    model.load_state_dict(state_dict, strict=False)
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

    model.eval()
    return model, class_names

# 🔴 THIS LINE IS CRITICAL (DO NOT MOVE)
model, class_names = load_model()

# ---------------- TRANSFORM ----------------
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
])

# ---------------- UI ----------------
st.title("🌿 Plant Disease Predictor")
st.write("Upload a leaf image to detect plant disease")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    # ✅ FIXED LINE (this was causing the error)
    st.image(image, use_container_width=True)

    img_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1)
        confidence, pred_idx = torch.max(probs, 1)

    st.success(f"Prediction: **{class_names[pred_idx.item()]}**")
    st.info(f"Confidence: **{confidence.item() * 100:.2f}%**")

st.markdown("---")
st.subheader("Describe Plant Symptoms (Optional)")

user_text = st.text_input(
    "Describe plant symptoms (e.g. yellow leaves, brown spots)"
)

def text_based_diagnosis(user_text):
    text = user_text.lower()

    if "yellow" in text:
        return "Possible Nitrogen Deficiency"
    elif "brown spot" in text or "brown spots" in text:
        return "Possible Fungal Leaf Spot Disease"
    elif "wilting" in text:
        return "Possible Water Stress or Root Disease"
    elif "holes" in text:
        return "Possible Pest Attack"
    else:
        return "No clear disease detected from text symptoms"

if user_text:
    text_prediction = text_based_diagnosis(user_text)
    st.warning(f"Text-based diagnosis: **{text_prediction}**")
