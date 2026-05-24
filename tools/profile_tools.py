import json
import os
import json
from datetime import datetime
from json import JSONDecodeError

from backend.database import get_student_profile, save_student_profile
from backend.storage import atomic_write_json

PROFILE_FOLDER = "profiles"
DEFAULT_PROFILE_EXAM = {
    "name": "JEE MAIN",
    "exam_date": "2099-12-31",
    "subjects": ["Physics", "Chemistry", "Mathematics"],
}


def _profile_path(name):
    return os.path.join(PROFILE_FOLDER, f"{name}.json")


def _ensure_profile_folder():
    os.makedirs(PROFILE_FOLDER, exist_ok=True)


def _timestamp():
    return datetime.utcnow().isoformat(timespec="seconds")


def _atomic_write_json(filepath, payload):
    atomic_write_json(filepath, payload)


def _normalize_profile(profile):
    profile = dict(profile or {})
    profile.setdefault("preferred_persona", "")
    profile.setdefault("preferred_voice", "")
    profile.setdefault("voice_rate", -2)
    profile.setdefault("selected_avatar", "calm-mentor")
    profile.setdefault("tutor_name", "Astra")
    profile.setdefault("tutor_personality_preset", "balanced")
    profile.setdefault("tutor_personality_traits", [])
    profile.setdefault("tutor_personality_notes", "")
    profile.setdefault("tutor_style", "positive, encouraging, and easy to talk to")
    profile.setdefault("preferred_language", "english")
    profile.setdefault("ui_language", "english")
    profile.setdefault("default_response_language", "English")
    profile.setdefault("default_tutor_level", 3)
    profile.setdefault("appearance_description", "friendly, fun, and human-like")
    profile.setdefault("avatar_visuals", {})
    profile.setdefault(
        "onboarding_profile",
        {
            "intro_completed": False,
            "why_astra": "",
            "interests": "",
            "dislikes": "",
            "conversation_style": "",
            "preferred_language": "",
            "explanation_depth": "",
            "stress_support": "",
            "goals_summary": "",
            "astra_question": "",
            "astra_question_answer": "",
        },
    )
    profile.setdefault(
        "group_study_preferences",
        {
            "enabled": False,
            "mode": "solo",
            "group_size": 3,
            "session_minutes": 60,
            "focus": "",
            "rotation_index": 0,
        },
    )
    if "exams" not in profile:
        profile["exams"] = [
            {
                "name": profile.get("exam", ""),
                "exam_date": profile.get("exam_date", ""),
                "subjects": profile.get("subjects", []),
            }
        ]
    if "max_study_hours_per_day" not in profile:
        profile["max_study_hours_per_day"] = profile.get("study_hours_per_day", 6)
    return profile


def _default_profile(name):
    clean_name = str(name or "Student").strip() or "Student"
    return _normalize_profile(
        {
            "name": clean_name,
            "exam": DEFAULT_PROFILE_EXAM["name"],
            "exam_date": DEFAULT_PROFILE_EXAM["exam_date"],
            "study_hours_per_day": 3,
            "subjects": list(DEFAULT_PROFILE_EXAM["subjects"]),
            "max_study_hours_per_day": 6,
            "preferred_persona": "",
            "preferred_voice": "",
            "voice_rate": -2,
            "selected_avatar": "calm-mentor",
            "tutor_name": "Astra",
            "tutor_personality_preset": "balanced",
            "tutor_personality_traits": [],
            "tutor_personality_notes": "",
            "tutor_style": "positive, encouraging, and easy to talk to",
            "preferred_language": "english",
            "ui_language": "english",
            "default_response_language": "English",
            "default_tutor_level": 3,
            "appearance_description": "friendly, fun, and human-like",
            "avatar_visuals": {},
            "onboarding_profile": {
                "intro_completed": False,
                "why_astra": "",
                "interests": "",
                "dislikes": "",
                "conversation_style": "",
                "preferred_language": "",
                "explanation_depth": "",
                "stress_support": "",
                "goals_summary": "",
                "astra_question": "",
                "astra_question_answer": "",
            },
            "group_study_preferences": {
                "enabled": False,
                "mode": "solo",
                "group_size": 3,
                "session_minutes": 60,
                "focus": "",
                "rotation_index": 0,
            },
            "exams": [dict(DEFAULT_PROFILE_EXAM)],
        }
    )


