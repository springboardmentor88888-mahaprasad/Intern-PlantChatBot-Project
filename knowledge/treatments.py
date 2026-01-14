# Knowledge Layer Treatments Module
# Loads disease data from JSON and provides confidence-aware treatment lookup

import json
import os
from datetime import datetime
from pathlib import Path

# Get the directory where this module is located
KNOWLEDGE_DIR = Path(__file__).parent
DISEASES_FILE = KNOWLEDGE_DIR / "diseases.json"
UNKNOWN_CASES_FILE = KNOWLEDGE_DIR / "unknown_cases.json"

# Load diseases at module initialization
_diseases_data = {}
_normalized_lookup = {}


def _normalize_key(key: str) -> str:
    """Normalize disease keys for robust lookup."""
    if not key:
        return ""
    return key.lower().replace("___", "_").replace("__", "_").strip()


def _load_diseases():
    """Load disease data from JSON file."""
    global _diseases_data, _normalized_lookup
    
    if DISEASES_FILE.exists():
        with open(DISEASES_FILE, "r", encoding="utf-8") as f:
            _diseases_data = json.load(f)
        # Build normalized lookup table
        _normalized_lookup = {_normalize_key(k): v for k, v in _diseases_data.items()}
    else:
        _diseases_data = {}
        _normalized_lookup = {}


def _log_unknown_case(disease_key: str, confidence: float = None):
    """Log an unknown disease case for later review."""
    try:
        # Load existing cases
        cases = []
        if UNKNOWN_CASES_FILE.exists():
            with open(UNKNOWN_CASES_FILE, "r", encoding="utf-8") as f:
                cases = json.load(f)
        
        # Add new case
        cases.append({
            "disease_key": disease_key,
            "normalized_key": _normalize_key(disease_key),
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        })
        
        # Save back (keep last 100 entries to prevent file bloat)
        with open(UNKNOWN_CASES_FILE, "w", encoding="utf-8") as f:
            json.dump(cases[-100:], f, indent=2)
    except Exception:
        pass  # Silently fail logging to not disrupt main flow


def get_treatment(disease_key: str, confidence: float = None) -> dict:
    """
    Get treatment information for a disease with confidence-aware handling.
    
    Args:
        disease_key: The disease classification string
        confidence: Model prediction confidence (0.0 to 1.0)
    
    Returns:
        Dictionary with treatment info and confidence_level indicator
    """
    # Ensure data is loaded
    if not _diseases_data:
        _load_diseases()
    
    norm_key = _normalize_key(disease_key)
    disease_info = _normalized_lookup.get(norm_key)
    
    # Determine confidence level
    if confidence is not None:
        if confidence >= 0.8:
            confidence_level = "high"
        elif confidence >= 0.4:
            confidence_level = "moderate"
        else:
            confidence_level = "low"
    else:
        confidence_level = "unknown"
    
    # If disease found in knowledge base
    if disease_info:
        return {
            **disease_info,
            "found": True,
            "confidence_level": confidence_level,
            "confidence_value": confidence
        }
    
    # Disease not found - log and return uncertain response
    _log_unknown_case(disease_key, confidence)
    
    return {
        "disease": disease_key.replace("___", " ").replace("_", " ").title() if disease_key else "Unknown",
        "crop": "Unknown",
        "type": "Unknown",
        "severity": "Unknown",
        "cause": "Not in knowledge base",
        "symptoms": "Unable to determine from available data",
        "treatment": ["Please consult a local agricultural expert for accurate diagnosis"],
        "prevention": ["Regular plant inspection recommended"],
        "found": False,
        "confidence_level": confidence_level,
        "confidence_value": confidence
    }


def get_uncertain_response() -> dict:
    """
    Return a standard response for low-confidence predictions.
    """
    return {
        "disease": "Uncertain",
        "crop": "Unknown",
        "type": "Unknown",
        "severity": "Unknown",
        "cause": "Prediction confidence too low",
        "symptoms": "Could not reliably identify symptoms",
        "treatment": [
            "Please provide a clearer image",
            "Try describing symptoms in more detail",
            "Consider uploading a voice description"
        ],
        "prevention": [],
        "found": False,
        "confidence_level": "low",
        "confidence_value": None
    }


def format_treatment_response(disease_key: str, confidence: float = None) -> str:
    """
    Format treatment information as a readable markdown string.
    
    Args:
        disease_key: The disease classification string
        confidence: Model prediction confidence
    
    Returns:
        Formatted markdown string with treatment information
    """
    info = get_treatment(disease_key, confidence)
    
    response = f"🌱 **{info['disease']}**\n\n"
    
    # Add confidence disclaimer for moderate confidence
    if info.get("confidence_level") == "moderate":
        response += "> ⚠️ *Moderate confidence - please verify with additional symptoms*\n\n"
    
    if info.get("found", True):
        if info.get("crop") and info["crop"] != "Unknown":
            response += f"**Crop:** {info['crop']}  |  "
        if info.get("type") and info["type"] != "Unknown":
            response += f"**Type:** {info['type']}  |  "
        if info.get("severity") and info["severity"] != "Unknown":
            response += f"**Severity:** {info['severity']}\n\n"
        
        response += f"**Cause:** {info['cause']}\n\n"
        response += f"**Symptoms:** {info['symptoms']}\n\n"
    
    response += "**Treatment:**\n"
    for item in info.get('treatment', []):
        response += f"  • {item}\n"
    
    if info.get('prevention'):
        response += "\n**Prevention:**\n"
        for item in info['prevention']:
            response += f"  • {item}\n"
    
    return response


def get_all_disease_keys() -> list:
    """Return all disease keys from the knowledge base."""
    if not _diseases_data:
        _load_diseases()
    return list(_diseases_data.keys())


# Initialize on module load
_load_diseases()
