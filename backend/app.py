# Backend application logic for Plant Disease ChatBot

from .voice_handler import transcribe_audio
from .symptom_matcher import text_diagnosis
from knowledge import format_treatment_response

def process_voice_input(audio_path: str) -> dict:
    """
    Process an audio file and return transcription and diagnosis results.
    
    Args:
        audio_path: Path to the audio file
        
    Returns:
        Dictionary with transcription, disease_key, and formatted_response
    """
    transcription = transcribe_audio(audio_path)
    
    if transcription.startswith("ERROR"):
        return {
            "error": transcription,
            "transcription": "",
            "disease_key": "Unknown",
            "response": ""
        }
        
    disease_key = text_diagnosis(transcription)
    
    return {
        "error": None,
        "transcription": transcription,
        "disease_key": disease_key,
        "response": format_treatment_response(disease_key) if disease_key != "Unknown" else ""
    }
