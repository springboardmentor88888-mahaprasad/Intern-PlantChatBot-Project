# backend/chatbot.py
import re
from backend.treatments import TREATMENTS, get_treatment

DISEASE_KEYWORDS = {
    "Pepper__bell___Bacterial_spot": ["pepper", "bell", "bacterial", "spot", "spots", "yellow", "dark brown", "water-soaked", "vesicatoria"],
    "Potato___Early_blight": ["potato", "early", "blight", "spots", "concentric", "rings", "target", "lower leaves", "alternaria"],
    "Potato___Late_blight": ["potato", "late", "blight", "lesions", "fuzzy", "white growth", "water-soaked", "stem", "phytophthora"],
    "Tomato_Bacterial_spot": ["tomato", "bacterial", "spot", "spots", "greasy", "yellow", "drop", "xanthomonas"],
    "Tomato_Early_blight": ["tomato", "early", "blight", "spots", "concentric", "rings", "target", "lower leaves", "alternaria"],
    "Tomato_Late_blight": ["tomato", "late", "blight", "lesions", "fuzzy", "white growth", "water-soaked", "stem", "phytophthora"],
    "Tomato_Leaf_Mold": ["tomato", "mold", "velvet", "fuzzy", "olive", "yellow spots", "green spots", "passalora"],
    "Tomato_Septoria_leaf_spot": ["tomato", "septoria", "spot", "spots", "dark margin", "grey center", "specks", "black dots", "lycopersici"],
    "Tomato_Spider_mites_Two_spotted_spider_mite": ["tomato", "spider", "mite", "mites", "web", "webbing", "stippling", "dots", "specks", "tetranychus"],
    "Tomato__Target_Spot": ["tomato", "target", "spot", "spots", "rings", "lesions", "cassiicola"],
    "Tomato__Tomato_YellowLeaf__Curl_Virus": ["tomato", "yellow", "curl", "curling", "crumple", "stunt", "stunted", "virus", "whitefly", "curl virus"],
    "Tomato__Tomato_mosaic_virus": ["tomato", "mosaic", "mottle", "mottling", "blister", "fern", "virus", "tobacco"]
}

def text_diagnosis(symptoms: str) -> str:
    """
    Analyzes symptoms string using keyword frequency scoring and returns the key of the best matched disease.
    """
    if not symptoms or len(symptoms.strip()) < 3:
        return "Unknown Disease"
    
    text = symptoms.lower()
    scores = {k: 0 for k in DISEASE_KEYWORDS.keys()}
    
    # Check for plant type first to narrow down
    has_tomato = any(w in text for w in ["tomato", "tomatoes"])
    has_potato = any(w in text for w in ["potato", "potatoes"])
    has_pepper = any(w in text for w in ["pepper", "peppers", "bell"])

    for disease, keywords in DISEASE_KEYWORDS.items():
        # Enforce plant specificity rules
        if "tomato" in disease.lower() and has_tomato:
            scores[disease] += 3
        elif "potato" in disease.lower() and has_potato:
            scores[disease] += 3
        elif "pepper" in disease.lower() and has_pepper:
            scores[disease] += 3
            
        # Match keywords
        for kw in keywords:
            if kw in text:
                scores[disease] += 2
                # Extra boost for exact phrase match
                if re.search(r'\b' + re.escape(kw) + r'\b', text):
                    scores[disease] += 1

    # Find top score
    best_disease = max(scores, key=scores.get)
    if scores[best_disease] > 2:  # Must have at least a minimum match score
        return best_disease
    return "Unknown Disease"


