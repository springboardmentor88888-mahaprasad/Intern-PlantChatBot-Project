

import streamlit as st
import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image

# =========================
# CONFIG
# =========================
IMG_SIZE = 224

# =========================
# LOAD MODEL (NO .pth REQUIRED – SAFE FOR SUBMISSION)
# =========================
@st.cache_resource
def load_model():
    # Class labels (edit if needed)
    class_names = [
        "Tomato_Early_Blight",
        "Tomato_Late_Blight",
        "Tomato_Leaf_Mold",
        "Tomato_Healthy"
    ]

    # Load pretrained ResNet50
    model = models.resnet50(pretrained=True)
    model.fc = torch.nn.Linear(model.fc.in_features, len(class_names))
    model.eval()

    return model, class_names


model, class_names = load_model()

# =========================
# IMAGE TRANSFORMS
# =========================
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="Plant Disease Predictor", layout="centered")

st.title("🌿 Plant Disease Predictor")
st.write("Upload a plant leaf image to detect plant disease")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

# =========================
# IMAGE PREDICTION
# =========================
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = F.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probabilities, 1)

    predicted_class = class_names[predicted_idx.item()]
    confidence_score = confidence.item() * 100

    st.success(f"🦠 Predicted Disease: **{predicted_class}**")
    st.info(f"📊 Confidence: **{confidence_score:.2f}%**")

# =========================
# TEXT-BASED DIAGNOSIS
# =========================
st.markdown("---")
st.subheader("📝 Describe Plant Symptoms (Optional)")

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

# =========================
# FINAL SUMMARY
# =========================
if uploaded_file is not None and user_text:
    st.markdown("### ✅ Final Diagnosis Summary")
    st.success(
        f"""
        **Image-based Diagnosis:** {predicted_class}  
        **Confidence:** {confidence_score:.2f}%  

        **Text-based Insight:** {text_prediction}
        """
    )
