import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

openrouter_api_url = "https://openrouter.ai/api/v1/chat/completions"
api_key = os.getenv("API_KEY")  # নিজের key বসা

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
            "model": "openai/gpt-3.5-turbo",  # বা যেকোনো compatible model
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1500
        }
    )

    result = response.json()
    
    try:
        quiz_text = result["choices"][0]["message"]["content"]
        return jsonify({"quiz": quiz_text})
    except Exception as e:
        return jsonify({"error": "Quiz generation failed.", "details": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