def _read_profile_file(filepath):
    with open(filepath, "r", encoding="utf-8-sig") as file:
        profile = json.load(file)
    return _normalize_profile(profile)


def _find_case_insensitive_match(name):
    _ensure_profile_folder()
    expected = f"{name}.json".lower()

    for filename in os.listdir(PROFILE_FOLDER):
        if filename.lower() == expected:
            return os.path.join(PROFILE_FOLDER, filename)

    return None


def _load_profile_from_db(name):
    try:
        profile = get_student_profile(name)
        if not profile:
            return None
        return _normalize_profile(profile)
    except Exception as exc:
        print(f"WARNING: Could not load profile {name} from database - returning default profile. {exc}")
        return _default_profile(name)


def _save_profile_to_db(profile):
    save_student_profile(profile["name"], profile)


def create_profile(
    name,
    exam,
    exam_date,
    study_hours_per_day,
    subjects,
    preferred_persona="",
    preferred_voice="",
    voice_rate=-2,
    exams=None,
    max_study_hours_per_day=None,
    onboarding_profile=None,
):
    _ensure_profile_folder()

    profile = _normalize_profile(
        {
            "name": name,
            "exam": exam,
            "exam_date": exam_date,
            "study_hours_per_day": study_hours_per_day,
            "subjects": subjects,
            "preferred_persona": preferred_persona,
            "tutor_name": "Astra",
            "tutor_style": "positive, encouraging, and easy to talk to",
            "appearance_description": "friendly, fun, and human-like",
            "avatar_visuals": {},
            "onboarding_profile": onboarding_profile
            if onboarding_profile is not None
            else {
                "intro_completed": False,
                "why_astra": "",
                "interests": "",
                "dislikes": "",
                "conversation_style": "",
                "preferred_language": "",
                "explanation_depth": "",
                "stress_support": "",
                "goals_summary": "",
                "astra_question": "",
                "astra_question_answer": "",
            },
            "group_study_preferences": {
                "enabled": False,
                "mode": "solo",
                "group_size": 3,
                "session_minutes": 60,
                "focus": "",
                "rotation_index": 0,
            },
            "preferred_voice": preferred_voice,
            "voice_rate": voice_rate,
            "exams": exams
            if exams is not None
            else [
                {
                    "name": exam,
                    "exam_date": exam_date,
                    "subjects": subjects,
                }
            ],
            "max_study_hours_per_day": max_study_hours_per_day
            if max_study_hours_per_day is not None
            else study_hours_per_day,
        }
    )

    _atomic_write_json(_profile_path(name), profile)
    _save_profile_to_db(profile)
    return profile


def load_profile(name):
    try:
        profile = _load_profile_from_db(name)
        if profile is not None:
            return profile

        filepath = _profile_path(name)

        if os.path.exists(filepath):
            profile = _read_profile_file(filepath)
            _save_profile_to_db(profile)
            return profile
    except Exception as exc:
        print(f"WARNING: Could not load profile {name} - returning default profile. {exc}")
        return _default_profile(name)

    try:
        alternate_path = _find_case_insensitive_match(name)
        if alternate_path:
            profile = _read_profile_file(alternate_path)
            save_profile(profile)
            return profile
    except Exception as exc:
        print(f"WARNING: Could not load profile {name} from alternate path - returning default profile. {exc}")
        return _default_profile(name)

    return _default_profile(name)


def save_profile(profile):
    _ensure_profile_folder()
    profile = _normalize_profile(profile)
    filepath = _profile_path(profile["name"])
    _atomic_write_json(filepath, profile)
    _save_profile_to_db(profile)
    return profile


def update_preferred_persona(name, preferred_persona):
    profile = load_profile(name)
    if profile is None:
        return None

    profile["preferred_persona"] = preferred_persona
    return save_profile(profile)


def update_voice_preferences(name, preferred_voice=None, voice_rate=None):
    profile = load_profile(name)
    if profile is None:
        return None

    if preferred_voice is not None:
        profile["preferred_voice"] = preferred_voice
    if voice_rate is not None:
        profile["voice_rate"] = voice_rate
    return save_profile(profile)
