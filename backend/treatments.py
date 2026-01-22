TREATMENTS = {
    "Tomato___Late_blight": {
        "cause": "Fungal infection",
        "treatment": "Use copper-based fungicide",
        "prevention": "Avoid overhead watering"
    },
    "Potato___Early_blight": {
        "cause": "Fungal disease",
        "treatment": "Apply chlorothalonil spray",
        "prevention": "Crop rotation"
    },
    "Tomato___Septoria_leaf_spot": {
        "cause": "Fungal infection",
        "treatment": "Apply copper fungicide or chlorothalonil",
        "prevention": "Avoid wet leaves and remove plant debris"
    },
     "Potato___Early_blight": {
        "cause": "Fungal disease",
        "treatment": "Apply chlorothalonil or azoxystrobin",
        "prevention": "Crop rotation and proper spacing"
    },
     "Potato___Late_blight": {
        "cause": "Severe fungal infection",
        "treatment": "Use fungicides containing metalaxyl",
        "prevention": "Use certified seeds and destroy infected plants"
    },
     "Pepper___Bacterial_spot": {
        "cause": "Bacterial infection",
        "treatment": "Apply copper-based bactericides",
        "prevention": "Use disease-free seeds and avoid overhead irrigation"
    },
      "Corn___Common_rust": {
        "cause": "Fungal disease",
        "treatment": "Apply fungicides like propiconazole",
        "prevention": "Grow resistant varieties and monitor humidity"
    },
      "Apple___Scab": {
        "cause": "Fungal infection (Venturia inaequalis)",
        "treatment": "Apply sulfur or myclobutanil fungicide",
        "prevention": "Prune trees and remove fallen leaves"
    },
     "Grape___Black_rot": {
        "cause": "Fungal disease",
        "treatment": "Apply mancozeb or myclobutanil",
        "prevention": "Remove infected fruit and improve airflow"
    },

    "Healthy": {
        "cause": "No disease detected",
        "treatment": "No treatment required",
        "prevention": "Continue regular monitoring and proper plant care"
    }
}
def get_treatment(disease_name):
    return TREATMENTS.get(
        disease_name,
        {
            "cause": "Unknown disease",
            "treatment": "Consult a local agricultural extension office",
            "prevention": "Maintain good plant hygiene and monitor regularly"
        }
    )
  
