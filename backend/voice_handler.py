# Voice handling module using local Whisper for speech-to-text

import os
import whisper

# Load model lazily to avoid overhead if voice is not used
_model = None

def get_whisper_model():
    """Lazily load the Whisper model."""
    global _model
    if _model is None:
        # Using 'tiny' model for fast local inference
        # It will be downloaded on first use (~75MB)
        _model = whisper.load_model("tiny")
    return _model

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe an audio file to text.
    
    Args:
        audio_path: Path to the audio file
        
    Returns:
        Transcribed text string
    """
    if not os.path.exists(audio_path):
        return ""
        
    try:
        model = get_whisper_model()
        result = model.transcribe(audio_path)
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error during transcription: {e}")
        # Hint for missing ffmpeg which is a common error
        if "ffmpeg" in str(e).lower():
            return "ERROR: FFmpeg not found. Please install FFmpeg on your system to use voice features."
        return f"ERROR: Transcription failed - {str(e)}"
