import json
import os
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path

from backend.database import (
    get_active_chapter_session as db_get_active_chapter_session,
    get_all_chapter_scores as db_get_all_chapter_scores,
    save_chapter_score as db_save_chapter_score,
    save_chapter_session as db_save_chapter_session,
)
from backend.storage import atomic_write_json
from tools.analytics_tools import record_chapter_completion, record_subtopic_score
from tools.behavior_tools import record_behavior_event
from tools.jee_syllabus import build_chapter_ready_syllabus
from tools.planner_tools import record_topic_outcome
from tools.personal_memory_tools import add_memory
from tools.progress_tracker_tools import (
    load_chapter_scores_state,
    load_progress_state,
    log_chapter_score,
    log_checkpoint,
    save_chapter_scores_state,
    save_progress_state,
)
from tools.student_state_router import update_state
from tools.planner_tools import load_planner_state, save_planner_state

SESSION_FOLDER = Path("app_data") / "sessions"


def _ensure_session_folder():
    SESSION_FOLDER.mkdir(parents=True, exist_ok=True)


def _session_path(student_id):
    _ensure_session_folder()
    safe = str(student_id or "student").strip() or "student"
    return SESSION_FOLDER / f"{safe}_active_session.json"


def _chapter_scores_path(student_id):
    from tools.progress_tracker_tools import _chapter_scores_path as progress_chapter_scores_path

    return progress_chapter_scores_path(student_id)


def _timestamp():
    return datetime.utcnow().isoformat(timespec="seconds")


def _load_json(path, default):
    try:
        if not path.exists():
            return deepcopy(default)
        with open(path, "r", encoding="utf-8") as file:
            payload = json.load(file)
        if not isinstance(payload, dict):
            return deepcopy(default)
        return payload
    except Exception as exc:
        print(f"WARNING: Could not load chapter session data from {path}: {exc}")
        return deepcopy(default)


def _save_json(path, payload):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_json(str(path), payload)
    except Exception as exc:
        print(f"WARNING: Could not save chapter session data to {path}: {exc}")


def _find_unit(subject, unit_name):
    syllabus = build_chapter_ready_syllabus()
    for unit in syllabus.get(str(subject or "").strip().lower(), []):
        if str(unit.get("name") or "").strip().lower() == str(unit_name or "").strip().lower():
            return unit
    return None


def _default_session(student_id, unit_name, subject):
    unit = _find_unit(subject, unit_name) or {}
    subtopics = list(unit.get("subtopics") or [])
    return {
        "student_id": str(student_id or "").strip(),
        "unit_name": str(unit_name or "").strip(),
        "subject": str(subject or "").strip().lower(),
        "started_at": _timestamp(),
        "status": "in_progress",
        "current_subtopic_index": 0,
        "subtopics_completed": [],
        "subtopic_scores": {},
        "chapter_test_taken": False,
        "chapter_test_score": None,
        "total_concepts_covered": 0,
        "session_log": [],
        "subtopics": subtopics,
        "chapter_test_questions": int(unit.get("chapter_test_questions") or 15),
        "chapter_test_duration_minutes": int(unit.get("chapter_test_duration_minutes") or 30),
        "mastery_level": "in_progress",
        "revision_scheduled": [],
        "time_spent_minutes": 0,
    }


def _load_session(student_id):
    try:
        session = db_get_active_chapter_session(student_id)
        if session:
            return session
    except Exception as exc:
        print(f"WARNING: Could not load chapter session from database for {student_id}: {exc}")
    return _load_json(_session_path(student_id), {})


def get_active_chapter_session(student_id):
    try:
        session = _load_session(student_id)
        return session if isinstance(session, dict) else {}
    except Exception as exc:
        print(f"WARNING: Could not load active chapter session for {student_id}: {exc}")
        return {}


