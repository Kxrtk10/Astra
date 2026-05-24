import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

from backend.database import (
    get_all_chapter_scores as db_get_all_chapter_scores,
    get_student_progress_summary as db_get_student_progress_summary,
    log_progress_record as db_log_progress_record,
    save_chapter_score as db_save_chapter_score,
)
from backend.storage import atomic_write_json

PROGRESS_FOLDER = "progress_state"
CHAPTER_SCORE_FOLDER = Path("app_data") / "progress"
STATUS_META = {
    "done": {"label": "Done", "color": "green"},
    "revise": {"label": "Needs Revision", "color": "brown"},
    "pending": {"label": "Pending", "color": "red"},
}


def _progress_path(name):
    os.makedirs(PROGRESS_FOLDER, exist_ok=True)
    return os.path.join(PROGRESS_FOLDER, f"{name}.json")


def _chapter_scores_path(name):
    CHAPTER_SCORE_FOLDER.mkdir(parents=True, exist_ok=True)
    return CHAPTER_SCORE_FOLDER / f"{name}_chapter_scores.json"


def _timestamp():
    return datetime.utcnow().isoformat(timespec="seconds")


def _default_state():
    return {
        "items": [],
        "history": [],
        "checkpoint_attempts": [],
        "last_updated": "",
    }


def _default_chapter_scores_state():
    return {
        "chapters": {},
        "updated_at": "",
    }


def _normalize_state(state):
    state.setdefault("items", [])
    state.setdefault("history", [])
    state.setdefault("checkpoint_attempts", [])
    state.setdefault("last_updated", "")
    if not isinstance(state.get("history"), list):
        state["history"] = []
    if not isinstance(state.get("checkpoint_attempts"), list):
        state["checkpoint_attempts"] = []
    return state


def _normalize_chapter_scores_state(state):
    if not isinstance(state, dict):
        state = _default_chapter_scores_state()
    state.setdefault("chapters", {})
    state.setdefault("updated_at", "")
    if not isinstance(state.get("chapters"), dict):
        state["chapters"] = {}
    return state


def find_progress_item(name, exam, subject, topic):
    state = load_progress_state(name)
    clean_exam = str(exam or "").strip().lower()
    clean_subject = str(subject or "").strip().lower()
    clean_topic = str(topic or "").strip().lower()
    return next(
        (
            item
            for item in state["items"]
            if item.get("exam", "").lower() == clean_exam
            and item.get("subject", "").lower() == clean_subject
            and item.get("topic", "").lower() == clean_topic
        ),
        None,
    )


def _load_state_from_db(name):
    try:
        summary = db_get_student_progress_summary(name)
        if not summary:
            return None
        state = _default_state()
        state["progress_summary"] = summary
        return _normalize_state(state)
    except Exception as exc:
        print(f"WARNING: Could not load progress state for {name} from database - returning safe defaults. {exc}")
        return _default_state()


def _save_state_to_db(name, state):
    try:
        return None
    except Exception as exc:
        print(f"WARNING: Could not persist progress state summary for {name}: {exc}")


def load_progress_state(name):
    try:
        state = _load_state_from_db(name)
        if state is not None:
            return state

        filepath = _progress_path(name)
        if not os.path.exists(filepath):
            return _default_state()

        with open(filepath, "r", encoding="utf-8") as file:
            state = json.load(file)

        state = _normalize_state(state)
        _save_state_to_db(name, state)
        return state
    except Exception as exc:
        print(f"WARNING: Could not load progress state for {name} - returning safe defaults. {exc}")
        return _default_state()


def save_progress_state(name, state):
    try:
        filepath = _progress_path(name)
        state = _normalize_state(state)
        _append_history_snapshot(state)
        atomic_write_json(filepath, state)
        _save_state_to_db(name, state)
    except Exception as exc:
        print(f"WARNING: Could not save progress state for {name} - keeping safe defaults. {exc}")


