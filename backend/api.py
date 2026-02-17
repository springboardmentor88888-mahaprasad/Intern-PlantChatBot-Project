# Flask REST API for Plant Disease ChatBot
# Run with: python -m backend.api
# Or:       flask --app backend.api run --port 5000

import sys
import os
import tempfile

# Ensure project root is on the path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# ============================================================================
# App Factory
# ============================================================================

def create_app():
    app = Flask(__name__)
    CORS(app)

    # ---- Lazy-loaded heavy resources ----
    _model_cache = {}

    def _get_model():
        """Load the image classification model once."""
        if "model" not in _model_cache:
            import torch
            from torchvision import models, transforms

            MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "resnet50_plantvillage_checkpoint.pth")
            PLANTVILLAGE_CLASSES = [
                "Pepper__bell___Bacterial_spot",
                "Pepper__bell___healthy",
                "Potato___Early_blight",
                "Potato___Late_blight",
                "Potato___healthy",
                "Tomato___Bacterial_spot",
                "Tomato___Early_blight",
                "Tomato___Late_blight",
                "Tomato___Leaf_Mold",
                "Tomato___Septoria_leaf_spot",
                "Tomato___Spider_mites Two-spotted_spider_mite",
                "Tomato___Target_Spot",
                "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
                "Tomato___Tomato_mosaic_virus",
                "Tomato___healthy",
            ]

            checkpoint = torch.load(MODEL_PATH, map_location="cpu")
            state_dict = checkpoint["model_state_dict"]
            num_classes = state_dict["fc.weight"].shape[0]

            if num_classes == len(PLANTVILLAGE_CLASSES):
                class_names = PLANTVILLAGE_CLASSES
            else:
                class_names = checkpoint.get("class_names", [])[:num_classes]
                if not class_names:
                    class_names = [f"Disease_{i}" for i in range(num_classes)]

            model = models.resnet50(weights=None)
            model.fc = torch.nn.Linear(2048, num_classes)
            model.load_state_dict(state_dict, strict=True)
            model.eval()

            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])

            _model_cache["model"] = model
            _model_cache["class_names"] = class_names
            _model_cache["transform"] = transform

        return _model_cache["model"], _model_cache["class_names"], _model_cache["transform"]

    # ====================================================================
    # ENDPOINTS
    # ====================================================================

    @app.route("/api/health", methods=["GET"])
    def health():
        """Health check endpoint."""
        return jsonify({"status": "ok", "service": "PlantDocBot API"})

    # ----------------------------------------------------------------
    # Text Diagnosis
    # ----------------------------------------------------------------
    @app.route("/api/diagnose/text", methods=["POST"])
    def diagnose_text():
        """
        Diagnose plant disease from symptom text.

        Body (JSON): { "text": "My tomato leaves have dark spots..." }
        Returns:     { "disease_key": "...", "treatment": "..." }
        """
        data = request.get_json(silent=True) or {}
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "Missing 'text' field"}), 400

        from backend.symptom_matcher import text_diagnosis
        from knowledge import format_treatment_response

        disease_key = text_diagnosis(text)

        return jsonify({
            "disease_key": disease_key,
            "treatment": format_treatment_response(disease_key) if disease_key != "Unknown" else ""
        })

    # ----------------------------------------------------------------
    # Voice / Video Diagnosis
    # ----------------------------------------------------------------
    @app.route("/api/diagnose/voice", methods=["POST"])
    def diagnose_voice():
        """
        Diagnose from an uploaded audio or video file.

        Body (multipart/form-data): file field named 'audio'
        Returns: { "transcription": "...", "disease_key": "...", "treatment": "..." }
        """
        if "audio" not in request.files:
            return jsonify({"error": "Missing 'audio' file"}), 400

        audio_file = request.files["audio"]
        ext = os.path.splitext(audio_file.filename)[1] or ".wav"

        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            audio_file.save(tmp)
            tmp_path = tmp.name

        try:
            from backend.app import process_voice_input
            result = process_voice_input(tmp_path)

            if result["error"]:
                return jsonify({"error": result["error"]}), 500

            return jsonify({
                "transcription": result["transcription"],
                "disease_key": result["disease_key"],
                "treatment": result["response"]
            })
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    # ----------------------------------------------------------------
    # Image Diagnosis
    # ----------------------------------------------------------------
    @app.route("/api/diagnose/image", methods=["POST"])
    def diagnose_image():
        """
        Diagnose from an uploaded leaf image.

        Body (multipart/form-data): file field named 'image'
        Returns: { "disease_key": "...", "confidence": 0.95, "top3": [...], "treatment": "..." }
        """
        if "image" not in request.files:
            return jsonify({"error": "Missing 'image' file"}), 400

        import torch
        import torch.nn.functional as F
        from PIL import Image

        image_file = request.files["image"]

        try:
            image = Image.open(image_file).convert("RGB")
        except Exception:
            return jsonify({"error": "Invalid image file"}), 400

        model, class_names, transform = _get_model()

        img_tensor = transform(image).unsqueeze(0)
        with torch.no_grad():
            outputs = model(img_tensor)
            probs = F.softmax(outputs, dim=1)[0]

        pred_idx = torch.argmax(probs).item()
        disease_key = class_names[pred_idx]
        confidence = probs[pred_idx].item()

        # Top-3 predictions
        top3 = torch.topk(probs, min(3, len(class_names)))
        top3_results = [
            {"disease_key": class_names[top3.indices[i].item()], "confidence": round(top3.values[i].item(), 4)}
            for i in range(len(top3.indices))
        ]

        from knowledge import format_treatment_response
        return jsonify({
            "disease_key": disease_key,
            "confidence": round(confidence, 4),
            "top3": top3_results,
            "treatment": format_treatment_response(disease_key, confidence)
        })

    # ----------------------------------------------------------------
    # Disease List
    # ----------------------------------------------------------------
    @app.route("/api/diseases", methods=["GET"])
    def list_diseases():
        """List all known diseases."""
        from knowledge.treatments import get_all_disease_keys
        return jsonify({"diseases": get_all_disease_keys()})

    return app


# ============================================================================
# Run directly: python -m backend.api
# ============================================================================
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
