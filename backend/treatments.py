#backend/treatments.py

TREATMENTS= {
   "Tomato__Late_blight": "Use copper-based fungicide, Avold overhead satering.",
   "Tomato__Early_blight": "Remove infected leaves. Apply mancozeb or chlorotiuion.",
   "Potato__Late_blight" : "Spray fungicide and remove infected plants inmediately.",
   "Potato__Early_blight": "Apply appropriate fungicide and practice crop rotation.async",
   "Pepper__Bacterial_spot": "Use disease-free seeds and copper sprays.",
   "Healthy": "No treatment needed. Maintain proper irrigation and nutrition."
}

def get_treatment(disease_name):
    return TREATMENTS.get(
        disease_name,
        "No specific treatment found. Consult an agricultural expert."
    )
