import os
from dotenv import load_dotenv
from livekit.plugins import rime
from livekit.agents import AgentSession

# Load environment variables
load_dotenv()

# Get API key from environment
API_KEY = os.getenv('RIME_API_KEY')
if not API_KEY:
    raise ValueError("RIME_API_KEY not found in .env file")

# Create TTS instance with your voice settings
tts = rime.TTS(
    model="arcana",      # Options: arcana, coda, mistv2
    speaker="celeste",   # Voice ID
    speed_alpha=0.9,     # Speed adjustment
    use_websocket=True,  # Enable streaming
    api_key=API_KEY      # Pass API key explicitly
)

# Use in your agent
session = AgentSession(
    tts=tts,
    # ... other components like LLM, STT, etc.
)

print("LiveKit Rime plugin configured successfully!")
