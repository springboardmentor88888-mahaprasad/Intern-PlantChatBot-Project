def text_diagnosis(symptoms: str):
    text = symptoms.lower()

    if "yellow" in text and "spots" in text:
        return "Leaf Spot Disease"
    elif "brown" in text and "circles" in text:
        return "early Blight"
    elif "wilting" in text:
        return "Possible Root or Water Stress"
    elif "holes" in text:
        return "Pest Attack"
    else:
        return "Unknown Disease"