def record_checkpoint_attempt(
    name,
    exam,
    subject,
    topic,
    is_correct,
    question="",
    student_answer="",
    correct_answer="",
    explanation_level=3,
    feedback="",
    re_explanation="",
):
    state = load_progress_state(name)
    state = _normalize_state(state)
    timestamp = datetime.now().isoformat(timespec="seconds")
    attempt = {
        "timestamp": timestamp,
        "exam": str(exam or "").strip(),
        "subject": str(subject or "").strip(),
        "topic": str(topic or "").strip(),
        "question": str(question or "").strip(),
        "student_answer": str(student_answer or "").strip(),
        "correct_answer": str(correct_answer or "").strip(),
        "explanation_level": int(explanation_level or 3),
        "is_correct": bool(is_correct),
        "feedback": str(feedback or "").strip(),
        "re_explanation": str(re_explanation or "").strip(),
    }
    state["checkpoint_attempts"].append(attempt)
    state["checkpoint_attempts"] = state["checkpoint_attempts"][-120:]
    state["last_updated"] = timestamp
    db_log_progress_record(
        name,
        topic,
        subject,
        "",
        "checkpoint",
        100 if is_correct else 0,
        0,
    )
    filepath = _progress_path(name)
    atomic_write_json(filepath, state)
    _save_state_to_db(name, state)
    return get_progress_snapshot(name)


def load_chapter_scores_state(name):
    try:
        scores = db_get_all_chapter_scores(name)
        if scores:
            state = _default_chapter_scores_state()
            for entry in scores:
                chapter_key = str(entry.get("unit_name") or "Chapter").strip()
                state["chapters"][chapter_key] = {
                    "subject": entry.get("subject", ""),
                    "subtopic_scores": entry.get("subtopic_scores", {}),
                    "chapter_test_score": entry.get("chapter_test_score"),
                    "mastery_level": entry.get("mastery_level", "in_progress"),
                    "attempts": entry.get("attempts", 1),
                    "last_attempt_date": entry.get("completed_at", ""),
                    "revision_count": 0,
                    "time_spent_total_minutes": entry.get("time_spent_minutes", 0),
                    "subtopics_completed": [],
                    "revision_scheduled": [],
                    "completed_date": entry.get("completed_at", ""),
                }
            return _normalize_chapter_scores_state(state)
        filepath = _chapter_scores_path(name)
        if not filepath.exists():
            return _default_chapter_scores_state()
        with open(filepath, "r", encoding="utf-8") as file:
            state = json.load(file)
        return _normalize_chapter_scores_state(state)
    except Exception as exc:
        print(f"WARNING: Could not load chapter score state for {name}; returning safe defaults. {exc}")
        return _default_chapter_scores_state()


def save_chapter_scores_state(name, state):
    try:
        filepath = _chapter_scores_path(name)
        state = _normalize_chapter_scores_state(state)
        atomic_write_json(str(filepath), state)
        for chapter_name, chapter in (state.get("chapters", {}) or {}).items():
            db_save_chapter_score(
                name,
                chapter_name,
                chapter.get("subject", ""),
                chapter.get("subtopic_scores", {}),
                chapter.get("chapter_test_score", 0) or 0,
                chapter.get("mastery_level", "in_progress"),
                chapter.get("time_spent_total_minutes", 0) or 0,
            )
    except Exception as exc:
        print(f"WARNING: Could not save chapter score state for {name}; keeping safe defaults. {exc}")


