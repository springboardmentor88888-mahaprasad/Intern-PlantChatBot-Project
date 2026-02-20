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
            from torchvision import transforms
            import timm

            MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "resnet50_plantvillage_checkpoint1.pth")

            checkpoint = torch.load(MODEL_PATH, map_location="cpu")
            state_dict = checkpoint["model_state_dict"]

            # Get class mappings from checkpoint
            class_to_idx = checkpoint["class_to_idx"]
            idx_to_class = checkpoint["idx_to_class"]
            num_classes = len(class_to_idx)

            # Build ordered class_names list from idx_to_class
            class_names = [idx_to_class[i] for i in range(num_classes)]

            # Create EfficientNetV2-Small model
            model = timm.create_model('tf_efficientnetv2_s', pretrained=False, num_classes=num_classes)
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
        from database import format_treatment_response

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

        # Guard: reject non-plant images
        if disease_key == "Not_a_Plant":
            return jsonify({"error": "Not a plant leaf. Please upload a plant image.", "disease_key": "Not_a_Plant"}), 400

        # Top-3 predictions
        top3 = torch.topk(probs, min(3, len(class_names)))
        top3_results = [
            {"disease_key": class_names[top3.indices[i].item()], "confidence": round(top3.values[i].item(), 4)}
            for i in range(len(top3.indices))
        ]

        from database import format_treatment_response
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
        from database import get_all_disease_keys
        return jsonify({"diseases": get_all_disease_keys()})

    return app


# ============================================================================
# Run directly: python -m backend.api
# ============================================================================
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
