import whisper
import os
from static_ffmpeg import add_paths

# This line ensures ffmpeg is available automatically
add_paths()

def transcribe_audio(file_path):
    """Transcribes audio file to text using OpenAI Whisper."""
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    try:
        # Load the base model (good balance of speed and accuracy)
        # Options: tiny, base, small, medium, large
        print("Loading AI transcription model (this may take a moment on first run)...")
        model = whisper.load_model("base")
        
        print(f"Transcribing {file_path}...")
        result = model.transcribe(file_path)
        
        return result['text'].strip()
    except Exception as e:
        return f"Error during transcription: {e}"
