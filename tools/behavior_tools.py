import json
import os
from datetime import datetime

from backend.database import fetch_json_record, upsert_json_record
from backend.storage import atomic_write_json

BEHAVIOR_STATE_FOLDER = "behavior_state"
CASE_STUDIES_PATH = os.path.join("data", "behavior_case_studies.json")
MAX_RECENT_EVENTS = 25
RECENT_WINDOW = 8

SIGNAL_KEYWORDS = {
    "anxiety": [
        "scared",
        "anxious",
        "stress",
        "stressed",
        "worried",
        "panic",
        "fear",
        "afraid",
    ],
    "confusion": [
        "confused",
        "don't understand",
        "dont understand",
        "not sure",
        "don't know",
        "dont know",
        "hard to understand",
        "unclear",
    ],
    "avoidance": [
        "later",
        "tomorrow",
        "skip",
        "not now",
        "don't want",
        "dont want",
        "avoid",
        "can't do this now",
    ],
    "burnout": [
        "tired",
        "exhausted",
        "burned out",
        "burnt out",
        "drained",
        "can't focus",
        "cant focus",
        "too much",
    ],
    "motivation": [
        "let's do",
        "lets do",
        "ready",
        "i can do this",
        "want to improve",
        "i'll try",
        "ill try",
        "excited",
    ],
    "low_confidence": [
        "i'm bad",
        "im bad",
        "i can't do",
        "i cant do",
        "not good enough",
        "weak at",
        "i always mess up",
    ],
    "confidence": [
        "got it",
        "easy",
        "i know this",
        "i can handle this",
        "confident",
    ],
    "frustration": [
        "annoying",
        "frustrated",
        "hate this",
        "this sucks",
        "stupid",
        "irritating",
    ],
}


def _behavior_state_path(name):
    if not os.path.exists(BEHAVIOR_STATE_FOLDER):
        os.makedirs(BEHAVIOR_STATE_FOLDER)
    return os.path.join(BEHAVIOR_STATE_FOLDER, f"{name}.json")


def _timestamp():
    return datetime.utcnow().isoformat(timespec="seconds")


def _default_signal_counts():
    return {
        "anxiety": 0,
        "confusion": 0,
        "avoidance": 0,
        "burnout": 0,
        "motivation": 0,
        "low_confidence": 0,
        "confidence": 0,
        "frustration": 0,
    }


def _default_behavior_state():
    return {
        "events": [],
        "long_term_signal_counts": _default_signal_counts(),
        "last_analysis": {},
    }


def _normalize_behavior_state(state):
    state.setdefault("events", [])
    state.setdefault("long_term_signal_counts", _default_signal_counts())
    state.setdefault("last_analysis", {})
    return state


def _load_behavior_from_db(name):
    raw = fetch_json_record("student_behavior", "student_name", name, "state_json")
    if not raw:
        return None
    return _normalize_behavior_state(json.loads(raw))


def _save_behavior_to_db(name, state):
    upsert_json_record(
        "student_behavior",
        "student_name",
        name,
        "state_json",
        json.dumps(state, indent=2),
        _timestamp(),
    )


