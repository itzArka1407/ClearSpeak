# ClearSpeak AI

A preprocessing layer that makes critical information (OTPs, phone numbers, transaction IDs, amounts, times) easier to understand when spoken by a TTS engine.

## Problem

TTS engines read numeric and alphanumeric strings as continuous units, which reduces intelligibility for information that must be heard exactly.

Example: `"Your OTP is 583291."` — spoken quickly, `583291` can be misheard as `583921` or similar.

This affects OTPs, phone numbers, transaction/reference IDs, alphanumeric codes, dates/times, and payment amounts.

## Solution

ClearSpeak detects critical information in a message, rewrites it into a speech-friendly form, and forwards the result to Rime for audio generation. Only the relevant spans are transformed; the rest of the sentence is left natural.

| Input | Output |
|---|---|
| `Your OTP is 583291.` | `Your OTP is 5 8 3 2 9 1.` |
| `Your reference ID is 678-ABC-007.` | `Your reference ID is 6 7 8 dash A B C dash 0 0 7.` |

## Pipeline

```
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
```

1. User enters a message.
2. Message is scanned for patterns indicating critical information.
3. Detected spans are classified by type (phone number, code, time, money, mixed identifier).
4. Each span is rewritten into a speech-optimized form.
5. The processed text is sent to Rime for TTS synthesis.

## Detection & Transformation Rules

### Phone Numbers
Spoken digit by digit.
`9876543210` → `9 8 7 6 5 4 3 2 1 0`

### Numeric Codes (OTPs, verification codes)
Spoken digit by digit to prevent the sequence being read as a single number.
`583291` → `5 8 3 2 9 1`

### Mixed Identifiers
Letters, digits, and symbols are spelled out individually; symbols are converted to their spoken names.
`678-ABC-007` → `6 7 8 dash A B C dash 0 0 7`
`TXN@89#X21` → `T X N at symbol 8 9 hash X 2 1`

### Time
Converted to natural spoken form.
`4:30 PM` → `four thirty P M`

### Money
Converted to words.
`₹1,500` → `one thousand five hundred rupees`

## Tech Stack

- Python
- Streamlit — UI
- Rime AI — TTS engine
- Requests — API calls
- python-dotenv — environment variable management
- Regular expressions — pattern-based detection (no ML model required)

## Setup

A virtual environment is recommended to avoid installing dependencies into the global Python environment.

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install streamlit
```

Set your Rime API key in a `.env` file (not committed to source control):

```
RIME_API_KEY=your_api_key_here
```

## Running the App

```bash
streamlit run app.py
```

This launches the Streamlit interface in your default browser.

## Usage

1. Enter a message.
2. Analyze the message.
3. View detected critical information.
4. View the speech-optimized version.
5. Generate audio via Rime.
6. Play or download the generated audio.

## Notes

- Detection is rule/pattern-based, keeping the app lightweight and fast.
- Rime integration is decoupled from detection/transformation logic for easier testing and modification.
- API keys are loaded from environment variables, never hardcoded.
