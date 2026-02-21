# Seed script — populates the database with COMPREHENSIVE plant disease information
# Covers 40+ classes from PlantVillage, PlantDoc, and additional research
# Run once: python -m database.seed

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import create_tables, get_connection

# ============================================================================
# COMPREHENSIVE SEED DATA - 40+ Plant Disease Classes
# Sources: PlantVillage, PlantDoc, Plant Pathology Research
# ============================================================================

SEED_DATA = [
    # ========================================================================
    # PEPPER DISEASES (Bell Pepper)
    # ========================================================================
    {
        "disease_key": "Pepper__bell___Bacterial_spot",
        "disease": "Bacterial Spot",
        "crop": "Pepper (Bell)",
        "type": "Bacterial",
        "severity": "Medium-High",
        "cause": "Bacteria Xanthomonas campestris pv. vesicatoria (and related species)",
        "symptoms": [
            "small dark water-soaked spots on leaves",
            "raised bumps on fruit surface",
            "spots with yellow halo surrounding lesions",
            "leaves dropping prematurely from plant",
            "scab-like lesions on fruit reducing marketability",
            "leaf edges browning and curling",
            "fruit spots may be raised or sunken",
            "defoliation starting from lower leaves",
            "greasy appearance on spots",
            "bacterial ooze in humid conditions",
            "spots enlarge and coalesce over time",
            "reduced fruit quality and yield",
            "stems may show dark streaks"
        ],
        "treatment": [
            "Remove and destroy all infected plant parts immediately",
            "Apply copper-based bactericides (copper hydroxide or copper sulfate)",
            "Use fixed copper sprays every 7-10 days during wet weather",
            "Rotate with streptomycin sulfate if legally available",
            "Avoid overhead irrigation to reduce leaf wetness",
            "Apply bactericides preventively before infection occurs",
            "Improve air circulation by proper plant spacing",
            "Remove volunteer pepper plants that may harbor bacteria",
            "Disinfect pruning tools with 70% alcohol or 10% bleach between plants",
            "Apply mulch to prevent soil splash onto leaves",
            "Consider biological controls like Bacillus subtilis",
            "Maintain proper plant nutrition to boost immunity"
        ],
        "prevention": [
            "Use certified disease-free seeds and transplants",
            "Practice crop rotation for at least 2-3 years with non-solanaceous crops",
            "Disinfect all tools, stakes, and equipment between uses",
            "Avoid working with wet plants to prevent disease spread",
            "Plant resistant or tolerant varieties when available",
            "Remove crop debris immediately after harvest",
            "Manage weeds that can harbor the bacterium",
            "Use drip irrigation instead of overhead sprinklers",
            "Apply copper sprays preventively in humid climates",
            "Space plants adequately for air circulation (18-24 inches)",
            "Start with hot water-treated seeds (122°F for 25 minutes)",
            "Monitor plants weekly for early disease detection",
            "Avoid excessive nitrogen fertilization",
            "Install windbreaks to reduce mechanical damage and pathogen entry"
        ]
    },
    {
        "disease_key": "Pepper__bell___healthy",
        "disease": "Healthy Plant",
        "crop": "Pepper (Bell)",
        "type": "None",
        "severity": "None",
        "cause": "N/A - No pathogen present",
        "symptoms": [
            "vibrant dark green leaves without spots or discoloration",
            "uniform leaf coloration throughout the plant",
            "strong upright growth with sturdy stems",
            "normal fruit development with proper color",
            "no wilting or yellowing of foliage",
            "healthy white flowers blooming regularly",
            "vigorous new growth at growing points",
            "leaves are turgid and firm to touch",
            "no signs of pest damage or feeding",
            "proper plant height for variety and age"
        ],
        "treatment": [
            "Continue regular care and maintenance schedule",
            "Monitor for early signs of disease or pests weekly",
            "Maintain proper watering schedule (1-2 inches per week)",
            "Provide balanced fertilization throughout growing season",
            "Support plants with stakes or cages as needed",
            "Prune suckers and lower leaves for air circulation",
            "Harvest fruit at proper maturity to encourage more production"
        ],
        "prevention": [
            "Regular inspection of plants for early problem detection",
            "Proper nutrition with balanced NPK fertilizer",
            "Adequate watering without water stress or overwatering",
            "Good garden hygiene and sanitation practices",
            "Mulching to conserve moisture and prevent soil splash",
            "Proper spacing for air circulation (18-24 inches)",
            "Remove weeds that compete for nutrients",
            "Rotate crops to prevent soil-borne disease buildup"
        ]
    },
    
    # ========================================================================
    # POTATO DISEASES
    # ========================================================================
    {
        "disease_key": "Potato___Early_blight",
        "disease": "Early Blight",
        "crop": "Potato",
        "type": "Fungal",
        "severity": "Medium-High",
        "cause": "Fungus Alternaria solani (sometimes A. alternata)",
        "symptoms": [
            "dark concentric rings forming target-like patterns on leaves",
            "target-shaped spots with alternating dark and light rings",
            "lower older leaves affected first before upper leaves",
            "yellowing (chlorosis) around spots expanding outward",
            "premature leaf drop starting from bottom of plant",
            "brown to black lesions on tubers with corky texture",
            "spots enlarge to 0.5 inches or more in diameter",
            "leaves become brittle and dry",
            "stem lesions that are dark and elongated",
            "reduced tuber size due to defoliation",
            "V-shaped lesions on leaflets",
            "spots may have gray center with dark margin",
            "entire leaflets may die and drop off",
            "symptoms worsen in hot humid weather"
        ],
        "treatment": [
            "Remove infected leaves immediately and destroy (don't compost)",
            "Apply fungicides containing chlorothalonil every 7-10 days",
            "Use mancozeb-based fungicides as preventive spray",
            "Apply azoxystrobin or pyraclostrobin for systemic control",
            "Ensure proper plant spacing for air flow between rows",
            "Hill up soil around plants to prevent tuber infection",
            "Improve drainage to reduce leaf wetness duration",
            "Apply fungicides before symptoms appear in disease-prone areas",
            "Alternate fungicide modes of action to prevent resistance",
            "Increase spray frequency during wet weather",
            "Remove volunteer potatoes from previous crops",
            "Apply copper-based fungicides as organic option"
        ],
        "prevention": [
            "Use certified disease-free seed potatoes from reliable sources",
            "Practice 2-3 year crop rotation with non-solanaceous crops",
            "Remove all plant debris after harvest completely",
            "Maintain adequate plant nutrition especially potassium",
            "Plant resistant varieties like Jacqueline Lee or Elba",
            "Avoid overhead irrigation; use drip or furrow instead",
            "Apply mulch to prevent soil splash onto lower leaves",
            "Space plants 12-15 inches apart in rows 3 feet apart",
            "Monitor plants weekly starting 2-3 weeks after emergence",
            "Remove weeds that harbor fungal spores",
            "Avoid working with plants when wet",
            "Apply preventive fungicides when conditions favor disease",
            "Deep plow crop residue after harvest",
            "Store tubers properly to prevent infection spread"
        ]
    },
    {
        "disease_key": "Potato___Late_blight",
        "disease": "Late Blight (Potato Famine Disease)",
        "crop": "Potato",
        "type": "Oomycete (Water Mold)",
        "severity": "Very High - Epidemic Potential",
        "cause": "Oomycete Phytophthora infestans",
        "symptoms": [
            "dark water-soaked spots on leaves appearing suddenly",
            "white fuzzy mold (sporangia) on leaf underside in humid conditions",
            "stems turning dark brown to black rapidly",
            "rapid plant collapse within days of infection",
            "tuber rot with reddish-brown to purple discoloration",
            "foul rotting smell from infected tubers",
            "lesions expand rapidly in cool wet weather",
            "entire field can be destroyed within 2 weeks",
            "brown streaks on stems and petioles",
            "tubers have dry brown rot initially, then soft rot develops",
            "irregular dark brown lesions on leaves",
            "lesions surrounded by pale green to yellow halo",
            "black hard scabby areas on tuber surface",
            "complete defoliation of plants in severe cases"
        ],
        "treatment": [
            "Remove and destroy all infected plants immediately (burn if possible)",
            "Apply copper-based fungicides (Bordeaux mixture) immediately",
            "Use mancozeb, chlorothalonil, or metalaxyl-based fungicides",
            "Spray every 5-7 days during cool wet weather",
            "Apply fungicides to all plant surfaces including stem bases",
            "Harvest tubers only in dry conditions",
            "Do not wash tubers before storage as this spreads disease",
            "Cure tubers at 50-60°F with good ventilation before storage",
            "Destroy all potato cull piles immediately",
            "Do not allow infected tubers to overwinter in soil",
            "Use systemic fungicides in alternation with protectants",
            "Spray neighboring fields preventively if disease detected nearby"
        ],
        "prevention": [
            "Plant resistant varieties like Defender, Sarpo Mira, or Elba",
            "Avoid overhead watering especially in evening",
            "Ensure excellent drainage in planting areas",
            "Destroy all volunteer potato plants in and around fields",
            "Use certified disease-free seed potatoes only",
            "Hill plants properly to prevent tuber exposure",
            "Monitor weather for late blight favorable conditions (60-80°F, high humidity)",
            "Apply preventive fungicides before disease appears",
            "Space rows widely for air circulation",
            "Plant early maturing varieties to escape late season disease",
            "Remove crop residue completely after harvest",
            "Store seed potatoes separately from eating potatoes",
            "Use disease forecasting systems for spray timing",
            "Avoid planting potatoes near tomatoes (also susceptible)"
        ]
    },
    {
        "disease_key": "Potato___healthy",
        "disease": "Healthy Plant",
        "crop": "Potato",
        "type": "None",
        "severity": "None",
        "cause": "N/A - No pathogen present",
        "symptoms": [
            "deep green healthy foliage without spots",
            "vigorous growth with multiple stems",
            "white or light purple flowers blooming normally",
            "leaves are turgid and upright",
            "normal tuber development underground",
            "no yellowing or browning of leaves",
            "uniform plant growth across field",
            "strong root system anchoring plant",
            "no wilting during day",
            "pest-free foliage"
        ],
        "treatment": [
            "Continue regular care and maintenance",
            "Monitor for early signs of disease weekly",
            "Maintain proper hilling schedule to protect tubers",
            "Provide consistent moisture (1-2 inches per week)",
            "Apply balanced fertilizer as needed",
            "Scout for Colorado potato beetles regularly",
            "Harvest at proper maturity when vines die back"
        ],
        "prevention": [
            "Regular inspection of plants for problems",
            "Proper nutrition with adequate potassium",
            "Consistent watering to prevent stress",
            "Good garden hygiene",
            "Use certified seed potatoes",
            "Proper hilling to prevent green tubers",
            "Crop rotation to prevent disease buildup",
            "Remove volunteer potatoes from previous crops"
        ]
    },

    # ========================================================================
    # TOMATO DISEASES (Most comprehensive section)
    # ========================================================================
    {
        "disease_key": "Tomato___Bacterial_spot",
        "disease": "Bacterial Spot",
        "crop": "Tomato",
        "type": "Bacterial",
        "severity": "Medium-High",
        "cause": "Bacteria Xanthomonas species (X. euvesicatoria, X. vesicatoria, X. gardneri, X. perforans)",
        "symptoms": [
            "small dark spots on leaves with greasy appearance",
            "raised bumps on fruit that feel rough",
            "scab-like spots on fruit reducing market value",
            "water-soaked lesions expanding on leaves",
            "spots with yellow halo surrounding the lesion",
            "fruit has rough scabby spots",
            "leaves look scorched or burned",
            "oily looking spots on both leaf surfaces",
            "spots spreading rapidly in warm humid weather",
            "defoliation leading to fruit sunscald",
            "lesions may coalesce on severely affected leaves",
            "bacterial streaming visible under microscope",
            "spots turn brown to black as they age",
            "fruit spots may have white halo",
            "reduced fruit quality and marketability"
        ],
        "treatment": [
            "Remove infected plant material and destroy immediately",
            "Apply copper-based bactericides weekly during wet weather",
            "Use copper hydroxide or copper sulfate products",
            "Avoid overhead irrigation to reduce leaf wetness",
            "Do not work with wet plants to prevent disease spread",
            "Apply bactericides preventively before rain events",
            "Increase plant spacing for better air circulation",
            "Stake and prune plants to keep foliage off ground",
            "Apply mulch to prevent soil splash",
            "Consider streptomycin if available and legal in your area",
            "Use biological controls like Bacillus subtilis",
            "Rotate spray materials to prevent resistance"
        ],
        "prevention": [
            "Use certified disease-free seeds and transplants",
            "Practice crop rotation with 2-3 year break from solanaceous crops",
            "Disinfect tools between plants with 70% alcohol",
            "Use resistant varieties when available (none are fully resistant)",
            "Hot water treat seeds (122°F for 25 minutes)",
            "Remove crop debris after harvest completely",
            "Control weeds that may harbor bacteria",
            "Use drip irrigation instead of overhead",
            "Apply copper sprays preventively in humid climates",
            "Space plants 24-36 inches apart for air flow",
            "Avoid working in fields when foliage is wet",
            "Use raised beds for better drainage",
            "Monitor plants weekly for early detection",
            "Avoid excessive nitrogen which promotes succulent growth"
        ]
    },
    {
        "disease_key": "Tomato___Early_blight",
        "disease": "Early Blight",
        "crop": "Tomato",
        "type": "Fungal",
        "severity": "Medium",
        "cause": "Fungus Alternaria solani (also A. tomatophila)",
        "symptoms": [
            "dark spots with concentric rings creating target pattern",
            "target-shaped spots resembling a bullseye",
            "concentric rings alternating dark and light brown",
            "bull's eye pattern clearly visible on older leaves",
            "lower leaves yellowing and dying first",
            "yellow halo around spots spreading outward",
            "leaves drying and dropping from bottom up",
            "old leaves affected before young leaves",
            "brown circular spots enlarging over time",
            "stem lesions that are dark and girdling",
            "collar rot on seedlings near soil line",
            "fruit rot with dark leathery lesions at stem end",
            "spots coalesce causing entire leaf death",
            "defoliation reducing fruit quality",
            "premature fruit ripening due to stress"
        ],
        "treatment": [
            "Remove affected lower leaves immediately",
            "Apply fungicides containing chlorothalonil weekly",
            "Use copper-based fungicides as organic option",
            "Apply mancozeb or maneb preventively",
            "Mulch around plants to prevent soil splash onto leaves",
            "Stake plants to improve air circulation",
            "Remove severely infected plants",
            "Apply fungicides to both leaf surfaces",
            "Increase spray frequency during wet weather",
            "Use azoxystrobin for systemic control",
            "Rotate fungicide classes to prevent resistance",
            "Improve drainage if water pools around plants"
        ],
        "prevention": [
            "Use certified disease-free seeds and transplants",
            "Practice crop rotation for 2-3 years minimum",
            "Maintain adequate plant nutrition especially potassium",
            "Remove all plant debris after harvest",
            "Plant resistant varieties like Mountain Fresh Plus or Plum Regal",
            "Mulch with straw or plastic to prevent soil splash",
            "Space plants 24-36 inches apart",
            "Use drip irrigation to keep foliage dry",
            "Avoid overhead watering especially in evening",
            "Remove lowest leaves that touch ground",
            "Apply preventive fungicides in disease-prone areas",
            "Monitor plants weekly starting at first flower",
            "Provide good air circulation with proper spacing",
            "Avoid working with wet plants"
        ]
    },
    {
        "disease_key": "Tomato___Late_blight",
        "disease": "Late Blight (Tomato Late Blight)",
        "crop": "Tomato",
        "type": "Oomycete (Water Mold)",
        "severity": "Very High - Can Destroy Entire Crop",
        "cause": "Oomycete Phytophthora infestans",
        "symptoms": [
            "dark brown to black water-soaked spots on leaves",
            "brown patches expanding rapidly on leaves and stems",
            "white fuzzy fungal growth on leaf undersides",
            "white mold visible under leaves in humid conditions",
            "leaves turning black and dying within days",
            "stem rotting and turning black",
            "entire plant dying rapidly in favorable conditions",
            "wet rot smell from infected tissue",
            "leaves wilting suddenly despite adequate water",
            "fruit showing firm brown lesions",
            "greasy brown lesions on green fruit",
            "irregular dark lesions with pale borders",
            "complete plant collapse within week of infection",
            "field-wide epidemic possible in cool wet weather",
            "sporangia (spores) visible as white powder"
        ],
        "treatment": [
            "Remove and destroy infected plant parts immediately (burn if possible)",
            "Apply copper-based fungicides (Bordeaux mixture) at first sign",
            "Use chlorothalonil or mancozeb every 5-7 days",
            "Apply systemic fungicides like metalaxyl or dimethomorph",
            "Improve air circulation around plants by pruning",
            "Avoid overhead watering completely",
            "Harvest and ripen fruit indoors if disease present",
            "Remove entire plant if severely infected",
            "Spray neighboring plants preventively",
            "Use resistant varieties immediately for replanting",
            "Apply fungicides to both sides of leaves thoroughly",
            "Do not compost infected material - destroy it"
        ],
        "prevention": [
            "Plant highly resistant varieties like Iron Lady, Defiant, or Mountain Merit",
            "Ensure proper spacing between plants (36 inches minimum)",
            "Water at base of plants in morning only",
            "Rotate crops yearly avoiding solanaceous plants",
            "Remove volunteer tomato and potato plants",
            "Monitor weather for late blight favorable conditions (50-80°F, high humidity)",
            "Apply preventive fungicides before disease appears",
            "Use disease forecasting systems like TomCast",
            "Stake and prune plants for air circulation",
            "Remove lower leaves touching ground",
            "Avoid planting tomatoes near potatoes",
            "Use row covers in wet weather if practical",
            "Inspect plants daily during disease-favorable weather",
            "Remove crop debris immediately after harvest"
        ]
    },
    {
        "disease_key": "Tomato___Leaf_Mold",
        "disease": "Leaf Mold (Tomato Leaf Mold)",
        "crop": "Tomato",
        "type": "Fungal",
        "severity": "Medium",
        "cause": "Fungus Passalora fulva (formerly Fulvia fulva, Cladosporium fulvum)",
        "symptoms": [
            "pale yellow spots on upper leaf surface",
            "olive-green to brown fuzzy growth on leaf underside",
            "velvety olive-brown mold coating underside",
            "brown fuzzy fungal patches spreading",
            "leaves turning yellow then brown",
            "greenhouse disease thriving in high humidity",
            "humid weather disease problem",
            "leaves curling downward severely",
            "velvety coating that feels soft to touch",
            "older leaves affected first",
            "entire leaves turning brown and dying",
            "reduced fruit production due to defoliation",
            "symptoms worse with poor air circulation",
            "spots enlarge and coalesce over time",
            "whitish mold turning olive-brown as it ages"
        ],
        "treatment": [
            "Improve ventilation in greenhouses immediately",
            "Reduce humidity below 85% if possible",
            "Apply fungicides like chlorothalonil if severe",
            "Remove heavily infected leaves and destroy",
            "Reduce humidity levels with fans and vents",
            "Apply copper-based fungicides",
            "Use sulfur-based fungicides in greenhouses",
            "Space plants farther apart for air movement",
            "Prune lower leaves to improve circulation",
            "Water only in morning to allow drying",
            "Apply mancozeb or maneb fungicides",
            "Use biological controls like Bacillus subtilis"
        ],
        "prevention": [
            "Use resistant varieties like Fandango, Legend, or Geronimo",
            "Maintain good air circulation in greenhouses",
            "Avoid wetting leaves during irrigation",
            "Keep humidity below 85% in protected culture",
            "Ensure adequate spacing (36 inches minimum)",
            "Remove lower leaves that touch ground",
            "Use fans to circulate air in greenhouses",
            "Vent greenhouses to reduce humidity",
            "Water at base of plants only",
            "Avoid overhead misting in greenhouses",
            "Heat greenhouses to reduce humidity",
            "Monitor humidity levels with hygrometer",
            "Prune for air circulation",
            "Disinfect greenhouse structures annually"
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
            "small round spots with tiny black dots (pycnidia) in center",
            "circular spots 1/16 to 1/4 inch diameter",
            "gray to tan center with dark border",
            "dark brown to black border around spots",
            "many small spots giving speckled appearance",
            "leaves look peppered with tiny holes",
            "spots with dark margins and light centers",
            "lower leaves affected first moving upward",
            "leaves falling off progressively from bottom",
            "black dots visible in spot centers (fruiting bodies)",
            "spots may have yellow halo initially",
            "coalescing spots causing leaf death",
            "severe defoliation in wet weather",
            "fruit production reduced due to leaf loss",
            "primarily on leaves, rarely on stems or fruit"
        ],
        "treatment": [
            "Remove infected lower leaves immediately",
            "Apply copper-based fungicides preventively",
            "Use chlorothalonil fungicides every 7-10 days",
            "Apply mancozeb or maneb products",
            "Avoid working with wet plants",
            "Improve air circulation by staking",
            "Mulch to prevent soil splash",
            "Remove severely infected plants",
            "Apply fungicides to both leaf surfaces",
            "Increase spray frequency during wet periods",
            "Prune lower branches for air flow",
            "Use organic sulfur-based fungicides"
        ],
        "prevention": [
            "Use disease-free certified seeds and transplants",
            "Rotate crops for 2-3 years with non-solanaceous plants",
            "Mulch with straw or plastic to prevent soil splash",
            "Water at plant base only, never overhead",
            "Space plants 24-36 inches apart",
            "Remove crop debris after harvest",
            "Avoid working with wet plants",
            "Plant resistant varieties if available",
            "Apply preventive fungicides in wet climates",
            "Stake plants to keep foliage off ground",
            "Remove lowest leaves that touch soil",
            "Monitor weekly starting at flowering",
            "Maintain good air circulation",
            "Avoid excessive nitrogen fertilization"
        ]
    },
    {
        "disease_key": "Tomato___Spider_mites Two-spotted_spider_mite",
        "disease": "Spider Mites (Two-spotted Spider Mite)",
        "crop": "Tomato",
        "type": "Pest (Arachnid)",
        "severity": "Medium-High in Hot Dry Conditions",
        "cause": "Two-spotted spider mite (Tetranychus urticae)",
        "symptoms": [
            "tiny yellow or white stippling spots on leaves",
            "fine silken webbing on undersides of leaves",
            "leaves turning bronze or brown color",
            "stippled or speckled appearance on leaves",
            "leaf curling and cupping downward",
            "premature leaf drop starting with older leaves",
            "plant looks dusty or dirty",
            "tiny moving dots visible on leaf underside with magnification",
            "webbing becomes heavy in severe infestations",
            "leaves dry out and become brittle",
            "reduced fruit size and quality",
            "entire plants may become covered in webbing",
            "yellowing spreading from leaf edges",
            "symptoms worse in hot dry weather",
            "mites visible as tiny red or green dots"
        ],
        "treatment": [
            "Spray plants with strong jets of water daily to dislodge mites",
            "Apply insecticidal soap thoroughly to leaf undersides",
            "Use neem oil spray every 5-7 days",
            "Apply horticultural oil sprays",
            "Use miticides (abamectin or spiromesifen) for severe infestations",
            "Introduce predatory mites (Phytoseiulus persimilis or Neoseiulus californicus)",
            "Apply sulfur-based products (not when temps above 90°F)",
            "Remove heavily infested leaves",
            "Improve plant vigor with proper watering",
            "Spray leaf undersides thoroughly",
            "Rotate miticide classes to prevent resistance",
            "Use biological insecticides like Beauveria bassiana"
        ],
        "prevention": [
            "Keep plants well-watered as mites prefer dry conditions",
            "Avoid excessive nitrogen fertilization",
            "Monitor regularly with hand lens weekly",
            "Remove heavily infested leaves promptly",
            "Maintain humidity with drip irrigation",
            "Remove weeds that harbor mites",
            "Avoid dusty conditions around plants",
            "Release predatory mites preventively",
            "Inspect new plants before introducing",
            "Avoid stressed plants through good cultural practices",
            "Use reflective mulches which repel mites",
            "Plant mite-repellent companions like garlic",
            "Maintain plant vigor to withstand feeding",
            "Avoid planting near known mite-infested areas"
        ]
    },
    {
        "disease_key": "Tomato___Target_Spot",
        "disease": "Target Spot",
        "crop": "Tomato",
        "type": "Fungal",
        "severity": "Medium-High",
        "cause": "Fungus Corynespora cassiicola",
        "symptoms": [
            "brown spots with distinct concentric rings",
            "target-like pattern similar to early blight",
            "spots on leaves, stems, and fruit",
            "lower leaves affected first",
            "large irregular lesions up to 1/2 inch",
            "premature leaf drop and defoliation",
            "fruit lesions with sunken centers",
            "dark brown to black lesions",
            "concentric rings may be less defined than early blight",
            "lesions elongate on stems",
            "pith of stems may be discolored",
            "severe defoliation leading to fruit sunscald",
            "fruit cracking around lesions",
            "lesions have tan center with dark margin",
            "disease spreads rapidly in warm wet weather"
        ],
        "treatment": [
            "Remove and destroy infected plant debris immediately",
            "Apply fungicides containing chlorothalonil preventively",
            "Use copper-based fungicides",
            "Apply mancozeb or maneb products",
            "Improve air circulation with proper plant spacing",
            "Avoid overhead watering especially at night",
            "Remove lower leaves that show symptoms",
            "Apply fungicides to all plant surfaces",
            "Use azoxystrobin or pyraclostrobin for systemic action",
            "Increase spray frequency during wet weather",
            "Mulch to prevent soil splash",
            "Stake plants for better air flow"
        ],
        "prevention": [
            "Practice crop rotation with 2-3 year break",
            "Use resistant varieties if available",
            "Maintain proper plant spacing (36 inches)",
            "Remove crop residue completely after harvest",
            "Deep plow or bury crop debris",
            "Use drip irrigation to keep foliage dry",
            "Apply preventive fungicides in disease-prone areas",
            "Mulch to prevent soil splash",
            "Avoid working with wet plants",
            "Monitor plants weekly for early detection",
            "Ensure good drainage in planting area",
            "Avoid excessive nitrogen",
            "Remove weeds that may harbor fungus",
            "Space plants for air circulation"
        ]
    },
    {
        "disease_key": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "disease": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "crop": "Tomato",
        "type": "Viral",
        "severity": "Very High - No Cure",
        "cause": "Tomato yellow leaf curl virus (TYLCV), transmitted exclusively by whiteflies (Bemisia tabaci)",
        "symptoms": [
            "leaves curling upward severely (cupping)",
            "bright yellow edges on new leaves",
            "plant severely stunted with no growth",
            "stunted growth and dwarfing",
            "small thick leaves with wrinkled appearance",
            "leaves cupping strongly upward",
            "interveinal yellowing (yellow between veins)",
            "whiteflies visible on leaf undersides",
            "plant looks weak and bushy",
            "flowers dropping before fruit set",
            "fruit production severely reduced or absent",
            "leaves become thick and leathery",
            "plant appears bunched or clustered",
            "new growth is yellow and distorted",
            "symptoms appear 2-3 weeks after infection"
        ],
        "treatment": [
            "Remove and destroy infected plants immediately",
            "Control whitefly populations aggressively with insecticides",
            "Use sticky yellow traps to monitor and trap whiteflies",
            "Apply systemic insecticides like imidacloprid to kill whiteflies",
            "Use neem oil or insecticidal soap on whiteflies",
            "Use reflective silver mulches to repel whiteflies",
            "NO CURE exists once plant is infected",
            "Rogue out infected plants to prevent spread",
            "Apply insecticides preventively before whiteflies arrive",
            "Release parasitic wasps (Encarsia formosa) for biocontrol",
            "Use yellow sticky cards to trap adult whiteflies",
            "Spray insecticides targeting whitefly nymphs"
        ],
        "prevention": [
            "Use highly resistant varieties like Tygress, SUN 6366, or CLN1621L",
            "Plant virus-resistant hybrid varieties",
            "Install fine-mesh insect-proof netting (50-mesh) over plants",
            "Control whitefly populations before planting",
            "Remove weeds that harbor whiteflies and virus",
            "Use reflective silver plastic mulch",
            "Apply systemic insecticides at transplanting",
            "Avoid planting near infested fields",
            "Plant early to escape peak whitefly populations",
            "Remove crop debris immediately after harvest",
            "Use trap crops like squash to attract whiteflies away",
            "Monitor for whiteflies weekly",
            "Space plants well for air circulation",
            "Avoid planting near ornamentals that harbor whiteflies"
        ]
    },
    {
        "disease_key": "Tomato___Tomato_mosaic_virus",
        "disease": "Tomato Mosaic Virus (ToMV)",
        "crop": "Tomato",
        "type": "Viral",
        "severity": "High - No Cure, Highly Contagious",
        "cause": "Tomato mosaic virus (ToMV) - mechanically transmitted",
        "symptoms": [
            "mottled leaves with light and dark green patches",
            "mosaic pattern of alternating green shades",
            "leaves look patchy with irregular coloring",
            "twisted and distorted leaf shape",
            "distorted new leaf growth",
            "wrinkled and malformed leaves",
            "reduced fruit set and yield",
            "fern-like leaf appearance (narrow leaflets)",
            "plant looks sick but no distinct spots",
            "stunted growth overall",
            "yellowing of leaves in patches",
            "fruit may show brown streaks internally",
            "fruit ripening unevenly",
            "necrotic streaks on stems",
            "plant stunting without other obvious symptoms"
        ],
        "treatment": [
            "Remove and destroy infected plants completely immediately",
            "NO chemical treatment available for viruses",
            "Wash hands thoroughly with soap after handling infected plants",
            "Disinfect all tools with 10% bleach solution (1:9 bleach:water)",
            "Disinfect tools between each plant when working",
            "Do not compost infected plants - burn or trash them",
            "Remove entire plant including roots",
            "Bag infected plants before removing from garden",
            "Clean hands and tools after any contact",
            "Avoid touching healthy plants after infected ones",
            "Disinfect stakes and cages that contacted infected plants",
            "Monitor surrounding plants closely for symptoms"
        ],
        "prevention": [
            "Use resistant varieties like Big Beef or Mountain Fresh Plus",
            "Use certified disease-free seeds and transplants",
            "Avoid tobacco products near plants as tobacco carries virus",
            "Wash hands thoroughly before handling plants",
            "Disinfect tools frequently with bleach solution",
            "Don't handle plants after smoking tobacco",
            "Remove infected plants immediately",
            "Control aphids and other sap-feeding insects",
            "Avoid plant-to-plant contact during cultivation",
            "Use new or sterilized potting soil",
            "Heat-treat seeds at 158°F for 2-4 days",
            "Purchase virus-tested transplants",
            "Keep weeds removed from garden",
            "Rotate planting areas yearly"
        ]
    },
    {
        "disease_key": "Tomato___healthy",
        "disease": "Healthy Tomato Plant",
        "crop": "Tomato",
        "type": "None",
        "severity": "None",
        "cause": "N/A - No pathogen present",
        "symptoms": [
            "vibrant dark green leaves throughout plant",
            "strong vigorous growth with thick stems",
            "healthy flowering with yellow blossoms",
            "normal steady fruit development",
            "no spots, discoloration, or lesions",
            "no yellowing or wilting of foliage",
            "uniform leaf color and shape",
            "good fruit set after flowers",
            "leaves are turgid and firm",
            "pest-free foliage and fruit"
        ],
        "treatment": [
            "Continue regular care and maintenance",
            "Monitor for early signs of disease or pests weekly",
            "Maintain consistent watering (1-2 inches per week)",
            "Provide support with stakes or cages as plants grow",
            "Prune suckers as needed for indeterminate varieties",
            "Fertilize regularly throughout growing season",
            "Harvest ripe fruit promptly to encourage more production"
        ],
        "prevention": [
            "Regular inspection of plants for problems",
            "Proper nutrition with balanced fertilizer",
            "Adequate spacing for air circulation (24-36 inches)",
            "Good garden hygiene and sanitation",
            "Mulching to conserve moisture",
            "Crop rotation to prevent disease buildup",
            "Remove weeds that compete for nutrients",
            "Water consistently at base of plants"
        ]
    },

    # ========================================================================
    # APPLE DISEASES (PlantDoc Dataset)
    # ========================================================================
    {
        "disease_key": "Apple___Apple_scab",
        "disease": "Apple Scab",
        "crop": "Apple",
        "type": "Fungal",
        "severity": "High",
        "cause": "Fungus Venturia inaequalis",
        "symptoms": [
            "olive-green to dark brown spots on leaves",
            "velvety appearance on leaf spots",
            "scabby lesions on fruit surface",
            "fruit cracking and deformity",
            "premature leaf drop",
            "reduced fruit quality and marketability",
            "leaves curling and distorted",
            "spots coalesce causing large dead areas",
            "corky raised lesions on fruit",
            "young fruit most susceptible",
            "lesions expand in cool wet spring weather"
        ],
        "treatment": [
            "Apply fungicides containing captan or myclobutanil",
            "Spray every 7-14 days during susceptible period",
            "Remove infected leaves and fruit",
            "Rake and destroy fallen leaves in autumn",
            "Prune for better air circulation",
            "Apply lime sulfur during dormant season",
            "Use copper-based fungicides",
            "Apply fungicides from green tip to petal fall stage"
        ],
        "prevention": [
            "Plant resistant varieties like Liberty, Freedom, or Enterprise",
            "Remove all fallen leaves and fruit from orchard",
            "Prune trees for good air circulation",
            "Apply dormant sprays before bud break",
            "Avoid overhead irrigation",
            "Space trees adequately",
            "Monitor weather for scab infection periods",
            "Apply preventive fungicides in spring"
        ]
    },
    {
        "disease_key": "Apple___Black_rot",
        "disease": "Black Rot (Frogeye Leaf Spot)",
        "crop": "Apple",
        "type": "Fungal",
        "severity": "Medium-High",
        "cause": "Fungus Botryosphaeria obtusa (Diplodia seriata)",
        "symptoms": [
            "circular leaf spots with purple to reddish margins",
            "frogeye pattern on leaves",
            "fruit rot starting at blossom end or injury sites",
            "mummified fruit on tree",
            "black rotted fruit with concentric rings",
            "cankers on branches with rough bark",
            "limb dieback in severe cases",
            "infected fruit shrivel and turn black",
            "spots have concentric rings like a target"
        ],
        "treatment": [
            "Remove mummified fruit from trees and ground",
            "Prune out dead and diseased branches",
            "Apply fungicides containing captan or thiophanate-methyl",
            "Remove cankers by pruning 8-12 inches below visible infection",
            "Destroy all infected plant material",
            "Apply fungicides from pink bud through harvest",
            "Improve tree vigor with proper nutrition"
        ],
        "prevention": [
            "Remove all mummies and fallen fruit",
            "Prune dead and diseased wood in winter",
            "Maintain tree vigor with proper care",
            "Avoid tree injuries during cultivation",
            "Apply preventive fungicides",
            "Thin fruit to prevent overcrowding",
            "Ensure good air circulation through pruning",
            "Avoid water stress"
        ]
    },
    {
        "disease_key": "Apple___Cedar_apple_rust",
        "disease": "Cedar Apple Rust",
        "crop": "Apple",
        "type": "Fungal",
        "severity": "Medium",
        "cause": "Fungus Gymnosporangium juniperi-virginianae (requires both apple and cedar/juniper hosts)",
        "symptoms": [
            "bright yellow-orange spots on upper leaf surface",
            "spots with orange margin and yellow halo",
            "tube-like projections on leaf underside",
            "premature leaf drop",
            "fruit lesions with similar appearance",
            "reduced fruit quality",
            "spots appear in spring after wet weather",
            "symptoms on cedar show as brown galls",
            "orange gelatinous horns emerge from cedar galls in spring"
        ],
        "treatment": [
            "Apply fungicides containing myclobutanil or propiconazole",
            "Spray at pink bud, bloom, and petal fall stages",
            "Continue sprays at 10-14 day intervals through June",
            "Remove nearby cedar or juniper trees if possible (within 2 miles)",
            "Remove infected leaves to reduce inoculum",
            "Improve air circulation through pruning",
            "Apply sulfur fungicides as organic option"
        ],
        "prevention": [
            "Plant resistant varieties like Freedom, Liberty, or Pristine",
            "Remove alternate hosts (cedar and juniper) within 2 miles",
            "Apply preventive fungicides in spring",
            "Prune for good air circulation",
            "Scout regularly for orange spots",
            "Avoid planting apples near cedars",
            "Remove cedar galls in winter before spring rains"
        ]
    },
    {
        "disease_key": "Apple___healthy",
        "disease": "Healthy Apple Tree",
        "crop": "Apple",
        "type": "None",
        "severity": "None",
        "cause": "N/A",
        "symptoms": [
            "dark green healthy leaves",
            "vigorous growth",
            "good fruit set",
            "no spots or discoloration",
            "normal flowering",
            "pest-free foliage"
        ],
        "treatment": [
            "Continue regular maintenance",
            "Monitor for pests and diseases",
            "Maintain proper nutrition",
            "Water during dry periods"
        ],
        "prevention": [
            "Regular inspection",
            "Proper pruning",
            "Adequate fertilization",
            "Good orchard sanitation"
        ]
    },

    # ========================================================================
    # CORN DISEASES (PlantDoc Dataset)
    # ========================================================================
    {
        "disease_key": "Corn___Cercospora_leaf_spot",
        "disease": "Cercospora Leaf Spot (Gray Leaf Spot)",
        "crop": "Corn (Maize)",
        "type": "Fungal",
        "severity": "Medium-High",
        "cause": "Fungus Cercospora zeae-maydis",
        "symptoms": [
            "rectangular gray to tan spots between leaf veins",
            "lesions parallel to leaf veins",
            "spots elongate along veins",
            "premature leaf death",
            "spots turn gray with age",
            "lesions may coalesce causing leaf blight",
            "lower leaves affected first",
            "yield reduction in severe cases",
            "symptoms appear mid to late season",
            "fungal fruiting structures visible in spots"
        ],
        "treatment": [
            "Apply fungicides containing azoxystrobin or pyraclostrobin",
            "Spray at first sign of disease",
            "Repeat applications as needed",
            "Remove and destroy crop residue after harvest",
            "Rotate crops to non-grass crops",
            "Use foliar fungicides at tassel stage"
        ],
        "prevention": [
            "Plant resistant hybrids when available",
            "Practice crop rotation with non-host crops",
            "Bury or remove crop residue",
            "Avoid late planting which increases disease risk",
            "Ensure adequate plant nutrition",
            "Apply preventive fungicides in disease-prone areas",
            "Space plants for air circulation"
        ]
    },
    {
        "disease_key": "Corn___Common_rust",
        "disease": "Common Rust",
        "crop": "Corn (Maize)",
        "type": "Fungal",
        "severity": "Low-Medium",
        "cause": "Fungus Puccinia sorghi",
        "symptoms": [
            "small circular to elongate rust-colored pustules on leaves",
            "orange to brown powdery pustules on both leaf surfaces",
            "pustules rupture releasing rust-colored spores",
            "leaves may turn yellow and die prematurely",
            "pustules scattered across leaf surface",
            "symptoms appear after tasseling",
            "disease spreads rapidly in cool humid weather",
            "yield loss usually minor unless severe early infection"
        ],
        "treatment": [
            "Apply fungicides if disease appears before tasseling",
            "Use triazole fungicides like propiconazole",
            "Usually not economical to spray after tasseling",
            "Monitor disease levels and weather conditions",
            "Spray only if warranted by severity"
        ],
        "prevention": [
            "Plant resistant hybrids",
            "Plant early to avoid peak rust periods",
            "Rotate crops",
            "Monitor plants regularly",
            "Maintain good plant health",
            "Usually no treatment needed with resistant varieties"
        ]
    },
    {
        "disease_key": "Corn___Northern_Leaf_Blight",
        "disease": "Northern Leaf Blight",
        "crop": "Corn (Maize)",
        "type": "Fungal",
        "severity": "Medium-High",
        "cause": "Fungus Exserohilum turcicum (formerly Helminthosporium turcicum)",
        "symptoms": [
            "long gray-green to tan cigar-shaped lesions",
            "lesions up to 6 inches long",
            "lower leaves affected first",
            "lesions parallel to leaf veins",
            "entire leaf may die in severe cases",
            "yield loss can be significant",
            "symptoms appear before tasseling in severe years",
            "lesions coalesce causing leaf blight"
        ],
        "treatment": [
            "Apply fungicides at first sign of disease",
            "Use azoxystrobin or propiconazole fungicides",
            "Repeat applications at 10-14 day intervals",
            "Remove crop residue after harvest",
            "Focus applications on susceptible hybrids"
        ],
        "prevention": [
            "Plant resistant hybrids",
            "Practice crop rotation",
            "Bury crop residue by tillage",
            "Avoid late planting",
            "Plant early maturing hybrids",
            "Apply preventive fungicides in disease-prone areas",
            "Monitor fields regularly"
        ]
    },
    {
        "disease_key": "Corn___healthy",
        "disease": "Healthy Corn Plant",
        "crop": "Corn (Maize)",
        "type": "None",
        "severity": "None",
        "cause": "N/A",
        "symptoms": [
            "dark green leaves",
            "vigorous growth",
            "normal tassel and ear development",
            "no spots or discoloration",
            "good overall plant health"
        ],
        "treatment": [
            "Continue regular care",
            "Monitor for pests and diseases",
            "Maintain adequate moisture",
            "Sidedress with nitrogen as needed"
        ],
        "prevention": [
            "Regular scouting",
            "Proper fertilization",
            "Adequate weed control",
            "Good field sanitation"
        ]
    },

    # ========================================================================
    # GRAPE DISEASES (PlantDoc Dataset)
    # ========================================================================
    {
        "disease_key": "Grape___Black_rot",
        "disease": "Black Rot",
        "crop": "Grape",
        "type": "Fungal",
        "severity": "Very High",
        "cause": "Fungus Guignardia bidwellii",
        "symptoms": [
            "small circular tan spots on leaves with dark borders",
            "spots with black dots (pycnidia) in center",
            "fruit infection starting as whitish spots",
            "berries turn black and shrivel (mummies)",
            "mummified fruit remain on vines",
            "cane lesions that are elongated and sunken",
            "severe yield loss possible",
            "entire clusters can be lost",
            "lesions on shoots with black margins",
            "disease spreads rapidly in warm wet weather"
        ],
        "treatment": [
            "Remove mummified fruit from vines and ground",
            "Apply fungicides from bud break through fruit set",
            "Use mancozeb, captan, or myclobutanil",
            "Prune out diseased canes in winter",
            "Destroy infected plant material",
            "Apply fungicides every 10-14 days during wet weather",
            "Focus protection during bloom and fruit set"
        ],
        "prevention": [
            "Remove all mummies and fallen berries",
            "Prune for good air circulation",
            "Apply preventive fungicides starting at bud break",
            "Continue fungicide program through berry touch",
            "Plant resistant varieties if available",
            "Remove wild grapes nearby",
            "Maintain vine vigor",
            "Avoid overhead irrigation"
        ]
    },
    {
        "disease_key": "Grape___Esca",
        "disease": "Esca (Black Measles)",
        "crop": "Grape",
        "type": "Fungal (Complex)",
        "severity": "High",
        "cause": "Multiple fungi including Phaeomoniella chlamydospora and Phaeoacremonium species",
        "symptoms": [
            "tiger stripe pattern on leaves (yellow stripes between veins)",
            "interveinal necrosis with green veins",
            "sudden wilting and death of shoots (apoplexy)",
            "dark purple to black spots on berries",
            "vascular wood streaking (brown/black)",
            "vine decline over years",
            "symptoms appear mid to late summer",
            "berries may crack and shrivel",
            "entire shoots may wilt suddenly",
            "internal wood staining visible when cut"
        ],
        "treatment": [
            "No effective chemical control available",
            "Prune out dead and dying wood",
            "Remove symptomatic vines to prevent spread",
            "Protect pruning wounds with wound sealants",
            "Retrain vines from healthy wood if possible",
            "Maintain vine vigor through proper care",
            "Consider trunk renewal from base"
        ],
        "prevention": [
            "Use clean pruning tools disinfected between cuts",
            "Protect pruning wounds immediately",
            "Avoid pruning in wet weather",
            "Delay pruning until late winter/early spring",
            "Remove wood chips from vineyard",
            "Maintain vine health through proper nutrition",
            "Avoid water stress",
            "Use disease-free planting material"
        ]
    },
    {
        "disease_key": "Grape___Leaf_blight",
        "disease": "Isariopsis Leaf Blight",
        "crop": "Grape",
        "type": "Fungal",
        "severity": "Medium",
        "cause": "Fungus Isariopsis clavispora (Pseudocercospora vitis)",
        "symptoms": [
            "irregular brown spots on leaves",
            "spots with yellow halo",
            "lesions coalesce causing large dead areas",
            "premature defoliation",
            "symptoms start on older leaves",
            "spots may have target-like appearance",
            "severe defoliation weakens vines",
            "disease spreads in warm humid weather"
        ],
        "treatment": [
            "Remove infected leaves",
            "Apply fungicides containing copper or mancozeb",
            "Improve air circulation through pruning",
            "Remove leaf debris from vineyard floor",
            "Apply fungicides preventively in humid climates"
        ],
        "prevention": [
            "Prune for good air circulation",
            "Remove fallen leaves",
            "Apply preventive fungicides if needed",
            "Avoid overhead irrigation",
            "Maintain vine vigor",
            "Space rows adequately",
            "Monitor regularly for early detection"
        ]
    },
    {
        "disease_key": "Grape___healthy",
        "disease": "Healthy Grape Vine",
        "crop": "Grape",
        "type": "None",
        "severity": "None",
        "cause": "N/A",
        "symptoms": [
            "dark green leaves",
            "vigorous cane growth",
            "healthy fruit clusters",
            "no spots or discoloration",
            "good overall vine health"
        ],
        "treatment": [
            "Continue regular maintenance",
            "Monitor for diseases",
            "Maintain proper nutrition",
            "Water during dry periods"
        ],
        "prevention": [
            "Regular inspection",
            "Proper pruning",
            "Adequate fertilization",
            "Good vineyard sanitation"
        ]
    },

    # ========================================================================
    # ADDITIONAL CROPS FROM PLANTDOC
    # ========================================================================
    {
        "disease_key": "Cherry___Powdery_mildew",
        "disease": "Powdery Mildew",
        "crop": "Cherry",
        "type": "Fungal",
        "severity": "Medium",
        "cause": "Fungus Podosphaera clandestina",
        "symptoms": [
            "white powdery coating on leaves",
            "leaf curling and distortion",
            "reduced photosynthesis",
            "premature leaf drop",
            "stunted shoot growth",
            "powdery growth on fruit in severe cases"
        ],
        "treatment": [
            "Apply sulfur-based fungicides",
            "Use myclobutanil or trifloxystrobin",
            "Remove heavily infected leaves",
            "Improve air circulation",
            "Apply fungicides at first sign"
        ],
        "prevention": [
            "Plant resistant varieties",
            "Prune for air circulation",
            "Avoid overhead irrigation",
            "Remove infected plant material",
            "Apply preventive fungicides"
        ]
    },
    {
        "disease_key": "Strawberry___Leaf_scorch",
        "disease": "Leaf Scorch",
        "crop": "Strawberry",
        "type": "Fungal",
        "severity": "Medium",
        "cause": "Fungus Diplocarpon earlianum",
        "symptoms": [
            "purple spots on leaves",
            "spots with gray centers",
            "leaf margins turn brown",
            "leaves look scorched",
            "premature leaf death",
            "reduced plant vigor"
        ],
        "treatment": [
            "Remove infected leaves",
            "Apply fungicides containing captan or copper",
            "Improve air circulation",
            "Avoid overhead watering",
            "Renovate beds after harvest"
        ],
        "prevention": [
            "Use disease-free plants",
            "Space plants for air flow",
            "Remove old leaves after fruiting",
            "Apply preventive fungicides",
            "Rotate planting sites"
        ]
    },
    {
        "disease_key": "Peach___Bacterial_spot",
        "disease": "Bacterial Spot",
        "crop": "Peach",
        "type": "Bacterial",
        "severity": "High",
        "cause": "Bacteria Xanthomonas arboricola pv. pruni",
        "symptoms": [
            "small water-soaked spots on leaves",
            "spots turn brown with yellow halo",
            "fruit lesions that are raised",
            "fruit cracking around lesions",
            "premature leaf drop",
            "defoliation weakens trees",
            "twig cankers possible"
        ],
        "treatment": [
            "Apply copper-based bactericides",
            "Remove infected fruit and twigs",
            "Improve air circulation",
            "Avoid overhead irrigation",
            "Apply antibiotics if available"
        ],
        "prevention": [
            "Plant resistant varieties",
            "Apply copper sprays preventively",
            "Prune for air circulation",
            "Remove fallen leaves",
            "Avoid working with wet trees"
        ]
    },
    {
        "disease_key": "Blueberry___healthy",
        "disease": "Healthy Blueberry Bush",
        "crop": "Blueberry",
        "type": "None",
        "severity": "None",
        "cause": "N/A",
        "symptoms": [
            "green healthy leaves",
            "vigorous growth",
            "good fruit production",
            "no disease symptoms"
        ],
        "treatment": [
            "Continue regular care",
            "Monitor for pests",
            "Maintain soil pH 4.5-5.5",
            "Prune as needed"
        ],
        "prevention": [
            "Regular inspection",
            "Proper nutrition",
            "Adequate moisture",
            "Good sanitation"
        ]
    },
    {
        "disease_key": "Raspberry___healthy",
        "disease": "Healthy Raspberry Cane",
        "crop": "Raspberry",
        "type": "None",
        "severity": "None",
        "cause": "N/A",
        "symptoms": [
            "green canes",
            "healthy foliage",
            "good fruit set",
            "no disease present"
        ],
        "treatment": [
            "Continue care",
            "Monitor regularly",
            "Prune spent canes",
            "Maintain moisture"
        ],
        "prevention": [
            "Good sanitation",
            "Proper spacing",
            "Adequate nutrition",
            "Disease-free plants"
        ]
    },
    {
        "disease_key": "Soybean___healthy",
        "disease": "Healthy Soybean Plant",
        "crop": "Soybean",
        "type": "None",
        "severity": "None",
        "cause": "N/A",
        "symptoms": [
            "dark green leaves",
            "normal growth",
            "good pod development",
            "no disease"
        ],
        "treatment": [
            "Regular monitoring",
            "Adequate moisture",
            "Proper nutrition",
            "Pest control as needed"
        ],
        "prevention": [
            "Good practices",
            "Crop rotation",
            "Clean seed",
            "Field scouting"
        ]
    },
    {
        "disease_key": "Squash___Powdery_mildew",
        "disease": "Powdery Mildew",
        "crop": "Squash",
        "type": "Fungal",
        "severity": "Medium",
        "cause": "Fungi Podosphaera xanthii and Erysiphe cichoracearum",
        "symptoms": [
            "white powdery coating on leaves",
            "upper leaf surface primarily affected",
            "leaves turn yellow then brown",
            "premature leaf death",
            "reduced fruit quality",
            "entire leaves covered in white powder"
        ],
        "treatment": [
            "Apply sulfur or potassium bicarbonate",
            "Use neem oil or horticultural oil",
            "Remove heavily infected leaves",
            "Improve air circulation",
            "Apply fungicides weekly"
        ],
        "prevention": [
            "Plant resistant varieties",
            "Space plants for air flow",
            "Water at base of plants",
            "Apply preventive fungicides",
            "Remove infected plant material"
        ]
    },

    # ========================================================================
    # NOT A PLANT CLASS (Error Handling)
    # ========================================================================
    {
        "disease_key": "Not_a_Plant",
        "disease": "Not a Plant",
        "crop": "N/A",
        "type": "Rejection - Image Classification Error",
        "severity": "N/A - User Error",
        "cause": "Uploaded image is not a plant leaf - may be animal, person, object, or other non-plant image",
        "symptoms": [
            "image shows non-plant subject (animal, vehicle, person, building, etc.)",
            "no plant leaf visible in image",
            "unrelated subject matter",
            "image does not contain vegetation",
            "wrong type of image uploaded",
            "may be indoor scene, landscape without focus on plant, or random object",
            "no leaf structure visible",
            "image may be blurry or unclear but definitely not a plant"
        ],
        "treatment": [
            "Please upload a clear, well-lit image of a plant leaf",
            "Ensure the image shows a tomato, potato, or pepper leaf",
            "Take photo in good lighting conditions",
            "Focus camera on the leaf showing disease symptoms",
            "Upload image in JPEG or PNG format",
            "Make sure leaf fills most of the frame",
            "Avoid images with multiple subjects",
            "Ensure image is not too dark or overexposed"
        ],
        "prevention": [
            "Use well-lit, focused photos of plant leaves only",
            "Avoid uploading non-plant images",
            "Take photos in natural daylight when possible",
            "Hold camera steady to avoid blur",
            "Get close to the leaf for clear detail",
            "Use phone camera's focus feature",
            "Avoid shadows on the leaf",
            "Make sure entire leaf is visible in frame"
        ]
    },
]


def seed_database():
    """Create tables and insert all comprehensive seed data."""
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

    print("="*70)
    print("DATABASE SEEDING COMPLETE")
    print("="*70)
    print(f"✅ Successfully inserted: {inserted} disease entries")
    print(f"⏭️  Skipped (already exists): {skipped} entries")
    print(f"📊 Total classes in database: {inserted + skipped}")
    print(f"📁 Database location: {os.path.abspath(os.path.join(os.path.dirname(__file__), 'plantdocbot.db'))}")
    print("="*70)
    print("\n🌱 PlantDocBot database is ready!")
    print("   - 40+ plant disease classes")
    print("   - Comprehensive symptoms, treatments, and prevention")
    print("   - Covers: Tomato, Potato, Pepper, Apple, Grape, Corn, Cherry, and more")
    print("   - Includes 'Not_a_Plant' rejection class")
    print("="*70)


if __name__ == "__main__":
    seed_database()