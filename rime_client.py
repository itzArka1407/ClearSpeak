import asyncio
import json
import websockets
import base64
import os
from dotenv import load_dotenv
from enum import Enum
from urllib.parse import quote

load_dotenv()


class RimeClient:
    def __init__(self, speaker, api_key, debug=False):
        self.speaker = speaker
        self.api_key = api_key
        self.debug = debug
        self.auth_headers = {"Authorization": f"Bearer {api_key}"}
        self.audio_data = b''

    def build_url(self, inline_speed_alpha=None):
        url = (
            f"wss://users-ws.rime.ai/ws3"
            f"?speaker={self.speaker}"
            f"&modelId=mistv3"
            f"&audioFormat=mp3"
        )
        if inline_speed_alpha:
            url += f"&inlineSpeedAlpha={quote(inline_speed_alpha)}"
        if self.debug:
            print(f"🔧 Debug: URL = {url}")
        return url

    async def send_messages(self, websocket, messages):
        for msg in messages:
            print(f"Sending: {msg}")
            await websocket.send(json.dumps(msg))

    async def handle_audio(self, websocket):
        async for message in websocket:
            if isinstance(message, str):
                try:
                    data = json.loads(message)
                    if self.debug:
                        print(f"🔧 Debug: Received: {data}")

                    if data.get('type') == 'chunk' and 'data' in data:
                        audio_chunk = base64.b64decode(data['data'])
                        self.audio_data += audio_chunk
                        print(f"Received audio chunk: {len(audio_chunk)} bytes")

                    if data.get('type') == 'timestamps' and 'word_timestamps' in data:
                        timestamps = data['word_timestamps']
                        print("\n📝 Word timestamps:")
                        for w, t in zip(timestamps['words'], timestamps['start']):
                            print(f"    '{w}' at {t}s")
                except json.JSONDecodeError:
                    print(f"Received non-JSON message: {message[:100]}...")

    async def run(self, messages, inline_speed_alpha=None):
        url = self.build_url(inline_speed_alpha)
        try:
            print(f"🔗 Connecting to {url}")
            async with websockets.connect(url, additional_headers=self.auth_headers) as ws:
                print("✅ Connected! Sending messages...")
                await asyncio.gather(
                    self.send_messages(ws, messages),
                    self.handle_audio(ws)
                )
        except Exception as e:
            print(f"❌ Error: {e}")
            raise

    def save_audio(self, file_path):
        if self.audio_data:
            with open(file_path, 'wb') as f:
                f.write(self.audio_data)
            print(f"💾 Audio saved to {file_path} ({len(self.audio_data)} bytes)")
        else:
            print("❌ No audio data received!")
