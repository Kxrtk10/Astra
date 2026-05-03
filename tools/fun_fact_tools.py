import json
import os
from datetime import date

from tools.personal_memory_tools import load_personal_memory

FUN_FACTS_PATH = os.path.join("data", "fun_facts.json")


def load_fun_facts():
    with open(FUN_FACTS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def _pick_category(memory):
    interests = " ".join(memory.get("interests", [])).lower()
    category_map = {
        "music": ["music", "song", "singing", "guitar", "piano"],
        "sports": ["sport", "cricket", "football", "basketball", "badminton", "tennis"],
        "space": ["space", "astronomy", "planet", "stars"],
        "history": ["history", "civilization", "war", "ancient"],
        "technology": ["technology", "coding", "tech", "computer", "ai"],
        "movies": ["movie", "cinema", "film", "anime"],
        "reading": ["reading", "books", "novel", "literature"],
    }

    for category, keywords in category_map.items():
        if any(keyword in interests for keyword in keywords):
            return category
    return "default"


def get_daily_fun_fact(name):
    memory = load_personal_memory(name)
    facts = load_fun_facts()
    category = _pick_category(memory)
    options = facts.get(category) or facts["default"]
    index = date.today().toordinal() % len(options)

    return {
        "category": category,
        "fact": options[index],
        "interest_hint": memory.get("interests", [])[-3:],
    }
