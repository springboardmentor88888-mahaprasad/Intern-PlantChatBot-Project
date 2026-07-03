# backend/treatments.py

TREATMENTS = {
    "Pepper__bell___Bacterial_spot": {
        "common_name": "Pepper Bell - Bacterial Spot",
        "cause": "Bacterium (*Xanthomonas campestris pv. vesicatoria*)",
        "symptoms": "Small, water-soaked, circular spots on leaves that turn dark brown. Leaves may turn yellow and drop off, exposing fruit to sunscald.",
        "organic": "Apply copper-based bactericides early. Remove and destroy infected leaves/plants immediately. Use mulch to prevent soil splashing.",
        "chemical": "Copper sprays (e.g., copper hydroxide) are the primary chemical treatment, though effectiveness is limited if the strain is resistant.",
        "prevention": "Use pathogen-free certified seeds. Avoid overhead irrigation; use drip watering instead. Rotate crops every 2-3 years."
    },
    "Pepper__bell___healthy": {
        "common_name": "Pepper Bell - Healthy",
        "cause": "None",
        "symptoms": "Leaves are vibrant green, glossy, firm, and free from spots, discoloration, or deformities.",
        "organic": "No treatment required. Maintain rich soil with compost and balanced watering.",
        "chemical": "None",
        "prevention": "Ensure 6-8 hours of sunlight daily, prune lower leaves for airflow, and apply organic mulch to retain soil moisture."
    },
    "Potato___Early_blight": {
        "common_name": "Potato - Early Blight",
        "cause": "Fungus (*Alternaria solani*)",
        "symptoms": "Dark brown to black circular spots with concentric rings ('target board' appearance) starting on older lower leaves.",
        "organic": "Apply organic copper fungicides or Bacillus subtilis formulations. Remove lower leaves to prevent spread from soil.",
        "chemical": "Fungicides containing Chlorothalonil, Mancozeb, or Azoxystrobin can control early blight if applied when symptoms first appear.",
        "prevention": "Rotate crops with non-solanaceous plants. Maintain adequate soil nutrients (especially nitrogen) to keep plants vigorous."
    },
    "Potato___Late_blight": {
        "common_name": "Potato - Late Blight",
        "cause": "Oomycete / Water Mold (*Phytophthora infestans*)",
        "symptoms": "Dark, water-soaked lesions on leaves and stems, often with a white fuzzy growth on the undersides in humid conditions. Highly destructive.",
        "organic": "Prune and destroy infected plants immediately (do not compost). Apply copper fungicides defensively before weather becomes wet and cool.",
        "chemical": "Fungicides containing Metalaxyl, Chlorothalonil, or Mancozeb are highly effective but must be applied early and regularly.",
        "prevention": "Plant certified disease-free seed tubers. Avoid overhead watering and ensure excellent soil drainage. Harvest during dry weather."
    },
    "Potato___healthy": {
        "common_name": "Potato - Healthy",
        "cause": "None",
        "symptoms": "Sturdy green foliage, strong stems, and healthy leaves with no dark lesions or water-soaked spots.",
        "organic": "No treatment required. Feed with organic liquid seaweed or compost tea.",
        "chemical": "None",
        "prevention": "Keep plants well-hilled with soil to protect developing tubers. Maintain consistent soil moisture."
    },
    "Tomato_Bacterial_spot": {
        "common_name": "Tomato - Bacterial Spot",
        "cause": "Bacterium (*Xanthomonas spp.*)",
        "symptoms": "Small, dark, greasy-looking spots on leaves and stems. Leaf edges may appear scorched, eventually turning yellow and dropping.",
        "organic": "Spray with a mixture of copper-based bactericides and organic neem oil. Prune lower foliage to keep leaves dry.",
        "chemical": "Apply copper hydroxide mixed with Mancozeb for improved bacterial control.",
        "prevention": "Avoid overhead watering. Avoid working in the garden when leaves are wet. Practice a 3-year crop rotation."
    },
    "Tomato_Early_blight": {
        "common_name": "Tomato - Early Blight",
        "cause": "Fungus (*Alternaria solani*)",
        "symptoms": "Dark brown circular spots with characteristic concentric rings (target pattern) on older leaves first. Leads to yellowing and defoliation.",
        "organic": "Apply copper fungicides, sulfur dust, or Serenade (Bacillus subtilis). Remove infected lower leaves.",
        "chemical": "Use preventative fungicides such as Chlorothalonil or Mancozeb when conditions are warm and humid.",
        "prevention": "Mulch the base of the plant to prevent soil splash. Space plants at least 2-3 feet apart to maximize airflow."
    },
    "Tomato_Late_blight": {
        "common_name": "Tomato - Late Blight",
        "cause": "Oomycete / Water Mold (*Phytophthora infestans*)",
        "symptoms": "Large, blue-grey to black water-soaked lesions on leaves and stems. White mildew-like growth appears on leaf undersides in wet conditions.",
        "organic": "Copper-based sprays can act as a preventative. Destroy infected plants immediately to prevent neighborhood-wide spread.",
        "chemical": "Systemic and contact fungicides containing Chlorothalonil, Mancozeb, or Propamocarb should be sprayed immediately.",
        "prevention": "Grow resistant tomato varieties. Ensure plants are watered at the roots rather than from above."
    },
    "Tomato_Leaf_Mold": {
        "common_name": "Tomato - Leaf Mold",
        "cause": "Fungus (*Passalora fulva*)",
        "symptoms": "Pale green or yellow spots on the upper leaf surface, with olive-green to brown velvety mold growth on the corresponding lower surface.",
        "organic": "Improve greenhouse ventilation. Spray with organic copper-based or sulfur-based fungicides.",
        "chemical": "Chlorothalonil or copper fungicides can control leaf mold if applied early in the infection cycle.",
        "prevention": "Prune lower suckers and branches to increase air circulation. Keep greenhouse humidity below 85%."
    },
    "Tomato_Septoria_leaf_spot": {
        "common_name": "Tomato - Septoria Leaf Spot",
        "cause": "Fungus (*Septoria lycopersici*)",
        "symptoms": "Numerous small, circular spots with dark brown margins and light grey centers. Tiny black specks (fruiting bodies) appear in the centers.",
        "organic": "Remove infected lower leaves. Spray with copper-based organic fungicides. Mulch well to suppress spores.",
        "chemical": "Fungicides containing Chlorothalonil or Mancozeb are highly effective for managing Septoria.",
        "prevention": "Clean stakes, cages, and tools at the end of the season. Water at the base of the plant."
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "common_name": "Tomato - Two-Spotted Spider Mite",
        "cause": "Pest / Arachnid (*Tetranychus urticae*)",
        "symptoms": "Fine yellow stippling (tiny dots) on the upper surface of leaves. Fine webbing may cover stems and leaf undersides. Leaves turn yellow and dry up.",
        "organic": "Release beneficial predatory mites (e.g., Phytoseiulus persimilis). Spray with insecticidal soap, rosemary oil, or neem oil.",
        "chemical": "Apply miticides/acaricides such as Abamectin or Spiromesifen if organic treatments fail.",
        "prevention": "Keep plants well-watered (spider mites thrive in hot, dry conditions). Mist foliage occasionally to deter mites."
    },
    "Tomato__Target_Spot": {
        "common_name": "Tomato - Target Spot",
        "cause": "Fungus (*Corynespora cassiicola*)",
        "symptoms": "Small, water-soaked spots on leaves that expand into large circular lesions with dark brown margins and light centers, exhibiting target-like rings.",
        "organic": "Apply copper-based sprays or Bacillus subtilis. Clean up all crop debris at the end of the season.",
        "chemical": "Fungicides containing Chlorothalonil, Azoxystrobin, or Pyraclostrobin are effective options.",
        "prevention": "Provide adequate spacing for airflow. Do not plant new crops next to old, diseased fields."
    },
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "common_name": "Tomato - Yellow Leaf Curl Virus",
        "cause": "Virus (Geminivirus transmitted by Silverleaf Whitefly)",
        "symptoms": "Severe stunting of plants. Leaves curl upward and inward, become yellow, crumpled, and significantly reduced in size. No fruit forms.",
        "organic": "Control whitefly vectors using yellow sticky cards, neem oil, or horticultural oils. Cover young crops with fine insect mesh.",
        "chemical": "Chemical control is focused entirely on managing whiteflies with insecticides like Imidacloprid or Acetamiprid.",
        "prevention": "Use virus-resistant cultivars. Immediately remove and bag infected plants to prevent whiteflies from spreading the virus."
    },
    "Tomato__Tomato_mosaic_virus": {
        "common_name": "Tomato - Mosaic Virus",
        "cause": "Tobacco/Tomato Mosaic Virus (TMV/ToMV)",
        "symptoms": "Mottling patterns of light and dark green on leaves. Leaves may become blistered, distorted, or 'fern-like'. Stunted plant growth.",
        "organic": "There is no cure for viral infections. Dig up and destroy infected plants immediately. Wash hands with soap/milk before handling healthy plants.",
        "chemical": "No chemical treatment is available for viral plant diseases.",
        "prevention": "Avoid smoking near tomato plants (tobacco can carry the virus). Disinfect tools with a bleach solution or trisodium phosphate."
    },
    "Tomato_healthy": {
        "common_name": "Tomato - Healthy",
        "cause": "None",
        "symptoms": "Healthy, lush green foliage with robust stems and active flowering or fruit production. No signs of pathogens or mites.",
        "organic": "No treatment required. Maintain a weekly watering schedule and apply organic compost.",
        "chemical": "None",
        "prevention": "Ensure deep watering once or twice a week. Support plants with stakes/cages to keep leaves off the ground."
    }
}

def get_treatment(disease_name):
    """
    Lookup treatment and preventative measures for a given plant/disease class.
    Args:
        disease_name (str): The exact class identifier output by the model.
    Returns:
        dict: A dictionary of common_name, cause, symptoms, organic, chemical, prevention.
    """
    return TREATMENTS.get(
        disease_name,
        {
            "common_name": disease_name.replace("___", " - ").replace("__", " - ").replace("_", " ") if disease_name else "Unknown",
            "cause": "Unknown Pathogen",
            "symptoms": "Specific symptoms for this strain are not documented in the local database.",
            "organic": "Consult a local agricultural extension office. Practice crop hygiene and remove heavily damaged leaves.",
            "chemical": "Consult an agricultural expert before applying any chemical pesticides or fungicides.",
            "prevention": "Maintain proper plant spacing, avoid overhead watering, and monitor soil nutrition."
        }
    )
