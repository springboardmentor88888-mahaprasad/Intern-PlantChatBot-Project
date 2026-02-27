def text_diagnosis(symptoms: str):
    text = symptoms.lower()

    # Tomato Yellow Leaf Curl Virus (flexible)
    if "yellow" in text and "leaf" in text:
        return "Tomato__Tomato_YellowLeaf__Curl_Virus"

    # Mosaic Virus
    elif "mosaic" in text:
        return "Tomato__Tomato_mosaic_virus"

    # Leaf Mold
    elif "leaf mold" in text or ("mold" in text and "leaf" in text):
        return "Tomato_Leaf_Mold"

    # Septoria Leaf Spot
    elif "septoria" in text or ("leaf" in text and "spot" in text):
        return "Tomato_Septoria_leaf_spot"

    # Spider Mites / Holes
    elif "spider" in text or "mites" in text or "holes" in text:
        return "Tomato_Spider_mites_Two_spotted_spider_mite"

    # Target Spot
    elif "target" in text and "spot" in text:
        return "Tomato__Target_Spot"

    # Tomato Bacterial Spot
    elif "bacterial" in text and "spot" in text:
        return "Tomato_Bacterial_spot"

    # Early / Late Blight
    elif "early blight" in text:
        return "Tomato_Early_blight"
    elif "late blight" in text:
        return "Tomato_Late_blight"

    # Healthy
    elif "healthy" in text:
        return "Tomato_healthy"

    # Pepper
    elif "pepper" in text and "bacterial" in text:
        return "Pepper__bell___Bacterial_spot"
    elif "pepper" in text and "healthy" in text:
        return "Pepper__bell___healthy"

    # Potato
    elif "potato" in text and "early blight" in text:
        return "Potato___Early_blight"
    elif "potato" in text and "late blight" in text:
        return "Potato___Late_blight"
    elif "potato" in text and "healthy" in text:
        return "Potato___healthy"

    # Generic Symptoms
    elif "yellow" in text and "spots" in text:
        return "Tomato__Tomato_YellowLeaf__Curl_Virus"
    elif "brown" in text:
        return "Potato___Early_blight"
    elif "wilting" in text:
        return "Root or Water Stress"
    elif "holes" in text:
        return "Tomato_Spider_mites_Two_spotted_spider_mite"

    else:
        return None
