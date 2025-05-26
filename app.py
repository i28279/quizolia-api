from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json

app = Flask(__name__)
CORS(app)

openrouter_api_url = "https://openrouter.ai/api/v1/chat/completions"
api_key = os.getenv("API_KEY")  # .env থেকে নিবে। চাইলে সরাসরি লিখে রাখতে পারিস


def extract_json_block(text):
    start = text.find('[')
    end = text.rfind(']')
    if start != -1 and end != -1 and end > start:
        return text[start:end+1]
    return None

@app.route("/generate-quiz", methods=["POST"])
def generate_quiz():
    data = request.json
    book = data.get("book", "NCTB Book")
    chapter = data.get("chapter", "Chapter 1")
    topic = data.get("topic", "General Science")
    count = data.get("count", 5)
    options = data.get("options", 4)

    prompt = f"""
Generate {count} multiple choice questions (with {options} options each) on the topic '{topic}' under the chapter '{chapter}' in the book '{book}'.

Each question must be returned as a JSON object with the following format:
[
  {{
    "question": "Your question here",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "answer": "Correct option",
    "explanation": "Short explanation of why the answer is correct"
  }},
  ...
]

**Important:** Only return a pure JSON array without any extra text, headers, or explanations.
    """

    try:
        response = requests.post(
            openrouter_api_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "openchat/openchat-3.5-1210",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that returns pure JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1800
            }
        )

        result = response.json()
        answer_text = result["choices"][0]["message"]["content"].strip()
        print('AI response \n', answer_text)

        json_only = extract_json_block(answer_text)

        if json_only:
            questions = json.loads(json_only)
            return jsonify(questions)
        else:
            return jsonify({"error": "Valid JSON block not found in response."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
