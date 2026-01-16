def text_diagnosis(symptoms: str):
    text = symptoms.lower()

    if "yellow" in text and "spots" in text:
        return "Tomato___Septoria_leaf_spot"

    elif "brown" in text and ("circles" in text or "rings" or "spots" in text):
        return "Tomato___Early_blight"

    elif "wilting" in text:
        return "Tomato___Late_blight"

    elif "holes" in text or "insects" in text or "pest" in text:
        return "Pest_Attack"

    else:
        return None
