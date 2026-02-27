TREATMENTS = {
    "Tomato___Late_blight": {
        "disease": "Late Blight",
        "cause": "Fungus Phytophthora infestans",
        "symptoms": "Dark brown spots on leaves and stems, white fuzzy growth on leaf undersides",
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

    "Tomato___Early_blight": {
        "disease": "Early Blight",
        "cause": "Fungus Alternaria solani",
        "symptoms": "Dark spots with concentric rings on lower leaves, yellowing around spots",
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

    "Tomato___Leaf_Mold": {
        "disease": "Leaf Mold",
        "cause": "Fungus Passalora fulva",
        "symptoms": "Yellow spots on upper leaf surface, olive-green to brown fuzzy growth underneath",
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

    "Tomato___Septoria_leaf_spot": {
        "disease": "Septoria Leaf Spot",
        "cause": "Fungus Septoria lycopersici",
        "symptoms": "Small circular spots with dark borders and gray centers, tiny black dots in spots",
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

    "Tomato___Bacterial_spot": {
        "disease": "Bacterial Spot",
        "cause": "Bacteria Xanthomonas species",
        "symptoms": "Small dark spots on leaves, raised scab-like spots on fruit",
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

    "Tomato___YellowLeaf__Curl_Virus": {
        "disease": "Yellow Leaf Curl Virus",
        "cause": "Tomato yellow leaf curl virus (TYLCV), transmitted by whiteflies",
        "symptoms": "Upward curling of leaves, yellowing between veins, stunted growth",
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

    "Tomato___mosaic_virus": {
        "disease": "Tomato Mosaic Virus",
        "cause": "Tomato mosaic virus (ToMV)",
        "symptoms": "Mottled light and dark green pattern on leaves, distorted leaf shape, reduced yield",
        "treatment": [
            "Remove and destroy infected plants",
            "No chemical treatment available",
            "Wash hands thoroughly after handling infected plants",
            "Disinfect all tools with 10% bleach solution"
        ],
        "prevention": [
            "Use resistant varieties",
            "Use disease-free seeds",
            "Avoid tobacco products near plants",
            "Wash hands before handling plants"
        ]
    },

    "Tomato___healthy": {
        "disease": "Healthy Plant",
        "cause": "N/A",
        "symptoms": "No disease symptoms present",
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

    "Pest_Attack": {
        "disease": "Pest Attack",
        "cause": "Insects such as caterpillars, aphids, beetles",
        "symptoms": "Holes in leaves, chewed edges, visible insects",
        "treatment": [
            "Remove insects manually if possible",
            "Use neem oil or organic insecticides",
            "Apply recommended chemical pesticides if severe"
        ],
        "prevention": [
            "Regular plant inspection",
            "Use insect netting",
            "Maintain garden hygiene"
        ]
    },
    "Pepper__bell___Bacterial_spot": {
    "disease": "Bacterial Spot (Pepper)",
    "cause": "Bacteria Xanthomonas campestris",
    "symptoms": "Small water-soaked spots that turn brown or black on leaves and fruits",
    "treatment": [
        "Remove infected leaves and fruits",
        "Apply copper-based bactericides",
        "Avoid overhead irrigation",
        "Improve air circulation"
    ],
    "prevention": [
        "Use certified disease-free seeds",
        "Rotate crops",
        "Disinfect tools regularly",
        "Avoid working with wet plants"
    ]
  }

}


def get_treatment(disease_class: str) -> dict:
    """
    Get treatment information for a specific disease class.
    
    Args:
        disease_class: The disease classification string (e.g., "Tomato___Late_blight")
    
    Returns:
        Dictionary containing disease information and treatment recommendations
    """
    return TREATMENTS.get(disease_class, {
        "disease": "Unknown",
        "cause": "Unknown",
        "symptoms": "Unable to determine",
        "treatment": ["Please consult a local agricultural expert"],
        "prevention": ["Regular plant inspection recommended"]
    })


def format_treatment_response(disease_class: str) -> str:
    """
    Format treatment information as a readable string.
    
    Args:
        disease_class: The disease classification string
    
    Returns:
        Formatted string with treatment information
    """
    info = get_treatment(disease_class)
    
    response = f"🌱 **{info['disease']}**\n\n"
    response += f"**Cause:** {info['cause']}\n\n"
    response += f"**Symptoms:** {info['symptoms']}\n\n"
    
    response += "**Treatment:**\n"
    for item in info['treatment']:
        response += f"  • {item}\n"
    
    response += "\n**Prevention:**\n"
    for item in info['prevention']:
        response += f"  • {item}\n"
    
    return response