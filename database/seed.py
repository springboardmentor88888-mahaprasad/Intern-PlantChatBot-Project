# Seed script — populates the database with all 16 PLANTVILLAGE_CLASSES
# Run once: python -m database.seed

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import create_tables, get_connection

# ============================================================================
# All 16 PlantVillage classes with complete disease information
# ============================================================================
SEED_DATA = [
    {
        "disease_key": "Pepper__bell___Bacterial_spot",
        "disease": "Bacterial Spot",
        "crop": "Pepper (Bell)",
        "type": "Bacterial",
        "severity": "Medium",
        "cause": "Bacteria Xanthomonas campestris pv. vesicatoria",
        "symptoms": [
            "small dark water-soaked spots on leaves",
            "raised bumps on fruit",
            "spots with yellow halo",
            "leaves dropping prematurely",
            "scab-like lesions on fruit",
            "leaf edges browning"
        ],
        "treatment": [
            "Remove and destroy infected plant parts",
            "Apply copper-based bactericides",
            "Use disease-free seeds and transplants",
            "Avoid overhead irrigation"
        ],
        "prevention": [
            "Use certified disease-free seeds",
            "Practice crop rotation (2-3 years)",
            "Disinfect tools between plants",
            "Avoid working with wet plants"
        ]
    },
    {
        "disease_key": "Pepper__bell___healthy",
        "disease": "Healthy Plant",
        "crop": "Pepper (Bell)",
        "type": "None",
        "severity": "None",
        "cause": "N/A",
        "symptoms": [
            "no disease",
            "plant looks good",
            "healthy green leaves",
            "normal growth"
        ],
        "treatment": [
            "Continue regular care and maintenance",
            "Monitor for early signs of disease",
            "Maintain proper watering schedule"
        ],
        "prevention": [
            "Regular inspection of plants",
            "Proper nutrition and watering",
            "Good garden hygiene"
        ]
    },
    {
        "disease_key": "Potato___Early_blight",
        "disease": "Early Blight",
        "crop": "Potato",
        "type": "Fungal",
        "severity": "Medium",
        "cause": "Fungus Alternaria solani",
        "symptoms": [
            "dark concentric rings on leaves",
            "target-shaped spots",
            "lower leaves affected first",
            "yellowing around spots",
            "leaf drop",
            "brown lesions on tubers"
        ],
        "treatment": [
            "Remove infected leaves immediately",
            "Apply fungicides containing chlorothalonil or mancozeb",
            "Ensure proper plant spacing for air flow",
            "Hill up soil around plants"
        ],
        "prevention": [
            "Use certified disease-free seed potatoes",
            "Practice 2-3 year crop rotation",
            "Remove plant debris after harvest",
            "Maintain adequate plant nutrition"
        ]
    },
    {
        "disease_key": "Potato___Late_blight",
        "disease": "Late Blight",
        "crop": "Potato",
        "type": "Fungal",
        "severity": "High",
        "cause": "Oomycete Phytophthora infestans",
        "symptoms": [
            "dark water-soaked spots on leaves",
            "white fuzzy mold on leaf underside",
            "stems turning dark brown",
            "rapid plant collapse",
            "tuber rot with reddish-brown discoloration",
            "foul smell from infected tubers"
        ],
        "treatment": [
            "Remove and destroy all infected plants",
            "Apply copper-based fungicides or mancozeb",
            "Harvest tubers in dry conditions",
            "Do not wash tubers before storage"
        ],
        "prevention": [
            "Plant resistant varieties",
            "Avoid overhead watering",
            "Ensure good drainage",
            "Destroy volunteer potato plants"
        ]
    },
    {
        "disease_key": "Potato___healthy",
        "disease": "Healthy Plant",
        "crop": "Potato",
        "type": "None",
        "severity": "None",
        "cause": "N/A",
        "symptoms": [
            "no disease",
            "plant looks good",
            "healthy green foliage",
            "normal tuber development"
        ],
        "treatment": [
            "Continue regular care and maintenance",
            "Monitor for early signs of disease",
            "Maintain proper hilling schedule"
        ],
        "prevention": [
            "Regular inspection of plants",
            "Proper nutrition and watering",
            "Good garden hygiene",
            "Use certified seed potatoes"
        ]
    },
    {
        "disease_key": "Tomato___Bacterial_spot",
        "disease": "Bacterial Spot",
        "crop": "Tomato",
        "type": "Bacterial",
        "severity": "Medium",
        "cause": "Bacteria Xanthomonas species",
        "symptoms": [
            "small dark spots on leaves",
            "raised bumps on fruit",
            "scab like spots",
            "water soaked lesions",
            "spots with yellow halo",
            "fruit has rough spots",
            "leaves look burned",
            "oily looking spots",
            "spots spreading fast"
        ],
        "treatment": [
            "Remove infected plant material",
            "Apply copper-based bactericides",
            "Avoid overhead irrigation",
            "Do not work with wet plants"
        ],
        "prevention": [
            "Use certified disease-free seeds",
            "Practice crop rotation",
            "Disinfect tools between plants",
            "Use resistant varieties when available"
        ]
    },
    {
        "disease_key": "Tomato___Early_blight",
        "disease": "Early Blight",
        "crop": "Tomato",
        "type": "Fungal",
        "severity": "Medium",
        "cause": "Fungus Alternaria solani",
        "symptoms": [
            "dark spots with rings",
            "target spots",
            "concentric rings",
            "bull's eye pattern",
            "lower leaves yellowing",
            "yellow halo around spots",
            "leaves drying from bottom",
            "old leaves affected first",
            "brown circular spots"
        ],
        "treatment": [
            "Remove affected leaves immediately",
            "Apply fungicides containing chlorothalonil or copper",
            "Mulch around plants to prevent soil splash",
            "Stake plants to improve air flow"
        ],
        "prevention": [
            "Use certified disease-free seeds",
            "Practice crop rotation",
            "Maintain adequate plant nutrition",
            "Remove plant debris after harvest"
        ]
    },
    {
        "disease_key": "Tomato___Late_blight",
        "disease": "Late Blight",
        "crop": "Tomato",
        "type": "Fungal",
        "severity": "High",
        "cause": "Fungus Phytophthora infestans",
        "symptoms": [
            "dark brown spots",
            "brown patches on leaves",
            "white fuzzy growth",
            "white mold under leaves",
            "leaves turning black",
            "stem rotting",
            "plant dying fast",
            "wet rot smell",
            "leaves wilting suddenly"
        ],
        "treatment": [
            "Remove and destroy infected plant parts",
            "Apply copper-based fungicides",
            "Improve air circulation around plants",
            "Avoid overhead watering",
            "Use resistant varieties"
        ],
        "prevention": [
            "Plant resistant varieties",
            "Ensure proper spacing between plants",
            "Water at the base of plants in the morning",
            "Rotate crops yearly"
        ]
    },
    {
        "disease_key": "Tomato___Leaf_Mold",
        "disease": "Leaf Mold",
        "crop": "Tomato",
        "type": "Fungal",
        "severity": "Medium",
        "cause": "Fungus Passalora fulva",
        "symptoms": [
            "yellow spots on top of leaf",
            "fuzzy growth underneath",
            "olive green mold",
            "brown fuzzy patches",
            "leaves turning yellow",
            "greenhouse disease",
            "humid weather problem",
            "leaves curling down",
            "velvety coating under leaf"
        ],
        "treatment": [
            "Improve ventilation in greenhouses",
            "Apply fungicides if severe",
            "Remove heavily infected leaves",
            "Reduce humidity levels"
        ],
        "prevention": [
            "Use resistant varieties",
            "Maintain good air circulation",
            "Avoid wetting leaves during irrigation",
            "Keep humidity below 85%"
        ]
    },
    {
        "disease_key": "Tomato___Septoria_leaf_spot",
        "disease": "Septoria Leaf Spot",
        "crop": "Tomato",
        "type": "Fungal",
        "severity": "Medium",
        "cause": "Fungus Septoria lycopersici",
        "symptoms": [
            "small round spots",
            "tiny black dots in spots",
            "gray center spots",
            "dark border around spots",
            "many small holes",
            "leaves look speckled",
            "spots with dark edges",
            "lower leaves affected",
            "leaves falling off"
        ],
        "treatment": [
            "Remove infected leaves",
            "Apply copper-based or chlorothalonil fungicides",
            "Avoid working with wet plants",
            "Improve air circulation"
        ],
        "prevention": [
            "Use disease-free seeds and transplants",
            "Rotate crops for 2-3 years",
            "Mulch to prevent soil splash",
            "Water at plant base"
        ]
    },
    {
        "disease_key": "Tomato___Spider_mites Two-spotted_spider_mite",
        "disease": "Spider Mites (Two-spotted)",
        "crop": "Tomato",
        "type": "Pest",
        "severity": "Medium",
        "cause": "Two-spotted spider mite (Tetranychus urticae)",
        "symptoms": [
            "tiny yellow or white spots on leaves",
            "fine webbing on undersides of leaves",
            "leaves turning bronze or brown",
            "stippled or speckled appearance",
            "leaf curling and dropping",
            "plant looks dusty",
            "tiny moving dots on leaf underside"
        ],
        "treatment": [
            "Spray plants with strong water jets to dislodge mites",
            "Apply insecticidal soap or neem oil",
            "Use miticides for severe infestations",
            "Introduce predatory mites (Phytoseiulus persimilis)"
        ],
        "prevention": [
            "Keep plants well-watered (mites prefer dry conditions)",
            "Avoid excessive nitrogen fertilization",
            "Monitor regularly with a hand lens",
            "Remove heavily infested leaves"
        ]
    },
    {
        "disease_key": "Tomato___Target_Spot",
        "disease": "Target Spot",
        "crop": "Tomato",
        "type": "Fungal",
        "severity": "Medium",
        "cause": "Fungus Corynespora cassiicola",
        "symptoms": [
            "brown spots with concentric rings",
            "target-like pattern on leaves",
            "spots on stems and fruit",
            "lower leaves affected first",
            "large irregular lesions",
            "premature leaf drop",
            "fruit lesions with sunken centers"
        ],
        "treatment": [
            "Remove and destroy infected plant debris",
            "Apply fungicides (chlorothalonil or copper-based)",
            "Improve air circulation with proper spacing",
            "Avoid overhead watering"
        ],
        "prevention": [
            "Practice crop rotation",
            "Use resistant varieties if available",
            "Maintain proper plant spacing",
            "Remove crop residue after harvest"
        ]
    },
    {
        "disease_key": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "disease": "Yellow Leaf Curl Virus",
        "crop": "Tomato",
        "type": "Viral",
        "severity": "High",
        "cause": "Tomato yellow leaf curl virus (TYLCV), transmitted by whiteflies",
        "symptoms": [
            "leaves curling up",
            "yellow edges on leaves",
            "plant not growing",
            "stunted growth",
            "small leaves",
            "leaves cupping upward",
            "yellow between veins",
            "whiteflies on plant",
            "plant looks weak",
            "flowers dropping"
        ],
        "treatment": [
            "Remove and destroy infected plants",
            "Control whitefly populations with insecticides or sticky traps",
            "Use reflective mulches to deter whiteflies",
            "No cure once infected - prevention is key"
        ],
        "prevention": [
            "Use virus-resistant varieties",
            "Install insect-proof netting",
            "Control whitefly populations early",
            "Remove weeds that harbor whiteflies"
        ]
    },
    {
        "disease_key": "Tomato___Tomato_mosaic_virus",
        "disease": "Tomato Mosaic Virus",
        "crop": "Tomato",
        "type": "Viral",
        "severity": "High",
        "cause": "Tomato mosaic virus (ToMV)",
        "symptoms": [
            "mottled leaves",
            "light and dark green patches",
            "mosaic pattern",
            "leaves look patchy",
            "twisted leaves",
            "distorted leaf shape",
            "wrinkled leaves",
            "reduced fruit",
            "fern leaf appearance",
            "plant looks sick but no spots"
        ],
        "treatment": [
            "Remove and destroy infected plants",
            "No chemical treatment available",
            "Wash hands thoroughly after handling infected plants",
            "Disinfect all tools with 10% bleach solution"
        ],
        "prevention": [
            "Use resistant varieties",
            "Use disease-free seeds",
            "Avoid tobacco products near plants (can carry virus)",
            "Wash hands before handling plants"
        ]
    },
    {
        "disease_key": "Tomato___healthy",
        "disease": "Healthy Plant",
        "crop": "Tomato",
        "type": "None",
        "severity": "None",
        "cause": "N/A",
        "symptoms": [
            "no disease",
            "plant looks good",
            "healthy green leaves",
            "normal growth",
            "no spots",
            "no yellowing"
        ],
        "treatment": [
            "Continue regular care and maintenance",
            "Monitor for early signs of disease",
            "Maintain proper watering schedule"
        ],
        "prevention": [
            "Regular inspection of plants",
            "Proper nutrition and watering",
            "Good garden hygiene",
            "Adequate spacing for air circulation"
        ]
    },
    {
        "disease_key": "Not_a_Plant",
        "disease": "Not a Plant",
        "crop": "N/A",
        "type": "Rejection",
        "severity": "N/A",
        "cause": "Uploaded image is not a plant leaf",
        "symptoms": [
            "not a plant",
            "non-plant image",
            "unrelated image"
        ],
        "treatment": [
            "Please upload a clear image of a plant leaf",
            "Ensure the image shows a leaf, not other objects"
        ],
        "prevention": [
            "Use well-lit, focused photos of plant leaves",
            "Avoid uploading non-plant images"
        ]
    },
]


