# Groq API for Semantic Symptom Classification
#
# Primary symptom classifier using Groq LLM.
# Returns only disease key, no explanations.

import os
from dotenv import load_dotenv

# Load environment variables
# Force loading from project root to avoid path issues with Streamlit
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print(f"DEBUG: Loaded .env from {dotenv_path}")
else:
    load_dotenv()
    print("DEBUG: Loaded .env from default location")

# Debug: Print key status (masked)
key = os.environ.get("GROQ_API_KEY")
if key:
    print(f"DEBUG: GROQ_API_KEY loaded: {key[:10]}...")
else:
    print("DEBUG: GROQ_API_KEY NOT FOUND in environment")


def _get_disease_keys():
    """Get valid disease keys from the knowledge base."""
    from knowledge.treatments import _diseases_data
    return list(_diseases_data.keys())


def classify_symptoms_with_groq(symptom_text: str) -> str:
    """
    Send symptom text to Groq API for classification.
    
    Args:
        symptom_text: User's symptom description
        
    Returns:
        Disease key string or "Unknown" if classification fails
    """
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key or api_key == "your_groq_api_key_here":
        return "Unknown"
    
    try:
        from groq import Groq
        
        client = Groq(api_key=api_key)
        disease_keys = _get_disease_keys()
        
        # Build a deterministic classification prompt
        prompt = f"""You are a plant disease classifier. Given the symptom description, return ONLY the matching disease key from this list:

{chr(10).join(disease_keys)}

Symptom description: "{symptom_text}"

Return ONLY the disease key that best matches. No explanation, no formatting, just the key."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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
        print(f"ERROR in classify_symptoms_with_groq: {str(e)}")
        # Check for specific authentication or model errors
        if "401" in str(e):
            return "Error: Invalid API Key"
        if "404" in str(e):
            # Fallback to another model if the primary one fails
            try:
                print("Primary model failed, trying fallback model...")
                response = client.chat.completions.create(
                     model="llama3-70b-8192",
                     messages=[{"role": "user", "content": prompt}],
                     max_tokens=50,
                )
                result = response.choices[0].message.content.strip()
                if result in disease_keys:
                    return result
            except Exception as e2:
                print(f"Fallback model failed: {str(e2)}")
        
        return "Unknown"
