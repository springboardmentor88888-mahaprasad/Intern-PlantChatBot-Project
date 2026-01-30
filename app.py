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
        /* background-color handled by config.toml */
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

# ---------------- STATE MANAGEMENT ----------------
# Initialize uploader key to force reset
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "current_mode" not in st.session_state:
    st.session_state.current_mode = None  # "image", "voice", or "text"

if "diagnosis_result" not in st.session_state:
    st.session_state.diagnosis_result = {
        "disease": None,
        "confidence": None,
        "source": None,
        "transcription": None,
        "image": None,
        "user_text": None
    }


def clear_diagnosis():
    """Reset all diagnosis state."""
    st.session_state.current_mode = None
    st.session_state.diagnosis_result = {
        "disease": None,
        "confidence": None,
        "source": None,
        "transcription": None,
        "image": None,
        "user_text": None
    }
    
    # Clear text input explicitly (setting to empty string forces reset)
    st.session_state["text_input"] = ""
    
    # Increment uploader key to force re-render of file uploaders (clears them)
    st.session_state.uploader_key += 1


def set_mode(mode: str):
    """Set the current diagnosis mode and clear previous results."""
    if st.session_state.current_mode != mode:
        st.session_state.current_mode = mode
        st.session_state.diagnosis_result = {
            "disease": None,
            "confidence": None,
            "source": None,
            "transcription": None,
            "image": None,
            "user_text": None
        }


# ---------------- LOAD MODEL ----------------
# PlantVillage class names in alphabetical order (standard DataLoader ordering)
PLANTVILLAGE_CLASSES = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]

@st.cache_resource
def load_model():
    checkpoint = torch.load(MODEL_PATH, map_location="cpu")
    state_dict = checkpoint["model_state_dict"]

    num_classes = state_dict["fc.weight"].shape[0]
    
    # Use explicit class names if they match, else fallback
    if num_classes == len(PLANTVILLAGE_CLASSES):
        class_names = PLANTVILLAGE_CLASSES
    else:
        class_names = checkpoint.get("class_names", [])[:num_classes]
        if not class_names:
            from knowledge.treatments import _diseases_data as TREATMENTS
            class_names = list(TREATMENTS.keys())[:num_classes]
            if len(class_names) < num_classes:
                class_names.extend([f"Disease_{i}" for i in range(len(class_names), num_classes)])

    model = models.resnet50(pretrained=False)
    model.fc = torch.nn.Linear(2048, num_classes)
    model.load_state_dict(state_dict, strict=True)
    model.eval()

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

# ---------------- UI HEADER ----------------
st.markdown("<h1>🌿 PlantDocBot – AI Plant Disease Diagnosis</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center;'>Professional AI-powered diagnosis using Images, Voice, or Text symptoms.</p>", unsafe_allow_html=True)

# ---------------- CLEAR BUTTON ----------------
st.markdown("""
<style>
    .new-diagnosis-btn button {
        white-space: nowrap !important;
        min-width: 160px !important;
    }
</style>
""", unsafe_allow_html=True)

col_clear = st.columns([2, 1.5, 2])
with col_clear[1]:
    st.markdown('<div class="new-diagnosis-btn">', unsafe_allow_html=True)
    if st.button("🔄 New Diagnosis", use_container_width=True):
        clear_diagnosis()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------- INPUT TABS ----------------
tab1, tab2, tab3 = st.tabs(["📷 Image Upload", "🎤 Voice Input", "💬 Text Symptoms"])

with tab1:
    st.subheader("Visual Diagnosis")
    uploaded_file = st.file_uploader(
        "Upload a clear photo of the infected leaf",
        type=["jpg", "jpeg", "png"],
        key=f"image_upload_{st.session_state.uploader_key}"
    )
    
    if uploaded_file:
        set_mode("image")
        image = Image.open(uploaded_file).convert("RGB")
        st.session_state.diagnosis_result["image"] = image
        
        # Run image prediction
        img_tensor = transform(image).unsqueeze(0)
        with torch.no_grad():
            outputs = model(img_tensor)
            probs = F.softmax(outputs, dim=1)[0]
        
        pred_idx = torch.argmax(probs).item()
        st.session_state.diagnosis_result["disease"] = class_names[pred_idx]
        st.session_state.diagnosis_result["confidence"] = probs[pred_idx].item()
        st.session_state.diagnosis_result["source"] = "Image Analysis"
        st.session_state.diagnosis_result["top3"] = torch.topk(probs, min(3, len(class_names)))

