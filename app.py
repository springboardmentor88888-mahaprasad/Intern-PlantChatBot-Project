# app.py
import streamlit as st
import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image

from backend.treatments import get_treatment, TREATMENTS
from backend.chatbot import text_diagnosis, get_chat_response

# ---------------- CONFIG ----------------
MODEL_PATH = "models/plant_disease_resnet50.pth"
IMG_SIZE = 224

st.set_page_config(
    page_title="PlantDocBot - Professional Crop Health Dashboard",
    page_icon="🌿",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-title {
        color: #1b5e20;
        font-weight: 700;
        margin-bottom: 0.1rem;
    }
    
    .subtitle {
        color: #558b2f;
        font-size: 1.15rem;
        margin-bottom: 1.5rem;
    }
    
    /* Elegant card containers */
    .dashboard-card {
        background-color: #ffffff;
        border: 1px solid #e8f5e9;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 6px 18px rgba(46, 125, 50, 0.04);
        margin-bottom: 1.2rem;
    }
    
    .diagnosis-header {
        font-size: 1.35rem;
        font-weight: 600;
        color: #1b5e20;
        border-bottom: 2px solid #c8e6c9;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Custom treatment details styling */
    .treatment-title {
        color: #2e7d32;
        font-weight: 600;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        margin-bottom: 0.2rem;
    }
    
    .pill-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .badge-organic {
        background-color: #e8f5e9;
        color: #2e7d32;
    }
    
    .badge-chemical {
        background-color: #ffebee;
        color: #c62828;
    }
    
    .badge-prevention {
        background-color: #e3f2fd;
        color: #1565c0;
    }
    
    /* Quick chip buttons styling */
    div.stButton > button {
        border-radius: 20px !important;
        border: 1px solid #c8e6c9 !important;
        background-color: #f1f8e9 !important;
        color: #2e7d32 !important;
        font-weight: 500 !important;
        padding: 0.4rem 1rem !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease-in-out !important;
        margin-bottom: 0.5rem !important;
    }
    div.stButton > button:hover {
        background-color: #2e7d32 !important;
        color: white !important;
        border-color: #2e7d32 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(46, 125, 50, 0.15);
    }
    
    /* Make prediction progress bars look nice */
    .prediction-row {
        margin-bottom: 0.8rem;
    }
    
    .prediction-label {
        font-weight: 500;
        color: #37474f;
        margin-bottom: 0.1rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    checkpoint = torch.load(MODEL_PATH, map_location="cpu")
    model = models.resnet50(weights=None)
    num_classes = len(checkpoint["idx_to_class"])
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    # Get class names in correct index order
    idx_to_class = checkpoint["idx_to_class"]
    class_names = [idx_to_class[i] for i in range(len(idx_to_class))]
    return model, class_names

try:
    model, class_names = load_model()
except Exception as e:
    st.error(f"Failed to load ResNet50 model: {e}")
    class_names = []

# ---------------- IMAGE TRANSFORM ----------------
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ---------------- HEADER ----------------
st.markdown('<h1 class="main-title">🌿 PlantDocBot</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Crop Disease Diagnosis & Multimodal Chat Assistant</p>', unsafe_allow_html=True)

# ---------------- SESSION STATE SETUP ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": "🌿 **Welcome to the PlantDoc assistant!**\n\nI can help you grow healthy crops. You can upload a leaf image above, or describe plant symptoms here. What crop are we looking at today?",
            "suggestions": ["How to grow Tomatoes", "How to grow Potatoes", "How to grow Peppers", "Compare Potato Blights"]
        }
    ]
if "last_suggestions" not in st.session_state:
    st.session_state.last_suggestions = ["How to grow Tomatoes", "How to grow Potatoes", "How to grow Peppers", "Compare Potato Blights"]
if "latest_diagnosis" not in st.session_state:
    st.session_state.latest_diagnosis = None

# Helper to handle chatbot messages
def handle_chat_message(user_msg):
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_msg})
    
    # Process through bot
    uploaded_diag = st.session_state.get("latest_diagnosis", None)
    bot_out = get_chat_response(user_msg, uploaded_diag)
    
    # Add bot message
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": bot_out["response"],
        "suggestions": bot_out.get("suggestions", [])
    })
    st.session_state.last_suggestions = bot_out.get("suggestions", [])
    st.rerun()

