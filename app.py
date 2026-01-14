import streamlit as st
import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image

from backend import text_diagnosis, process_voice_input
from knowledge import get_treatment, format_treatment_response, get_uncertain_response
import tempfile
import os

# ---------------- CONFIG ----------------
MODEL_PATH = "models/resnet50_plantvillage_checkpoint.pth"
IMG_SIZE = 224

st.set_page_config(
    page_title="PlantDocBot | AI Diagnosis",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Premium Look and Center Alignment
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    
    /* Center the main block container */
    .block-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }
    
    /* Center all headings and subheadings */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        text-align: center;
    }
    
    .stMarkdown h1 {
        color: #1b5e20;
        margin-bottom: 10px;
    }
    
    /* Center paragraph text under title */
    .stMarkdown p {
        text-align: center;
    }
    
    /* Center the tabs container */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 20px;
    }
    
    /* Center tab panel content */
    .stTabs [data-baseweb="tab-panel"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    /* Center subheaders within tabs */
    .stTabs [data-baseweb="tab-panel"] h2,
    .stTabs [data-baseweb="tab-panel"] h3 {
        text-align: center;
        width: 100%;
    }
    
    /* Center file uploader */
    .stFileUploader {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }
    
    .stFileUploader > div {
        width: 100%;
        max-width: 500px;
    }
    
    /* Center text area */
    .stTextArea {
        width: 100%;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Center audio player */
    .stAudio {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
    }
    
    /* Card styling */
    .diagnosis-card {
        padding: 20px;
        border-radius: 15px;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Center the footer caption */
    .stCaption {
        text-align: center;
        width: 100%;
    }
    
    /* Ensure columns are centered */
    .stColumns {
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
def load_model():
    checkpoint = torch.load(MODEL_PATH, map_location="cpu")
    state_dict = checkpoint["model_state_dict"]

    num_classes = state_dict["fc.weight"].shape[0]
    class_names = checkpoint.get("class_names", [])[:num_classes]

    model = models.resnet50(pretrained=False)
    model.fc = torch.nn.Linear(2048, num_classes)
    model.load_state_dict(state_dict, strict=True)
    model.eval()

    # Silently use disease keys from knowledge base if class names are missing
    if not class_names:
        from knowledge.treatments import _diseases_data as TREATMENTS
        class_names = list(TREATMENTS.keys())[:num_classes]
        # Pad with generic names if knowledge base has fewer entries than model classes
        if len(class_names) < num_classes:
            class_names.extend([f"Disease_{i}" for i in range(len(class_names), num_classes)])


    return model, class_names


model, class_names = load_model()

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
st.markdown("<h1>🌿 PlantDocBot – AI Plant Disease Diagnosis</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center;'>Professional AI-powered diagnosis using Images, Voice, and Text symptoms.</p>", unsafe_allow_html=True)

# Initialize states
image_disease = None
image_confidence = None
text_disease = None
voice_disease = None
transcription = None

# ---------------- INPUT TABS ----------------
tab1, tab2, tab3 = st.tabs(["📷 Image Upload", "🎤 Voice Input", "💬 Text Symptoms"])

with tab1:
    st.subheader("Visual Diagnosis")
    uploaded_file = st.file_uploader(
        "Upload a clear photo of the infected leaf",
        type=["jpg", "jpeg", "png"],
        key="image_upload"
    )

with tab2:
    st.subheader("Voice Assistant")
    audio_file = st.file_uploader("Speak about the symptoms (audio file)", type=["mp3", "wav", "m4a", "ogg"], key="voice_upload")
    if audio_file:
        st.audio(audio_file)
        with st.spinner("Analyzing your voice..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as tmp:
                tmp.write(audio_file.getvalue())
                tmp_path = tmp.name
            try:
                result = process_voice_input(tmp_path)
                if result["error"]:
                    st.error(result["error"])
                else:
                    transcription = result["transcription"]
                    voice_disease = result["disease_key"]
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

with tab3:
    st.subheader("Manual Description")
    user_text = st.text_area(
        "Describe what you see in detail...",
        placeholder="Example: My tomato leaves have yellow halos and concentric rings.",
        key="text_input"
    )
    if user_text:
        text_disease = text_diagnosis(user_text)

# ---------------- RESULTS COLUMN ----------------
st.markdown("---")
col1, col2 = st.columns([1, 1.2])

with col1:
    # ---------------- IMAGE ANALYSIS RESULTS ----------------
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Leaf Detail", use_container_width=True)

        img_tensor = transform(image).unsqueeze(0)
        with torch.no_grad():
            outputs = model(img_tensor)
            probs = F.softmax(outputs, dim=1)[0]

        top3 = torch.topk(probs, min(3, len(class_names)))
        
        st.write("### 🔍 Image Insights")
        for i in range(len(top3.indices)):
            label = class_names[top3.indices[i].item()]
            conf = top3.values[i].item() * 100
            st.progress(top3.values[i].item(), text=f"{label} ({conf:.1f}%)")

        pred_idx = torch.argmax(probs).item()
        image_disease = class_names[pred_idx]
        image_confidence = probs[pred_idx].item()

with col2:
    # ---------------- SYMPTOM OVERVIEW ----------------
    st.write("### 🧠 Symptom Match")
    
    # Display results from Voice/Text if available
    if transcription:
        st.info(f"**Voice Transcription:** \"{transcription}\"")
        if voice_disease != "Unknown":
            st.success(f"**Found in Voice:** {voice_disease}")
    
    if text_disease and text_disease != "Unknown":
        st.success(f"**Found in Text:** {text_disease}")
    
    if not (image_disease or text_disease or voice_disease):
        st.info("Awaiting input for diagnosis...")

    # ---------------- FINAL RECOMMENDATION ----------------
    # Combining sources with confidence-aware handling
    final_disease = None
    final_confidence = None
    source = None

    # Priority: Image (if >80% confident) > Voice > Text > Image (moderate) > Uncertain
    if image_confidence and image_confidence >= 0.8:
        final_disease = image_disease
        final_confidence = image_confidence
        source = "High Confidence Image"
    elif voice_disease and voice_disease != "Unknown":
        final_disease = voice_disease
        final_confidence = None  # Voice doesn't have confidence
        source = "Voice Symptoms"
    elif text_disease and text_disease != "Unknown":
        final_disease = text_disease
        final_confidence = None  # Text doesn't have confidence
        source = "Text Symptoms"
    elif image_confidence and image_confidence >= 0.4:
        final_disease = image_disease
        final_confidence = image_confidence
        source = "Image Analysis (Moderate Confidence)"
    elif image_disease and image_confidence and image_confidence < 0.4:
        # Low confidence - show uncertain response
        st.markdown("""
        <div style="background-color: #fff3e0; padding: 20px; border-radius: 15px; border-left: 5px solid #ff9800;">
            <h3 style="margin-top: 0; color: #e65100;">⚠️ Uncertain Diagnosis</h3>
            <p style="color: #666;">The prediction confidence is too low to provide a reliable diagnosis.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        uncertain_info = get_uncertain_response()
        st.write("**Please try one of the following:**")
        for item in uncertain_info["treatment"]:
            st.write(f"  • {item}")
        final_disease = None  # Prevent further processing

    if final_disease and final_disease != "Unknown":
        st.markdown(f"""
        <div style="background-color: #e8f5e9; padding: 20px; border-radius: 15px; border-left: 5px solid #2e7d32;">
            <h3 style="margin-top: 0; color: #1b5e20;">✅ Targeted Diagnosis: {final_disease.replace('___', ' ').replace('_', ' ').title()}</h3>
            <p style="color: #666; font-size: 0.9em;">Verified via <b>{source}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        # Use confidence-aware formatting
        formatted_response = format_treatment_response(final_disease, final_confidence)
        st.markdown(formatted_response)
    elif not final_disease and (image_disease or text_disease or voice_disease):
        st.warning("🔍 We analyzed your inputs but couldn't find a high-confidence match in our knowledge base.")
    elif not (image_disease or text_disease or voice_disease):
        st.write("---")
        st.write("🚀 **Ready to assist!** Please upload an image, recording, or description to begin.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("PlantDocBot | Image + Chatbot based Plant Disease Diagnosis")