with tab2:
    st.subheader("Voice Assistant")
    audio_file = st.file_uploader(
        "Upload an audio file describing symptoms",
        type=["mp3", "wav", "m4a", "ogg"],
        key=f"voice_upload_{st.session_state.uploader_key}"
    )
    
    if audio_file:
        set_mode("voice")
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
                    st.session_state.diagnosis_result["transcription"] = result["transcription"]
                    st.session_state.diagnosis_result["disease"] = result["disease_key"]
                    st.session_state.diagnosis_result["source"] = "Voice Symptoms"
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
    
    if st.button("🔍 Diagnose", key="text_search_btn", use_container_width=True):
        if user_text:
            set_mode("text")
            st.session_state.diagnosis_result["user_text"] = user_text
            with st.spinner("Analyzing symptoms..."):
                disease = text_diagnosis(user_text)
            st.session_state.diagnosis_result["disease"] = disease
            st.session_state.diagnosis_result["source"] = "Text Symptoms"
        else:
            st.warning("Please enter some symptoms first.")

# ---------------- RESULTS SECTION ----------------
st.markdown("---")

current_mode = st.session_state.current_mode
result = st.session_state.diagnosis_result

if current_mode is None:
    st.info("🚀 **Ready to assist!** Please upload an image, recording, or describe your plant's symptoms to begin.")
else:
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.write(f"### 📊 {current_mode.title()} Analysis")
        
        if current_mode == "image" and result["image"]:
            st.image(result["image"], caption="Uploaded Leaf", use_container_width=True)
            
            if "top3" in result:
                st.write("**Top Predictions:**")
                top3 = result["top3"]
                for i in range(len(top3.indices)):
                    label = class_names[top3.indices[i].item()]
                    conf = top3.values[i].item() * 100
                    st.progress(top3.values[i].item(), text=f"{label} ({conf:.1f}%)")
        
        elif current_mode == "voice" and result["transcription"]:
            st.info(f"**Transcription:** \"{result['transcription']}\"")
        
        elif current_mode == "text" and result["user_text"]:
            st.info(f"**Your Description:** \"{result['user_text']}\"")
    
    with col2:
        st.write("### 🩺 Diagnosis Result")
        
        disease = result["disease"]
        confidence = result["confidence"]
        source = result["source"]
        
        if disease and disease != "Unknown":
            # Determine confidence level for image mode
            if current_mode == "image" and confidence:
                if confidence >= 0.8:
                    conf_label = "High Confidence"
                    conf_color = "#2e7d32"
                elif confidence >= 0.4:
                    conf_label = "Moderate Confidence"
                    conf_color = "#f57c00"
                else:
                    conf_label = "Low Confidence"
                    conf_color = "#d32f2f"
                
                st.markdown(f"""
                <div style="background-color: #e8f5e9; padding: 20px; border-radius: 15px; border-left: 5px solid {conf_color};">
                    <h3 style="margin-top: 0; color: #1b5e20;">✅ {disease.replace('___', ' ').replace('_', ' ').title()}</h3>
                    <p style="color: #666; font-size: 0.9em;">{conf_label} ({confidence*100:.1f}%) via {source}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Voice/Text mode - no confidence score
                st.markdown(f"""
                <div style="background-color: #e8f5e9; padding: 20px; border-radius: 15px; border-left: 5px solid #2e7d32;">
                    <h3 style="margin-top: 0; color: #1b5e20;">✅ {disease.replace('___', ' ').replace('_', ' ').title()}</h3>
                    <p style="color: #666; font-size: 0.9em;">Diagnosed via {source}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            formatted_response = format_treatment_response(disease, confidence)
            st.markdown(formatted_response)
        
        elif disease == "Unknown" or disease is None:
            if current_mode == "image" and confidence and confidence < 0.4:
                st.markdown("""
                <div style="background-color: #fff3e0; padding: 20px; border-radius: 15px; border-left: 5px solid #ff9800;">
                    <h3 style="margin-top: 0; color: #e65100;">⚠️ Uncertain Diagnosis</h3>
                    <p style="color: #666;">The image prediction confidence is too low for a reliable diagnosis.</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("---")
                uncertain_info = get_uncertain_response()
                st.write("**Please try:**")
                for item in uncertain_info["treatment"]:
                    st.write(f"  • {item}")
            else:
                st.markdown("""
                <div style="background-color: #e3f2fd; padding: 20px; border-radius: 15px; border-left: 5px solid #1976d2;">
                    <h3 style="margin-top: 0; color: #1565c0;">📷 Try Image Upload</h3>
                    <p style="color: #555;">We couldn't identify a disease from your input. For better accuracy, try uploading a clear photo of the affected leaf.</p>
                </div>
                """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("PlantDocBot | Single-mode AI Plant Disease Diagnosis")