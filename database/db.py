# Database query functions for PlantDocBot
# Drop-in replacement for knowledge/treatments.py JSON lookups

import os
from .models import get_connection, DB_PATH, create_tables


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
    """
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
    """
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
