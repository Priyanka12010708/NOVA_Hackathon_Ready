import os
import json
import time

from google import genai


def analyze_information(text, language="English"):
    """
    Analyze only the current document using Gemini AI.
    Automatically falls back to another Gemini model if
    the primary model is temporarily unavailable.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "priority": "Configuration error",
            "category": "Unknown",
            "deadline": "Not found",
            "summary": "Gemini API key was not found.",
            "actions": [],
            "important_points": [],
            "warnings": [
                "Please check your .env file and GEMINI_API_KEY."
            ],
            "simple_explanation": "Add your Gemini API key to the .env file.",
            "demo_mode": True
        }

    if not text or not text.strip():
        return {
            "priority": "No input",
            "category": "Unknown",
            "deadline": "Not found",
            "summary": "No document or text was provided.",
            "actions": [],
            "important_points": [],
            "warnings": ["Please upload a document or paste some text."],
            "simple_explanation": "Give NOVA some information to analyze.",
            "demo_mode": False
        }

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are NOVA, an AI assistant that converts difficult information
into clear, actionable information.

IMPORTANT RULES:

- Analyze ONLY the CURRENT DOCUMENT.
- Never use information from previous documents.
- Never use information from previous examples.
- Never use information from memory.
- Do not invent facts.
- Do not invent dates, deadlines, names, locations, requirements,
  eligibility rules, documents, or warnings.
- If something is not present in the document, write "Not found".
- Keep dates and times exactly as they appear in the document.
- Create practical actions based only on the document.
- Return ONLY valid JSON.

CURRENT DOCUMENT:
========================
{text}
========================

OUTPUT LANGUAGE:
{language}

Return exactly this JSON structure:

{{
    "priority": "High | Medium | Low",
    "category": "short category name",
    "deadline": "most important deadline or Not found",
    "summary": "2-3 sentence summary based only on the current document",
    "actions": [
        "specific action 1",
        "specific action 2",
        "specific action 3"
    ],
    "important_points": [
        "important fact 1",
        "important fact 2",
        "important fact 3"
    ],
    "warnings": [
        "important warning or Not found"
    ],
    "simple_explanation": "Explain what the person needs to do in very simple language."
}}

IMPORTANT:
Use ONLY the CURRENT DOCUMENT.
Do not reuse information from any previous document.
"""

    # Try the latest model first, then use a lighter fallback
    models = [
        "gemini-3.8-flash",
        "gemini-3.5-flash-lite"
    ]

    last_error = None

    for model_name in models:

        try:

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )

            response_text = response.text.strip()

            result = json.loads(response_text)

            # Make sure required fields exist
            result.setdefault("priority", "Not found")
            result.setdefault("category", "Not found")
            result.setdefault("deadline", "Not found")
            result.setdefault("summary", "Not found")
            result.setdefault("actions", [])
            result.setdefault("important_points", [])
            result.setdefault("warnings", [])
            result.setdefault(
                "simple_explanation",
                "Not found"
            )

            result["demo_mode"] = False
            result["model_used"] = model_name

            return result

        except Exception as e:

            last_error = e

            error_text = str(e).lower()

            # If it is a temporary server/high-demand error,
            # immediately try the fallback model.
            if (
                "503" in error_text
                or "unavailable" in error_text
                or "high demand" in error_text
                or "overloaded" in error_text
            ):
                time.sleep(1)
                continue

            # For other errors, try the fallback model as well.
            continue

    # Both models failed
    return {
        "priority": "Analysis error",
        "category": "AI service temporarily unavailable",
        "deadline": "Not found",
        "summary": "NOVA could not complete the AI analysis right now.",
        "actions": [],
        "important_points": [],
        "warnings": [
            f"{type(last_error).__name__}: {str(last_error)}"
        ],
        "simple_explanation": (
            "The AI service is temporarily unavailable. "
            "Please try the analysis again."
        ),
        "demo_mode": False
    }