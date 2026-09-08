from livekit.plugins import rime
from livekit.agents import AgentSession

# Create TTS instance with your voice settings
tts = rime.TTS(
    model="arcana",      # Options: arcana, coda, mistv2
    speaker="celeste",   # Voice ID
    speed_alpha=0.9,     # Speed adjustment
    use_websocket=True   # Enable streaming
)

# Use in your agent
session = AgentSession(
    tts=tts,
    # ... other components like LLM, STT, etc.
)
