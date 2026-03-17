# Centralized configuration for PlantDocBot
# All hardcoded values live here, loaded from .env with sensible defaults.

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# ============================================================================
# Project paths
# ============================================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load .env from project root
_env_path = PROJECT_ROOT / ".env"
if _env_path.exists():
    load_dotenv(_env_path)
else:
    load_dotenv()

# ============================================================================
# Model settings
# ============================================================================
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_FILENAME = os.getenv("MODEL_FILENAME", "resnet50_plantvillage_checkpoint.pth")
MODEL_PATH = str(MODEL_DIR / MODEL_FILENAME)
MODEL_ARCH = os.getenv("MODEL_ARCH", "tf_efficientnetv2_s")
IMG_SIZE = int(os.getenv("IMG_SIZE", "224"))

# HuggingFace repo for auto-downloading the model checkpoint
HF_REPO_ID = os.getenv("HF_REPO_ID", "sayandip05/plantdocbot-efficientnetv2s")

# ImageNet normalisation (used by all EfficientNet / ResNet variants)
IMG_MEAN = [0.485, 0.456, 0.406]
IMG_STD = [0.229, 0.224, 0.225]

# ============================================================================
# Confidence thresholds
# ============================================================================
CONFIDENCE_LOW = float(os.getenv("CONFIDENCE_LOW", "0.6"))
CONFIDENCE_HIGH = float(os.getenv("CONFIDENCE_HIGH", "0.8"))
CONFIDENCE_MODERATE = float(os.getenv("CONFIDENCE_MODERATE", "0.4"))

# ============================================================================
# Groq API
# ============================================================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_FALLBACK_MODEL = os.getenv("GROQ_FALLBACK_MODEL", "llama3-70b-8192")

# ============================================================================
# Whisper
# ============================================================================
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "tiny")

# ============================================================================
# API server
# ============================================================================
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "5000"))

# ============================================================================
# Not-a-Plant rejection class name (must match checkpoint class)
# ============================================================================
NOT_A_PLANT_CLASS = os.getenv("NOT_A_PLANT_CLASS", "Not_a_Plant")


# ============================================================================
# Auto-download model from HuggingFace if not present locally
# ============================================================================
def ensure_model():
    """Download the model checkpoint from HuggingFace if it doesn't exist."""
    if os.path.exists(MODEL_PATH):
        return MODEL_PATH

    logger.info(f"Model not found at {MODEL_PATH}. Downloading from HuggingFace ({HF_REPO_ID})...")
    os.makedirs(str(MODEL_DIR), exist_ok=True)

    try:
        from huggingface_hub import hf_hub_download
        downloaded = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename=MODEL_FILENAME,
            local_dir=str(MODEL_DIR),
            local_dir_use_symlinks=False,
        )
        logger.info(f"Model downloaded to {downloaded}")
        return MODEL_PATH
    except Exception as e:
        logger.error(f"Failed to download model: {e}")
        raise RuntimeError(
            f"Model file not found at {MODEL_PATH} and auto-download failed. "
            f"Please download manually from https://huggingface.co/{HF_REPO_ID}"
        ) from e


# Run on import — ensures model is available before anything tries to load it
ensure_model()