def get_chat_response(message: str, uploaded_diagnosis: str = None) -> dict:
    """
    Generates a conversational response based on message content, plant facts, and diagnosis context.
    Returns:
        dict: {
            "response": str (markdown formatted response),
            "suggestions": list of str (quick replies for buttons)
        }
    """
    text = message.lower().strip()
    
    # 1. Greetings
    if any(greet in text for greet in ["hi", "hello", "hey", "greetings", "good morning", "good afternoon"]):
        resp = (
            "🌿 **Hello! Welcome to the PlantDocBot Chat.**\n\n"
            "I can help you diagnose diseases on **Tomato, Potato, and Pepper** plants. "
            "You can upload a leaf image above for instant AI diagnosis, or describe your plant's symptoms here.\n\n"
            "**What would you like to do?**"
        )
        return {
            "response": resp,
            "suggestions": ["Diagnose symptoms", "How to grow Tomatoes", "How to grow Potatoes", "How to grow Peppers"]
        }
        
    # 2. General Plant Care Requests
    if "grow tomato" in text or "care for tomato" in text:
        return {
            "response": (
                "🍅 **Tomato Care Guide Quick Tips:**\n\n"
                "- **Sunlight:** Tomatoes need at least 6-8 hours of direct sunlight daily.\n"
                "- **Watering:** Water deeply and consistently at the roots. Avoid getting the leaves wet to prevent fungal diseases.\n"
                "- **Soil:** Well-drained, sandy loam soil with a pH between 6.0 and 6.8 is ideal.\n"
                "- **Support:** Use stakes or tomato cages early to keep the foliage off the ground.\n\n"
                "Would you like to know about common tomato diseases?"
            ),
            "suggestions": ["Tomato Diseases", "Organic Pest Control", "Upload Leaf Image"]
        }
        
    if "grow potato" in text or "care for potato" in text:
        return {
            "response": (
                "🥔 **Potato Care Guide Quick Tips:**\n\n"
                "- **Sunlight:** Full sun is best (6-8 hours).\n"
                "- **Watering:** Keep soil evenly moist, especially when flowering. Avoid waterlogging which causes tuber rot.\n"
                "- **Hilling:** Draw soil up around the stems as they grow to protect developing tubers from sun exposure (which turns them green and toxic).\n"
                "- **Soil:** Loose, acidic soil (pH 5.0 to 6.0) helps prevent Potato Scab disease.\n\n"
                "Would you like to know about Early or Late Potato Blight?"
            ),
            "suggestions": ["Potato Blight Differences", "Potato Care Guide", "Upload Leaf Image"]
        }
        
    if "grow pepper" in text or "care for pepper" in text:
        return {
            "response": (
                "🫑 **Bell Pepper Care Guide Quick Tips:**\n\n"
                "- **Sunlight:** Peppers love heat and need 6-8 hours of full sun.\n"
                "- **Watering:** Water moderately. Let the top inch of soil dry out between waterings. Use mulch to maintain even moisture.\n"
                "- **Spacing:** Plant 18-24 inches apart to ensure good airflow.\n"
                "- **Fertilizer:** Use a balanced organic fertilizer, but avoid excessive nitrogen which yields leaves instead of peppers.\n\n"
                "Would you like to learn about Bell Pepper Bacterial Spot?"
            ),
            "suggestions": ["Pepper Bacterial Spot", "Pepper Care Guide", "Upload Leaf Image"]
        }

    # 3. Requesting Info on Uploaded Diagnosis
    if any(x in text for x in ["uploaded image", "my image", "what was the diagnosis", "explain prediction"]):
        if uploaded_diagnosis and uploaded_diagnosis != "Unknown Disease":
            t = get_treatment(uploaded_diagnosis)
            return {
                "response": (
                    f"🔍 Based on your uploaded image, the AI detected **{t['common_name']}**.\n\n"
                    f"**Cause:** {t['cause']}\n\n"
                    f"**Primary Symptoms:** {t['symptoms']}\n\n"
                    f"Would you like to see the **Organic** or **Chemical** treatments for this?"
                ),
                "suggestions": ["Organic treatments", "Chemical treatments", "Prevention tips"]
            }
        else:
            return {
                "response": "📷 I don't see an uploaded leaf image yet. Please upload one in the section above, and I will instantly analyze it for you!",
                "suggestions": ["Diagnose symptoms by text", "General plant care"]
            }

    # 4. Organic / Chemical Treatment requests
    if "organic" in text and uploaded_diagnosis:
        t = get_treatment(uploaded_diagnosis)
        return {
            "response": f"🌱 **Organic Remedies for {t['common_name']}:**\n\n{t['organic']}",
            "suggestions": ["Chemical treatments", "Prevention tips", "Start over"]
        }
        
    if "chemical" in text and uploaded_diagnosis:
        t = get_treatment(uploaded_diagnosis)
        return {
            "response": f"💊 **Chemical Treatments for {t['common_name']}:**\n\n{t['chemical']}",
            "suggestions": ["Organic treatments", "Prevention tips", "Start over"]
        }
        
    if "prevention" in text and uploaded_diagnosis:
        t = get_treatment(uploaded_diagnosis)
        return {
            "response": f"🛡️ **Prevention Strategies for {t['common_name']}:**\n\n{t['prevention']}",
            "suggestions": ["Organic treatments", "Chemical treatments", "Start over"]
        }

    # 5. Comparing Potato Blights
    if "blight differences" in text or "early vs late blight" in text:
        return {
            "response": (
                "📊 **Early Blight vs. Late Blight: The Key Differences**\n\n"
                "1. **Early Blight (*Alternaria solani*):**\n"
                "   - **Symptom:** Small, dark brown spots on *older leaves* first, developing concentric rings like a target board.\n"
                "   - **Condition:** Occurs in warm, humid weather. Spreads slowly.\n\n"
                "2. **Late Blight (*Phytophthora infestans*):**\n"
                "   - **Symptom:** Large water-soaked blue-grey lesions on leaves/stems, with white fuzzy mold underneath when damp. Can kill plants in days.\n"
                "   - **Condition:** Thrives in cool, wet, foggy conditions. Spreads very rapidly.\n\n"
                "Both require fungicides and leaf pruning, but Late Blight requires immediate removal of infected plants to protect nearby crops."
            ),
            "suggestions": ["Potato Early Blight treatment", "Potato Late Blight treatment", "Go Back"]
        }

    # 6. Specific disease info requests
    for key, keywords in DISEASE_KEYWORDS.items():
        common_name_clean = key.replace("___", " - ").replace("__", " - ").replace("_", " ").lower()
        # If user types the disease name
        if any(kw in text for kw in keywords) and len([w for w in keywords if w in text]) >= 2:
            t = get_treatment(key)
            return {
                "response": (
                    f"🌿 **Information on {t['common_name']}:**\n\n"
                    f"🔬 **Cause:** {t['cause']}\n"
                    f"📋 **Symptoms:** {t['symptoms']}\n\n"
                    f"🌱 **Organic Remedies:** {t['organic']}\n\n"
                    f"💊 **Chemical Control:** {t['chemical']}\n\n"
                    f"🛡️ **Prevention:** {t['prevention']}"
                ),
                "suggestions": ["Tomato Diseases", "Potato Diseases", "Pepper Diseases"]
            }

    # 7. Fallback symptom search based on text_diagnosis
    detected_key = text_diagnosis(message)
    if detected_key != "Unknown Disease":
        t = get_treatment(detected_key)
        return {
            "response": (
                f"🧐 Based on your symptom description, I suspect it could be **{t['common_name']}**.\n\n"
                f"🔬 **Cause:** {t['cause']}\n"
                f"📋 **Symptoms:** {t['symptoms']}\n\n"
                f"Would you like to know the treatment options?"
            ),
            "suggestions": [f"Organic for {t['common_name']}", f"Chemical for {t['common_name']}", "Prevention tips"]
        }
        
    # 8. Organic or Chemical for dynamic diseases
    if "organic for" in text or "chemical for" in text or "prevention for" in text:
        # Extract disease name
        match_key = None
        for key in DISEASE_KEYWORDS.keys():
            clean = key.replace("___", " - ").replace("__", " - ").replace("_", " ").lower()
            # Clean up the spaces
            clean_words = clean.split()
            if all(w in text for w in clean_words if len(w) > 2):
                match_key = key
                break
        if match_key:
            t = get_treatment(match_key)
            if "organic" in text:
                return {"response": f"🌱 **Organic Remedies for {t['common_name']}:**\n\n{t['organic']}", "suggestions": ["Prevention", "Go Back"]}
            elif "chemical" in text:
                return {"response": f"💊 **Chemical Treatments for {t['common_name']}:**\n\n{t['chemical']}", "suggestions": ["Prevention", "Go Back"]}
            else:
                return {"response": f"🛡️ **Prevention Strategies for {t['common_name']}:**\n\n{t['prevention']}", "suggestions": ["Organic Remedies", "Go Back"]}

    # Default fallback
    return {
        "response": (
            "🤖 **I'm not quite sure about those symptoms or question.**\n\n"
            "Could you specify if it's on a **Tomato, Potato, or Pepper** plant, and describe the leaves (e.g., yellow spots, white powder, wilting, curling)?"
        ),
        "suggestions": ["Tomato Care", "Potato Care", "Pepper Care", "Identify Symptoms"]
    }