def get_resume_summary(student_id, unit_name):
    try:
        session = _load_session(student_id)
        if not session:
            return {
                "resuming": False,
                "unit_name": str(unit_name or "").strip(),
                "subject": "",
                "subtopics_completed": [],
                "current_subtopic": {},
                "subtopics_remaining": [],
                "chapter_progress_percent": 0,
                "time_spent_so_far_minutes": 0,
                "chapter_test_taken": False,
                "resume_message": "No active chapter session was found.",
            }
        session_unit = str(session.get("unit_name") or unit_name or "").strip()
        if str(unit_name or "").strip() and session_unit.lower() != str(unit_name).strip().lower():
            return {
                "resuming": False,
                "unit_name": str(unit_name or "").strip(),
                "subject": str(session.get("subject") or "").strip(),
                "subtopics_completed": [],
                "current_subtopic": {},
                "subtopics_remaining": [],
                "chapter_progress_percent": 0,
                "time_spent_so_far_minutes": 0,
                "chapter_test_taken": bool(session.get("chapter_test_taken")),
                "resume_message": "No matching active chapter session was found.",
            }

        subtopics = list(session.get("subtopics") or [])
        completed_ids = list(session.get("subtopics_completed") or [])
        session_log = list(session.get("session_log") or [])
        completed = []
        for item in subtopics:
            subtopic_id = str(item.get("id") or "").strip()
            if subtopic_id and subtopic_id not in completed_ids:
                continue
            score = round(float((session.get("subtopic_scores") or {}).get(subtopic_id, 0) or 0), 1)
            completed_at = ""
            for log_item in reversed(session_log):
                if str(log_item.get("event", "")).strip().lower() == "subtopic_completed" and str(log_item.get("subtopic_id", "")).strip() == subtopic_id:
                    completed_at = log_item.get("timestamp", "")
                    break
            pretty_completed_at = str(completed_at or session.get("completed_date") or session.get("started_at", "")).replace("T", " ")[:16]
            completed.append(
                {
                    "name": item.get("name", ""),
                    "score": score,
                    "completed_at": pretty_completed_at,
                }
            )
        current_payload = _current_subtopic_payload(session) or {}
        remaining = []
        current_index = int(session.get("current_subtopic_index") or 0)
        for index, item in enumerate(subtopics[current_index:], start=current_index + 1):
            name = str(item.get("name") or "").strip()
            if name:
                remaining.append(name)
        current_name = current_payload.get("subtopic_name") or (remaining[0] if remaining else "")
        total = max(1, len(subtopics))
        completed_count = len(completed)
        completed_lines = ", ".join(
            f"{item['name']} ({item['score']}%)" for item in completed if item.get("name")
        ) or "none yet"
        remaining_future = remaining[1:] if len(remaining) > 1 else []
        future_lines = ", ".join(remaining_future) or "nothing else"
        resume_message = (
            f"Welcome back. In {session_unit} you have completed {completed_count} of {total} subtopics"
            + (f" — {completed_lines}" if completed_lines != "none yet" else "")
            + (f". You are currently on Subtopic {current_payload.get('subtopic_number', completed_count + 1)}: {current_name}." if current_name else ".")
            + (f" After this you still have {future_lines} left before the Chapter Test." if future_lines != "nothing else" else " You are ready for the Chapter Test.")
            + f" Total time spent so far: {round(float(session.get('time_spent_minutes', 0) or 0), 1)} minutes."
        )
        return {
            "resuming": True,
            "unit_name": session_unit,
            "subject": str(session.get("subject") or "").strip(),
            "subtopics_completed": completed,
            "current_subtopic": {
                "name": current_name,
                "subtopic_number": current_payload.get("subtopic_number", completed_count + 1),
                "total_subtopics": total,
            },
            "subtopics_remaining": remaining,
            "chapter_progress_percent": _unit_progress_percent(session),
            "time_spent_so_far_minutes": round(float(session.get("time_spent_minutes", 0) or 0), 1),
            "chapter_test_taken": bool(session.get("chapter_test_taken")),
            "resume_message": resume_message,
            "session": session,
        }
    except Exception as exc:
        print(f"WARNING: Could not build chapter resume summary for {student_id}: {exc}")
        return {
            "resuming": False,
            "unit_name": str(unit_name or "").strip(),
            "subject": "",
            "subtopics_completed": [],
            "current_subtopic": {},
            "subtopics_remaining": [],
            "chapter_progress_percent": 0,
            "time_spent_so_far_minutes": 0,
            "chapter_test_taken": False,
            "resume_message": "No active chapter session is available right now.",
        }


