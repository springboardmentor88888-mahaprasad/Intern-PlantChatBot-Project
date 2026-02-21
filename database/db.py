# Database query functions for PlantDocBot
# Drop-in replacement for knowledge/treatments.py JSON lookups

import os
from .models import get_connection, DB_PATH, create_tables


# ============================================================================
# Model Class Name → Database Disease Key Mapping
# ============================================================================
# The model (Train3, EfficientNetV2-S) was trained on combined PlantDoc +
# PlantVillage datasets. The ImageFolder class names (model output) differ
# from the standardised disease_key values used in seed.py.
#
# This mapping translates every model output class name to its matching
# database disease_key so that treatment lookups always succeed.
# ============================================================================

MODEL_CLASS_TO_DB_KEY = {
    # ---- Apple ----
    "Apple Scab Leaf":              "Apple___Apple_scab",
    "Apple leaf":                   "Apple___healthy",
    "Apple rust leaf":              "Apple___Cedar_apple_rust",
    # ---- Bell Pepper ----
    "Bell_pepper leaf":             "Pepper__bell___healthy",
    "Bell_pepper leaf spot":        "Pepper__bell___Bacterial_spot",
    # ---- Blueberry ----
    "Blueberry leaf":               "Blueberry___healthy",
    # ---- Cherry ----
    "Cherry leaf":                  "Cherry___Powdery_mildew",
    # ---- Corn ----
    "Corn Gray leaf spot":          "Corn___Cercospora_leaf_spot",
    "Corn leaf blight":             "Corn___Northern_Leaf_Blight",
    "Corn rust leaf":               "Corn___Common_rust",
    # ---- Grape ----
    "grape leaf":                   "Grape___healthy",
    "grape leaf black rot":         "Grape___Black_rot",
    # ---- Not a Plant ----
    "Not_a_Plant":                  "Not_a_Plant",
    # ---- Peach ----
    "Peach leaf":                   "Peach___Bacterial_spot",
    # ---- Potato ----
    "Potato leaf early blight":     "Potato___Early_blight",
    "Potato leaf late blight":      "Potato___Late_blight",
    # ---- Raspberry ----
    "Raspberry leaf":               "Raspberry___healthy",
    # ---- Soybean ----
    "Soyabean leaf":                "Soybean___healthy",
    # ---- Squash ----
    "Squash Powdery mildew leaf":   "Squash___Powdery_mildew",
    # ---- Strawberry ----
    "Strawberry leaf":              "Strawberry___Leaf_scorch",
    # ---- Tomato ----
    "Tomato Early blight leaf":     "Tomato___Early_blight",
    "Tomato Septoria leaf spot":    "Tomato___Septoria_leaf_spot",
    "Tomato leaf":                  "Tomato___healthy",
    "Tomato leaf bacterial spot":   "Tomato___Bacterial_spot",
    "Tomato leaf late blight":      "Tomato___Late_blight",
    "Tomato leaf mosaic virus":     "Tomato___Tomato_mosaic_virus",
    "Tomato leaf yellow virus":     "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato mold leaf":             "Tomato___Leaf_Mold",
}


def resolve_disease_key(model_class_name: str) -> str:
    """
    Convert a model output class name to the corresponding database disease_key.

    If the name is already a valid database key (e.g. 'Tomato___Early_blight'),
    it is returned unchanged.  Otherwise the MODEL_CLASS_TO_DB_KEY mapping is
    consulted.  If no mapping exists, the original name is returned as-is so
    that the downstream fallback in get_treatment_info() can still handle it.
    """
    # Direct hit in mapping
    if model_class_name in MODEL_CLASS_TO_DB_KEY:
        return MODEL_CLASS_TO_DB_KEY[model_class_name]
    # Already a valid DB key (e.g. from older code paths)
    return model_class_name


def init_db():
    """Initialize the database (create tables if not exist)."""
    if not os.path.exists(DB_PATH):
        create_tables()
        # Auto-seed if database is fresh
        from .seed import seed_database
        seed_database()
    return True


def _row_to_dict(row):
    """Convert a sqlite3.Row to a plain dict."""
    if row is None:
        return None
    return dict(row)


# ============================================================================
# Disease Queries
# ============================================================================

