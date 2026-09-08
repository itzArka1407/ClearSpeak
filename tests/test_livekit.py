import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
API_KEY = os.getenv('RIME_API_KEY')
if not API_KEY:
    raise ValueError("RIME_API_KEY not found in .env file")

print(f"API Key loaded: {API_KEY[:10]}... (truncated for security)")

try:
    from livekit.plugins import rime
    print("✅ LiveKit Rime plugin imported successfully!")
    
    # Test creating a TTS instance
    tts = rime.TTS(
        model="arcana",
        speaker="celeste",
        speed_alpha=0.9,
        use_websocket=True,
        api_key=API_KEY
    )
    print("✅ TTS instance created successfully!")
    print("LiveKit Rime plugin is ready to use!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