def reset_chapter_session(student_id, unit_name, subject):
    try:
        session = _load_session(student_id)
        previous_scores = dict((session or {}).get("subtopic_scores", {}) or {})
        previous_time = round(float((session or {}).get("time_spent_minutes", 0) or 0), 1)
        previous_best = round(float((session or {}).get("chapter_test_score", 0) or 0), 1)
        reset_date = datetime.now().date().isoformat()
        if session and str(session.get("unit_name", "")).strip().lower() == str(unit_name or "").strip().lower():
            try:
                _session_path(student_id).unlink(missing_ok=True)
            except Exception as exc:
                print(f"WARNING: Could not delete chapter session file for {student_id}: {exc}")

        chapter_state = load_chapter_scores_state(student_id)
        chapter_entry = (chapter_state.get("chapters") or {}).get(unit_name, {})
        chapter_state.setdefault("chapters", {})
        chapter_state["chapters"][unit_name] = {
            **chapter_entry,
            "subject": subject,
            "subtopic_scores": {},
            "chapter_test_score": None,
            "mastery_level": "not_started",
            "revision_scheduled": [],
            "time_spent_total_minutes": previous_time,
            "attempts": int(chapter_entry.get("attempts", 0) or 0),
            "last_attempt_date": chapter_entry.get("last_attempt_date", ""),
            "revision_count": int(chapter_entry.get("revision_count", 0) or 0),
            "reset_history": list(chapter_entry.get("reset_history", []) or []) + [
                {
                    "date": reset_date,
                    "previous_scores": previous_scores,
                    "previous_time_spent_minutes": previous_time,
                    "reason": "student_reset",
                }
            ],
        }
        chapter_state["updated_at"] = datetime.utcnow().isoformat(timespec="seconds")
        save_chapter_scores_state(student_id, chapter_state)

        progress_state = load_progress_state(student_id)
        if progress_state:
            progress_state["checkpoint_attempts"] = [
                item for item in progress_state.get("checkpoint_attempts", []) or []
                if not (
                    str(item.get("subject", "")).strip().lower() == str(subject or "").strip().lower()
                    and str(item.get("unit_name", item.get("topic", ""))).strip().lower() == str(unit_name or "").strip().lower()
                )
            ]
            save_progress_state(student_id, progress_state)

        planner_state = load_planner_state(student_id)
        for item in planner_state.get("topics", []) or []:
            if str(item.get("unit_name", "")).strip().lower() == str(unit_name or "").strip().lower():
                item["status"] = "not_started"
                item["covered"] = False
                item["confidence_level"] = "new"
                item["best_score"] = 0
                item["last_studied"] = ""
                item["next_revision_dates"] = []
                item.pop("priority_revision", None)
        planner_state["updated_at"] = datetime.utcnow().isoformat(timespec="seconds")
        save_planner_state(student_id, planner_state)

        add_memory(
            student_id,
            f"Student reset {unit_name} on {reset_date}. Previous best score was {previous_best}%. Starting fresh.",
        )
        update_state(student_id)
        return {
            "student_id": student_id,
            "unit_name": unit_name,
            "subject": subject,
            "status": "reset",
            "reset_date": reset_date,
            "previous_scores": previous_scores,
            "previous_time_spent_minutes": previous_time,
            "fresh_session": _default_session(student_id, unit_name, subject),
        }
    except Exception as exc:
        print(f"WARNING: Could not reset chapter session for {student_id}: {exc}")
        return {
            "student_id": student_id,
            "unit_name": unit_name,
            "subject": subject,
            "status": "reset_failed",
            "message": "Could not reset the chapter session right now.",
        }


