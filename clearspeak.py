import asyncio
import json
import websockets
import base64
import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class EmphasisLevel(Enum):
    """Pre-defined emphasis levels for different types of content"""
    NORMAL = 1.0
    SUBTLE = 1.5
    MEDIUM = 2.5
    STRONG = 3.5
    EXTREME = 5.0
    
    # Specialized presets
    PHONE_NUMBER = 5.0
    OTP = 10.0
    CRITICAL = 12.0

class RimeClient:
    def __init__(self, speaker, api_key, inline_speed=1.0):
        self.url = (
            f"wss://users-ws.rime.ai/ws3"
            f"?speaker={speaker}"
            f"&modelId=mistv3"
            f"&audioFormat=mp3"
            f"&inlineSpeedAlpha={inline_speed}"
        )
        self.auth_headers = {"Authorization": f"Bearer {api_key}"}
        self.audio_data = b''

    async def send_messages(self, websocket, messages):
        for msg in messages:
            print(f"Sending: {msg}")
            await websocket.send(json.dumps(msg))

    async def handle_audio(self, websocket):
        async for message in websocket:
            if isinstance(message, str):
                try:
                    data = json.loads(message)
                    if 'data' in data:
                        audio_chunk = base64.b64decode(data['data'])
                        self.audio_data += audio_chunk
                        print(f"Received audio chunk: {len(audio_chunk)} bytes")
                    
                    if 'word_timestamps' in data:
                        timestamps = data['word_timestamps']
                        for w, t in zip(timestamps['words'], timestamps['start']):
                            print(f"'{w}' at {t}s")
                except json.JSONDecodeError:
                    print(f"Received non-JSON message: {message[:100]}...")

    async def run(self, messages):
        try:
            print(f"Connecting to {self.url}")
            async with websockets.connect(self.url, additional_headers=self.auth_headers) as ws:
                print("Connected! Sending messages...")
                await asyncio.gather(
                    self.send_messages(ws, messages),
                    self.handle_audio(ws)
                )
        except Exception as e:
            print(f"Error: {e}")
            raise

    def save_audio(self, file_path):
        if self.audio_data:
            with open(file_path, 'wb') as f:
                f.write(self.audio_data)
            print(f"Audio saved to {file_path} ({len(self.audio_data)} bytes)")
        else:
            print("No audio data received!")

# Get API key from environment
API_KEY = os.getenv('RIME_API_KEY')
if not API_KEY:
    raise ValueError("RIME_API_KEY not found in .env file")

async def main():
    # Choose your emphasis level
    speed = EmphasisLevel.OTP.value  # 3.0x slower - perfect for OTPs
    
    # Or use custom values:
    # speed = 2.5  # 2.5x slower
    
    client = RimeClient("cove", API_KEY, inline_speed=speed)
    
    print(f"🔊 Using inline speed: {speed}x")
    print("📝 Words in [brackets] will be emphasized")
    print("-" * 50)
    
    # Example with different types of content
    messages = [
        {"text": "Welcome to ClearSpeak verification service."},
        {"text": "Your phone number is [555-0199]."},
        {"text": "The one-time password for your account is [8472]."},
        {"text": "Please enter this code to continue."},
        {"text": "I repeat: your OTP is [eight-four-seven-two]."},
        {"operation": "eos"}
    ]
    
    try:
        await client.run(messages)
        client.save_audio("output.mp3")
        print(f"✅ Audio generated successfully!")
        print(f"📊 Speed multiplier applied to bracketed text: {speed}x")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
