import json
import os
import re
from datetime import datetime

from backend.database import fetch_json_record, upsert_json_record
from backend.storage import atomic_write_json

MEMORY_FOLDER = "personal_memory"
MAX_MEMORY_ITEMS = 30

PERSON_PATTERNS = [
    re.compile(
        r"\b([A-Z][a-z]+)\s+is\s+my\s+(friend|brother|sister|mentor|teacher|partner|mother|mom|father|dad)\b"
    ),
    re.compile(
        r"\bmy\s+(friend|brother|sister|mentor|teacher|partner|mother|mom|father|dad)\s+([A-Z][a-z]+)\b"
    ),
]

EMOTION_PATTERNS = [
    "i feel",
    "i am feeling",
    "today was",
    "my day was",
    "i'm worried about",
    "im worried about",
    "i'm upset",
    "im upset",
]

EXPLICIT_MEMORY_PHRASES = [
    "remember this",
    "please remember",
    "save this",
    "remember that",
]


def _memory_path(name):
    if not os.path.exists(MEMORY_FOLDER):
        os.makedirs(MEMORY_FOLDER)
    return os.path.join(MEMORY_FOLDER, f"{name}.json")


def _timestamp():
    return datetime.utcnow().isoformat(timespec="seconds")


def _default_memory():
    return {
        "known_people": [],
        "interests": [],
        "life_notes": [],
        "recent_checkins": [],
    }


def _normalize_memory(memory):
    memory.setdefault("known_people", [])
    memory.setdefault("interests", [])
    memory.setdefault("life_notes", [])
    memory.setdefault("recent_checkins", [])
    return memory


def _load_memory_from_db(name):
    raw = fetch_json_record("student_memory", "student_name", name, "state_json")
    if not raw:
        return None
    return _clean_legacy_memory(_normalize_memory(json.loads(raw)))


def _save_memory_to_db(name, memory):
    upsert_json_record(
        "student_memory",
        "student_name",
        name,
        "state_json",
        json.dumps(memory, indent=2),
        _timestamp(),
    )


def load_personal_memory(name):
    memory = _load_memory_from_db(name)
    if memory is not None:
        return memory

    path = _memory_path(name)
    if not os.path.exists(path):
        return _default_memory()

    with open(path, "r", encoding="utf-8") as file:
        memory = json.load(file)

    memory = _clean_legacy_memory(_normalize_memory(memory))
    _save_memory_to_db(name, memory)
    return memory


def save_personal_memory(name, memory):
    path = _memory_path(name)
    memory = _normalize_memory(memory)
    atomic_write_json(path, memory)
    _save_memory_to_db(name, memory)


def _append_limited(items, value):
    items.append(value)
    del items[:-MAX_MEMORY_ITEMS]


def _clean_legacy_memory(memory):
    generic_people = {
        "my mother",
        "my mom",
        "my father",
        "my dad",
        "my brother",
        "my sister",
        "my friend",
        "my teacher",
        "my mentor",
        "my partner",
    }
    memory["known_people"] = [
        item for item in memory.get("known_people", [])
        if item.strip().lower() not in generic_people
    ]
    return memory


def add_memory_item(name, category, value):
    text = (value or "").strip()
    if not text:
        return load_personal_memory(name)

    memory = _normalize_memory(load_personal_memory(name))
    valid_categories = {"known_people", "interests", "life_notes"}
    if category not in valid_categories:
        return memory

    existing = memory[category]
    if text not in existing:
        _append_limited(existing, text)
        save_personal_memory(name, memory)
    return memory


def add_memory(name, value, category="life_notes"):
    text = (value or "").strip()
    if not text:
        return load_personal_memory(name)
    if category not in {"known_people", "interests", "life_notes"}:
        category = "life_notes"
    return add_memory_item(name, category, text)


def remove_memory_item(name, category, value):
    text = (value or "").strip()
    memory = _normalize_memory(load_personal_memory(name))
    valid_categories = {"known_people", "interests", "life_notes"}
    if category not in valid_categories or not text:
        return memory

    memory[category] = [item for item in memory[category] if item != text]
    save_personal_memory(name, memory)
    return memory


def update_personal_memory(name, user_input):
    text = (user_input or "").strip()
    if not text:
        return load_personal_memory(name)

    memory = _normalize_memory(load_personal_memory(name))
    lowered = text.lower()
    timestamp = datetime.now().isoformat(timespec="seconds")

    for pattern in PERSON_PATTERNS:
        match = pattern.search(text)
        if match:
            person_note = match.group(0)
            if person_note not in memory["known_people"]:
                _append_limited(memory["known_people"], person_note)

    interest_phrases = [
        "i like ",
        "i love ",
        "my hobby is ",
        "my hobbies are ",
        "i enjoy ",
        "i am interested in ",
    ]
    for phrase in interest_phrases:
        if phrase in lowered:
            interest_text = text[lowered.index(phrase) + len(phrase):].strip(" .!")
            if interest_text:
                interest_text = interest_text.split(".")[0].split(",")[0].strip()
                if interest_text and interest_text not in memory["interests"]:
                    _append_limited(memory["interests"], interest_text)

    if any(phrase in lowered for phrase in EMOTION_PATTERNS):
        _append_limited(
            memory["recent_checkins"],
            {
                "timestamp": timestamp,
                "note": text,
            },
        )

    if any(phrase in lowered for phrase in EXPLICIT_MEMORY_PHRASES):
        if text not in memory["life_notes"]:
            _append_limited(memory["life_notes"], text)

    save_personal_memory(name, memory)
    return memory


def format_personal_memory_context(name):
    memory = load_personal_memory(name)
    lines = []

    if memory["known_people"]:
        lines.append("People the student has mentioned:")
        for person in memory["known_people"][-5:]:
            lines.append(f"- {person}")

    if memory["interests"]:
        lines.append("Interests and hobbies the student likes:")
        for interest in memory["interests"][-5:]:
            lines.append(f"- {interest}")

    if memory["life_notes"]:
        lines.append("Important life context the student has shared:")
        for note in memory["life_notes"][-4:]:
            lines.append(f"- {note}")

    if memory["recent_checkins"]:
        lines.append("Recent emotional check-ins:")
        for checkin in memory["recent_checkins"][-3:]:
            lines.append(f"- {checkin['note']}")

    return "\n".join(lines) if lines else "No personal memory yet."


def build_tutor_brief_memory_context(name):
    memory = load_personal_memory(name)
    snippets = []

    if memory["interests"]:
        snippets.append(
            f"Student interests: {', '.join(memory['interests'][-3:])}"
        )
    if memory["life_notes"]:
        snippets.append(
            f"Useful personal notes: {', '.join(memory['life_notes'][-2:])}"
        )
    if memory["recent_checkins"]:
        snippets.append(
            f"Recent check-in: {memory['recent_checkins'][-1]['note']}"
        )

    return " | ".join(snippets) if snippets else "No brief personal memory yet."
