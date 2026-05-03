import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"


def evaluate_answer(question, answer):

    prompt = f"""
You are a tutor evaluating a student's answer.

Question:
{question}

Student answer:
{answer}

Give feedback and say if the answer is correct or incorrect.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text