def load_case_studies():
    with open(CASE_STUDIES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def load_behavior_state(name):
    state = _load_behavior_from_db(name)
    if state is not None:
        return state

    filepath = _behavior_state_path(name)
    if not os.path.exists(filepath):
        return _default_behavior_state()

    with open(filepath, "r", encoding="utf-8") as file:
        state = json.load(file)

    state = _normalize_behavior_state(state)
    _save_behavior_to_db(name, state)
    return state


def save_behavior_state(name, state):
    filepath = _behavior_state_path(name)
    state = _normalize_behavior_state(state)
    atomic_write_json(filepath, state)
    _save_behavior_to_db(name, state)


def _extract_signals_from_text(text):
    lowered = (text or "").lower()
    signals = _default_signal_counts()

    for signal, keywords in SIGNAL_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lowered:
                signals[signal] += 1

    return signals


def _merge_signal_counts(base_counts, delta_counts):
    merged = dict(base_counts)
    for signal, value in delta_counts.items():
        merged[signal] = merged.get(signal, 0) + value
    return merged


def _score_case(case_study, combined_counts):
    score = 0
    for signal, weight in case_study.get("signals", {}).items():
        score += combined_counts.get(signal, 0) * weight
    return score


def _derive_support_style(combined_counts):
    if combined_counts["burnout"] >= 2:
        return "gentle_recovery"
    if combined_counts["anxiety"] >= 2 or combined_counts["low_confidence"] >= 2:
        return "reassuring_stepwise"
    if combined_counts["confusion"] >= 2:
        return "simplified_structured"
    if combined_counts["motivation"] >= 2 and combined_counts["confidence"] >= 1:
        return "challenging_coach"
    if combined_counts["avoidance"] >= 2:
        return "accountability_focused"
    return "balanced_support"


def _derive_pacing(combined_counts):
    if combined_counts["burnout"] >= 2 or combined_counts["anxiety"] >= 2:
        return "slow"
    if combined_counts["confusion"] >= 2:
        return "step_by_step"
    if combined_counts["motivation"] >= 2 and combined_counts["confidence"] >= 1:
        return "stretch"
    return "steady"


def analyze_behavior_state(state):
    recent_events = state.get("events", [])[-RECENT_WINDOW:]
    recent_counts = _default_signal_counts()

    for event in recent_events:
        recent_counts = _merge_signal_counts(recent_counts, event.get("signals", {}))

    long_term_counts = state.get("long_term_signal_counts", _default_signal_counts())
    combined_counts = {}
    for signal in _default_signal_counts():
        combined_counts[signal] = recent_counts.get(signal, 0) * 2 + long_term_counts.get(signal, 0)

    ranked_cases = []
    for case_study in load_case_studies():
        ranked_cases.append(
            {
                "id": case_study["id"],
                "name": case_study["name"],
                "description": case_study["description"],
                "support_strategy": case_study["support_strategy"],
                "score": _score_case(case_study, combined_counts),
            }
        )

    ranked_cases.sort(key=lambda item: item["score"], reverse=True)
    top_cases = [case for case in ranked_cases if case["score"] > 0][:3]

    analysis = {
        "recent_signal_counts": recent_counts,
        "long_term_signal_counts": long_term_counts,
        "combined_signal_counts": combined_counts,
        "top_cases": top_cases,
        "support_style": _derive_support_style(combined_counts),
        "pacing_style": _derive_pacing(combined_counts),
        "dropout_risk": "high"
        if combined_counts["avoidance"] + combined_counts["burnout"] >= 5
        else "medium"
        if combined_counts["avoidance"] + combined_counts["burnout"] >= 2
        else "low",
    }
    return analysis


def record_behavior_event(name, event_type, user_input="", tutor_response="", metadata=None):
    state = load_behavior_state(name)
    metadata = metadata or {}

    signals = _extract_signals_from_text(user_input)

    if event_type == "missed_work":
        signals["avoidance"] += 1
    elif event_type == "study_completion":
        signals["motivation"] += 1
        signals["confidence"] += 1
    elif event_type == "mock_update":
        signals["motivation"] += 1
    elif event_type == "encouragement_request":
        signals["low_confidence"] += 1

    state["events"].append(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "event_type": event_type,
            "user_input": user_input,
            "tutor_response": tutor_response,
            "signals": signals,
            "metadata": metadata,
        }
    )
    state["events"] = state["events"][-MAX_RECENT_EVENTS:]
    state["long_term_signal_counts"] = _merge_signal_counts(
        state.get("long_term_signal_counts", _default_signal_counts()),
        signals,
    )
    state["last_analysis"] = analyze_behavior_state(state)
    save_behavior_state(name, state)
    return state


def get_behavior_snapshot(profile):
    state = load_behavior_state(profile["name"])
    if not state.get("last_analysis"):
        state["last_analysis"] = analyze_behavior_state(state)
        save_behavior_state(profile["name"], state)
    return state["last_analysis"]


def format_behavior_context(profile):
    analysis = get_behavior_snapshot(profile)

    lines = [
        "Behavior context:",
        f"- Support style: {analysis['support_style']}",
        f"- Pacing style: {analysis['pacing_style']}",
        f"- Dropout risk: {analysis['dropout_risk']}",
        "- Recent signal strengths:",
    ]

    for signal, value in analysis["recent_signal_counts"].items():
        lines.append(f"- {signal}: {value}")

    if analysis["top_cases"]:
        lines.append("- Best matching case-study patterns:")
        for case in analysis["top_cases"]:
            lines.append(
                f"- {case['name']}: {case['description']} | strategy: {case['support_strategy']}"
            )
    else:
        lines.append("- No strong behavior pattern detected yet. Use balanced support.")

    return "\n".join(lines)


def format_behavior_report(profile):
    analysis = get_behavior_snapshot(profile)

    lines = [
        f"Behavior Report for {profile['name']}",
        "",
        f"Recommended support style: {analysis['support_style']}",
        f"Recommended pacing: {analysis['pacing_style']}",
        f"Current dropout risk: {analysis['dropout_risk']}",
        "",
        "What this means right now:",
    ]

    support_style_notes = {
        "gentle_recovery": "Use lighter workload, reassurance, and recovery-first planning.",
        "reassuring_stepwise": "Use calm language, smaller tasks, and steady confidence-building.",
        "simplified_structured": "Use step-by-step explanations, fewer concepts at once, and examples.",
        "challenging_coach": "Use stretch tasks, direct feedback, and higher challenge.",
        "accountability_focused": "Use shorter deadlines, tighter check-ins, and momentum-building tasks.",
        "balanced_support": "Use a balanced mix of structure, encouragement, and challenge.",
    }
    pacing_notes = {
        "slow": "The student may currently need lower pressure and less overload.",
        "step_by_step": "The student may benefit from one concept or one question at a time.",
        "stretch": "The student can likely handle stronger challenge right now.",
        "steady": "A normal, sustainable pace is appropriate right now.",
    }

    lines.append(f"- {support_style_notes.get(analysis['support_style'], 'Use balanced support.')}")
    lines.append(f"- {pacing_notes.get(analysis['pacing_style'], 'Use a steady pace.')}")

    if analysis["top_cases"]:
        lines.extend(["", "Closest behavior patterns:"])
        for case in analysis["top_cases"]:
            lines.append(f"- {case['name']}: {case['support_strategy']}")

    lines.extend(["", "Recent signal levels:"])
    for signal, value in analysis["recent_signal_counts"].items():
        lines.append(f"- {signal}: {value}")

    return "\n".join(lines)
