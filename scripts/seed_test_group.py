from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend import database
from backend.auth import create_user, get_user_by_email, get_user_by_student_name, hash_password
from tools.analytics_tools import load_analytics_state, save_analytics_state
from tools.profile_tools import create_profile, load_profile, save_profile
from tools.progress_tracker_tools import load_progress_state, save_progress_state

TEST_USERS = ["sanman", "shashank"]
TEST_PASSWORD = "AstraTest123!"
SEED_NOTE = "seed_test_group"
DEFAULT_MAIN_STUDENT = "SSK Kartik"


def normalize_topic(value: str) -> str:
    return " ".join(str(value or "").strip().lower().split())


def display_topic(topic: str, subject: str) -> str:
    topic_text = str(topic or "").strip() or "topic"
    subject_text = str(subject or "").strip()
    return f"{topic_text} - {subject_text}" if subject_text else topic_text


def derive_pace_band(user_id: str) -> str:
    """Mirror the Study Groups pace-band formula without importing web_api."""
    analytics = load_analytics_state(user_id) or {}
    groups = [
        (list(analytics.get("practice_attempts") or [])[-8:], "accuracy_percent", "time_taken_minutes"),
        (list(analytics.get("chapter_completions") or [])[-6:], "score", "time_taken_minutes"),
        (list(analytics.get("subtopic_scores") or [])[-10:], "score", "duration_minutes"),
    ]
    accuracy_values = []
    duration_values = []
    for rows, accuracy_key, duration_key in groups:
        for row in rows:
            try:
                accuracy_values.append(float(row.get(accuracy_key, 0) or 0))
            except (TypeError, ValueError):
                pass
            try:
                minutes = float(row.get(duration_key, 0) or 0)
                if minutes > 0:
                    duration_values.append(minutes)
            except (TypeError, ValueError):
                pass

    if not accuracy_values and not duration_values:
        return "steady"
    avg_accuracy = sum(accuracy_values) / len(accuracy_values) if accuracy_values else 65
    avg_duration = sum(duration_values) / len(duration_values) if duration_values else 60
    if avg_accuracy >= 75 and avg_duration <= 55:
        return "fast"
    if avg_accuracy < 55 or avg_duration >= 90:
        return "slow"
    return "steady"


def profile_exists(student_name: str) -> bool:
    profile_path = ROOT / "profiles" / f"{student_name}.json"
    if profile_path.exists():
        return True
    row = database.execute_query(
        "SELECT 1 FROM student_profiles WHERE lower(student_id) = lower(?) LIMIT 1",
        (student_name,),
        fetchone=True,
    )
    return bool(row)


def planner_today_path(student_name: str) -> Path:
    return ROOT / "app_data" / "planner" / f"{student_name}_today.json"


def find_main_student(explicit: str = "") -> str:
    if explicit:
        return explicit
    if profile_exists(DEFAULT_MAIN_STUDENT) or planner_today_path(DEFAULT_MAIN_STUDENT).exists():
        return DEFAULT_MAIN_STUDENT
    profile_dir = ROOT / "profiles"
    if profile_dir.exists():
        for path in profile_dir.glob("*.json"):
            if path.stem.lower() not in {user.lower() for user in TEST_USERS}:
                return path.stem
    planner_dir = ROOT / "app_data" / "planner"
    if planner_dir.exists():
        for path in planner_dir.glob("*_today.json"):
            name = path.name[: -len("_today.json")]
            if name.lower() not in {user.lower() for user in TEST_USERS}:
                return name
    return DEFAULT_MAIN_STUDENT


def first_pending_from_progress(student_name: str) -> dict:
    state = load_progress_state(student_name)
    for item in state.get("items", []) or []:
        status = str(item.get("status") or "").strip().lower()
        if status in {"pending", "red", "not_started", "not started"} and item.get("topic"):
            return {
                "topic": str(item.get("topic") or "").strip(),
                "subject": str(item.get("subject") or "").strip(),
                "exam": str(item.get("exam") or "").strip() or "JEE MAIN",
                "source": "progress_state",
            }
    return {}


