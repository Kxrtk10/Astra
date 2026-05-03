from google import genai
import os

# ensure API key is loaded
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

print("Available models:\n")

for model in client.models.list():
    print(model.name)