def _save_session(student_id, session):
    try:
        db_save_chapter_session(
            student_id,
            session.get("unit_name", ""),
            session.get("subject", ""),
            session,
            session.get("status", "in_progress"),
        )
    except Exception as exc:
        print(f"WARNING: Could not save chapter session to database for {student_id}: {exc}")
    _save_json(_session_path(student_id), session)


def _unit_progress_percent(session):
    subtopics = list(session.get("subtopics") or [])
    total = len(subtopics)
    done = len(session.get("subtopics_completed") or [])
    if not total:
        return 0
    return round((done / total) * 100, 1)


def _current_subtopic_payload(session):
    subtopics = list(session.get("subtopics") or [])
    index = int(session.get("current_subtopic_index") or 0)
    if index >= len(subtopics):
        return None
    current = subtopics[index]
    return {
        "subtopic_id": current.get("id", ""),
        "subtopic_name": current.get("name", ""),
        "concepts": list(current.get("concepts") or []),
        "unit_name": session.get("unit_name", ""),
        "subject": session.get("subject", ""),
        "chapter_name": session.get("unit_name", ""),
        "subtopic_number": index + 1,
        "total_subtopics": len(subtopics),
        "is_last_subtopic": index == len(subtopics) - 1,
        "chapter_progress_percent": _unit_progress_percent(session),
        "estimated_minutes": current.get("estimated_minutes", 0),
    }


def start_chapter_session(student_id, unit_name, subject):
    try:
        session = _default_session(student_id, unit_name, subject)
        _save_session(student_id, session)
        return session
    except Exception as exc:
        print(f"WARNING: Could not start chapter session for {student_id}: {exc}")
        return _default_session(student_id, unit_name, subject)


def get_current_subtopic(student_id):
    try:
        session = _load_session(student_id)
        if not session:
            return {}
        current = _current_subtopic_payload(session)
        return current or {}
    except Exception as exc:
        print(f"WARNING: Could not load current subtopic for {student_id}: {exc}")
        return {}


def complete_subtopic(student_id, subtopic_id, checkpoint_score, time_spent_minutes):
    try:
        session = _load_session(student_id)
        if not session:
            return {
                "next_subtopic": None,
                "ready_for_chapter_test": False,
                "chapter_progress_percent": 0,
                "encouragement": "No active chapter session is running.",
            }
        subtopic_id = str(subtopic_id or "").strip()
        if subtopic_id and subtopic_id not in session.get("subtopics_completed", []):
            session.setdefault("subtopics_completed", []).append(subtopic_id)
        session.setdefault("subtopic_scores", {})[subtopic_id or f"subtopic-{len(session.get('subtopics_completed', []))}"] = round(float(checkpoint_score or 0), 1)
        session["current_subtopic_index"] = min(int(session.get("current_subtopic_index", 0) or 0) + 1, len(session.get("subtopics") or []))
        session["total_concepts_covered"] = len(session.get("subtopics_completed") or [])
        session["time_spent_minutes"] = round(float(session.get("time_spent_minutes", 0) or 0) + float(time_spent_minutes or 0), 1)
        session["session_log"].append(
            {
                "timestamp": _timestamp(),
                "event": "subtopic_completed",
                "subtopic_id": subtopic_id,
                "score": round(float(checkpoint_score or 0), 1),
                "time_spent_minutes": round(float(time_spent_minutes or 0), 1),
            }
        )
        ready = session["current_subtopic_index"] >= len(session.get("subtopics") or [])
        session["status"] = "ready_for_chapter_test" if ready else "in_progress"
        _save_session(student_id, session)
        next_subtopic = _current_subtopic_payload(session)
        progress = _unit_progress_percent(session)
        total = max(1, len(session.get("subtopics") or []))
        encouragement = f"{len(session.get('subtopics_completed') or [])} of {total} subtopics done. "
        if ready:
            encouragement += "You have finished the chapter path. Chapter test time."
        else:
            encouragement += f"Halfway through {session.get('unit_name', 'this chapter')}."
        return {
            "next_subtopic": next_subtopic,
            "ready_for_chapter_test": ready,
            "chapter_progress_percent": progress,
            "encouragement": encouragement,
            "session": session,
        }
    except Exception as exc:
        print(f"WARNING: Could not complete subtopic for {student_id}: {exc}")
        return {
            "next_subtopic": None,
            "ready_for_chapter_test": False,
            "chapter_progress_percent": 0,
            "encouragement": "That subtopic was saved, but the session needs another pass.",
        }