def iter_planner_entries(payload):
    if isinstance(payload, dict):
        for key in ("primary", "morning", "afternoon", "evening"):
            value = payload.get(key)
            if isinstance(value, dict):
                yield value
        for value in payload.values():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        yield item
            elif isinstance(value, dict):
                yield value
    elif isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                yield item


def topic_from_planner_today(student_name: str) -> dict:
    path = planner_today_path(student_name)
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    for entry in iter_planner_entries(payload):
        topic = str(entry.get("topic") or entry.get("revision_topic") or "").strip()
        if topic:
            return {
                "topic": topic,
                "subject": str(entry.get("subject") or "").strip() or "Mathematics",
                "exam": str(entry.get("exam") or "").strip() or "JEE MAIN",
                "source": str(path.relative_to(ROOT)),
            }
    return {}


def resolve_target_topic(main_student: str, override_topic: str = "", override_subject: str = "", override_exam: str = "") -> dict:
    if override_topic:
        return {
            "topic": override_topic.strip(),
            "subject": override_subject.strip() or "Mathematics",
            "exam": override_exam.strip() or "JEE MAIN",
            "source": "command line override",
        }
    return first_pending_from_progress(main_student) or topic_from_planner_today(main_student) or {
        "topic": "relations",
        "subject": "Mathematics",
        "exam": "JEE MAIN",
        "source": "fallback default",
    }


