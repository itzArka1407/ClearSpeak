import asyncio
import json
import websockets
import base64
import os
from dotenv import load_dotenv

class RimeClient:
    def __init__(self, speaker, api_key):
        # Model can be mistv3, arcana, or coda
        self.url = f"wss://users-ws.rime.ai/ws3?speaker={speaker}&modelId=mistv3&audioFormat=mp3"
        self.auth_headers = {"Authorization": f"Bearer {api_key}"}
        self.audio_data = b''

    async def send_messages(self, websocket, messages):
        for msg in messages:
            await websocket.send(json.dumps(msg))

    async def handle_audio(self, websocket):
        async for audio in websocket:
            if isinstance(audio, str):
                message = json.loads(audio)
                if 'data' in message:
                    self.audio_data += base64.b64decode(message['data'])
                # Word timestamps available here
                if 'word_timestamps' in message:
                    for w, t in zip(message['word_timestamps']['words'], 
                                   message['word_timestamps']['start']):
                        print(f"'{w}' at {t}s")

    async def run(self, messages):
        async with websockets.connect(self.url, additional_headers=self.auth_headers) as ws:
            await asyncio.gather(
                self.send_messages(ws, messages),
                self.handle_audio(ws)
            )

    def save_audio(self, file_path):
        with open(file_path, 'wb') as f:
            f.write(self.audio_data)

API_KEY = os.getenv('RIME_API_KEY')
if not API_KEY:
    raise ValueError("The api key isn't found in the .env file")

# Usage
client = RimeClient("cove", "API KEY GOES HERE")
messages = [
    {"text": "Hello, this is a test. "},
    {"text": "This is the second sentence."},
    {"operation": "eos"}  # Signals end of input
]
asyncio.run(client.run(messages))
client.save_audio("output.mp3")
