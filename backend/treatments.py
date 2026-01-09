# backend/treatments.py
TREATMENTS = {
"Tomato___Late_blight": "Use copper-based fungicide. Avoid overhead watering.",
"Tomato___Early_blight": "Remove infected leaves. Apply mancozeb or chlorothalonil.",
"Potato___Late_blight": "Spray fungicide and remove infected plants immediately.",
"Potato___Early_blight": "Apply appropriate fungicide and practice crop rotation.",
"Pepper___Bacterial_spot": "Use disease-free seeds and copper sprays.",
"Healthy": "No treatment needed. Maintain proper irrigation and nutrition."
}

def get_treatment(disease_name):
    return TREATMENTS.get(
        disease_name, 
        "No specific treatment found. Consult an agricultural expert.")
