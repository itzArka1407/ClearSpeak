import sys
import os
import asyncio
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rime_client import RimeClient

load_dotenv()
API_KEY = os.getenv('RIME_API_KEY')


async def test_emphasis():
    print("=" * 60)
    print("🔬 Testing Rime Emphasis Feature")
    print("=" * 60)

    # Test different speeds
    test_cases = [
        (1.0, "Normal speed (no emphasis)"),
        (2.0, "2x slower"),
        (3.0, "3x slower"),
        (4.0, "4x slower"),
        (5.0, "5x slower"),
    ]

    for speed, description in test_cases:
        print(f"\n{'='*60}")
        print(f"🎯 Testing: {description}")
        print(f"📊 Speed: {speed}x")
        print("-" * 60)

        client = RimeClient("cove", API_KEY, debug=False)
        messages = [
            {"text": f"This is a test. The number is [1234]. Speed is {speed}x."},
            {"operation": "eos"}
        ]

        try:
            await client.run(messages, inline_speed_alpha=str(speed))
            client.save_audio(f"test_speed_{speed}x.mp3")
            print(f"✅ Saved: test_speed_{speed}x.mp3")
        except Exception as e:
            print(f"❌ Failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_emphasis())
