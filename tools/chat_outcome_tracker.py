"""
Chat Outcome Tracker — The self-learning loop for Astra.

Tracks what happens DURING and AFTER teaching interactions:
- Did the student re-ask the same topic? (comprehension failure)
- Did they move from confused → confident? (breakthrough)
- Which topics keep recurring as pain points? (difficulty patterns)
- Did accuracy improve after an explanation? (teaching effectiveness)

This feeds back into student_insight_tools so the router learns over time.
"""

import json
import os
from collections import Counter
from datetime import datetime

from backend.database import fetch_json_record, upsert_json_record
from backend.storage import atomic_write_json
from tools.analytics_tools import load_analytics_state

OUTCOME_FOLDER = "learning_state"
MAX_OUTCOMES = 120
TOPIC_DIFFICULTY_WINDOW = 30
TASK_MODES = ("tutor", "practice", "lounge", "last_minute", "tips", "guide")


def _outcome_path(name):
    if not os.path.exists(OUTCOME_FOLDER):
        os.makedirs(OUTCOME_FOLDER)
    return os.path.join(OUTCOME_FOLDER, f"{name}_outcomes.json")


def _timestamp():
    return datetime.utcnow().isoformat(timespec="seconds")


def _default_state():
    return {
        "outcomes": [],
        "topic_difficulty_map": {},
        "teaching_effectiveness": {},
        "last_updated": "",
    }


def _normalize_state(state):
    state.setdefault("outcomes", [])
    state.setdefault("topic_difficulty_map", {})
    state.setdefault("teaching_effectiveness", {})
    state.setdefault("last_updated", "")
    return state


def _normalize_mode(mode):
    clean = str(mode or "tutor").strip().lower()
    return clean if clean in TASK_MODES else clean or "tutor"


def _mode_label(mode):
    return _normalize_mode(mode).replace("_", " ").title()


def _load_from_db(name):
    raw = fetch_json_record("student_chat_outcomes", "student_name", name, "state_json")
    if not raw:
        return None
    return _normalize_state(json.loads(raw))


def _save_to_db(name, state):
    upsert_json_record(
        "student_chat_outcomes",
        "student_name",
        name,
        "state_json",
        json.dumps(state, indent=2),
        _timestamp(),
    )


def load_outcome_state(name):
    state = _load_from_db(name)
    if state is not None:
        return state

    filepath = _outcome_path(name)
    if not os.path.exists(filepath):
        return _default_state()

    with open(filepath, "r", encoding="utf-8") as file:
        state = json.load(file)

    state = _normalize_state(state)
    _save_to_db(name, state)
    return state


def save_outcome_state(name, state):
    filepath = _outcome_path(name)
    state = _normalize_state(state)
    atomic_write_json(filepath, state)
    _save_to_db(name, state)


# ---------------------------------------------------------------------------
# Core: record a chat outcome after every teaching interaction
# ---------------------------------------------------------------------------

def record_chat_outcome(
    name,
    topic="",
    subject="",
    outcome="neutral",
    user_sentiment_before="neutral",
    user_sentiment_after="neutral",
    follow_up_needed=False,
    re_ask=False,
    conversation_mode="tutor",
    metadata=None,
):
    """
    Record the outcome of a single teaching interaction.

    outcome: "understood" | "partially_understood" | "confused" | "breakthrough" | "neutral"
    user_sentiment_before/after: "negative" | "neutral" | "positive"
    follow_up_needed: True if the student asked for more explanation
    re_ask: True if this topic was already explained recently
    """
    state = load_outcome_state(name)
    metadata = metadata or {}

    clean_topic = str(topic or "").strip().lower()
    clean_subject = str(subject or "").strip().lower()

    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "topic": clean_topic,
        "subject": clean_subject,
        "outcome": outcome,
        "sentiment_before": user_sentiment_before,
        "sentiment_after": user_sentiment_after,
        "follow_up_needed": follow_up_needed,
        "re_ask": re_ask,
        "conversation_mode": conversation_mode,
        "metadata": metadata,
    }

    state["outcomes"].append(entry)
    state["outcomes"] = state["outcomes"][-MAX_OUTCOMES:]
    state["last_updated"] = entry["timestamp"]

    # Update topic difficulty map
    if clean_topic:
        _update_topic_difficulty(state, clean_topic, clean_subject, entry)

    # Update teaching effectiveness
    _update_teaching_effectiveness(state)

    save_outcome_state(name, state)
    return entry