def log_checkpoint(student_id, unit_name, subject, subtopic_id, score, time_spent_minutes=0, chapter_name=""):
    state = load_chapter_scores_state(student_id)
    chapter_key = str(chapter_name or unit_name or "Chapter").strip()
    chapter = state["chapters"].setdefault(
        chapter_key,
        {
            "subject": str(subject or "").strip(),
            "subtopic_scores": {},
            "chapter_test_score": None,
            "mastery_level": "in_progress",
            "attempts": 0,
            "last_attempt_date": "",
            "revision_count": 0,
            "time_spent_total_minutes": 0,
            "subtopics_completed": [],
            "revision_scheduled": [],
        },
    )
    chapter["subject"] = str(subject or chapter.get("subject", "")).strip()
    chapter["subtopic_scores"][str(subtopic_id or "subtopic").strip()] = round(float(score or 0), 1)
    chapter["attempts"] = int(chapter.get("attempts", 0) or 0) + 1
    chapter["last_attempt_date"] = _timestamp()
    chapter["time_spent_total_minutes"] = round(float(chapter.get("time_spent_total_minutes", 0) or 0) + float(time_spent_minutes or 0), 1)
    if subtopic_id and subtopic_id not in chapter["subtopics_completed"]:
        chapter["subtopics_completed"].append(subtopic_id)
    state["updated_at"] = _timestamp()
    db_log_progress_record(
        student_id,
        subtopic_id or chapter_key,
        subject,
        unit_name,
        "checkpoint",
        score,
        time_spent_minutes,
    )
    save_chapter_scores_state(student_id, state)
    return state


def log_chapter_score(student_id, unit_name, subject, score, mastery_level, subtopic_scores=None, time_spent_minutes=0, revision_count=0, completed_date=None):
    state = load_chapter_scores_state(student_id)
    chapter_key = str(unit_name or "Chapter").strip()
    chapter = state["chapters"].setdefault(
        chapter_key,
        {
            "subject": str(subject or "").strip(),
            "subtopic_scores": {},
            "chapter_test_score": None,
            "mastery_level": "in_progress",
            "attempts": 0,
            "last_attempt_date": "",
            "revision_count": 0,
            "time_spent_total_minutes": 0,
            "subtopics_completed": [],
            "revision_scheduled": [],
        },
    )
    chapter["subject"] = str(subject or chapter.get("subject", "")).strip()
    if isinstance(subtopic_scores, dict):
        chapter["subtopic_scores"] = {
            str(key).strip(): round(float(value or 0), 1)
            for key, value in subtopic_scores.items()
            if str(key).strip()
        }
    chapter["chapter_test_score"] = round(float(score or 0), 1)
    chapter["mastery_level"] = str(mastery_level or "developing").strip().lower()
    chapter["revision_count"] = int(revision_count or 0)
    chapter["time_spent_total_minutes"] = round(float(time_spent_minutes or chapter.get("time_spent_total_minutes", 0) or 0), 1)
    chapter["completed_date"] = str(completed_date or datetime.now().date().isoformat())
    chapter["last_attempt_date"] = _timestamp()
    state["updated_at"] = _timestamp()
    db_log_progress_record(
        student_id,
        unit_name,
        subject,
        unit_name,
        "chapter_test",
        score,
        time_spent_minutes,
    )
    save_chapter_scores_state(student_id, state)
    return state


def get_chapter_mastery_board(name):
    state = load_chapter_scores_state(name)
    chapters = state.get("chapters", {}) or {}
    board = []
    for chapter_name, chapter in chapters.items():
        score = chapter.get("chapter_test_score")
        mastery_level = str(chapter.get("mastery_level") or "not_started").lower()
        if score is None:
            color = "grey"
            status = "not_started"
        elif score >= 85:
            color = "green"
            status = "mastered"
        elif score >= 70:
            color = "yellow"
            status = "proficient"
        elif score >= 50:
            color = "orange"
            status = "developing"
        else:
            color = "red"
            status = "needs_revision"
        if chapter.get("attempts", 0):
            color = "blue" if status == "not_started" else color
        board.append(
            {
                "chapter_name": chapter_name,
                "subject": chapter.get("subject", ""),
                "status": status,
                "color": color,
                "mastery_level": mastery_level,
                "chapter_test_score": score,
                "subtopic_scores": chapter.get("subtopic_scores", {}),
                "time_spent_total_minutes": chapter.get("time_spent_total_minutes", 0),
                "revision_count": chapter.get("revision_count", 0),
                "completed_date": chapter.get("completed_date", ""),
                "revision_scheduled": chapter.get("revision_scheduled", []),
            }
        )
    board.sort(key=lambda item: (item["subject"], item["chapter_name"]))
    return {"chapters": board, "updated_at": state.get("updated_at", "")}