def _mastery_level_from_score(score):
    score = float(score or 0)
    if score >= 85:
        return "mastered"
    if score >= 70:
        return "proficient"
    if score >= 50:
        return "developing"
    return "needs_revision"


def _extract_weak_subtopics(session, answers, score):
    weak = []
    subtopic_scores = session.get("subtopic_scores", {}) or {}
    for subtopic_id, sub_score in subtopic_scores.items():
        if float(sub_score or 0) < 70:
            weak.append(subtopic_id)
    if isinstance(answers, dict):
        for key, value in answers.items():
            if isinstance(value, dict):
                if not value.get("is_correct", True) or float(value.get("score", 100) or 0) < 70:
                    weak.append(str(value.get("subtopic_id") or key).strip())
    if float(score or 0) < 50 and not weak:
        weak = list(subtopic_scores.keys())
    weak = [item for item in weak if str(item).strip()]
    return list(dict.fromkeys(weak))


def _session_to_chapter_summary(student_id, unit_name, session, mastery_level, weak_subtopics, strong_subtopics, chapter_test_score):
    completed_date = session.get("completed_date") or datetime.now().date().isoformat()
    return {
        "unit_name": unit_name,
        "subtopic_scores": session.get("subtopic_scores", {}) or {},
        "chapter_test_score": round(float(chapter_test_score or 0), 1) if chapter_test_score is not None else None,
        "mastery_level": mastery_level,
        "weak_subtopics": weak_subtopics,
        "strong_subtopics": strong_subtopics,
        "revision_scheduled": session.get("revision_scheduled", []) or [],
        "time_spent_minutes": round(float(session.get("time_spent_minutes", 0) or 0), 1),
        "completed_date": completed_date,
    }


def record_chapter_test(student_id, unit_name, subject, score, answers, time_taken_minutes):
    try:
        session = _load_session(student_id) or _default_session(student_id, unit_name, subject)
        mastery_level = _mastery_level_from_score(score)
        weak_subtopics = _extract_weak_subtopics(session, answers, score)
        subtopic_scores = session.get("subtopic_scores", {}) or {}
        strong_subtopics = [key for key, value in subtopic_scores.items() if float(value or 0) >= 85]
        revision_scheduled = weak_subtopics if mastery_level == "needs_revision" else [item for item in weak_subtopics if item not in strong_subtopics]
        session["chapter_test_taken"] = True
        session["chapter_test_score"] = round(float(score or 0), 1)
        session["mastery_level"] = mastery_level
        session["revision_scheduled"] = revision_scheduled
        session["status"] = "completed"
        session["completed_date"] = datetime.now().date().isoformat()
        session["time_spent_minutes"] = round(float(session.get("time_spent_minutes", 0) or 0) + float(time_taken_minutes or 0), 1)
        session["session_log"].append(
            {
                "timestamp": _timestamp(),
                "event": "chapter_test",
                "score": round(float(score or 0), 1),
                "time_taken_minutes": round(float(time_taken_minutes or 0), 1),
                "mastery_level": mastery_level,
                "weak_subtopics": weak_subtopics,
            }
        )
        _save_session(student_id, session)
        chapter_summary = _session_to_chapter_summary(student_id, unit_name, session, mastery_level, weak_subtopics, strong_subtopics, score)
        log_chapter_score(
            student_id,
            unit_name,
            subject,
            score,
            mastery_level,
            subtopic_scores=subtopic_scores,
            time_spent_minutes=session.get("time_spent_minutes", 0),
            revision_count=len(revision_scheduled),
            completed_date=session.get("completed_date"),
        )
        record_chapter_completion(student_id, unit_name, subject, score, mastery_level, time_taken_minutes, answers=answers)
        record_topic_outcome(student_id, unit_name, subject, unit_name, score, time_taken_minutes, "chapter_test")
        add_memory(
            student_id,
            f"Completed {unit_name} on {session.get('completed_date', datetime.now().date().isoformat())}. Score: {round(float(score or 0), 1)}%. Weak areas: {weak_subtopics}. Mastery: {mastery_level}.",
        )
        record_behavior_event(
            student_id,
            event_type="chapter_test_completed",
            user_input=f"Completed chapter test for {unit_name}",
            tutor_response="Chapter test recorded.",
            metadata={
                "unit_name": unit_name,
                "subject": subject,
                "score": round(float(score or 0), 1),
                "mastery_level": mastery_level,
            },
        )
        update_state(student_id)
        return {
            "student_id": student_id,
            "unit_name": unit_name,
            "subject": subject,
            "score": round(float(score or 0), 1),
            "mastery_level": mastery_level,
            "weak_subtopics": weak_subtopics,
            "strong_subtopics": strong_subtopics,
            "revision_scheduled": revision_scheduled,
            "chapter_summary": chapter_summary,
            "session": session,
        }
    except Exception as exc:
        print(f"WARNING: Could not record chapter test for {student_id}: {exc}")
        return {
            "student_id": student_id,
            "unit_name": unit_name,
            "subject": subject,
            "score": round(float(score or 0), 1),
            "mastery_level": "needs_revision",
            "weak_subtopics": [],
            "strong_subtopics": [],
            "revision_scheduled": [],
            "chapter_summary": {},
            "session": _default_session(student_id, unit_name, subject),
        }


