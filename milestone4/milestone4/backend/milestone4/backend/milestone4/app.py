import streamlit as st
import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image

from backend.chatbot import text_diagnosis
from backend.treatments import get_treatment

# ----------------- MODEL PATH -----------------
MODEL_PATH = r"models\resnet50_plantvillage_checkpoint.pth"
IMG_SIZE = 224

# ----------------- Load Model -----------------
@st.cache_resource
def load_model():
    checkpoint = torch.load(MODEL_PATH, map_location="cpu")
    num_classes = len(checkpoint["idx_to_class"])

    model = models.resnet50(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    class_names = [checkpoint["idx_to_class"][i] for i in range(num_classes)]
    return model, class_names

model, class_names = load_model()

# ----------------- Image Transforms -----------------
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ----------------- Streamlit UI -----------------
st.title("🌿 PlantDocBot – AI Plant Disease Diagnosis")
st.write("Upload a leaf image or describe plant symptoms to get diagnosis and treatment.")

# ----------------- Image Upload -----------------
uploaded_file = st.file_uploader("📷 Upload a leaf image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Leaf Image", width=300)

    img_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1)[0]

    pred_idx = torch.argmax(probs).item()
    image_disease = class_names[pred_idx]
    image_conf = probs[pred_idx].item() * 100

    st.markdown("### 🔍 Image Prediction")
    st.write(f"**Predicted Disease:** {image_disease}")
    st.write(f"**Confidence:** {image_conf:.2f}%")

    # Final Recommendation for image
    treatment = get_treatment(image_disease)
    st.markdown("### ✅ Final Recommendation")
    st.write(f"**Final Disease Decision:** {image_disease}")
    st.write(f"**Cause:** {treatment.get('cause', 'Unknown')}")
    st.write(f"**Treatment:** {treatment.get('treatment', 'N/A')}")
    st.write(f"**Prevention:** {treatment.get('prevention', 'N/A')}")

# ----------------- Chatbot / Text Input -----------------
st.markdown(
    "💬 Describe Plant Symptoms (Chatbot)  \n"
    "<span style='color:white'>Example: yellow leaves, holes, wilting plant</span>",
    unsafe_allow_html=True
)

user_text = st.text_input("", "")

if user_text.strip() != "":
    text_disease = text_diagnosis(user_text.strip())

    if text_disease:
        treatment = get_treatment(text_disease)
        st.markdown("### 🧠 Text-based Diagnosis")
        st.write(f"**Possible Disease:** {text_disease}")
        st.write(f"**Cause:** {treatment.get('cause', 'Unknown')}")
        st.write(f"**Treatment:** {treatment.get('treatment', 'N/A')}")
        st.write(f"**Prevention:** {treatment.get('prevention', 'N/A')}")
    else:
        st.warning("No matching disease found for the provided symptoms.")
