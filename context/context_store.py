import json
import os

CONTEXT_FILE = "context/conversation_history.json"


def save_context(user_message, ai_response):

    os.makedirs("context", exist_ok=True)

    conversation = []

    if os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE, "r") as f:
            conversation = json.load(f)

    conversation.append({
        "user": user_message,
        "assistant": ai_response
    })

    with open(CONTEXT_FILE, "w") as f:
        json.dump(conversation, f, indent=4)