# ---------------- DASHBOARD TABS ----------------
tab1, tab2, tab3 = st.tabs([
    "🔍 Diagnosis & Chat Center", 
    "📚 Disease Encyclopedia", 
    "🌿 Plant Care Manuals"
])

# ================= TAB 1: DIAGNOSIS & CHAT CENTER =================
with tab1:
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="diagnosis-header">📷 AI Leaf Scanner</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload a clear image of a pepper, potato, or tomato leaf:",
            type=["jpg", "jpeg", "png"],
            key="leaf_scanner"
        )
        
        if uploaded_file:
            if uploaded_file.size > 3 * 1024 * 1024:
                st.error("⚠️ Image file is too large. Please upload an image smaller than 3MB.")
            else:
                st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                
                # Double column within upload card
                sub_col1, sub_col2 = st.columns([1, 1.2])
                with sub_col1:
                    image = Image.open(uploaded_file).convert("RGB")
                    st.image(image, caption="Uploaded Leaf Specimen", use_container_width=True)
                    
                with sub_col2:
                    st.markdown("##### **Scanning Results:**")
                    img_tensor = transform(image).unsqueeze(0)
                    
                    with torch.no_grad():
                        outputs = model(img_tensor)
                        probs = F.softmax(outputs, dim=1)[0]
                        
                    top3 = torch.topk(probs, min(3, len(class_names)))
                    
                    for i in range(len(top3.indices)):
                        idx = top3.indices[i].item()
                        label = class_names[idx]
                        conf = top3.values[i].item()
                        
                        # Clean label for presentation
                        t_data = get_treatment(label)
                        label_clean = t_data["common_name"]
                        
                        st.markdown(f'<div class="prediction-row"><div class="prediction-label">{label_clean} ({conf*100:.1f}%)</div></div>', unsafe_allow_html=True)
                        st.progress(conf)
                        
                    pred_idx = torch.argmax(probs).item()
                    top_disease = class_names[pred_idx]
                    top_confidence = probs[pred_idx].item()
                    
                    # Update session state for the chatbot context
                    if top_confidence >= 0.25:
                        st.session_state.latest_diagnosis = top_disease
                    else:
                        st.session_state.latest_diagnosis = None
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Detailed Diagnostic Card
                if st.session_state.latest_diagnosis:
                    diag_data = get_treatment(st.session_state.latest_diagnosis)
                    st.markdown(f"""
                    <div class="dashboard-card" style="border-left: 6px solid #2e7d32;">
                        <h4 style="margin-top:0px; color:#1b5e20;">🌿 AI Diagnosis: {diag_data['common_name']}</h4>
                        <p><strong>🔬 Cause:</strong> {diag_data['cause']}</p>
                        <p><strong>📋 Primary Symptoms:</strong> {diag_data['symptoms']}</p>
                        
                        <div class="treatment-title"><span class="pill-badge badge-organic">Organic</span> Organic Remediation</div>
                        <p style="font-size:0.95rem; color:#2e7d32;">{diag_data['organic']}</p>
                        
                        <div class="treatment-title"><span class="pill-badge badge-chemical">Chemical</span> Chemical Control</div>
                        <p style="font-size:0.95rem; color:#b71c1c;">{diag_data['chemical']}</p>
                        
                        <div class="treatment-title"><span class="pill-badge badge-prevention">Prevention</span> Preventative Practices</div>
                        <p style="font-size:0.95rem; color:#0d47a1;">{diag_data['prevention']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Scanner confidence is low. Please ensure leaf is centered and well-lit, or ask the chatbot below for help.")
        else:
            st.info("💡 Tip: Upload a clear close-up leaf image for the best diagnostic accuracy.")

    with col2:
        st.markdown('<div class="diagnosis-header">💬 Conversational Plant Assistant</div>', unsafe_allow_html=True)
        
        # Scrollable container for chat history
        chat_container = st.container(height=480)
        with chat_container:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Action chips for quick replies
        if st.session_state.last_suggestions:
            st.markdown("<p style='font-size:0.8rem; font-weight:600; color:#558b2f; margin-bottom: 0.3rem;'>Suggested Inquiries:</p>", unsafe_allow_html=True)
            cols = st.columns(len(st.session_state.last_suggestions))
            for i, suggestion in enumerate(st.session_state.last_suggestions):
                if cols[i].button(suggestion, key=f"chat_chip_{i}"):
                    handle_chat_message(suggestion)
                    
        # Chat input text box
        user_input = st.chat_input("Describe symptoms (e.g., 'yellow circles on potato leaves') or ask a question...")
        if user_input:
            handle_chat_message(user_input)

# ================= TAB 2: DISEASE ENCYCLOPEDIA =================
with tab2:
    st.markdown('<div class="diagnosis-header">📚 Supported Plant Disease Library</div>', unsafe_allow_html=True)
    st.write("Browse details, causes, symptoms, and cures for all conditions supported by our AI neural network scanner.")
    
    # Filter search box
    search_query = st.text_input("🔍 Search diseases by name or crop (e.g. 'Blight', 'Tomato'):", "")
    
    # Crop selector buttons
    crop_filter = st.radio("Filter by Crop:", ["All Crops", "Tomato 🍅", "Potato 🥔", "Bell Pepper 🫑"], horizontal=True)
    
    enc_col1, enc_col2 = st.columns([1, 1], gap="medium")
    
    # Retrieve all 15 conditions keys
    sorted_keys = sorted(list(TREATMENTS.keys()))
    
    left_keys = []
    right_keys = []
    
    count = 0
    for key in sorted_keys:
        t_data = TREATMENTS[key]
        name = t_data["common_name"]
        
        # Check Search query
        if search_query and search_query.lower() not in name.lower() and search_query.lower() not in t_data["cause"].lower():
            continue
            
        # Check Crop filter
        if crop_filter == "Tomato 🍅" and "tomato" not in key.lower():
            continue
        elif crop_filter == "Potato 🥔" and "potato" not in key.lower():
            continue
        elif crop_filter == "Bell Pepper 🫑" and "pepper" not in key.lower():
            continue
            
        if count % 2 == 0:
            left_keys.append(key)
        else:
            right_keys.append(key)
        count += 1
        
    def draw_disease_details(key):
        data = TREATMENTS[key]
        is_healthy = "healthy" in key.lower()
        border_color = "#2e7d32" if is_healthy else "#d32f2f"
        
        with st.expander(f"{data['common_name']}"):
            st.markdown(f"""
            <div style="border-left: 4px solid {border_color}; padding-left: 10px; margin-top: 5px;">
                <p><strong>🔬 Scientific Cause:</strong> {data['cause']}</p>
                <p><strong>📋 Symptoms:</strong> {data['symptoms']}</p>
                <hr style="margin: 8px 0; border: 0; border-top: 1px solid #eee;"/>
                <p style="color:#2e7d32;"><strong>🌱 Organic Remedies:</strong><br/>{data['organic']}</p>
                <p style="color:#c62828;"><strong>💊 Chemical Control:</strong><br/>{data['chemical']}</p>
                <p style="color:#1565c0;"><strong>🛡️ Preventative Practices:</strong><br/>{data['prevention']}</p>
            </div>
            """, unsafe_allow_html=True)

    with enc_col1:
        for key in left_keys:
            draw_disease_details(key)
            
    with enc_col2:
        for key in right_keys:
            draw_disease_details(key)

# ================= TAB 3: PLANT CARE MANUALS =================
with tab3:
    st.markdown('<div class="diagnosis-header">🌿 Plant Care & Growing Guides</div>', unsafe_allow_html=True)
    st.write("Ensure optimal plant health from seeding to harvest. Prevent disease occurrence with these agronomic best practices.")
    
    g_tab1, g_tab2, g_tab3 = st.tabs(["Tomato (Solanum lycopersicum)", "Potato (Solanum tuberosum)", "Bell Pepper (Capsicum annuum)"])
    
    with g_tab1:
        st.markdown("""
        ### 🍅 Tomato Growing & Care Manual
        
        Tomatoes are heavy feeders and require proper setup to avoid soil-borne pathogens.
        
        | Parameter | Ideal Target | Rationale |
        |---|---|---|
        | **Sunlight** | 6 - 8 hours full sun | Promotes robust stems and high fruit yield. |
        | **Watering** | 1 - 2 inches per week | Consistent watering prevents blossom end rot. |
        | **Soil pH** | 6.0 - 6.8 | Ensures optimal nutrient bioavailability. |
        | **Spacing** | 24 - 36 inches apart | Vital for airflow to mitigate leaf fungal spores. |
        
        #### 🌟 Crucial Agronomic Practices
        * **Pruning Suckers:** Pinch off non-flowering shoots (suckers) growing in leaf joints to concentrate energy on main stems and improve ventilation.
        * **Soil Mulching:** Apply a 2-inch organic straw or wood mulch cover. This prevents soil water splash-back, which is the primary transmission route for *Early Blight* and *Septoria* spores.
        * **Support Structures:** Never let tomato leaves touch the ground. Install cages or trellis lines immediately at planting.
        """)
        
    with g_tab2:
        st.markdown("""
        ### 🥔 Potato Growing & Care Manual
        
        Potatoes produce crops underground, making root-zone sanitation and soil quality vital.
        
        | Parameter | Ideal Target | Rationale |
        |---|---|---|
        | **Sunlight** | 6 - 8 hours full sun | Maximizes leaf photosynthesis for starch creation. |
        | **Watering** | Even moisture (avoid soggy) | Prevents tuber soft rots and hollow heart. |
        | **Soil Type** | Sandy loam, loose drainage | Allows tubers to expand easily without deformation. |
        | **Soil pH** | 5.0 - 6.0 | Acidic levels actively suppress Potato Scab bacteria. |
        
        #### 🌟 Crucial Agronomic Practices
        * **Hilling:** Every few weeks, draw soil up around the base of the stems (hilling). This covers the growing spuds, preventing sunlight exposure that develops green chlorophyll (associated with toxic *solanine*).
        * **Certified Seed Tubers:** Always purchase certified virus-free seed potatoes. Viruses and late blight are easily passed down from supermarket potato tubers.
        * **Post-Harvest Rotation:** Never plant potatoes where tomatoes, eggplants, or peppers grew in the past 2 seasons.
        """)
        
    with g_tab3:
        st.markdown("""
        ### 🫑 Bell Pepper Growing & Care Manual
        
        Peppers love heat but are susceptible to leaf drop from dry spells or cold winds.
        
        | Parameter | Ideal Target | Rationale |
        |---|---|---|
        | **Sunlight** | 8+ hours (very heat tolerant) | Essential for bell thickness and ripening. |
        | **Watering** | Moderate (let top dry out) | Susceptible to root rot under waterlogged conditions. |
        | **Soil pH** | 6.0 - 6.5 | Supports magnesium and calcium absorption. |
        | **Spacing** | 18 - 24 inches apart | Balancing crop density and ventilation. |
        
        #### 🌟 Crucial Agronomic Practices
        * **Pinching Blooms:** Remove the initial flowers that form when the transplant is small. This directs plant resources into forming a sturdy root network before fruit development.
        * **Calcium Nutrition:** Supply bone meal or calcium spray. Peppers are highly prone to blossom end rot from calcium deficiency, particularly in erratic watering setups.
        * **Windbreaks:** Tall staking supports prevent heavy crop loads from splitting the brittle branches during summer storms.
        """)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #777; font-size: 0.85rem;'>"
    "PlantDocBot Dashboard | Deep Learning ResNet50 Classifier & Agronomy Assistant | virtual internship project"
    "</div>",
    unsafe_allow_html=True
)