def get_chapter_summary(student_id, unit_name):
    try:
        session = _load_session(student_id)
        if not session or str(session.get("unit_name", "")).strip().lower() != str(unit_name or "").strip().lower():
            return {}
        mastery_level = str(session.get("mastery_level") or "in_progress").strip().lower()
        weak_subtopics = [
            subtopic_id
            for subtopic_id, score in (session.get("subtopic_scores", {}) or {}).items()
            if float(score or 0) < 70
        ]
        strong_subtopics = [
            subtopic_id
            for subtopic_id, score in (session.get("subtopic_scores", {}) or {}).items()
            if float(score or 0) >= 85
        ]
        return _session_to_chapter_summary(
            student_id,
            unit_name,
            session,
            mastery_level,
            weak_subtopics,
            strong_subtopics,
            session.get("chapter_test_score"),
        )
    except Exception as exc:
        print(f"WARNING: Could not load chapter summary for {student_id}: {exc}")
        return {}


def get_all_chapter_summaries(student_id):
    try:
        path = _chapter_scores_path(student_id)
        if not path.exists():
            return {"chapters": [], "updated_at": ""}
        state = _load_json(path, {"chapters": {}, "updated_at": ""})
        chapters = []
        for chapter_name, chapter in (state.get("chapters") or {}).items():
            chapters.append(
                {
                    "unit_name": chapter_name,
                    "subject": chapter.get("subject", ""),
                    "subtopic_scores": chapter.get("subtopic_scores", {}),
                    "chapter_test_score": chapter.get("chapter_test_score", None),
                    "mastery_level": chapter.get("mastery_level", "not_started"),
                    "weak_subtopics": [subtopic for subtopic, score in (chapter.get("subtopic_scores") or {}).items() if float(score or 0) < 70],
                    "strong_subtopics": [subtopic for subtopic, score in (chapter.get("subtopic_scores") or {}).items() if float(score or 0) >= 85],
                    "revision_scheduled": chapter.get("revision_scheduled", []),
                    "time_spent_minutes": chapter.get("time_spent_total_minutes", 0),
                    "completed_date": chapter.get("completed_date", ""),
                }
            )
        return {"chapters": chapters, "updated_at": state.get("updated_at", "")}
    except Exception as exc:
        print(f"WARNING: Could not load all chapter summaries for {student_id}: {exc}")
        return {"chapters": [], "updated_at": ""}
