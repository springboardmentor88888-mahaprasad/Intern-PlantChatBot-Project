import streamlit as st
import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image

# ---------------- CONFIG ----------------
MODEL_PATH = "models/plant_disease_resnet50 (1).pth"
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

model, class_names = load_model()

# ---------------- TRANSFORM ----------------
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ---------------- UI ----------------
st.title("🌿 Plant Disease Predictor")
st.write("Upload a leaf image to detect plant disease")

uploaded_file = st.file_uploader(
    "Choose a leaf image",
    type=["jpg", "png", "jpeg"]
)

# ---------------- IMAGE PREDICTION ----------------
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, width=350)

    img_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1)[0]

        top3 = torch.topk(probs, 3)

        st.subheader("🔍 Top Predictions")
        for i in range(3):
            label = class_names[top3.indices[i].item()]
            conf = top3.values[i].item() * 100
            st.write(f"{i+1}. {label} — {conf:.2f}%")

        # Best prediction
        pred_idx = torch.argmax(probs)
        best_label = class_names[pred_idx.item()]
        confidence = probs[pred_idx].item()

        st.success(f"Prediction: **{best_label}**")
        st.info(f"Confidence: **{confidence * 100:.2f}%**")

# ---------------- TEXT DIAGNOSIS ----------------
st.markdown("---")
st.subheader("📝 Describe Plant Symptoms (Optional)")

user_text = st.text_input(
    "Describe symptoms (e.g. yellow leaves, brown spots)"
)

def text_based_diagnosis(text):
    text = text.lower()

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

# ---------------- FINAL SUMMARY ----------------
if uploaded_file and user_text:
    st.markdown("### ✅ Final Diagnosis Summary")
    st.success(
        f"""
        **Image-based Diagnosis:** {best_label}  
        **Confidence:** {confidence * 100:.2f}%  

        **Text-based Insight:** {text_prediction}
        """
    ) 