def _update_topic_difficulty(state, topic, subject, entry):
    """Track how difficult each topic is for this student."""
    key = f"{subject}::{topic}" if subject else topic
    topic_data = state["topic_difficulty_map"].get(key, {
        "attempts": 0,
        "understood": 0,
        "confused": 0,
        "re_asks": 0,
        "breakthroughs": 0,
        "last_outcome": "",
        "difficulty_score": 50,
    })

    topic_data["attempts"] += 1
    if entry["outcome"] == "understood":
        topic_data["understood"] += 1
    elif entry["outcome"] == "confused":
        topic_data["confused"] += 1
    elif entry["outcome"] == "breakthrough":
        topic_data["breakthroughs"] += 1
        topic_data["understood"] += 1
    if entry["re_ask"]:
        topic_data["re_asks"] += 1

    topic_data["last_outcome"] = entry["outcome"]

    # Compute difficulty score (0 = easy, 100 = extremely hard for this student)
    attempts = max(topic_data["attempts"], 1)
    confusion_rate = topic_data["confused"] / attempts
    re_ask_rate = topic_data["re_asks"] / attempts
    understand_rate = topic_data["understood"] / attempts

    topic_data["difficulty_score"] = round(
        min(100, max(0,
            50
            + (confusion_rate * 30)
            + (re_ask_rate * 25)
            - (understand_rate * 25)
            - (topic_data["breakthroughs"] * 5)
        ))
    )

    state["topic_difficulty_map"][key] = topic_data


def _update_teaching_effectiveness(state):
    """Compute aggregate teaching effectiveness signals."""
    outcomes = state.get("outcomes", [])
    if not outcomes:
        state["teaching_effectiveness"] = {}
        return

    recent = outcomes[-TOPIC_DIFFICULTY_WINDOW:]

    total = len(recent)
    understood_count = sum(1 for o in recent if o["outcome"] in {"understood", "breakthrough"})
    confused_count = sum(1 for o in recent if o["outcome"] == "confused")
    re_ask_count = sum(1 for o in recent if o.get("re_ask"))
    follow_up_count = sum(1 for o in recent if o.get("follow_up_needed"))

    # Sentiment shift tracking
    positive_shifts = sum(
        1 for o in recent
        if o.get("sentiment_before") in {"negative", "neutral"}
        and o.get("sentiment_after") == "positive"
    )
    negative_shifts = sum(
        1 for o in recent
        if o.get("sentiment_before") in {"positive", "neutral"}
        and o.get("sentiment_after") == "negative"
    )

    comprehension_rate = round(understood_count / total * 100, 1) if total else 0
    confusion_rate = round(confused_count / total * 100, 1) if total else 0
    re_ask_rate = round(re_ask_count / total * 100, 1) if total else 0

    # Teaching quality signal
    if comprehension_rate >= 75 and confusion_rate < 15:
        quality = "strong"
    elif comprehension_rate >= 55:
        quality = "adequate"
    elif confusion_rate >= 40:
        quality = "struggling"
    else:
        quality = "building"

    state["teaching_effectiveness"] = {
        "comprehension_rate": comprehension_rate,
        "confusion_rate": confusion_rate,
        "re_ask_rate": re_ask_rate,
        "follow_up_rate": round(follow_up_count / total * 100, 1) if total else 0,
        "positive_sentiment_shifts": positive_shifts,
        "negative_sentiment_shifts": negative_shifts,
        "quality_signal": quality,
        "sample_size": total,
    }


# ---------------------------------------------------------------------------
# Query: get insights for the intelligence layer
# ---------------------------------------------------------------------------

def get_difficult_topics(name, max_topics=5):
    """Return the hardest topics for this student, sorted by difficulty."""
    state = load_outcome_state(name)
    topic_map = state.get("topic_difficulty_map", {})

    ranked = sorted(
        [
            {"key": key, **data}
            for key, data in topic_map.items()
            if data.get("attempts", 0) >= 1
        ],
        key=lambda x: x["difficulty_score"],
        reverse=True,
    )
    return ranked[:max_topics]


def get_recurring_pain_points(name, min_re_asks=2):
    """Return topics the student keeps coming back to (re-asking)."""
    state = load_outcome_state(name)
    topic_map = state.get("topic_difficulty_map", {})

    pain_points = [
        {"key": key, **data}
        for key, data in topic_map.items()
        if data.get("re_asks", 0) >= min_re_asks
    ]
    return sorted(pain_points, key=lambda x: x["re_asks"], reverse=True)


def get_teaching_effectiveness(name):
    """Return the aggregate teaching effectiveness snapshot."""
    state = load_outcome_state(name)
    return state.get("teaching_effectiveness", {})


def get_recent_topic_outcomes(name, last_n=10):
    """Return the last N chat outcomes for context."""
    state = load_outcome_state(name)
    return state.get("outcomes", [])[-last_n:]