def get_chapter_score_summary(name):
    state = load_chapter_scores_state(name)
    chapters = state.get("chapters", {}) or {}
    completed = [chapter for chapter in chapters.values() if chapter.get("chapter_test_score") is not None]
    if not completed:
        return {
            "average_score": 0,
            "best_chapter": "",
            "most_improved_chapter": "",
            "subject_averages": {},
            "score_trend": [],
            "time_spent_week": {},
        }
    average_score = round(sum(float(chapter.get("chapter_test_score", 0) or 0) for chapter in completed) / len(completed), 1)
    best = max(completed, key=lambda chapter: float(chapter.get("chapter_test_score", 0) or 0))
    subject_buckets = {}
    for chapter in completed:
        subject = str(chapter.get("subject") or "General").strip() or "General"
        bucket = subject_buckets.setdefault(subject, {"score_total": 0.0, "count": 0})
        bucket["score_total"] += float(chapter.get("chapter_test_score", 0) or 0)
        bucket["count"] += 1
    subject_averages = {
        subject: round(bucket["score_total"] / bucket["count"], 1) if bucket["count"] else 0
        for subject, bucket in subject_buckets.items()
    }
    return {
        "average_score": average_score,
        "best_chapter": best.get("chapter_name") or "",
        "most_improved_chapter": best.get("chapter_name") or "",
        "subject_averages": subject_averages,
        "score_trend": [
            {
                "chapter_name": chapter_name,
                "score": chapter.get("chapter_test_score", 0),
                "mastery_level": chapter.get("mastery_level", ""),
            }
            for chapter_name, chapter in list(chapters.items())[-10:]
        ],
        "time_spent_week": {
            chapter_name: chapter.get("time_spent_total_minutes", 0)
            for chapter_name, chapter in list(chapters.items())[-10:]
        },
    }


def _score_to_confidence_level(score):
    try:
        value = float(score)
    except (TypeError, ValueError):
        value = 0.0
    if value >= 85:
        return "strong"
    if value >= 75:
        return "good"
    if value >= 60:
        return "medium"
    if value >= 40:
        return "low"
    return "new"


def log_topic_completion(student_id, topic, subject, score, session_type, unit_name="", exam="JEE MAIN"):
    state = load_progress_state(student_id)
    status = "done" if float(score or 0) >= 75 else "revise" if float(score or 0) >= 60 else "pending"
    topic_label = str(topic or "").strip()
    subject_label = str(subject or "").strip()
    note = f"{session_type} session | score {round(float(score or 0), 1)}% | unit {str(unit_name or '').strip()}"
    snapshot = upsert_progress_item(student_id, exam, subject_label, topic_label, status, note=note)
    db_log_progress_record(
        student_id,
        topic_label,
        subject_label,
        str(unit_name or "").strip(),
        str(session_type or "learn").strip(),
        int(round(float(score or 0))),
        0,
    )
    state = load_progress_state(student_id)
    state.setdefault("topic_completions", [])
    state["topic_completions"].append(
        {
            "timestamp": _timestamp(),
            "topic": topic_label,
            "subject": subject_label,
            "score": round(float(score or 0), 1),
            "session_type": str(session_type or "learn").strip().lower(),
            "unit_name": str(unit_name or "").strip(),
            "confidence_level": _score_to_confidence_level(score),
        }
    )
    state["topic_completions"] = state["topic_completions"][-120:]
    filepath = _progress_path(student_id)
    atomic_write_json(filepath, state)
    _save_state_to_db(student_id, state)
    return {
        "snapshot": snapshot,
        "confidence_level": _score_to_confidence_level(score),
        "status": status,
        "next_revision_days": [1, 2, 4, 7] if status != "done" else [3, 7, 14],
    }


