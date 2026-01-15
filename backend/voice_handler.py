# Voice handling module using local Whisper for speech-to-text

import os
import glob
import shutil
import whisper

# ============================================================================
# FFmpeg Path Setup
# ============================================================================

def _ensure_ffmpeg_in_path():
    """Add FFmpeg to PATH if it's not already accessible."""
    if shutil.which("ffmpeg"):
        return
    
    # Common FFmpeg installation paths on Windows
    ffmpeg_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin"),
        r"C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin",
        os.path.expandvars(r"%USERPROFILE%\scoop\apps\ffmpeg\current\bin"),
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
    ]
    
    for path_pattern in ffmpeg_paths:
        for match in glob.glob(path_pattern):
            if os.path.isdir(match) and os.path.exists(os.path.join(match, "ffmpeg.exe")):
                os.environ["PATH"] = match + os.pathsep + os.environ.get("PATH", "")
                return

_ensure_ffmpeg_in_path()


# ============================================================================
# Whisper Model Management
# ============================================================================

_model = None

def get_whisper_model():
    """Lazily load the Whisper model (tiny, ~75MB, downloaded on first use)."""
    global _model
    if _model is None:
        _model = whisper.load_model("tiny")
    return _model


# ============================================================================
# Audio Transcription
# ============================================================================

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe an audio file to text using Whisper.
    
    Args:
        audio_path: Path to the audio file
        
    Returns:
        Transcribed text string, or error message prefixed with "ERROR:"
    """
    if not os.path.exists(audio_path):
        return ""
    
    try:
        model = get_whisper_model()
        result = model.transcribe(audio_path)
        return result.get("text", "").strip()
    except Exception as e:
        error_msg = str(e).lower()
        if "ffmpeg" in error_msg:
            return "ERROR: FFmpeg not found. Please install FFmpeg to use voice features."
        return f"ERROR: Transcription failed - {str(e)}"
