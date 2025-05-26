from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

openrouter_api_url = "https://openrouter.ai/api/v1/chat/completions"
api_key = os.getenv("API_KEY")

@app.route("/generate-quiz", methods=["POST"])
def generate_quiz():
    data = request.json
    book = data.get("book")
    chapter = data.get("chapter")
    topic = data.get("topic")
    count = data.get("count")
    options = data.get("options")

    prompt = f"""
Generate {count} multiple choice questions (with {options} options each) on the topic '{topic}' under '{chapter}' in '{book}'. 
For each question, provide exactly these fields in JSON format:
- question: string
- options: array of strings
- answer: string (one of the options)
- explanation: string

Return ONLY a valid JSON array of these question objects, without any extra text.
Example:
[
  {{
    "question": "...",
    "options": ["...", "...", "...", "..."],
    "answer": "...",
    "explanation": "..."
  }},
  ...
]
"""
    
    response = requests.post(
        openrouter_api_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "model": "openchat/openchat-3.5-1210",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1500
        }
    )

    try:
        result = response.json()
        answer_text = result["choices"][0]["message"]["content"]
        return jsonify({"result": answer_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