def seed_database():
    """Create tables and insert all seed data."""
    create_tables()
    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0
    skipped = 0

    for entry in SEED_DATA:
        # Check if already exists
        existing = cursor.execute(
            "SELECT id FROM diseases WHERE disease_key = ?", (entry["disease_key"],)
        ).fetchone()

        if existing:
            skipped += 1
            continue

        # Insert disease
        cursor.execute("""
            INSERT INTO diseases (disease_key, disease, crop, type, severity, cause)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            entry["disease_key"],
            entry["disease"],
            entry["crop"],
            entry["type"],
            entry["severity"],
            entry["cause"]
        ))
        disease_id = cursor.lastrowid

        # Insert symptoms
        for symptom in entry.get("symptoms", []):
            cursor.execute(
                "INSERT INTO symptoms (disease_id, symptom) VALUES (?, ?)",
                (disease_id, symptom)
            )

        # Insert treatments
        for treatment in entry.get("treatment", []):
            cursor.execute(
                "INSERT INTO treatments (disease_id, treatment) VALUES (?, ?)",
                (disease_id, treatment)
            )

        # Insert prevention tips
        for prevention in entry.get("prevention", []):
            cursor.execute(
                "INSERT INTO prevention (disease_id, prevention) VALUES (?, ?)",
                (disease_id, prevention)
            )

        inserted += 1

    conn.commit()
    conn.close()

    print(f"Seeding complete: {inserted} inserted, {skipped} skipped (already existed)")
    print(f"Database: {os.path.abspath(os.path.join(os.path.dirname(__file__), 'plantdocbot.db'))}")


if __name__ == "__main__":
    seed_database()
