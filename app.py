from flask import Flask, request, jsonify
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = Flask(__name__)

# CORS configuration (optional but useful)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI or OpenRouter API key
openai.api_key = os.getenv("API_KEY")  # or set manually here

@app.post("/generate-quiz")
async def generate_quiz(request: Request):
    data = await request.json()
    topic = data.get("topic")
    chapter = data.get("chapter")
    book = data.get("book")
    count = data.get("count", 5)
    options = data.get("options", 4)

    prompt = f"""
Generate {count} multiple choice questions (with {options} options each) on the topic '{topic}' under the chapter '{chapter}' in the book '{book}'.

Each question must include the following fields and be returned in this **exact JSON format**:
[
  {{
    "question": "Write the question here",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Correct Option",
    "explanation": "Short explanation of the correct answer"
  }},
  ...
]

Only return a valid JSON array of question objects. Do not include any text before or after the JSON array.
    """

    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates multiple choice quizzes in JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        result = response["choices"][0]["message"]["content"].strip()
        return {"quiz": result}  # frontend should parse result as JSON

    except Exception as e:
        return {"error": str(e)}
