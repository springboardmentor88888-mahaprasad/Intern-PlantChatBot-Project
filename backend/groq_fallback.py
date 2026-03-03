# Groq API for Semantic Symptom Classification
#
# Primary symptom classifier using Groq LLM.
# Returns only disease key, no explanations.

import os
import logging
from config import GROQ_API_KEY, GROQ_MODEL, GROQ_FALLBACK_MODEL

logger = logging.getLogger(__name__)


def _get_disease_keys():
    """Get valid disease keys from the knowledge base."""
    from database import get_all_disease_keys
    return get_all_disease_keys()


def classify_symptoms_with_groq(symptom_text: str) -> str:
    """
    Send symptom text to Groq API for classification.

    Args:
        symptom_text: User's symptom description

    Returns:
        Disease key string or "Unknown" if classification fails
    """
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        logger.warning("GROQ_API_KEY not configured")
        return "Unknown"

    try:
        from groq import Groq

        client = Groq(api_key=GROQ_API_KEY)
        disease_keys = _get_disease_keys()

        prompt = f"""You are a plant disease classifier. Given the symptom description, return ONLY the matching disease key from this list:

{chr(10).join(disease_keys)}

Symptom description: "{symptom_text}"

Return ONLY the disease key that best matches. No explanation, no formatting, just the key."""

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
        )

        result = response.choices[0].message.content.strip()

        # Validate the response is a valid disease key
        if result in disease_keys:
            return result

        # Try to find a partial match
        for key in disease_keys:
            if key.lower() in result.lower() or result.lower() in key.lower():
                return key

        return "Unknown"

    except Exception as e:
        logger.error(f"Groq classification failed: {e}")
        if "401" in str(e):
            return "Error: Invalid API Key"
        if "404" in str(e):
            try:
                logger.info(f"Primary model failed, trying fallback: {GROQ_FALLBACK_MODEL}")
                response = client.chat.completions.create(
                    model=GROQ_FALLBACK_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=50,
                )
                result = response.choices[0].message.content.strip()
                if result in disease_keys:
                    return result
            except Exception as e2:
                logger.error(f"Fallback model failed: {e2}")

        return "Unknown"
