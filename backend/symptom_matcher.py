# Rule-based symptom matching for Plant Disease ChatBot

from knowledge.treatments import _diseases_data as TREATMENTS

# Mapping of symptoms and keywords to disease keys

SYMPTOM_MAP = {
    # Tomato___Late_blight
    "late blight": "Tomato___Late_blight",
    "brown spots": "Tomato___Late_blight",
    "dark brown spots": "Tomato___Late_blight",
    "white fuzzy": "Tomato___Late_blight",
    "fuzzy growth": "Tomato___Late_blight",
    "underside": "Tomato___Late_blight",
    
    # Tomato___Early_blight
    "early blight": "Tomato___Early_blight",
    "concentric rings": "Tomato___Early_blight",
    "yellowing around spots": "Tomato___Early_blight",
    "target spots": "Tomato___Early_blight",
    
    # Tomato___Leaf_Mold
    "leaf mold": "Tomato___Leaf_Mold",
    "yellow spots": "Tomato___Leaf_Mold",
    "olive-green": "Tomato___Leaf_Mold",
    "olive green": "Tomato___Leaf_Mold",
    "fuzzy underneath": "Tomato___Leaf_Mold",
    
    # Tomato___Septoria_leaf_spot
    "septoria": "Tomato___Septoria_leaf_spot",
    "circular spots": "Tomato___Septoria_leaf_spot",
    "dark borders": "Tomato___Septoria_leaf_spot",
    "gray centers": "Tomato___Septoria_leaf_spot",
    "black dots": "Tomato___Septoria_leaf_spot",
    
    # Tomato___Bacterial_spot
    "bacterial spot": "Tomato___Bacterial_spot",
    "scab-like": "Tomato___Bacterial_spot",
    "raised spots": "Tomato___Bacterial_spot",
    "bacterial": "Tomato___Bacterial_spot",
    
    # Tomato___YellowLeaf__Curl_Virus
    "yellow leaf curl": "Tomato___YellowLeaf__Curl_Virus",
    "upward curling": "Tomato___YellowLeaf__Curl_Virus",
    "curling leaves": "Tomato___YellowLeaf__Curl_Virus",
    "veins": "Tomato___YellowLeaf__Curl_Virus",
    "stunted": "Tomato___YellowLeaf__Curl_Virus",
    
    # Tomato___mosaic_virus
    "mosaic": "Tomato___mosaic_virus",
    "mottled": "Tomato___mosaic_virus",
    "distorted": "Tomato___mosaic_virus",
    "reduced yield": "Tomato___mosaic_virus",
    
    # Tomato___healthy
    "healthy": "Tomato___healthy",
    "no symptoms": "Tomato___healthy",
    "looks fine": "Tomato___healthy"
}

def text_diagnosis(query: str) -> str:
    """
    Map spoken/written symptoms to a disease key.
    
    Args:
        query: User's text or transcribed speech
        
    Returns:
        Disease key string (e.g., "Tomato___Late_blight") or "Unknown"
    """
    if not query:
        return "Unknown"
        
    query_lower = query.lower().strip()
    
    # Score each disease based on keyword matches
    scores = {key: 0 for key in TREATMENTS.keys()}
    scores["Unknown"] = 0
    
    for symptom, disease_key in SYMPTOM_MAP.items():
        if symptom in query_lower:
            scores[disease_key] += 1
            
    # Find the disease with the highest score
    max_score = 0
    best_match = "Unknown"
    
    for disease_key, score in scores.items():
        if score > max_score:
            max_score = score
            best_match = disease_key
            
    # Fallback to general unknown if no keywords matched
    if max_score == 0:
        return "Unknown"
        
    return best_match