def get_disease(disease_key: str) -> dict | None:
    """
    Get full disease info by disease_key.
    Returns dict with disease info, symptoms, treatments, prevention.
    """
    conn = get_connection()
    cursor = conn.cursor()

    disease = cursor.execute(
        "SELECT * FROM diseases WHERE disease_key = ?", (disease_key,)
    ).fetchone()

    if not disease:
        conn.close()
        return None

    disease_id = disease["id"]
    result = _row_to_dict(disease)

    # Fetch related data
    result["symptoms"] = [
        r["symptom"] for r in
        cursor.execute("SELECT symptom FROM symptoms WHERE disease_id = ?", (disease_id,)).fetchall()
    ]
    result["treatment"] = [
        r["treatment"] for r in
        cursor.execute("SELECT treatment FROM treatments WHERE disease_id = ?", (disease_id,)).fetchall()
    ]
    result["prevention"] = [
        r["prevention"] for r in
        cursor.execute("SELECT prevention FROM prevention WHERE disease_id = ?", (disease_id,)).fetchall()
    ]

    conn.close()
    return result


def get_all_diseases() -> list[dict]:
    """Get all diseases with their full info."""
    conn = get_connection()
    cursor = conn.cursor()

    diseases = cursor.execute("SELECT * FROM diseases ORDER BY crop, disease").fetchall()
    results = []

    for d in diseases:
        disease_id = d["id"]
        entry = _row_to_dict(d)
        entry["symptoms"] = [
            r["symptom"] for r in
            cursor.execute("SELECT symptom FROM symptoms WHERE disease_id = ?", (disease_id,)).fetchall()
        ]
        entry["treatment"] = [
            r["treatment"] for r in
            cursor.execute("SELECT treatment FROM treatments WHERE disease_id = ?", (disease_id,)).fetchall()
        ]
        entry["prevention"] = [
            r["prevention"] for r in
            cursor.execute("SELECT prevention FROM prevention WHERE disease_id = ?", (disease_id,)).fetchall()
        ]
        results.append(entry)

    conn.close()
    return results


def get_all_disease_keys() -> list[str]:
    """Return all disease keys."""
    conn = get_connection()
    keys = [
        r["disease_key"] for r in
        conn.execute("SELECT disease_key FROM diseases ORDER BY disease_key").fetchall()
    ]
    conn.close()
    return keys


# ============================================================================
# Treatment Response (drop-in replacement for knowledge layer)
# ============================================================================

def get_treatment_info(disease_key: str, confidence: float = None) -> dict:
    """
    Get treatment info — compatible with knowledge/treatments.py format.
    Automatically resolves model class names to database keys.
    """
    disease_key = resolve_disease_key(disease_key)
    info = get_disease(disease_key)

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

    if info:
        return {
            "disease": info["disease"],
            "crop": info["crop"],
            "type": info["type"],
            "severity": info["severity"],
            "cause": info["cause"],
            "symptoms": info["symptoms"],
            "treatment": info["treatment"],
            "prevention": info["prevention"],
            "found": True,
            "confidence_level": confidence_level,
            "confidence_value": confidence
        }

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


def format_treatment_response_db(disease_key: str, confidence: float = None) -> str:
    """
    Format treatment info as markdown — same output as knowledge layer.
    Automatically resolves model class names to database keys.
    """
    disease_key = resolve_disease_key(disease_key)
    info = get_treatment_info(disease_key, confidence)

    response = f"🌱 **{info['disease']}**\n\n"

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
        if isinstance(info.get("symptoms"), list):
            response += f"**Symptoms:** {', '.join(info['symptoms'])}\n\n"
        else:
            response += f"**Symptoms:** {info['symptoms']}\n\n"

    response += "**Treatment:**\n"
    for item in info.get("treatment", []):
        response += f"  • {item}\n"

    if info.get("prevention"):
        response += "\n**Prevention:**\n"
        for item in info["prevention"]:
            response += f"  • {item}\n"

    return response


# ============================================================================
# Unknown Case Logging
# ============================================================================

def log_unknown_case(disease_key: str, confidence: float = None, source: str = None):
    """Log an unknown disease case for later review."""
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO unknown_cases (disease_key, confidence, source) VALUES (?, ?, ?)",
            (disease_key, confidence, source)
        )
        conn.commit()
        conn.close()

    except Exception:
        pass


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
