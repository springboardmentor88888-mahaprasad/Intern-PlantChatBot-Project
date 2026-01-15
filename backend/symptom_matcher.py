# Symptom Matcher for Plant Disease ChatBot
#
# Uses Groq API for semantic symptom classification.

from backend.groq_fallback import classify_symptoms_with_groq


def text_diagnosis(query: str) -> str:
    """
    Classify symptoms using Groq API.
    
    Args:
        query: User's text or transcribed speech
        
    Returns:
        Disease key (e.g., "Tomato___Late_blight") or "Unknown"
    """
    if not query or not query.strip():
        return "Unknown"
    
    return classify_symptoms_with_groq(query)


def text_diagnosis_with_score(query: str) -> tuple:
    """
    Classify symptoms and return result with score.
    
    Args:
        query: User's text or transcribed speech
        
    Returns:
        Tuple of (disease_key, match_score)
    """
    if not query or not query.strip():
        return ("Unknown", 0)
    
    result = classify_symptoms_with_groq(query)
    
    if result != "Unknown":
        return (result, 1)
    
    return ("Unknown", 0)