def _mode_summary_from_outcomes(name, mode):
    state = load_outcome_state(name)
    outcomes = state.get("outcomes", [])
    mode_key = _normalize_mode(mode)
    mode_outcomes = [item for item in outcomes if _normalize_mode(item.get("conversation_mode")) == mode_key]
    if not mode_outcomes:
        return None

    total = len(mode_outcomes)
    understood = sum(1 for item in mode_outcomes if item.get("outcome") in {"understood", "breakthrough"})
    confused = sum(1 for item in mode_outcomes if item.get("outcome") == "confused")
    follow_up = sum(1 for item in mode_outcomes if item.get("follow_up_needed"))
    re_asks = sum(1 for item in mode_outcomes if item.get("re_ask"))
    positive_shifts = sum(
        1
        for item in mode_outcomes
        if item.get("sentiment_before") in {"negative", "neutral"} and item.get("sentiment_after") == "positive"
    )
    negative_shifts = sum(
        1
        for item in mode_outcomes
        if item.get("sentiment_before") in {"positive", "neutral"} and item.get("sentiment_after") == "negative"
    )

    topic_counter = Counter(item.get("topic", "") for item in mode_outcomes if item.get("topic"))
    subject_counter = Counter(item.get("subject", "") for item in mode_outcomes if item.get("subject"))
    recent_topics = []
    for item in reversed(mode_outcomes):
        topic = str(item.get("topic", "")).strip()
        if topic and topic not in recent_topics:
            recent_topics.append(topic)
        if len(recent_topics) >= 4:
            break

    practice_state = load_analytics_state(name)
    practice_profile = (practice_state.get("mode_profiles") or {}).get(mode_key, {})
    practice_attempts = int(practice_profile.get("attempts", 0) or 0)
    average_accuracy = practice_profile.get("average_accuracy", 0)
    recent_accuracy = practice_profile.get("recent_accuracy", 0)
    recent_time = practice_profile.get("recent_time_minutes", 0)
    trend_signal = practice_profile.get("trend_signal", "building")
    speed_signal = practice_profile.get("speed_signal", "steady")

    if mode_key == "practice":
        if recent_accuracy < 55:
            adaptation = "Keep practice shorter, more guided, and more correction-focused."
        elif speed_signal == "slow":
            adaptation = "Use timed drills and faster answer checks to improve pace."
        elif trend_signal == "improving":
            adaptation = "Mix harder sets in gradually and keep the pressure realistic."
        else:
            adaptation = "Keep a balanced mix of timed work, review, and error correction."
    elif mode_key == "tutor":
        if confused >= max(2, total // 3):
            adaptation = "Teach in smaller steps and check understanding more often."
        elif understood >= max(2, total // 2):
            adaptation = "Move a little faster and ask one stretch question after the explanation."
        else:
            adaptation = "Stay clear and balanced, with simple checks for comprehension."
    elif mode_key == "lounge":
        if positive_shifts >= negative_shifts:
            adaptation = "Keep the conversation relaxed, friendly, and natural."
        else:
            adaptation = "Stay gentle and supportive, and keep the exchange light."
    elif mode_key == "last_minute":
        adaptation = "Use crisp recall cues, short recaps, and high-yield revision."
    elif mode_key == "tips":
        adaptation = "Keep advice concrete and tied to exam behavior."
    elif mode_key == "guide":
        adaptation = "Keep instructions short, clear, and product-focused."
    else:
        adaptation = "Keep the current rhythm and adjust tone based on the student's response."

    best_topics = [topic for topic, _ in topic_counter.most_common(3)]
    best_subjects = [subject for subject, _ in subject_counter.most_common(3)]

    return {
        "mode": mode_key,
        "mode_label": _mode_label(mode_key),
        "interactions": total,
        "understood": understood,
        "confused": confused,
        "follow_up_needed": follow_up,
        "re_asks": re_asks,
        "positive_shifts": positive_shifts,
        "negative_shifts": negative_shifts,
        "practice_attempts": practice_attempts,
        "average_accuracy": average_accuracy,
        "recent_accuracy": recent_accuracy,
        "recent_time_minutes": recent_time,
        "trend_signal": trend_signal,
        "speed_signal": speed_signal,
        "recent_topics": recent_topics,
        "top_topics": best_topics,
        "top_subjects": best_subjects,
        "adaptation": adaptation,
    }


def get_task_learning_profiles(name):
    """Return task-specific learning profiles for the major app modes."""
    summaries = {}
    for mode in TASK_MODES:
        summary = _mode_summary_from_outcomes(name, mode)
        if summary:
            summaries[mode] = summary

    # Include any extra recorded practice modes if they exist.
    analytics_state = load_analytics_state(name)
    for mode_key in (analytics_state.get("mode_profiles") or {}).keys():
        if mode_key in summaries:
            continue
        summary = _mode_summary_from_outcomes(name, mode_key)
        if summary:
            summaries[mode_key] = summary

    return summaries


def build_task_learning_context(name, active_mode=None, max_modes=4):
    """Build a concise context block describing how Astra learns per task mode."""
    profiles = get_task_learning_profiles(name)
    if not profiles:
        return "Task learning profile: no mode-specific teaching data has been recorded yet."

    lines = ["Task learning profile:"]

    active_key = _normalize_mode(active_mode) if active_mode else ""
    if active_key and active_key in profiles:
        active = profiles[active_key]
        lines.append(
            f"- Active mode {active['mode_label']}: {active['adaptation']} "
            f"(interactions {active['interactions']}, recent accuracy {active['recent_accuracy']}%, "
            f"trend {active['trend_signal']})."
        )

    for mode_key, summary in sorted(
        profiles.items(),
        key=lambda item: (item[0] != active_key, -item[1].get("interactions", 0), item[0]),
    )[:max_modes]:
        lines.append(
            f"- {summary['mode_label']}: {summary['adaptation']} "
            f"(interactions {summary['interactions']}, recent accuracy {summary['recent_accuracy']}%, "
            f"top topics: {', '.join(summary['top_topics']) or 'none'})."
        )

    lines.append(
        "Use these task profiles to change explanation depth, pacing, question style, and the amount of guidance "
        "based on the mode the student chooses."
    )
    return "\n".join(lines)


def build_self_learning_context(name):
    """
    Build a text context block that feeds into the intelligence layer.
    This is what makes Astra smarter over time.
    """
    effectiveness = get_teaching_effectiveness(name)
    difficult = get_difficult_topics(name, max_topics=3)
    pain_points = get_recurring_pain_points(name, min_re_asks=2)
    task_profiles = get_task_learning_profiles(name)

    lines = ["Self-learning context (Astra's memory of teaching outcomes):"]

    # Teaching effectiveness
    if effectiveness:
        lines.append(f"- Teaching quality signal: {effectiveness.get('quality_signal', 'building')}")
        lines.append(f"- Comprehension rate: {effectiveness.get('comprehension_rate', 0)}%")
        lines.append(f"- Confusion rate: {effectiveness.get('confusion_rate', 0)}%")
        lines.append(f"- Re-ask rate: {effectiveness.get('re_ask_rate', 0)}%")
        if effectiveness.get("positive_sentiment_shifts", 0) > 0:
            lines.append(
                f"- Positive sentiment shifts: {effectiveness['positive_sentiment_shifts']} "
                f"(student moods improved after teaching)"
            )
        if effectiveness.get("negative_sentiment_shifts", 0) > 0:
            lines.append(
                f"- Negative sentiment shifts: {effectiveness['negative_sentiment_shifts']} "
                f"(teaching may need adjustment)"
            )

    # Difficult topics
    if difficult:
        lines.append("- Hardest topics for this student:")
        for item in difficult:
            lines.append(
                f"  - {item['key']}: difficulty {item['difficulty_score']}/100, "
                f"{item.get('confused', 0)} confused, {item.get('re_asks', 0)} re-asks"
            )

    # Pain points
    if pain_points:
        lines.append("- Recurring pain points (topics the student keeps re-asking):")
        for item in pain_points:
            lines.append(f"  - {item['key']}: asked {item['re_asks']} times again")

    # Coaching implication
    if effectiveness.get("quality_signal") == "struggling":
        lines.append(
            "- COACHING ACTION: Comprehension is low. Use simpler analogies, "
            "break concepts into smaller steps, and check understanding before moving on."
        )
    elif effectiveness.get("re_ask_rate", 0) > 30:
        lines.append(
            "- COACHING ACTION: Re-ask rate is high. The student forgets quickly. "
            "Add spaced repetition reminders and recap previous topics before new ones."
        )
    elif effectiveness.get("quality_signal") == "strong":
        lines.append(
            "- COACHING ACTION: Student is learning well. Safe to increase depth, "
            "introduce exam-level challenge, and reduce hand-holding."
        )

    if not effectiveness and not difficult:
        lines.append("- No teaching outcomes recorded yet. Data will build as sessions continue.")

    if task_profiles:
        lines.append("- Task-specific learning profiles:")
        for mode_key, summary in sorted(task_profiles.items(), key=lambda item: (-item[1].get("interactions", 0), item[0]))[:4]:
            lines.append(
                f"  - {summary['mode_label']}: {summary['adaptation']} "
                f"(interactions {summary['interactions']}, recent accuracy {summary['recent_accuracy']}%)."
            )

    return "\n".join(lines)
