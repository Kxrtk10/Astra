import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"


def ask_tutor(question):

    prompt = f"""
You are a friendly AI tutor who explains academic concepts clearly
and simply to students.

Student Question:
{question}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    print("Adaptive Tutor (Baseline Version)")
    print("Type 'exit' to quit\n")

    while True:

        question = input("Student: ")

        if question.lower() == "exit":
            break

        answer = ask_tutor(question)

        print("\nTutor:", answer)
        print()