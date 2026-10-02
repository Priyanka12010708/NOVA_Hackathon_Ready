# NOVA — AI Bridge for Everyday Independence

> **Understand → Decide → Act**

NOVA is an AI-powered accessibility solution that transforms complicated real-world information into clear, simple and actionable guidance.

## Problem

Important information is often locked inside long notices, documents and instructions. Students, elderly people, people with visual/language difficulties, and users with limited digital literacy may struggle to identify what actually matters:

- What is this document about?
- What is the deadline?
- What do I need to submit?
- Where do I need to go?
- What should I do next?

## Solution

NOVA creates an information-to-action layer:

**Upload/Paste → Understand → Extract → Prioritize → Act**

It can identify:
- document category
- deadline
- required actions
- important information
- warnings
- plain-language explanation

## Key Innovation

NOVA is not designed as a generic chatbot. Its output is structured around **actionability**. Instead of returning a large paragraph, it converts information into a checklist and highlights the information a user needs to act.

## AI / Technical Implementation

- Google Gemini for document understanding and structured extraction
- Streamlit for the interactive web interface
- PyMuPDF for PDF text extraction
- Pillow + optional Tesseract for image OCR
- JSON-based structured AI output

## Features

- PDF upload
- Image upload with optional OCR
- Text input
- AI-powered summarization and action extraction
- Priority and deadline detection
- Action checklist
- Important points and warnings
- Simple-language explanation
- Demo fallback mode for testing without an API key

## Run locally

### 1. Install Python

Python 3.10+ is recommended.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Gemini

Copy `.env.example` to `.env` and add your Gemini API key.

The current code reads `GEMINI_API_KEY` from the environment. If you use `.env`, add this line near the top of `app.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

### 5. Run

```powershell
streamlit run app.py
```

The browser will open the NOVA interface.

## Demo

The app includes a pre-filled scholarship-renewal notice. Analyze it to demonstrate the full **Understand → Decide → Act** workflow.

## Future scope

- stronger multilingual support
- voice input/output
- accessibility-first screen-reader optimization
- OCR improvements for low-quality documents
- personalized action reminders
- integrations with institutional portals
- local/private AI deployment for sensitive documents

## Responsible AI

NOVA is an information simplification tool. It does not replace professional medical, legal or financial advice. Users should verify critical information against the original source.