def _count_items(items):
    counts = {
        "done": sum(1 for item in items if item.get("status") == "done"),
        "revise": sum(1 for item in items if item.get("status") == "revise"),
        "pending": sum(1 for item in items if item.get("status") == "pending"),
        "total": len(items),
    }
    counts["completion_rate"] = round((counts["done"] / counts["total"] * 100), 1) if counts["total"] else 0
    return counts


def _history_entry_from_state(state, timestamp=None):
    items = state.get("items", [])
    counts = _count_items(items)
    topic_momentum = _build_topic_momentum(items)
    return {
        "timestamp": timestamp or _timestamp(),
        "counts": counts,
        "completion_rate": counts["completion_rate"],
        "mastery_signal": topic_momentum["mastery_signal"],
        "strongest_topics": topic_momentum["strongest_topics"][:5],
        "weakest_topics": topic_momentum["weakest_topics"][:5],
    }


def _append_history_snapshot(state):
    history = state.setdefault("history", [])
    if not isinstance(history, list):
        history = []
        state["history"] = history
    history.append(_history_entry_from_state(state))
    state["history"] = history[-120:]


def upsert_progress_item(name, exam, subject, topic, status, note=""):
    state = load_progress_state(name)
    clean_status = status if status in STATUS_META else "pending"
    clean_exam = str(exam or "").strip()
    clean_subject = str(subject or "").strip()
    clean_topic = str(topic or "").strip()
    clean_note = str(note or "").strip()

    if not clean_topic:
        raise ValueError("Topic or chapter name is required.")

    existing = next(
        (
            item
            for item in state["items"]
            if item.get("exam", "").lower() == clean_exam.lower()
            and item.get("subject", "").lower() == clean_subject.lower()
            and item.get("topic", "").lower() == clean_topic.lower()
        ),
        None,
    )

    timestamp = datetime.now().isoformat(timespec="seconds")
    if existing:
        existing["status"] = clean_status
        existing["note"] = clean_note
        existing["updated_at"] = timestamp
    else:
        state["items"].append(
            {
                "id": uuid4().hex[:12],
                "exam": clean_exam,
                "subject": clean_subject,
                "topic": clean_topic,
                "status": clean_status,
                "note": clean_note,
                "updated_at": timestamp,
            }
        )

    state["items"] = state["items"][-400:]
    state["last_updated"] = timestamp
    save_progress_state(name, state)
    return get_progress_snapshot(name)


def update_progress_status(name, item_id, status):
    state = load_progress_state(name)
    clean_status = status if status in STATUS_META else "pending"
    timestamp = datetime.now().isoformat(timespec="seconds")
    for item in state["items"]:
        if item.get("id") == item_id:
            item["status"] = clean_status
            item["updated_at"] = timestamp
            state["last_updated"] = timestamp
            save_progress_state(name, state)
            return get_progress_snapshot(name)
    raise ValueError("Progress item not found.")


def build_progress_reminders(items):
    pending = [item for item in items if item.get("status") == "pending"]
    revise = [item for item in items if item.get("status") == "revise"]
    done = [item for item in items if item.get("status") == "done"]

    reminders = []
    if pending:
        sample = pending[:3]
        labels = ", ".join(item["topic"] for item in sample)
        reminders.append(
            f"Red items still need attention: {labels}{' and more' if len(pending) > 3 else ''}."
        )
    if revise:
        sample = revise[:3]
        labels = ", ".join(item["topic"] for item in sample)
        reminders.append(
            f"Brown items deserve a quick second pass: {labels}{' and more' if len(revise) > 3 else ''}."
        )
    if done and not pending and not revise:
        reminders.append("Everything currently tracked looks covered. Use this board to keep revision from slipping.")
    if not reminders:
        reminders.append("Start by adding one topic or chapter so the tracker can guide what is done, pending, or due for revision.")
    return reminders


