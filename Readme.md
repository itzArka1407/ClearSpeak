# ClearSpeak AI

Making important information easier to hear and understand.

ClearSpeak is a voice-focused application designed to make important information easier to understand when it is spoken by an AI voice system.

The idea came from a simple problem: not every piece of text should be spoken in the same way.

A normal sentence can be spoken naturally. But an OTP, phone number, transaction ID, reference code, time, or payment amount can be difficult to understand when it is spoken quickly or treated like ordinary text.

ClearSpeak works as a layer between the message and the voice engine. It looks for information that needs extra clarity, changes the way that information is written for speech, and then sends the processed message to Rime for voice generation.

## The Problem

Voice assistants are generally good at speaking normal sentences, but they can struggle when a message contains information that people need to hear exactly.

For example, consider:

"Your OTP is 583291."

If the voice system reads the number too quickly, it can be difficult to tell whether the code was 583291, 583921, or something else.

The same problem can happen with:

- Phone numbers
- OTPs
- Transaction IDs
- Reference numbers
- Alphanumeric codes
- Dates and times
- Payment amounts
- Other important identifiers

These are small details, but getting them wrong can have serious consequences.

## What ClearSpeak Does

ClearSpeak identifies important pieces of information inside a message and changes how they are presented to the voice engine.

Instead of simply sending the original sentence to the TTS system, ClearSpeak first processes it.

For example:

Original:

"Your OTP is 583291."

Speech-optimized:

"Your OTP is 5 8 3 2 9 1."

Another example:

"Your reference ID is 678-ABC-007."

Speech-optimized:

"Your reference ID is 6 7 8 dash A B C dash 0 0 7."

The goal is not to make every sentence sound unnatural. The goal is to change only the parts where accuracy matters.

## How It Works

The application follows a simple pipeline:

User Message
        |
        v
Critical Information Detection
        |
        v
Information Classification
        |
        v
Speech Optimization
        |
        v
Rime Text-to-Speech
        |
        v
Audio Output

First, the user enters a message.

ClearSpeak scans the message and looks for patterns that could contain important information.

It then identifies what type of information was found, such as a phone number, numeric code, time, money amount, or mixed identifier.

The relevant information is then transformed into a form that is easier for a voice system to pronounce clearly.

Finally, the processed message is sent to Rime for text-to-speech generation.

## Information Detection

ClearSpeak currently looks for several types of critical information.

### Phone Numbers

Phone numbers are detected and spoken digit by digit.

Example:

9876543210

becomes:

9 8 7 6 5 4 3 2 1 0

### Numeric Codes

Short numeric sequences such as OTPs and verification codes are detected.

Example:

583291

becomes:

5 8 3 2 9 1

This helps prevent the voice system from treating the entire sequence as a normal number.

### Mixed Identifiers

ClearSpeak can also handle identifiers containing letters, numbers, and symbols.

For example:

678-ABC-007

can be converted into:

6 7 8 dash A B C dash 0 0 7

It can also handle identifiers such as:

TXN@89#X21

which can be spoken as:

T X N at symbol 8 9 hash X 2 1

### Time

Times are converted into a more natural spoken form.

For example:

4:30 PM

becomes:

four thirty P M

### Money

Payment amounts are converted into words where possible.

For example:

₹1,500

becomes:

one thousand five hundred rupees

This makes monetary values easier to understand when they are spoken aloud.

## Rime Integration

ClearSpeak uses Rime as its text-to-speech engine.

After the message has been processed, the speech-optimized text is sent to the Rime API and converted into audio.

The application then provides the generated audio directly in the Streamlit interface.

The Rime integration is handled separately from the detection and transformation logic, which keeps the project relatively simple to modify and test.

The API key is stored locally in an environment file rather than being placed directly in the source code.

## The Application

The interface is built using Streamlit.

The user can:

1. Enter a message.
2. Analyze the message.
3. See what critical information was detected.
4. See how ClearSpeak changed the message.
5. Generate the final voice output.
6. Listen to the generated audio.
7. Download the audio if needed.

The interface is designed to make the processing easy to understand during a demonstration.

Instead of only showing the final audio, the application shows the original message and the speech-optimized version so that the user can see what ClearSpeak is doing.

## Technology

The project uses:

- Python
- Streamlit
- Rime AI Text-to-Speech
- Requests
- Python-dotenv
- Regular expressions for information detection

The project does not require a large machine learning model for the detection layer. Most of the current detection is based on patterns and rules.

This keeps the application lightweight and makes it possible to process messages quickly.

## Project Structure

```text
ClearSpeak/
|
|-- app.py
|-- clearspeak.py
|-- rime_tts.py
|-- requirements.txt
|-- .env
|-- README.md
|-- RIME_EVIDENCE.md