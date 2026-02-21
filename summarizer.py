import requests
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "deepseek-r1:14b"

def summarize_text(text):
    """Uses Ollama (DeepSeek) to summarize the provided text."""
    if not text or not text.strip():
        return "No text provided for summarization."
    
    prompt = f"""You are a 'Conversation Agent'. Your goal is to provide a concise, high-quality summary of the following transcript. 
Focus on:
1. Main topics discussed.
2. Key decisions made.
3. Action items (if any).

Transcript:
{text}

Summary:"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )
        response.raise_for_status()
        full_response = response.json().get('response', '')
        
        # Remove thinking tokens if present
        summary = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL | re.IGNORECASE).strip()
        
        return summary
    except Exception as e:
        return f"Error during summarization: {e}"
