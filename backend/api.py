# FastAPI REST API for Plant Disease ChatBot
# Run with: uvicorn backend.api:app --host 0.0.0.0 --port 5000
# Or:       python -m backend.api

import sys
import os
import tempfile

# Ensure project root is on the path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import (
    MODEL_PATH, MODEL_ARCH, IMG_SIZE, IMG_MEAN, IMG_STD,
    NOT_A_PLANT_CLASS, API_HOST, API_PORT,
)

# ============================================================================
# Pydantic request / response models
# ============================================================================

class TextDiagnoseRequest(BaseModel):
    text: str

class DiagnoseResponse(BaseModel):
    disease_key: str
    treatment: str = ""

class ImageDiagnoseResponse(BaseModel):
    disease_key: str
    confidence: float
    top3: list
    treatment: str = ""

class VoiceDiagnoseResponse(BaseModel):
    transcription: str
    disease_key: str
    treatment: str = ""

# ============================================================================
# App
# ============================================================================

app = FastAPI(title="PlantDocBot API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Lazy-loaded heavy resources ----
_model_cache: dict = {}


def _get_model():
    """Load the image classification model once."""
    if "model" not in _model_cache:
        import torch
        from torchvision import transforms
        import timm

        checkpoint = torch.load(MODEL_PATH, map_location="cpu")
        state_dict = checkpoint["model_state_dict"]

        class_to_idx = checkpoint["class_to_idx"]
        idx_to_class = checkpoint["idx_to_class"]
        num_classes = len(class_to_idx)

        class_names = [idx_to_class[i] for i in range(num_classes)]

        model = timm.create_model(MODEL_ARCH, pretrained=False, num_classes=num_classes)
        model.load_state_dict(state_dict, strict=True)
        model.eval()

        transform = transforms.Compose([
            transforms.Resize((IMG_SIZE, IMG_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMG_MEAN, std=IMG_STD),
        ])

        _model_cache["model"] = model
        _model_cache["class_names"] = class_names
        _model_cache["transform"] = transform

    return _model_cache["model"], _model_cache["class_names"], _model_cache["transform"]


# ====================================================================
# ENDPOINTS
# ====================================================================

@app.get("/api/health")
def health():
    """Health check."""
    return {"status": "ok", "service": "PlantDocBot API"}


# ---- Text Diagnosis ----
@app.post("/api/diagnose/text", response_model=DiagnoseResponse)
def diagnose_text(body: TextDiagnoseRequest):
    """Diagnose plant disease from symptom text."""
    text = body.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Missing 'text' field")

    from backend.symptom_matcher import text_diagnosis
    from database import format_treatment_response

    disease_key = text_diagnosis(text)
    return {
        "disease_key": disease_key,
        "treatment": format_treatment_response(disease_key) if disease_key != "Unknown" else "",
    }


# ---- Voice Diagnosis ----
@app.post("/api/diagnose/voice", response_model=VoiceDiagnoseResponse)
async def diagnose_voice(audio: UploadFile = File(...)):
    """Diagnose from an uploaded audio / video file."""
    ext = os.path.splitext(audio.filename or "")[1] or ".wav"

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name

    try:
        from backend.app import process_voice_input
        result = process_voice_input(tmp_path)

        if result["error"]:
            raise HTTPException(status_code=500, detail=result["error"])

        return {
            "transcription": result["transcription"],
            "disease_key": result["disease_key"],
            "treatment": result["response"],
        }
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


# ---- Image Diagnosis ----
@app.post("/api/diagnose/image", response_model=ImageDiagnoseResponse)
async def diagnose_image(image: UploadFile = File(...)):
    """Diagnose from an uploaded leaf image."""
    import torch
    import torch.nn.functional as F
    from PIL import Image

    try:
        img = Image.open(image.file).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    model, class_names, transform = _get_model()

    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1)[0]

    pred_idx = torch.argmax(probs).item()
    disease_key = class_names[pred_idx]
    confidence = probs[pred_idx].item()

    if disease_key == NOT_A_PLANT_CLASS:
        raise HTTPException(
            status_code=400,
            detail="Not a plant leaf. Please upload a plant image.",
        )

    top3 = torch.topk(probs, min(3, len(class_names)))
    top3_results = [
        {"disease_key": class_names[top3.indices[i].item()], "confidence": round(top3.values[i].item(), 4)}
        for i in range(len(top3.indices))
    ]

    from database import format_treatment_response
    return {
        "disease_key": disease_key,
        "confidence": round(confidence, 4),
        "top3": top3_results,
        "treatment": format_treatment_response(disease_key, confidence),
    }


# ---- Disease List ----
@app.get("/api/diseases")
def list_diseases():
    """List all known diseases."""
    from database import get_all_disease_keys
    return {"diseases": get_all_disease_keys()}


# ============================================================================
# Run directly: python -m backend.api
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.api:app", host=API_HOST, port=API_PORT, reload=True)