def _build_exam_totals(items):
    exam_totals = {}
    for item in items:
        exam_key = str(item.get("exam", "")).strip() or "General"
        exam_bucket = exam_totals.setdefault(
            exam_key,
            {"done": 0, "revise": 0, "pending": 0, "total": 0},
        )
        status = item.get("status", "pending")
        exam_bucket["total"] += 1
        exam_bucket[status if status in STATUS_META else "pending"] += 1
    return dict(sorted(exam_totals.items(), key=lambda item: (-item[1]["total"], item[0].lower())))


def _build_topic_momentum(items):
    pending = [item for item in items if item.get("status") == "pending"]
    revise = [item for item in items if item.get("status") == "revise"]
    done = [item for item in items if item.get("status") == "done"]
    strongest = done[-5:]
    weakest = (pending[:5] + revise[:5])[:5]
    completion_rate = round((len(done) / len(items) * 100), 1) if items else 0

    if completion_rate >= 80:
        mastery_signal = "strong"
    elif completion_rate >= 55:
        mastery_signal = "building"
    elif completion_rate >= 30:
        mastery_signal = "fragile"
    else:
        mastery_signal = "starting"

    if pending and len(pending) >= len(done):
        next_focus = "Clear the pending topics before adding much more."
    elif revise:
        next_focus = "Revisit the revise topics with a short second pass."
    elif done:
        next_focus = "Keep a light revision loop so the done topics stay fresh."
    else:
        next_focus = "Add the first few topics so the tracker can guide what comes next."

    return {
        "completion_rate": completion_rate,
        "mastery_signal": mastery_signal,
        "next_focus": next_focus,
        "strongest_topics": [item.get("topic", "") for item in strongest if item.get("topic")],
        "weakest_topics": [item.get("topic", "") for item in weakest if item.get("topic")],
    }