def ensure_auth_user(student_name: str) -> dict:
    email = f"{student_name}@astra.test"
    display_name = student_name.title()
    existing = get_user_by_student_name(student_name) or get_user_by_email(email)
    if existing:
        with database.db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                UPDATE users
                SET email = ?, password_hash = ?, display_name = ?, student_name = ?
                WHERE id = ?
                """,
                (email, hash_password(TEST_PASSWORD), display_name, student_name, existing["id"]),
            )
        return get_user_by_student_name(student_name) or {"email": email, "student_name": student_name}
    return create_user(email, TEST_PASSWORD, display_name, student_name)


def ensure_profile(student_name: str, main_profile: dict) -> dict:
    exams = main_profile.get("exams") or [
        {
            "name": main_profile.get("exam") or "JEE MAIN",
            "exam_date": main_profile.get("exam_date") or "2099-12-31",
            "subjects": main_profile.get("subjects") or ["Physics", "Chemistry", "Mathematics"],
        }
    ]
    first_exam = exams[0] if exams and isinstance(exams[0], dict) else {}
    profile = create_profile(
        student_name,
        first_exam.get("name") or "JEE MAIN",
        first_exam.get("exam_date") or "2099-12-31",
        int(main_profile.get("study_hours_per_day") or 3),
        first_exam.get("subjects") or main_profile.get("subjects") or ["Physics", "Chemistry", "Mathematics"],
        exams=exams,
        max_study_hours_per_day=int(main_profile.get("max_study_hours_per_day") or 6),
    )
    profile["group_study_preferences"] = {
        "enabled": True,
        "mode": "group_session",
        "group_size": 3,
        "session_minutes": 60,
        "focus": "seeded dev group matching",
        "rotation_index": 0,
    }
    return save_profile(profile)


def set_next_pending_topic(student_name: str, target: dict) -> dict:
    state = load_progress_state(student_name)
    topic_key = normalize_topic(target["topic"])
    subject_key = normalize_topic(target.get("subject", ""))
    exam_key = normalize_topic(target.get("exam", ""))
    existing_items = []
    for item in state.get("items", []) or []:
        same_topic = normalize_topic(item.get("topic")) == topic_key
        same_subject = normalize_topic(item.get("subject")) == subject_key if subject_key else same_topic
        same_exam = normalize_topic(item.get("exam")) == exam_key if exam_key else same_topic
        if same_topic and same_subject and same_exam:
            continue
        existing_items.append(item)

    now = datetime.utcnow().isoformat(timespec="seconds")
    seeded_item = {
        "id": uuid4().hex[:12],
        "exam": target.get("exam") or "JEE MAIN",
        "subject": target.get("subject") or "Mathematics",
        "topic": target["topic"],
        "status": "pending",
        "note": f"{SEED_NOTE}: next-up group session test topic",
        "updated_at": now,
    }
    state["items"] = [seeded_item] + existing_items
    state["last_updated"] = now
    save_progress_state(student_name, state)
    return seeded_item


def placeholder_for_band(pace_band: str) -> tuple[float, float]:
    if pace_band == "fast":
        return 82.0, 45.0
    if pace_band == "slow":
        return 50.0, 95.0
    return 65.0, 60.0


def seed_pace_data(student_name: str, target: dict, desired_band: str) -> str:
    accuracy, minutes = placeholder_for_band(desired_band)
    state = load_analytics_state(student_name)
    state["practice_attempts"] = [
        item for item in state.get("practice_attempts", []) if item.get("notes") != SEED_NOTE
    ][-40:]
    state["chapter_completions"] = []
    state["subtopic_scores"] = []
    base_time = datetime.utcnow() - timedelta(days=8)
    for index in range(8):
        state["practice_attempts"].append(
            {
                "timestamp": (base_time + timedelta(days=index)).isoformat(timespec="seconds"),
                "mode": "group_seed_practice",
                "exam": target.get("exam") or "JEE MAIN",
                "time_taken_minutes": minutes,
                "accuracy_percent": accuracy,
                "question_count": 10,
                "notes": SEED_NOTE,
            }
        )
    state["attempts_by_mode"] = state.get("attempts_by_mode", {}) or {}
    state["attempts_by_exam"] = state.get("attempts_by_exam", {}) or {}
    state["attempts_by_mode"]["group_seed_practice"] = 8
    state["attempts_by_exam"][str(target.get("exam") or "JEE MAIN").upper()] = 8
    state["last_updated"] = datetime.utcnow().isoformat(timespec="seconds")
    save_analytics_state(student_name, state)
    return derive_pace_band(student_name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed two dev users for Study Groups matching.")
    parser.add_argument("--main", default="", help="Main account/student name to mirror. Defaults to SSK Kartik when present.")
    parser.add_argument("--topic", default="", help="Override topic. If omitted, use main account pending/Today topic.")
    parser.add_argument("--subject", default="", help="Subject for --topic override.")
    parser.add_argument("--exam", default="", help="Exam for --topic override.")
    args = parser.parse_args()

    database.init_db()
    main_student = find_main_student(args.main)
    main_profile = load_profile(main_student)
    target = resolve_target_topic(main_student, args.topic, args.subject, args.exam)
    main_band = derive_pace_band(main_student)

    print("Astra Study Groups test seed")
    print(f"Main account: {main_student}")
    print(f"Topic source: {target['source']}")
    print(f"Target next-up topic: {display_topic(target['topic'], target.get('subject', ''))}")
    print(f"Exam: {target.get('exam') or 'JEE MAIN'}")
    print(f"Main pace band: {main_band}")
    print("")

    for student_name in TEST_USERS:
        user = ensure_auth_user(student_name)
        ensure_profile(student_name, main_profile)
        seeded_topic = set_next_pending_topic(student_name, target)
        actual_band = seed_pace_data(student_name, target, main_band)
        print(f"Seeded {student_name}")
        print(f"  login email: {user.get('email') or student_name + '@astra.test'}")
        print(f"  login password: {TEST_PASSWORD}")
        print(f"  next pending: {display_topic(seeded_topic['topic'], seeded_topic.get('subject', ''))}")
        print(f"  pace band: {actual_band}")
        print("")

    print("Done. These accounts should now match the main account's next Study Groups candidate topic and pace band.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
