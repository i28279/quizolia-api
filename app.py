from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

openrouter_api_url = "https://openrouter.ai/api/v1/chat/completions"
api_key = "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"

@app.route("/generate-quiz", methods=["POST"])
def generate_quiz():
    data = request.json
    book = data.get("book")
    chapter = data.get("chapter")
    topic = data.get("topic")
    count = data.get("count")
    options = data.get("options")

    prompt = f"Generate {count} multiple choice questions (with {options} options) on the topic '{topic}' under '{chapter}' in '{book}'. Provide correct answer and short explanation for each. Format as JSON with fields: question, options, answer, explanation."

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
