# treatments.py

TREATMENTS = {
    "Pepper__bell___Bacterial_spot": {
        "cause": "Bacterial infection",
        "treatment": "Use copper-based bactericides and remove infected leaves",
        "prevention": "Use disease-free seeds and avoid overhead irrigation"
    },
    "Pepper__bell___healthy": {
        "cause": "No disease detected",
        "treatment": "No treatment required",
        "prevention": "Maintain proper watering, nutrition, and plant hygiene"
    },
    "Potato___Early_blight": {
        "cause": "Fungal disease",
        "treatment": "Apply chlorothalonil or copper fungicide",
        "prevention": "Practice crop rotation and remove infected leaves"
    },
    "Potato___Late_blight": {
        "cause": "Fungal infection",
        "treatment": "Use systemic fungicides like metalaxyl",
        "prevention": "Avoid wet foliage and maintain spacing between plants"
    },
    "Potato___healthy": {
        "cause": "No disease detected",
        "treatment": "No treatment required",
        "prevention": "Maintain proper watering and nutrition"
    },
    "Tomato_Bacterial_spot": {
        "cause": "Bacterial infection",
        "treatment": "Apply copper-based bactericides",
        "prevention": "Use disease-free seeds and avoid wet leaves"
    },
    "Tomato_Early_blight": {
        "cause": "Fungal disease",
        "treatment": "Use chlorothalonil or mancozeb sprays",
        "prevention": "Crop rotation and remove infected leaves"
    },
    "Tomato_Late_blight": {
        "cause": "Fungal infection",
        "treatment": "Apply systemic fungicides (metalaxyl, copper fungicides)",
        "prevention": "Avoid wet foliage and maintain plant spacing"
    },
    "Tomato_Leaf_Mold": {
        "cause": "Fungal infection",
        "treatment": "Apply fungicides and remove affected leaves",
        "prevention": "Maintain airflow and avoid overhead watering"
    },
    "Tomato_Septoria_leaf_spot": {
        "cause": "Fungal disease",
        "treatment": "Spray with chlorothalonil or mancozeb",
        "prevention": "Remove infected leaves and use crop rotation"
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "cause": "Pest attack (spider mites)",
        "treatment": "Use neem oil or miticides",
        "prevention": "Maintain humidity and regularly check leaves"
    },
    "Tomato__Target_Spot": {
        "cause": "Fungal infection",
        "treatment": "Apply copper fungicides",
        "prevention": "Avoid wetting leaves and practice crop rotation"
    },
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "cause": "Viral infection transmitted by whiteflies",
        "treatment": "No chemical cure; remove infected plants",
        "prevention": "Control whiteflies and use resistant varieties"
    },
    "Tomato__Tomato_mosaic_virus": {
        "cause": "Viral infection",
        "treatment": "Remove infected plants",
        "prevention": "Disinfect tools and avoid handling infected plants"
    },
    "Tomato_healthy": {
        "cause": "No disease detected",
        "treatment": "No treatment required",
        "prevention": "Maintain proper watering, nutrition, and hygiene"
    }
}

def get_treatment(disease_name):
    disease_name = disease_name.strip()
    if disease_name in TREATMENTS:
        return TREATMENTS[disease_name]
    else:
        return {
            "cause": "Unknown disease",
            "treatment": "Consult a local agricultural extension office",
            "prevention": "Maintain good plant hygiene and monitor regularly"
        }
