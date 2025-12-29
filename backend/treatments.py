# backend/treatments.py

def get_treatment(disease_name):
    treatments = {

        "Apple Scab": {
            "cause": "Fungal infection caused by Venturia inaequalis.",
            "treatment": [
                "Apply fungicides like captan or myclobutanil",
                "Remove infected leaves",
                "Prune trees for air circulation"
            ],
            "prevention": [
                "Use disease-resistant varieties",
                "Avoid overhead watering",
                "Maintain orchard hygiene"
            ]
        },

        "Apple Black Rot": {
            "cause": "Fungal disease caused by Botryosphaeria obtusa.",
            "treatment": [
                "Remove infected fruits and branches",
                "Apply copper-based fungicides",
                "Disinfect pruning tools"
            ],
            "prevention": [
                "Proper pruning",
                "Avoid plant stress",
                "Remove dead wood"
            ]
        },

        "Potato Early Blight": {
            "cause": "Fungal disease caused by Alternaria solani.",
            "treatment": [
                "Apply chlorothalonil fungicide",
                "Remove infected leaves",
                "Ensure proper fertilization"
            ],
            "prevention": [
                "Crop rotation",
                "Use certified seeds",
                "Avoid overhead irrigation"
            ]
        },

        "Potato Late Blight": {
            "cause": "Caused by Phytophthora infestans.",
            "treatment": [
                "Apply systemic fungicides",
                "Destroy infected plants",
                "Reduce field humidity"
            ],
            "prevention": [
                "Plant resistant varieties",
                "Avoid water stagnation",
                "Monitor weather conditions"
            ]
        },

        "Tomato Early Blight": {
            "cause": "Fungal infection caused by Alternaria solani.",
            "treatment": [
                "Use fungicides like mancozeb",
                "Remove infected foliage",
                "Provide adequate spacing"
            ],
            "prevention": [
                "Mulching",
                "Crop rotation",
                "Avoid wet leaves"
            ]
        },

        "Tomato Late Blight": {
            "cause": "Water mold infection by Phytophthora infestans.",
            "treatment": [
                "Apply copper fungicide",
                "Remove infected plants",
                "Improve air circulation"
            ],
            "prevention": [
                "Use certified seeds",
                "Avoid overcrowding",
                "Regular field inspection"
            ]
        },

        "Tomato Healthy": {
            "cause": "No disease detected.",
            "treatment": [
                "No treatment required"
            ],
            "prevention": [
                "Maintain regular watering",
                "Apply balanced fertilizers",
                "Monitor plant health"
            ]
        }
    }

    return treatments.get(
        disease_name,
        {
            "cause": "Information not available.",
            "treatment": ["Consult agricultural expert"],
            "prevention": ["Follow good farming practices"]
        }
    )
