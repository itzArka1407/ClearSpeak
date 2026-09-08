# To test different speeds of different speeches at different configs

import asyncio
import os
from dotenv import load_dotenv
import sys

# Import your RimeClient class
# Make sure this file is in the same directory or adjust the path
from import_asyncio import RimeClient

load_dotenv()
API_KEY = os.getenv('RIME_API_KEY')

async def test_speed(speed, filename, description):
    print(f"\n🎯 Testing: {description} ({speed}x)")
    client = RimeClient("cove", API_KEY, inline_speed=speed)
    messages = [
        {"text": f"This is a test. Your code is [8472]. Speed is {speed}x."},
        {"operation": "eos"}
    ]
    try:
        await client.run(messages)
        client.save_audio(filename)
        print(f"✅ Saved to {filename}")
    except Exception as e:
        print(f"❌ Failed: {e}")

async def main():
    # Test different speed values
    test_cases = [
        (1.0, "test_normal.mp3", "Normal (1.0x)"),
        (1.5, "test_subtle.mp3", "Subtle (1.5x)"),
        (2.0, "test_phone.mp3", "Phone number (2.0x)"),
        (3.0, "test_otp.mp3", "OTP (3.0x)"),
        (4.0, "test_critical.mp3", "Critical (4.0x)"),
        (5.0, "test_extreme.mp3", "Extreme (5.0x)"),
    ]
    
    print("🎵 Generating test audio files with different speeds...")
    print("=" * 50)
    
    for speed, filename, description in test_cases:
        await test_speed(speed, filename, description)
    
    print("\n" + "=" * 50)
    print("✅ All files generated! Listen to each to find the best speed.")
    print("📊 Speed comparison:")
    print("   - 1.0x = Normal speech")
    print("   - 1.5x = Slight emphasis")
    print("   - 2.0x = Good for phone numbers")
    print("   - 3.0x = Good for OTPs/codes")
    print("   - 4.0x = Strong emphasis")
    print("   - 5.0x = Very dramatic/slow")

if __name__ == "__main__":
    asyncio.run(main())