def _parse_timestamp(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None


def _week_key(timestamp):
    parsed = _parse_timestamp(timestamp)
    if not parsed:
        return "unknown"
    year, week, _ = parsed.isocalendar()
    return f"{year}-W{week:02d}"


def _week_label(timestamp):
    parsed = _parse_timestamp(timestamp)
    if not parsed:
        return "Unknown week"
    year, week, _ = parsed.isocalendar()
    return f"W{week:02d} {year}"


def _build_weekly_history(history):
    buckets = {}
    for entry in history or []:
        timestamp = entry.get("timestamp", "")
        key = _week_key(timestamp)
        counts = entry.get("counts", {}) or {}
        buckets[key] = {
            "label": _week_label(timestamp),
            "timestamp": timestamp,
            "done": int(counts.get("done", 0) or 0),
            "revise": int(counts.get("revise", 0) or 0),
            "pending": int(counts.get("pending", 0) or 0),
            "total": int(counts.get("total", 0) or 0),
            "completion_rate": float(entry.get("completion_rate", counts.get("completion_rate", 0) or 0) or 0),
            "samples": 1,
        }

    weekly = list(buckets.values())

    weekly.sort(key=lambda item: item.get("timestamp", ""))
    return weekly[-8:]


def _build_week_over_week(history, current_counts):
    history = history or []
    if not history:
        return {
            "current": current_counts,
            "previous": {},
            "delta": {},
            "improvement_rate": 0,
            "summary": "Start saving progress items to build your weekly comparison.",
        }

    latest = history[-1]
    threshold = datetime.utcnow()
    threshold = threshold.replace(microsecond=0)  # keep comparison stable
    previous = history[0]
    for entry in reversed(history[:-1]):
        parsed = _parse_timestamp(entry.get("timestamp"))
        if parsed and (threshold - parsed).days >= 7:
            previous = entry
            break

    current_rate = round((current_counts["done"] / current_counts["total"] * 100), 1) if current_counts["total"] else 0
    previous_counts = previous.get("counts", {}) or {}
    previous_rate = round((previous_counts.get("done", 0) / previous_counts.get("total", 0) * 100), 1) if previous_counts.get("total") else 0
    delta = {
        "done": current_counts["done"] - int(previous_counts.get("done", 0) or 0),
        "revise": current_counts["revise"] - int(previous_counts.get("revise", 0) or 0),
        "pending": current_counts["pending"] - int(previous_counts.get("pending", 0) or 0),
        "total": current_counts["total"] - int(previous_counts.get("total", 0) or 0),
        "completion_rate": round(current_rate - previous_rate, 1),
    }

    if delta["completion_rate"] > 0:
        summary = f"Completion is up by {delta['completion_rate']} points since the previous weekly snapshot."
    elif delta["completion_rate"] < 0:
        summary = f"Completion has dipped by {abs(delta['completion_rate'])} points, so the next week should focus on repair."
    else:
        summary = "Completion is steady, so the next shift should come from topic quality rather than raw volume."

    if delta["pending"] < 0:
        summary += " Pending work is shrinking, which is a healthy sign."
    elif delta["pending"] > 0:
        summary += " Pending work has grown, so the plan should trim distractions and refocus."

    return {
        "current": {
            "counts": current_counts,
            "completion_rate": current_rate,
            "timestamp": latest.get("timestamp", ""),
        },
        "previous": {
            "counts": previous_counts,
            "completion_rate": previous_rate,
            "timestamp": previous.get("timestamp", ""),
        },
        "delta": delta,
        "improvement_rate": delta["completion_rate"],
        "summary": summary,
    }


def get_progress_snapshot(name):
    state = load_progress_state(name)
    items = sorted(
        state.get("items", []),
        key=lambda item: (
            {"pending": 0, "revise": 1, "done": 2}.get(item.get("status"), 3),
            item.get("exam", ""),
            item.get("subject", ""),
            item.get("topic", ""),
        ),
    )
    counts = _count_items(items)
    grouped = {
        "done": [item for item in items if item.get("status") == "done"],
        "revise": [item for item in items if item.get("status") == "revise"],
        "pending": [item for item in items if item.get("status") == "pending"],
    }
    exam_totals = _build_exam_totals(items)
    topic_momentum = _build_topic_momentum(items)
    history = state.get("history", []) or []
    checkpoint_attempts = state.get("checkpoint_attempts", []) or []
    checkpoint_total = len(checkpoint_attempts)
    checkpoint_correct = sum(1 for item in checkpoint_attempts if item.get("is_correct"))
    weekly_history = _build_weekly_history(history)
    week_over_week = _build_week_over_week(history, counts)
    return {
        "counts": counts,
        "status_percentages": {
            key: round((value / counts["total"] * 100), 1) if counts["total"] else 0
            for key, value in counts.items()
            if key not in {"total", "completion_rate"}
        },
        "items": items,
        "grouped": grouped,
        "reminders": build_progress_reminders(items),
        "exam_totals": exam_totals,
        "topic_momentum": topic_momentum,
        "checkpoint_attempts": checkpoint_attempts[-10:],
        "checkpoint_summary": {
            "total": checkpoint_total,
            "correct": checkpoint_correct,
            "incorrect": max(0, checkpoint_total - checkpoint_correct),
            "accuracy": round((checkpoint_correct / checkpoint_total * 100), 1) if checkpoint_total else 0,
        },
        "weekly_history": weekly_history,
        "week_over_week": week_over_week,
        "history_size": len(history),
        "last_updated": state.get("last_updated", ""),
        "status_meta": STATUS_META,
    }
