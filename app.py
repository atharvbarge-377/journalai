from flask import Flask, render_template, request, jsonify
import anthropic
import os

app = Flask(__name__)

SYSTEM_PROMPT = """You are a journal PDF parser for Indian BCA/engineering students.
Extract experiment details from the uploaded PDF and return a JSON object ONLY (no markdown, no explanation).

Return this exact structure:
{
  "experiments": [
    {
      "expNo": "7",
      "title": "Java program based on method overriding.",
      "code": "full code here as a single string with \\n for newlines",
      "output": "terminal output lines here as a single string with \\n for newlines"
    }
  ]
}

Rules:
- expNo: just the number
- title: exact title after Title
- code: full code exactly as written
- output: only the terminal/console output block content
- Return ONLY valid JSON, nothing else"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/parse-pdf", methods=["POST"])
def parse_pdf():
    try:
        data = request.get_json()
        pdf_b64 = data.get("pdf_b64")

        if not pdf_b64:
            return jsonify({"error": "No PDF provided"}), 400

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return jsonify({"error": "API key not configured"}), 500

        client = anthropic.Anthropic(api_key=api_key)

        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_b64
                        }
                    },
                    {
                        "type": "text",
                        "text": "Extract all experiments from this journal PDF and return JSON only."
                    }
                ]
            }]
        )

        import json
        text = message.content[0].text
        clean = text.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
