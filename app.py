import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import APIError, OpenAI

load_dotenv()

app = Flask(__name__)

COMMON_ISSUES_PATH = Path(__file__).parent / "common_issues.md"

_common_issues_content: str | None = None


def get_common_issues() -> str:
    """Load and cache the common issues markdown file."""
    global _common_issues_content
    if _common_issues_content is None:
        _common_issues_content = COMMON_ISSUES_PATH.read_text(encoding="utf-8")
    return _common_issues_content


def build_system_prompt() -> str:
    common_issues = get_common_issues()
    return (
        "You are a helpful technical support assistant for the Maslow 4 CNC router. "
        "Answer questions accurately and concisely based on the reference documentation below. "
        "If a question is not covered by the documentation, say so and suggest the user check "
        "the official Maslow forums or documentation.\n\n"
        "--- MASLOW 4 REFERENCE DOCUMENTATION ---\n\n"
        f"{common_issues}\n\n"
        "--- END OF REFERENCE DOCUMENTATION ---"
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"error": "OPENAI_API_KEY is not configured on the server."}), 500

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body."}), 400

    messages = data.get("messages")
    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "A non-empty 'messages' list is required."}), 400

    # Validate each message has role and content strings
    for msg in messages:
        if not isinstance(msg, dict):
            return jsonify({"error": "Each message must be an object."}), 400
        if msg.get("role") not in ("user", "assistant"):
            return jsonify({"error": "Each message role must be 'user' or 'assistant'."}), 400
        if not isinstance(msg.get("content"), str):
            return jsonify({"error": "Each message content must be a string."}), 400

    client = OpenAI(api_key=api_key)

    openai_messages = [{"role": "system", "content": build_system_prompt()}] + messages

    try:
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=openai_messages,
            max_tokens=int(os.environ.get("OPENAI_MAX_TOKENS", "2048")),
            temperature=0.3,
        )
    except APIError as exc:
        return jsonify({"error": f"OpenAI API error: {exc.message}"}), 502

    if not response.choices:
        return jsonify({"error": "No response received from the AI model."}), 502

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
