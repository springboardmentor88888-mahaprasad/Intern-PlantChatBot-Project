# Backend module for Plant Disease ChatBot
# Re-exports from database layer and internal modules

from .chatbot import *
from .voice_handler import transcribe_audio
from .symptom_matcher import text_diagnosis
from .app import process_voice_input

# Import from database layer
from database import get_treatment, format_treatment_response, get_uncertain_response
