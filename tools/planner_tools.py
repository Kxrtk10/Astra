import json
import os
import re
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import OrderedDict

from google.adk.tools import ToolContext
from backend.database import get_planner_state as db_get_planner_state, save_planner_state as db_save_planner_state
from backend.storage import atomic_write_json
from tools.chat_outcome_tracker import build_task_learning_context, get_task_learning_profiles
from tools.behavior_tools import get_behavior_snapshot
from tools.progress_tracker_tools import load_progress_state
from tools.syllabus_tools import get_syllabus_documents
from tools.student_insight_tools import get_student_insight_snapshot
from tools.student_state_router import build_student_state_route, format_student_state_route
from tools.jee_syllabus import JEE_SYLLABUS, SPACED_REPETITION_INTERVALS, TOPIC_CONFIDENCE_THRESHOLDS, get_subject_units, iter_all_units

PLANNER_STATE_FOLDER = "planner_state"

DEFAULT_EXAM_SUBJECTS = {
    "JEE": ["Physics", "Chemistry", "Mathematics"],
    "JEE MAIN": ["Physics", "Chemistry", "Mathematics"],
    "JEE ADVANCED": ["Physics", "Chemistry", "Mathematics"],
}

JEE_EXAM_KEYS = {"JEE", "JEE MAIN", "JEE ADVANCED"}


def _canonical_jee_exam_name(exam_name):
    normalized = _subject_key(exam_name)
    if normalized == "JEE":
        return "JEE MAIN"
    return normalized

TOPIC_LIBRARY = {
    "JEE MAIN": {
        "PHYSICS": [
            "units and dimensions",
            "kinematics",
            "laws of motion",
            "work power energy",
            "rotation basics",
            "gravitation",
            "thermodynamics",
            "electrostatics",
            "current electricity",
            "magnetism",
            "ray optics",
            "modern physics",
        ],
        "CHEMISTRY": [
            "mole concept",
            "atomic structure",
            "periodic table",
            "chemical bonding",
            "states of matter",
            "thermodynamics",
            "equilibrium",
            "redox reactions",
            "organic basics",
            "hydrocarbons",
            "acids and bases",
            "solutions",
        ],
        "MATHEMATICS": [
            "sets and relations",
            "functions",
            "quadratic equations",
            "sequence and series",
            "complex numbers",
            "permutations and combinations",
            "probability",
            "limits and continuity",
            "differentiation",
            "integration",
            "coordinate geometry",
            "vectors and 3d",
        ],
    },
    "JEE ADVANCED": {
        "PHYSICS": [
            "vector mechanics",
            "advanced kinematics",
            "constraints and pulleys",
            "rotation and torque",
            "electrostatics deep dive",
            "capacitors and circuits",
            "magnetic effects",
            "optics and interference",
            "thermodynamics and heat",
            "modern physics",
            "waves and oscillations",
            "mixed concept applications",
        ],
        "CHEMISTRY": [
            "mole concept",
            "atomic structure",
            "chemical bonding",
            "equilibrium",
            "electrochemistry",
            "kinetics",
            "coordination compounds",
            "p-block trends",
            "organic reaction mechanisms",
            "carbonyl compounds",
            "amines",
            "named reactions",
        ],
        "MATHEMATICS": [
            "functions and graphs",
            "limits and continuity",
            "differentiation",
            "integration techniques",
            "definite integrals",
            "differential equations",
            "coordinate geometry",
            "vectors and 3d",
            "matrices and determinants",
            "probability",
            "complex numbers",
            "inequalities",
        ],
    },
    "NEET": {
        "PHYSICS": [
            "units and measurements",
            "kinematics",
            "laws of motion",
            "work power energy",
            "gravitation",
            "thermodynamics",
            "electrostatics",
            "current electricity",
            "magnetism",
            "ray optics",
            "wave optics",
            "modern physics",
        ],
        "CHEMISTRY": [
            "mole concept",
            "atomic structure",
            "periodic properties",
            "chemical bonding",
            "equilibrium",
            "thermodynamics",
            "solutions",
            "electrochemistry",
            "organic basics",
            "hydrocarbons",
            "biomolecules",
            "p-block",
        ],
        "BIOLOGY": [
            "cell structure",
            "biomolecules",
            "cell cycle and division",
            "plant physiology",
            "human physiology",
            "genetics",
            "molecular basis of inheritance",
            "evolution",
            "ecology",
            "reproduction",
            "biotechnology",
            "disease and immunity",
        ],
    },
    "GRE": {
        "QUANT": [
            "percentages",
            "ratios",
            "algebra",
            "number properties",
            "geometry",
            "statistics",
            "word problems",
            "data interpretation",
        ],
        "VERBAL": [
            "text completion",
            "sentence equivalence",
            "reading comprehension",
            "vocabulary",
            "argument strength",
            "inference",
        ],
        "AWA": [
            "argument analysis",
            "evidence evaluation",
            "logical flaw",
            "claim support",
        ],
    },
    "GMAT": {
        "QUANT": [
            "percentages",
            "ratios",
            "algebra",
            "number properties",
            "geometry",
            "word problems",
            "data sufficiency",
            "problem solving",
        ],
        "VERBAL": [
            "critical reasoning",
            "reading comprehension",
            "sentence correction",
            "argument evaluation",
        ],
        "DATA INSIGHTS": [
            "data sufficiency",
            "multi-source reasoning",
            "table analysis",
            "graph interpretation",
        ],
    },
    "SAT": {
        "MATH": [
            "linear equations",
            "systems of equations",
            "functions",
            "geometry",
            "trigonometry",
            "statistics",
            "word problems",
            "ratios and proportions",
        ],
        "READING AND WRITING": [
            "command of evidence",
            "main idea",
            "inference",
            "grammar",
            "rhetoric",
            "vocabulary in context",
        ],
    },
    "IELTS": {
        "LISTENING": [
            "form completion",
            "map labeling",
            "multiple choice",
            "matching",
        ],
        "READING": [
            "skimming",
            "scanning",
            "true false not given",
            "matching headings",
        ],
        "WRITING": [
            "task 1 overview",
            "task 1 comparisons",
            "task 2 opinion essay",
            "task 2 discussion essay",
        ],
        "SPEAKING": [
            "part 1 responses",
            "part 2 cue cards",
            "part 3 abstract discussion",
        ],
    },
    "TOEFL": {
        "READING": [
            "detail questions",
            "inference",
            "vocabulary in context",
            "sentence insertion",
        ],
        "LISTENING": [
            "main idea",
            "detail capture",
            "attitude questions",
            "lecture structure",
        ],
        "SPEAKING": [
            "independent task",
            "integrated speaking",
            "clear structure",
        ],
        "WRITING": [
            "integrated writing",
            "academic essay",
            "response structure",
        ],
    },
    "GATE": {
        "CORE SUBJECT": [
            "fundamentals",
            "important formulas",
            "concept applications",
            "standard derivations",
            "previous year patterns",
        ],
        "ENGINEERING MATHEMATICS": [
            "linear algebra",
            "calculus",
            "probability",
            "differential equations",
            "numerical methods",
        ],
        "GENERAL APTITUDE": [
            "verbal ability",
            "quantitative ability",
            "logical reasoning",
            "data interpretation",
        ],
    },
    "GENERAL": {
        "GENERAL": [
            "core concept",
            "worked examples",
            "timed practice",
            "revision recall",
            "error log review",
        ],
    },
}

TEST_FOCUS_TYPES = {"sectional_test", "timed_drill", "mock_review", "full_mock", "revision_quiz"}


def calculate_days_to_exam(exam_date):
    exam = datetime.strptime(exam_date, "%Y-%m-%d")
    today = datetime.today()
    return max(1, (exam - today).days)


def _normalize_topic(value):
    return re.sub(r"\s+", " ", str(value or "").strip()).lower()


def _subject_key(subject):
    return _normalize_topic(subject).upper()


def _dedupe_keep_order(values):
    seen = set()
    result = []
    for value in values:
        normalized = _normalize_topic(value)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(str(value).strip())
    return result


def _safe_load_progress_state(student_name):
    try:
        return load_progress_state(student_name)
    except Exception as exc:
        print(f"WARNING: Planner progress read failed for {student_name} — using safe defaults. {exc}")
        return {"items": [], "history": [], "last_updated": ""}


def _safe_get_syllabus_documents(student_name):
    try:
        return get_syllabus_documents(student_name)
    except Exception as exc:
        print(f"WARNING: Planner syllabus read failed for {student_name} — using safe defaults. {exc}")
        return []


def _topic_library_for(exam_name, subject):
    exam_key = _canonical_jee_exam_name(exam_name)
    subject_key = _subject_key(subject)
    exam_topics = TOPIC_LIBRARY.get(exam_key, {})
    subject_topics = exam_topics.get(subject_key, [])
    if subject_topics:
        return list(subject_topics)

    fallback = TOPIC_LIBRARY.get("GENERAL", {}).get("GENERAL", [])
    return list(fallback)


def _topic_candidates_from_progress(profile, exam_name, subject):
    state = _safe_load_progress_state(profile["name"])
    candidates = []
    for item in state.get("items", []):
        item_exam = _canonical_jee_exam_name(item.get("exam", ""))
        item_subject = _subject_key(item.get("subject", ""))
        if item_exam and item_exam != _canonical_jee_exam_name(exam_name):
            continue
        if item_subject and item_subject != _subject_key(subject):
            continue
        topic = str(item.get("topic", "")).strip()
        if topic:
            candidates.append(topic)
    return _dedupe_keep_order(candidates)


def _topic_candidates_from_syllabus(student_name):
    candidates = []
    for document in _safe_get_syllabus_documents(student_name):
        summary = str(document.get("topic_summary", "")).strip()
        if not summary:
            continue
        chunks = re.split(r"[;\n,]", summary)
        for chunk in chunks:
            topic = str(chunk).strip()
            if len(topic) < 4:
                continue
            candidates.append(topic)
    return _dedupe_keep_order(candidates)


def _topic_pool_for_subject(profile, state, exam_name, subject):
    pool = []
    pool.extend(_topic_library_for(exam_name, subject))
    pool.extend(_topic_candidates_from_progress(profile, exam_name, subject))
    pool.extend(_topic_candidates_from_syllabus(profile["name"]))
    return _dedupe_keep_order(pool)


def _topic_status_priority(status):
    status_key = _normalize_topic(status)
    if status_key == "pending":
        return 24
    if status_key == "revise":
        return 30
    if status_key == "done":
        return 10
    return 18


def _topic_progress_status(profile, exam_name, subject, topic):
    state = _safe_load_progress_state(profile["name"])
    topic_key = _normalize_topic(topic)
    status_rank = 0
    latest_status = ""
    for item in state.get("items", []):
        if _canonical_jee_exam_name(item.get("exam", "")) not in {"", _canonical_jee_exam_name(exam_name)}:
            continue
        if _subject_key(item.get("subject", "")) not in {"", _subject_key(subject)}:
            continue
        if _normalize_topic(item.get("topic", "")) != topic_key:
            continue
        status = str(item.get("status", "")).strip().lower()
        rank = {"pending": 3, "revise": 2, "done": 1}.get(status, 0)
        if rank >= status_rank:
            status_rank = rank
            latest_status = status
    return latest_status or "fresh"


def _subject_topic_frame(profile, state, exam_name, subject, day_index=0):
    pool = _topic_pool_for_subject(profile, state, exam_name, subject)
    if not pool:
        pool = ["core concept"]

    anchor = 0
    progress_statuses = [_topic_progress_status(profile, exam_name, subject, topic) for topic in pool]
    if any(status in {"pending", "revise"} for status in progress_statuses):
        for index, status in enumerate(progress_statuses):
            if status in {"pending", "revise"}:
                anchor = index
                break

    primary = pool[(anchor + day_index) % len(pool)]
    revision = pool[(anchor + day_index - 2) % len(pool)] if len(pool) > 1 else primary
    return {
        "topic": primary,
        "revision_topic": revision,
        "topic_pool": pool[:6],
        "topic_status": _topic_progress_status(profile, exam_name, subject, primary),
    }


def _planner_state_path(name):
    if not os.path.exists(PLANNER_STATE_FOLDER):
        os.makedirs(PLANNER_STATE_FOLDER)
    return os.path.join(PLANNER_STATE_FOLDER, f"{name}.json")


def _planner_timestamp():
    return datetime.utcnow().isoformat(timespec="seconds")


def _default_planner_state():
    return {
        "mock_scores": {},
        "backlog_hours": {},
        "current_day_plan": None,
        "history": [],
        "section_progress": {},
    }


def _normalize_planner_state(state):
    state.setdefault("mock_scores", {})
    state.setdefault("backlog_hours", {})
    state.setdefault("current_day_plan", None)
    state.setdefault("history", [])
    state.setdefault("section_progress", {})
    return state


def _load_planner_from_db(name):
    try:
        db_state = db_get_planner_state(name) or {}
        state = db_state.get("journey") or db_state.get("weekly") or db_state.get("today") or {}
        if not state:
            return None
        return _normalize_planner_state(state)
    except Exception as exc:
        print(f"WARNING: Could not load planner state from database for {name}: {exc}")
        return None


def _save_planner_to_db(name, state):
    try:
        db_save_planner_state(name, state, state.get("weekly", {}), state.get("today", {}))
    except Exception as exc:
        print(f"WARNING: Could not save planner state to database for {name}: {exc}")


def _task_key(exam_name, subject):
    return f"{exam_name}::{subject}"


def _task_label(exam_name, subject):
    return f"{exam_name} - {subject}"


def _normalize_profile(profile):
    normalized = dict(profile)

    if "exams" not in normalized:
        exam_name = normalized.get("exam", "")
        exam_date = normalized.get("exam_date", "")
        canonical_exam_name = _canonical_jee_exam_name(exam_name)
        subjects = normalized.get("subjects") or DEFAULT_EXAM_SUBJECTS.get(canonical_exam_name, [])
        normalized["exams"] = [
            {
                "name": canonical_exam_name,
                "exam_date": exam_date,
                "subjects": subjects,
            }
        ]

    if "max_study_hours_per_day" not in normalized:
        normalized["max_study_hours_per_day"] = normalized.get("study_hours_per_day", 6)

    normalized["preferred_persona"] = normalized.get("preferred_persona", "")
    return normalized


def get_exam_entries(profile):
    normalized = _normalize_profile(profile)
    exams = []

    for exam in normalized.get("exams", []):
        exam_name = _canonical_jee_exam_name(exam["name"])
        if exam_name not in JEE_EXAM_KEYS:
            continue
        default_subjects = DEFAULT_EXAM_SUBJECTS.get(exam_name, [])
        subjects = exam.get("subjects") or default_subjects
        exams.append(
            {
                "name": exam_name,
                "exam_date": exam["exam_date"],
                "subjects": subjects,
            }
        )

    return exams


def is_jee_profile(profile):
    exam_names = {exam["name"] for exam in get_exam_entries(profile)}
    return any(name in JEE_EXAM_KEYS for name in exam_names)


def get_jee_track_mode(profile):
    exam_names = {exam["name"] for exam in get_exam_entries(profile)}
    has_main = "JEE MAIN" in exam_names or "JEE" in exam_names
    has_advanced = "JEE ADVANCED" in exam_names

    if has_main and has_advanced:
        return "dual_track"
    if has_advanced and not has_main:
        return "advanced_only"
    if has_main:
        return "mains_priority"
    return "not_jee"


def has_exam_entries(profile):
    return bool(get_exam_entries(profile))


def get_max_study_hours(profile):
    normalized = _normalize_profile(profile)
    return float(normalized.get("max_study_hours_per_day", 6))


def get_adaptive_learning_profile(profile):
    state = load_planner_state(profile["name"])
    exams = get_exam_entries(profile)
    mock_values = []
    for exam in exams:
        for subject in exam["subjects"]:
            score = _get_mock_score(state, exam["name"], subject)
            if score is not None:
                mock_values.append(float(score))

    average_score = round(sum(mock_values) / len(mock_values), 2) if mock_values else 50.0
    history = state.get("history", [])
    completed = sum(1 for item in history if item.get("status") == "completed")
    considered = sum(1 for item in history if item.get("status") in {"completed", "missed", "rolled_over"})
    adherence_ratio = round(completed / considered, 2) if considered else 0.5

    behavior = get_behavior_snapshot(profile)
    pacing_style = behavior.get("pacing_style", "steady")
    support_style = behavior.get("support_style", "balanced_support")

    if average_score >= 80 and adherence_ratio >= 0.75:
        question_difficulty = "stretch"
        concept_depth = "advanced"
    elif average_score >= 65:
        question_difficulty = "challenging"
        concept_depth = "building"
    elif average_score >= 45:
        question_difficulty = "moderate"
        concept_depth = "foundation_plus"
    else:
        question_difficulty = "guided"
        concept_depth = "foundation"

    teaching_speed = "steady"
    if pacing_style in {"slow", "step_by_step"} or support_style in {"gentle_recovery", "reassuring_stepwise"}:
        teaching_speed = "slow"
    elif pacing_style == "stretch" and adherence_ratio >= 0.7:
        teaching_speed = "fast"

    percentile_band = "not_enough_data"
    if average_score >= 85:
        percentile_band = "top_band_readiness"
    elif average_score >= 70:
        percentile_band = "strong_readiness"
    elif average_score >= 55:
        percentile_band = "improving_readiness"
    else:
        percentile_band = "rebuild_readiness"

    return {
        "average_mock_score": average_score,
        "adherence_ratio": adherence_ratio,
        "question_difficulty": question_difficulty,
        "concept_depth": concept_depth,
        "teaching_speed": teaching_speed,
        "support_style": support_style,
        "pacing_style": pacing_style,
        "percentile_band": percentile_band,
    }


def _get_task_learning_bias(profile, insight_snapshot=None):
    task_profiles = get_task_learning_profiles(profile["name"])
    practice_profile = task_profiles.get("practice", {})
    tutor_profile = task_profiles.get("tutor", {})
    last_minute_profile = task_profiles.get("last_minute", {})
    tips_profile = task_profiles.get("tips", {})
    lounge_profile = task_profiles.get("lounge", {})

    practice_accuracy = float(practice_profile.get("recent_accuracy", 0) or 0)
    tutor_confused = int(tutor_profile.get("confused", 0) or 0)
    tutor_understood = int(tutor_profile.get("understood", 0) or 0)
    practice_trend = str(practice_profile.get("trend_signal", "building")).strip().lower()
    practice_speed = str(practice_profile.get("speed_signal", "steady")).strip().lower()
    tutor_trend = str(tutor_profile.get("trend_signal", "building")).strip().lower()
    insight_trend = str((insight_snapshot or {}).get("trend_signal", "building")).strip().lower()

    practice_priority = "balanced"
    if practice_accuracy < 55 or practice_trend == "dipping":
        practice_priority = "high"
    elif practice_accuracy >= 75 and practice_trend == "improving":
        practice_priority = "growth"

    tutor_support = "balanced"
    if tutor_confused > tutor_understood or tutor_trend == "dipping":
        tutor_support = "high"
    elif tutor_understood > 0 and tutor_trend in {"steady", "improving"}:
        tutor_support = "light"

    revision_priority = "standard"
    if practice_priority == "high" or tutor_support == "high":
        revision_priority = "tight"
    if last_minute_profile.get("interactions", 0) >= 3 and last_minute_profile.get("trend_signal") == "improving":
        revision_priority = "tight"
    if tips_profile.get("interactions", 0) >= 3 and tips_profile.get("trend_signal") == "improving":
        revision_priority = "strategy"
    if lounge_profile.get("negative_shifts", 0) > lounge_profile.get("positive_shifts", 0):
        revision_priority = "gentle"

    weekly_test_blocks = 4
    if practice_priority == "high":
        weekly_test_blocks = 5
    elif practice_priority == "growth" and insight_trend != "dipping":
        weekly_test_blocks = 4

    summary = []
    if practice_profile:
        if practice_priority == "high":
            summary.append(
                "Practice mode is still shaky, so the plan leans on shorter corrective drills, earlier revision, and one extra test touch."
            )
        elif practice_priority == "growth":
            summary.append(
                "Practice mode is improving, so the plan can introduce slightly tougher work without losing structure."
            )
        else:
            summary.append(
                "Practice mode is stable enough to keep a balanced mix of timed work, correction, and recall."
            )
    if tutor_profile:
        if tutor_support == "high":
            summary.append(
                "Tutor mode is showing more confusion than clarity, so concept rebuilds should stay smaller and more guided."
            )
        elif tutor_support == "light":
            summary.append(
                "Tutor mode is responding well, so Astra can stretch explanations a little while still keeping them neat."
            )
    if tips_profile:
        summary.append(
            "Tips mode can stay available as a short exam-strategy checkpoint when the weekly plan needs quick decision rules."
        )
    if last_minute_profile:
        summary.append(
            "Last-minute mode should remain a small rescue layer, not the main weekly rhythm."
        )
    if lounge_profile:
        summary.append(
            "Lounge mode is kept separate so the student can reset emotionally without disturbing the academic plan."
        )

    if not summary:
        summary.append("Use a balanced weekly mix of concept learning, practice, revision, and mock review.")

    return {
        "task_profiles": task_profiles,
        "practice_priority": practice_priority,
        "tutor_support": tutor_support,
        "revision_priority": revision_priority,
        "weekly_test_blocks": weekly_test_blocks,
        "summary": summary,
        "practice_accuracy": practice_accuracy,
        "practice_trend": practice_trend,
        "practice_speed": practice_speed,
    }


def load_planner_state(name):
    try:
        state = _load_planner_from_db(name)
        if state is not None:
            return state

        filepath = _planner_state_path(name)

        if not os.path.exists(filepath):
            return _default_planner_state()

        with open(filepath, "r", encoding="utf-8") as file:
            state = json.load(file)

        state = _normalize_planner_state(state)
        _save_planner_to_db(name, state)
        return state
    except Exception as exc:
        print(f"WARNING: Could not load planner state for {name} — using safe defaults. {exc}")
        return _default_planner_state()


def save_planner_state(name, state):
    try:
        filepath = _planner_state_path(name)
        state = _normalize_planner_state(state)
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(state, file, indent=2)
        _save_planner_to_db(name, state)
    except Exception as exc:
        print(f"WARNING: Could not save planner state for {name} — keeping safe defaults. {exc}")


def _get_mock_score(state, exam_name, subject):
    mock_scores = state.get("mock_scores", {})

    exam_scores = mock_scores.get(exam_name)
    if isinstance(exam_scores, dict):
        return exam_scores.get(subject)

    legacy_score = mock_scores.get(subject)
    if legacy_score is not None:
        return legacy_score

    return None


def _get_backlog_hours(state, exam_name, subject):
    backlog_hours = state.get("backlog_hours", {})
    return float(
        backlog_hours.get(_task_key(exam_name, subject), backlog_hours.get(subject, 0))
    )


def get_missing_mock_subjects(profile, state):
    missing = []

    for exam in get_exam_entries(profile):
        for subject in exam["subjects"]:
            if _get_mock_score(state, exam["name"], subject) is None:
                missing.append({"exam": exam["name"], "subject": subject})

    return missing


def save_mock_scores(profile, scores):
    state = load_planner_state(profile["name"])
    state.setdefault("mock_scores", {})

    for exam_name, exam_scores in scores.items():
        state["mock_scores"].setdefault(exam_name, {})
        for subject, score in exam_scores.items():
            state["mock_scores"][exam_name][subject] = score

    state.setdefault("backlog_hours", {})
    state.setdefault("history", [])
    state.setdefault("section_progress", {})
    save_planner_state(profile["name"], state)
    return state


def _section_progress_entry(state, exam_name, subject):
    section_progress = state.setdefault("section_progress", {})
    key = _task_key(exam_name, subject)
    section_progress.setdefault(
        key,
        {
            "completed_hours": 0.0,
            "completed_sessions": 0,
            "last_completed_on": "",
        },
    )
    return section_progress[key]


def get_section_progress(profile):
    try:
        state = load_planner_state(profile["name"])
        progress_cards = []

        for exam in get_exam_entries(profile):
            for subject in exam["subjects"]:
                progress = _section_progress_entry(state, exam["name"], subject)
                mock_score = _get_mock_score(state, exam["name"], subject)
                backlog = round(_get_backlog_hours(state, exam["name"], subject), 2)
                strengths = []
                weaknesses = []

                if mock_score is not None and float(mock_score) >= 75:
                    strengths.append("strong mock performance")
                if progress["completed_sessions"] >= 3:
                    strengths.append("consistent revision rhythm")
                if backlog <= 0.5:
                    strengths.append("low carry-forward backlog")

                if mock_score is not None and float(mock_score) < 60:
                    weaknesses.append("accuracy needs improvement")
                if backlog > 1.5:
                    weaknesses.append("time is getting lost here")
                if progress["completed_sessions"] <= 1:
                    weaknesses.append("needs more repeated exposure")

                progress_cards.append(
                    {
                        "exam": exam["name"],
                        "subject": subject,
                        "completed_hours": round(progress["completed_hours"], 2),
                        "completed_sessions": progress["completed_sessions"],
                        "mock_score": mock_score,
                        "backlog_hours": backlog,
                        "last_completed_on": progress["last_completed_on"],
                        "strengths": strengths or ["still building this section"],
                        "weaknesses": weaknesses or ["no major red flags right now"],
                        "summary": (
                            f"{subject} in {exam['name']}: "
                            f"{round(progress['completed_hours'], 2)} hours completed across "
                            f"{progress['completed_sessions']} sessions. "
                            f"Current focus should stay on {weaknesses[0] if weaknesses else 'steady strengthening and timed execution'}."
                        ),
                    }
                )

        return progress_cards
    except Exception as exc:
        print(f"WARNING: Could not build section progress for {profile.get('name', 'student')} — returning safe defaults. {exc}")
        return []


def _exam_pressure(days_left):
    return min(3.0, 180.0 / max(days_left, 1))


def _get_task_weights(profile, state):
    task_weights = {}

    for exam in get_exam_entries(profile):
        days_left = calculate_days_to_exam(exam["exam_date"])
        pressure = _exam_pressure(days_left)

        for subject in exam["subjects"]:
            score = float(_get_mock_score(state, exam["name"], subject) or 50)
            weakness = max(5.0, 100.0 - score)
            task_weights[_task_key(exam["name"], subject)] = pressure * weakness

    total_weight = sum(task_weights.values()) or 1.0
    return {
        task_key: weight / total_weight for task_key, weight in task_weights.items()
    }


def _recommended_daily_hours(profile, state):
    max_hours = get_max_study_hours(profile)
    exams = get_exam_entries(profile)

    pressure_total = sum(_exam_pressure(calculate_days_to_exam(exam["exam_date"])) for exam in exams)
    weakness_scores = []

    for exam in exams:
        for subject in exam["subjects"]:
            score = float(_get_mock_score(state, exam["name"], subject) or 50)
            weakness_scores.append((100.0 - score) / 100.0)

    average_weakness = sum(weakness_scores) / len(weakness_scores) if weakness_scores else 0.5
    target_hours = 2.0 + pressure_total + (2.5 * average_weakness)

    behavior = get_behavior_snapshot(profile)
    insight_snapshot = get_student_insight_snapshot(profile)
    route = build_student_state_route(
        profile,
        conversation_mode="tutor",
        tutor_level=profile.get("default_tutor_level", 3) or 3,
        support_style=behavior.get("support_style"),
        insight_snapshot=insight_snapshot,
    )
    support_style = behavior.get("support_style", "balanced_support")
    pacing_style = behavior.get("pacing_style", "steady")

    if support_style == "gentle_recovery":
        target_hours *= 0.75
    elif support_style == "reassuring_stepwise":
        target_hours *= 0.85
    elif support_style == "simplified_structured":
        target_hours *= 0.9
    elif support_style == "challenging_coach":
        target_hours *= 1.08
    elif support_style == "accountability_focused":
        target_hours *= 0.95

    if pacing_style == "slow":
        target_hours *= 0.9
    elif pacing_style == "step_by_step":
        target_hours *= 0.95
    elif pacing_style == "stretch":
        target_hours *= 1.08

    route_pressure = route.get("pressure", "medium")
    route_focus = route.get("focus", "")
    trend_signal = str(insight_snapshot.get("trend_signal", "building")).strip().lower()
    focus_recommendation = str(insight_snapshot.get("focus_recommendation", "")).strip()
    if route_pressure == "low":
        target_hours *= 0.88
    elif route_pressure == "low-medium":
        target_hours *= 0.94
    elif route_pressure == "medium-high":
        target_hours *= 1.04
    if "recovery" in route_focus or "one-step" in route_focus:
        target_hours *= 0.9
    elif "stretch" in route_focus or "deeper learning" in route_focus:
        target_hours *= 1.05
    if trend_signal == "improving":
        target_hours *= 1.05
    elif trend_signal == "dipping":
        target_hours *= 0.92
    elif trend_signal == "steady" and "balanced" in route_focus:
        target_hours *= 1.0

    if focus_recommendation and trend_signal == "dipping":
        target_hours *= 0.98

    return round(min(max_hours, max(1.5, target_hours)), 2)


def _normalize_task_hours(tasks, target_total):
    total = round(sum(tasks.values()), 2)
    if not tasks or total == 0:
        return tasks

    scale = target_total / total
    normalized = {key: round(hours * scale, 2) for key, hours in tasks.items()}
    drift = round(target_total - sum(normalized.values()), 2)

    if drift != 0:
        first_key = next(iter(normalized))
        normalized[first_key] = round(normalized[first_key] + drift, 2)

    return normalized


def _weekly_day_templates(is_jee=False, jee_track_mode="not_jee", planner_bias=None):
    planner_bias = planner_bias or {}
    practice_priority = planner_bias.get("practice_priority", "balanced")
    tutor_support = planner_bias.get("tutor_support", "balanced")
    revision_priority = planner_bias.get("revision_priority", "standard")

    def _tune(template):
        tuned = dict(template)
        if practice_priority == "high":
            if tuned["focus"] == "timed_drill":
                tuned["focus"] = "guided_practice"
                tuned["strategy"] = (
                    tuned["strategy"]
                    + " Keep the set short, correct mistakes immediately, and repeat the missed pattern once before moving on."
                )
            elif tuned["focus"] == "sectional_test":
                tuned["strategy"] = (
                    tuned["strategy"]
                    + " Follow the test with direct correction notes so the same errors do not repeat later in the week."
                )
            elif tuned["focus"] == "revision_quiz":
                tuned["strategy"] = (
                    "Use the final day for lighter recall plus one focused practice check so revision stays active instead of becoming passive reading."
                )
        elif practice_priority == "growth":
            if tuned["focus"] in {"timed_drill", "mock_review"}:
                tuned["strategy"] = (
                    tuned["strategy"]
                    + " Add a slightly tougher question mix so the student keeps stretching without losing structure."
                )

        if tutor_support == "high" and tuned["focus"] in {"concept_rebuild", "guided_practice", "targeted_revision"}:
            tuned["strategy"] = (
                tuned["strategy"]
                + " Break each idea into smaller steps, check understanding early, and keep the pacing intentionally gentle."
            )
        elif tutor_support == "light" and tuned["focus"] in {"concept_rebuild", "guided_practice"}:
            tuned["strategy"] = (
                tuned["strategy"]
                + " Keep the explanation neat and slightly more challenging now that the student is handling the basics better."
            )

        if revision_priority == "tight" and tuned["focus"] in {"mock_review", "targeted_revision", "sectional_test"}:
            tuned["strategy"] = (
                tuned["strategy"]
                + " Make the correction log explicit so revision topics are revisited again within the same week."
            )
        elif revision_priority == "strategy" and tuned["focus"] in {"mock_review", "light_revision", "revision_quiz"}:
            tuned["strategy"] = (
                tuned["strategy"]
                + " Include one short strategy note so exam decision-making stays visible."
            )
        elif revision_priority == "gentle" and tuned["focus"] in {"light_revision", "revision_quiz"}:
            tuned["strategy"] = (
                tuned["strategy"]
                + " Keep this block light, calm, and confidence-preserving."
            )
        return tuned

    if is_jee:
        templates = [
            {
                "label": "Day 1",
                "theme": "Physics Main Core + Advanced Touch",
                "strategy": (
                    "Begin with JEE Main Physics scoring concepts and clean numericals, then close with one deeper Advanced-style layer "
                    "so Main stays the priority without losing contact with depth."
                ),
                "multiplier": 1.0,
                "focus": "concept_rebuild",
                "preferred_subjects": ["Physics"],
            },
            {
                "label": "Day 2",
                "theme": "Chemistry Main Recall + Advanced Link",
                "strategy": (
                    "Use Chemistry to secure the direct JEE Main marks first, then add a short timed practice set that keeps the concepts active "
                    "while still bridging into mechanism, linkage, or multi-concept thinking."
                ),
                "multiplier": 0.95,
                "focus": "timed_drill",
                "preferred_subjects": ["Chemistry"],
            },
            {
                "label": "Day 3",
                "theme": "Mathematics Main Speed + Advanced Depth",
                "strategy": (
                    "Push Mathematics with Main-level speed and structure first, then finish with one tougher Advanced-style problem set "
                    "to keep depth alive without diluting the scoring foundation."
                ),
                "multiplier": 1.0,
                "focus": "timed_drill",
                "preferred_subjects": ["Mathematics", "Math"],
            },
            {
                "label": "Day 4",
                "theme": "Mains Weak-Spot Repair",
                "strategy": (
                    "Return to the PCM areas where JEE Main errors, silly mistakes, or backlog are still accumulating, because Main accuracy "
                    "has to become dependable before the Advanced push becomes heavier."
                ),
                "multiplier": 1.0,
                "focus": "targeted_revision",
                "preferred_subjects": [],
            },
            {
                "label": "Day 5",
                "theme": "Advanced Depth Window",
                "strategy": (
                    "Use one dedicated window for deeper multi-concept JEE Advanced thinking through a timed mixed set so the student stays in "
                    "touch with higher-level reasoning while the rest of the week protects JEE Main momentum."
                ),
                "multiplier": 1.05,
                "focus": "timed_drill",
                "preferred_subjects": ["Physics", "Chemistry", "Mathematics", "Math"],
            },
            {
                "label": "Day 6",
                "theme": "JEE Main Mock And Error Review",
                "strategy": (
                    "Use a JEE Main-like test block plus serious error-log review, because the first milestone is to make Main performance stable, "
                    "fast, and clean."
                ),
                "multiplier": 1.15,
                "focus": "mock_review",
                "preferred_subjects": [],
            },
            {
                "label": "Day 7",
                "theme": "Formula Reset + Advanced Recall",
                "strategy": (
                    "Close the week with formulas, reaction chains, short notes, and one small Advanced recall block so the next week starts clean "
                    "without losing touch with tougher material."
                ),
                "multiplier": 0.85,
                "focus": "light_revision",
                "preferred_subjects": [],
            },
        ]

        return [_tune(template) for template in templates]

    templates = [
        {
            "label": "Day 1",
            "theme": "Weakest Concepts",
            "strategy": "Start the week by attacking the weakest and most urgent concepts while your attention is fresh.",
            "multiplier": 1.0,
            "focus": "concept_rebuild",
            "preferred_subjects": [],
        },
        {
            "label": "Day 2",
            "theme": "Practice And Timed Recall",
            "strategy": "Convert yesterday's concepts into solved questions under time so the ideas stop feeling abstract.",
            "multiplier": 1.0,
            "focus": "timed_drill",
            "preferred_subjects": [],
        },
        {
            "label": "Day 3",
            "theme": "Timed Sectional Test",
            "strategy": "Run a timed sectional test so the student stays in contact with the concepts under pressure.",
            "multiplier": 0.95,
            "focus": "sectional_test",
            "preferred_subjects": [],
        },
        {
            "label": "Day 4",
            "theme": "Second Pass Strengthening",
            "strategy": "Revisit the sections that still feel shaky before they become silent weak spots.",
            "multiplier": 1.0,
            "focus": "targeted_revision",
            "preferred_subjects": [],
        },
        {
            "label": "Day 5",
            "theme": "Mixed Rotation And Timed Drill",
            "strategy": "Rotate across exams or subjects and include a short timed set so earlier topics do not fade out.",
            "multiplier": 1.05,
            "focus": "timed_drill",
            "preferred_subjects": [],
        },
        {
            "label": "Day 6",
            "theme": "Mock And Review",
            "strategy": "Use a test-like block plus error review, because practice under pressure reveals real gaps.",
            "multiplier": 1.1,
            "focus": "mock_review",
            "preferred_subjects": [],
        },
        {
            "label": "Day 7",
            "theme": "Revision Quiz And Recovery",
            "strategy": "Keep the final day lighter with a short revision quiz so the week ends with recall, not just reading.",
            "multiplier": 0.8,
            "focus": "revision_quiz",
            "preferred_subjects": [],
        },
    ]

    return [_tune(template) for template in templates]


def _task_pressure_rows(profile, state):
    rows = []
    for exam in get_exam_entries(profile):
        days_left = calculate_days_to_exam(exam["exam_date"])
        pressure = _exam_pressure(days_left)
        for subject in exam["subjects"]:
            score = float(_get_mock_score(state, exam["name"], subject) or 50)
            backlog = float(_get_backlog_hours(state, exam["name"], subject))
            weakness = max(5.0, 100.0 - score)
            rows.append(
                {
                    "key": _task_key(exam["name"], subject),
                    "exam": exam["name"],
                    "subject": subject,
                    "days_left": days_left,
                    "mock_score": score,
                    "backlog_hours": round(backlog, 2),
                    "priority_score": round((pressure * weakness) + (backlog * 8), 2),
                }
            )
    rows.sort(key=lambda item: (-item["priority_score"], item["days_left"], item["subject"]))
    return rows


def _status_from_score(score):
    if score >= 75:
        return "strength"
    if score >= 60:
        return "stable"
    return "needs_work"


def _focus_rows_for_day(task_rows, template, day_index=0, review_anchor=None):
    if not task_rows:
        return []

    preferred_subjects = {subject.lower() for subject in template.get("preferred_subjects", [])}
    if preferred_subjects:
        preferred_rows = [row for row in task_rows if row["subject"].lower() in preferred_subjects]
        other_rows = [row for row in task_rows if row["subject"].lower() not in preferred_subjects]
        ordered_pool = preferred_rows + other_rows
    else:
        ordered_pool = task_rows

    needs_work = [row for row in ordered_pool if _status_from_score(row["mock_score"]) == "needs_work"]
    stable = [row for row in ordered_pool if _status_from_score(row["mock_score"]) == "stable"]
    strengths = [row for row in ordered_pool if _status_from_score(row["mock_score"]) == "strength"]

    focus_type = template["focus"]
    rotation = (day_index * 2) % len(ordered_pool) if ordered_pool else 0

    if focus_type == "concept_rebuild":
        ordered = needs_work + stable + strengths
    elif focus_type == "guided_practice":
        ordered = needs_work[:2] + stable + strengths + needs_work[2:]
    elif focus_type in {"timed_drill", "sectional_test"}:
        ordered = stable + needs_work + strengths
    elif focus_type == "targeted_revision":
        ordered = needs_work[1:] + needs_work[:1] + stable + strengths
    elif focus_type == "mixed_rotation":
        ordered = stable + strengths + needs_work
    elif focus_type == "advanced_bridge":
        ordered = strengths + stable + needs_work
    elif focus_type in {"mock_review", "revision_quiz", "full_mock"}:
        ordered = stable + needs_work + strengths
    else:
        ordered = needs_work + stable + strengths

    selected = []
    seen_exams = set()
    seen_signatures = set()
    if ordered:
        rotation = day_index % len(ordered)
        ordered = ordered[rotation:] + ordered[:rotation]
    if review_anchor:
        selected.append(review_anchor)
        seen_exams.add(review_anchor["exam"])
        seen_signatures.add(
            f"{review_anchor['exam']}::{review_anchor['subject']}::{review_anchor.get('topic', review_anchor['subject'])}"
        )
    for row in ordered:
        row_key = f"{row['exam']}::{row['subject']}::{row.get('topic', row['subject'])}"
        if row_key in seen_signatures:
            continue
        exam_key = row["exam"]
        if len(selected) < 2 and exam_key in seen_exams and len(seen_exams) < 2:
            continue
        selected.append(row)
        seen_exams.add(exam_key)
        seen_signatures.add(row_key)
        if len(selected) >= 3:
            break

    return selected or task_rows[:3]


def _build_weekly_day_rows(profile, state, today_plan, planner_bias=None):
    templates = _weekly_day_templates(
        is_jee=is_jee_profile(profile),
        jee_track_mode=get_jee_track_mode(profile),
        planner_bias=planner_bias,
    )
    base_total = float(today_plan.get("scheduled_hours", today_plan.get("recommended_hours", 0.0)) or 0.0)
    if base_total <= 0:
        return []

    insight_snapshot = get_student_insight_snapshot(profile)
    route = build_student_state_route(
        profile,
        conversation_mode="tutor",
        tutor_level=profile.get("default_tutor_level", 3) or 3,
        support_style=get_behavior_snapshot(profile).get("support_style"),
        insight_snapshot=insight_snapshot,
    )
    route_pressure = route.get("pressure", "medium")
    route_focus = str(route.get("focus", "")).lower()

    raw_day_totals = [base_total * template["multiplier"] for template in templates]
    if route_pressure in {"low", "low-medium"}:
        raw_day_totals = [value * 0.95 for value in raw_day_totals]
    elif route_pressure == "medium-high":
        raw_day_totals = [value * 1.03 for value in raw_day_totals]
    if "recovery" in route_focus:
        raw_day_totals = [value * 0.92 for value in raw_day_totals]
    total_raw = sum(raw_day_totals) or 1.0
    target_week_total = round(base_total * 7, 2)
    normalized_day_totals = [round((value / total_raw) * target_week_total, 2) for value in raw_day_totals]
    drift = round(target_week_total - sum(normalized_day_totals), 2)
    if normalized_day_totals:
        normalized_day_totals[0] = round(normalized_day_totals[0] + drift, 2)

    task_rows = _task_pressure_rows(profile, state)
    days = []
    start_date = datetime.today().date()
    review_anchors = []
    for index, template in enumerate(templates):
        review_anchor = review_anchors[index - 2] if index >= 2 and index - 2 < len(review_anchors) else None
        focus_rows = _focus_rows_for_day(task_rows, template, day_index=index, review_anchor=review_anchor)
        total_hours = normalized_day_totals[index]
        if not focus_rows:
            allocations = []
        else:
            for row_index, row in enumerate(focus_rows):
                topic_frame = _subject_topic_frame(profile, state, row["exam"], row["subject"], day_index=index + row_index)
                row["topic"] = topic_frame["topic"]
                row["revision_topic"] = topic_frame["revision_topic"]
                row["topic_pool"] = topic_frame["topic_pool"]
                row["topic_status"] = topic_frame["topic_status"]
                if row_index == 0 and review_anchor:
                    row["session_type"] = "revision recall"
            review_anchors.append(dict(focus_rows[0]) if focus_rows else None)
            focus_weight_total = sum(max(item["priority_score"], 1.0) for item in focus_rows) or 1.0
            allocations = []
            for row in focus_rows:
                allocation = round(total_hours * (max(row["priority_score"], 1.0) / focus_weight_total), 2)
                allocations.append({**row, "hours": allocation})
            allocation_drift = round(total_hours - sum(item["hours"] for item in allocations), 2)
            if allocations:
                allocations[0]["hours"] = round(allocations[0]["hours"] + allocation_drift, 2)

        for item in allocations:
            if template["focus"] in {"timed_drill", "sectional_test", "mock_review", "full_mock"}:
                item["session_type"] = "timed practice"
            elif template["focus"] in {"targeted_revision", "light_revision", "revision_quiz"}:
                item["session_type"] = "revision"
            elif template["focus"] == "guided_practice":
                item["session_type"] = "worked questions"
            elif template["focus"] == "advanced_bridge":
                item["session_type"] = "advanced bridge"
            else:
                item["session_type"] = "concept learning"

        main_focus = ", ".join(f"{item['exam']} {item['subject']}" for item in allocations[:2]) if allocations else "No focus set"
        days.append(
            {
                "date": (start_date + timedelta(days=index)).isoformat(),
                "label": template["label"],
                "theme": template["theme"],
                "strategy": template["strategy"],
                "total_hours": round(total_hours, 2),
                "main_focus": main_focus,
                "tasks": [
                    {
                        "exam": item["exam"],
                        "subject": item["subject"],
                        "hours": item["hours"],
                        "session_type": item["session_type"],
                        "mock_score": item["mock_score"],
                        "backlog_hours": item["backlog_hours"],
                    }
                    for item in allocations
                ],
            }
        )
    return days


def _roll_over_unfinished_work(state, today_str):
    current_day_plan = state.get("current_day_plan")
    if not current_day_plan:
        return state

    plan_date = current_day_plan.get("date")
    status = current_day_plan.get("status", "pending")

    if plan_date == today_str or status == "completed":
        return state

    backlog_hours = state.setdefault("backlog_hours", {})
    for task in current_day_plan.get("tasks", []):
        key = _task_key(task["exam"], task["subject"])
        backlog_hours[key] = round(backlog_hours.get(key, 0) + task["hours"], 2)

    state.setdefault("history", []).append(
        {
            "date": plan_date,
            "status": "rolled_over",
            "tasks": current_day_plan.get("tasks", []),
        }
    )
    state["current_day_plan"] = None
    return state


def _build_daily_tasks(profile, state):
    if not has_exam_entries(profile):
        return [], 0.0

    weights = _get_task_weights(profile, state)
    target_hours = _recommended_daily_hours(profile, state)
    backlog_hours = state.setdefault("backlog_hours", {})
    tasks = {}
    behavior = get_behavior_snapshot(profile)
    insight_snapshot = get_student_insight_snapshot(profile)
    route = build_student_state_route(
        profile,
        conversation_mode="tutor",
        tutor_level=profile.get("default_tutor_level", 3) or 3,
        support_style=behavior.get("support_style"),
        insight_snapshot=insight_snapshot,
    )
    route_pressure = route.get("pressure", "medium")
    route_focus = str(route.get("focus", "")).lower()
    trend_signal = str(insight_snapshot.get("trend_signal", "building")).strip().lower()

    backlog_total = sum(float(value) for value in backlog_hours.values())
    rollover_capacity = min(backlog_total, round(target_hours * 0.35, 2))
    if behavior.get("support_style") == "gentle_recovery":
        rollover_capacity = min(backlog_total, round(target_hours * 0.15, 2))
    elif behavior.get("support_style") == "reassuring_stepwise":
        rollover_capacity = min(backlog_total, round(target_hours * 0.2, 2))
    elif behavior.get("support_style") == "accountability_focused":
        rollover_capacity = min(backlog_total, round(target_hours * 0.4, 2))
    elif behavior.get("support_style") == "challenging_coach":
        rollover_capacity = min(backlog_total, round(target_hours * 0.45, 2))

    if route_pressure in {"low", "low-medium"}:
        rollover_capacity = min(backlog_total, round(target_hours * 0.2, 2))
    elif route_pressure == "medium-high":
        rollover_capacity = min(backlog_total, round(target_hours * 0.42, 2))
    if "recovery" in route_focus or "one-step" in route_focus:
        rollover_capacity = min(backlog_total, round(target_hours * 0.18, 2))
    if trend_signal == "improving":
        rollover_capacity = min(backlog_total, round(rollover_capacity * 1.05, 2))
    elif trend_signal == "dipping":
        rollover_capacity = min(backlog_total, round(rollover_capacity * 0.9, 2))

    for exam in get_exam_entries(profile):
        for subject in exam["subjects"]:
            key = _task_key(exam["name"], subject)
            base_hours = target_hours * weights.get(key, 0)
            backlog_share = 0.0

            if backlog_total > 0:
                backlog_share = rollover_capacity * (
                    float(backlog_hours.get(key, backlog_hours.get(subject, 0))) / backlog_total
                )

            tasks[key] = round(base_hours + backlog_share, 2)

    tasks = _normalize_task_hours(tasks, target_hours + rollover_capacity)

    if backlog_total > 0:
        for key in list(tasks.keys()):
            carry = rollover_capacity * (
                float(backlog_hours.get(key, 0)) / backlog_total if backlog_total else 0
            )
            backlog_hours[key] = round(max(0.0, float(backlog_hours.get(key, 0)) - carry), 2)

    task_rows = []
    day_index = len(state.get("history", []))
    for exam in get_exam_entries(profile):
        for subject in exam["subjects"]:
            key = _task_key(exam["name"], subject)
            topic_frame = _subject_topic_frame(profile, state, exam["name"], subject, day_index=day_index)
            task_rows.append(
                {
                    "exam": exam["name"],
                    "subject": subject,
                    "hours": tasks.get(key, 0.0),
                    "topic": topic_frame["topic"],
                    "revision_topic": topic_frame["revision_topic"],
                    "topic_pool": topic_frame["topic_pool"],
                    "topic_status": topic_frame["topic_status"],
                }
            )

    return task_rows, round(target_hours, 2)


def ensure_today_plan(profile):
    if not has_exam_entries(profile):
        empty_plan = {
            "date": datetime.today().strftime("%Y-%m-%d"),
            "status": "pending",
            "recommended_hours": 0.0,
            "scheduled_hours": 0.0,
            "tasks": [],
        }
        return empty_plan, load_planner_state(profile["name"])

    state = load_planner_state(profile["name"])
    today_str = datetime.today().strftime("%Y-%m-%d")
    state = _roll_over_unfinished_work(state, today_str)

    current_day_plan = state.get("current_day_plan")
    if current_day_plan and current_day_plan.get("date") == today_str:
        current_day_plan["scheduled_hours"] = round(
            sum(task["hours"] for task in current_day_plan.get("tasks", [])),
            2,
        )
        save_planner_state(profile["name"], state)
        return current_day_plan, state

    tasks, recommended_hours = _build_daily_tasks(profile, state)
    scheduled_hours = round(sum(task["hours"] for task in tasks), 2)
    state["current_day_plan"] = {
        "date": today_str,
        "status": "pending",
        "recommended_hours": recommended_hours,
        "scheduled_hours": scheduled_hours,
        "tasks": tasks,
    }
    save_planner_state(profile["name"], state)
    return state["current_day_plan"], state


def mark_today_complete(profile):
    state = load_planner_state(profile["name"])
    today_plan = state.get("current_day_plan")

    if not today_plan:
        return "No active study plan for today yet. Ask for today's schedule first."

    for task in today_plan.get("tasks", []):
        progress = _section_progress_entry(state, task["exam"], task["subject"])
        progress["completed_hours"] = round(progress["completed_hours"] + float(task["hours"]), 2)
        progress["completed_sessions"] += 1
        progress["last_completed_on"] = today_plan["date"]

    today_plan["status"] = "completed"
    state.setdefault("history", []).append(
        {
            "date": today_plan["date"],
            "status": "completed",
            "tasks": today_plan["tasks"],
        }
    )
    save_planner_state(profile["name"], state)
    section_progress = get_section_progress(profile)
    focus_summary = ""
    if section_progress:
        weakest = sorted(
            section_progress,
            key=lambda item: (
                (item["mock_score"] if item["mock_score"] is not None else 50),
                -item["backlog_hours"],
            ),
        )[0]
        focus_summary = (
            f" Keep a closer eye on {weakest['exam']} | {weakest['subject']} next, "
            "because that is still one of your main sticking points."
        )
    return f"Great work. Today's study plan has been marked as completed.{focus_summary}"


def mark_today_missed(profile):
    state = load_planner_state(profile["name"])
    today_plan = state.get("current_day_plan")

    if not today_plan:
        return "No active study plan for today yet. Ask for today's schedule first."

    backlog_hours = state.setdefault("backlog_hours", {})
    for task in today_plan.get("tasks", []):
        key = _task_key(task["exam"], task["subject"])
        backlog_hours[key] = round(backlog_hours.get(key, 0) + task["hours"], 2)

    today_plan["status"] = "missed"
    state.setdefault("history", []).append(
        {
            "date": today_plan["date"],
            "status": "missed",
            "tasks": today_plan["tasks"],
        }
    )
    state["current_day_plan"] = None
    save_planner_state(profile["name"], state)
    return (
        "Today's work has been moved into your backlog and will be redistributed "
        "across future schedules."
    )


def _exam_time_split(profile, state):
    weights = _get_task_weights(profile, state)
    recommended_hours = _recommended_daily_hours(profile, state)
    split = {}

    for exam in get_exam_entries(profile):
        exam_total = 0.0
        for subject in exam["subjects"]:
            key = _task_key(exam["name"], subject)
            exam_total += recommended_hours * weights.get(key, 0)
        split[exam["name"]] = round(exam_total, 2)

    return split, recommended_hours


def format_study_plan(profile):
    if not has_exam_entries(profile):
        return (
            "You have not added any exams yet. Open the exam setup section and add an exam first, "
            "then I can build your adaptive study plan immediately."
        )

    state = load_planner_state(profile["name"])
    missing_subjects = get_missing_mock_subjects(profile, state)
    if missing_subjects:
        labels = ", ".join(
            _task_label(item["exam"], item["subject"]) for item in missing_subjects
        )
        return (
            "Before creating a weakness-based multi-exam plan, please enter your "
            f"trial mock scores for: {labels}."
        )

    exam_split, recommended_hours = _exam_time_split(profile, state)
    adaptive_profile = get_adaptive_learning_profile(profile)
    insight_snapshot = get_student_insight_snapshot(profile)
    route = build_student_state_route(
        profile,
        conversation_mode="tutor",
        tutor_level=profile.get("default_tutor_level", 3) or 3,
        support_style=insight_snapshot.get("support_style"),
        insight_snapshot=insight_snapshot,
    )
    jee_track_mode = get_jee_track_mode(profile)
    lines = [
        f"Study Plan for {profile['name']}",
        "",
        f"Recommended core study time per day: {recommended_hours} hours",
        f"Maximum available study time per day: {get_max_study_hours(profile)} hours",
        "Weekly rules:",
        "- Study specific topics, not just subject buckets.",
        "- Keep one revision touch inside every study block.",
        "- Complete at least 4 practice-test blocks every week.",
        f"Adaptive question difficulty: {adaptive_profile['question_difficulty']}",
        f"Concept depth progression: {adaptive_profile['concept_depth']}",
        f"Teaching speed right now: {adaptive_profile['teaching_speed']}",
        "",
        "Exam-wise daily allocation:",
    ]

    today_plan, _ = ensure_today_plan(profile)
    behavior = get_behavior_snapshot(profile)
    lines.append(f"Behavior-adjusted support style: {behavior.get('support_style', 'balanced_support')}")
    lines.append(f"Behavior-adjusted pacing style: {behavior.get('pacing_style', 'steady')}")
    lines.append(f"Emotional state trend: {insight_snapshot.get('emotional_state', 'steady')}")
    lines.append(f"Academic risk level: {insight_snapshot.get('academic_risk', 'low')}")
    lines.append(f"Practice trend: {insight_snapshot.get('trend_signal', 'building')}")
    if insight_snapshot.get("focus_recommendation"):
        lines.append(f"Current focus recommendation: {insight_snapshot.get('focus_recommendation')}")
    lines.append(f"Route focus: {route.get('focus', 'balanced academic clarity')}")
    lines.append(f"Route tone: {route.get('tone', 'balanced, clear, supportive')}")
    if jee_track_mode in {"mains_priority", "dual_track", "advanced_only"}:
        if jee_track_mode == "advanced_only":
            lines.append("JEE track strategy: keep Advanced depth central, but protect accuracy and clean execution like a Main-style scorer.")
        elif jee_track_mode == "dual_track":
            lines.append("JEE track strategy: JEE Main remains the scoring priority, while JEE Advanced stays alive through smaller depth bridges each week.")
        else:
            lines.append("JEE track strategy: secure JEE Main first, while keeping weekly contact with JEE Advanced depth so the transition later is not abrupt.")
    lines.append(
        f"Today's scheduled load including backlog recovery: {today_plan.get('scheduled_hours', recommended_hours)} hours"
    )
    lines.append("")

    for exam in get_exam_entries(profile):
        days_left = calculate_days_to_exam(exam["exam_date"])
        lines.append(
            f"- {exam['name']}: {exam_split.get(exam['name'], 0)} hours/day, exam in {days_left} days"
        )

        for subject in exam["subjects"]:
            score = _get_mock_score(state, exam["name"], subject)
            backlog = round(_get_backlog_hours(state, exam["name"], subject), 2)
            topic_frame = _subject_topic_frame(profile, state, exam["name"], subject, day_index=len(today_plan.get("tasks", [])))
            subject_hours = 0.0
            for task in today_plan["tasks"]:
                if task["exam"] == exam["name"] and task["subject"] == subject:
                    subject_hours = task["hours"]
                    break
            lines.append(
                f"  {subject}: focus topic {topic_frame['topic']}, revision touch {topic_frame['revision_topic']}, mock {score}/100, today {round(subject_hours, 2)} hours, backlog {backlog} hours"
            )

    lines.extend(
        [
            "",
            "Planning logic:",
            "- Weaker sections get more time.",
            "- Nearer exams get more weight.",
            "- Backlog is carried forward and spread gradually.",
            "- Current behavior profile can reduce or increase workload intensity.",
            "- Daily study time is recommended automatically instead of staying fixed.",
            "- Difficulty rises gradually as adherence and mock strength improve.",
            "- The same topic should reappear later in the week as revision, not only as first-time study.",
            "- Practice tests are scheduled through the week so the student does not drift away from the concepts.",
            "- For JEE, Main is treated as the first scoring target while Advanced stays in the plan through smaller bridge blocks.",
            f"- Current coach note: {insight_snapshot.get('coach_note', 'Keep balancing concept learning, practice, and review.')}",
            "",
            "Student state route:",
            format_student_state_route(route),
        ]
    )

    return "\n".join(lines)


def format_today_schedule(profile):
    if not has_exam_entries(profile):
        return (
            "You have not added any exams yet. Add your exam goals first and I will create today's plan."
        )

    state = load_planner_state(profile["name"])
    missing_subjects = get_missing_mock_subjects(profile, state)
    mock_notice = ""
    if missing_subjects:
        labels = ", ".join(
            _task_label(item["exam"], item["subject"]) for item in missing_subjects
        )
        mock_notice = (
            "Mock baseline note: trial scores are still missing for "
            f"{labels}. Astra is using a provisional baseline for now, and the plan will sharpen once those scores are added."
        )

    today_plan, state = ensure_today_plan(profile)
    adaptive_profile = get_adaptive_learning_profile(profile)
    insight_snapshot = get_student_insight_snapshot(profile)
    route = build_student_state_route(
        profile,
        conversation_mode="tutor",
        tutor_level=profile.get("default_tutor_level", 3) or 3,
        support_style=insight_snapshot.get("support_style"),
        insight_snapshot=insight_snapshot,
    )
    jee_track_mode = get_jee_track_mode(profile)
    backlog_total = round(sum(float(hours) for hours in state.get("backlog_hours", {}).values()), 2)

    lines = [
        f"Today's Plan for {profile['name']} ({today_plan['date']})",
        "",
        f"Recommended core study time today: {today_plan['recommended_hours']} hours",
        f"Scheduled time today including backlog recovery: {today_plan.get('scheduled_hours', today_plan['recommended_hours'])} hours",
        "Today will always include a topic target and a revision touch so concepts stay active.",
        f"Support style today: {get_behavior_snapshot(profile).get('support_style', 'balanced_support')}",
        f"Pacing style today: {get_behavior_snapshot(profile).get('pacing_style', 'steady')}",
        f"Emotional state trend: {insight_snapshot.get('emotional_state', 'steady')}",
        f"Academic risk level: {insight_snapshot.get('academic_risk', 'low')}",
        f"Practice trend: {insight_snapshot.get('trend_signal', 'building')}",
        f"Current focus recommendation: {insight_snapshot.get('focus_recommendation', 'Keep balancing concept review and practice.')}",
        f"Route focus: {route.get('focus', 'balanced academic clarity')}",
        f"Route tone: {route.get('tone', 'balanced, clear, supportive')}",
        f"Question difficulty right now: {adaptive_profile['question_difficulty']}",
        f"Teaching speed right now: {adaptive_profile['teaching_speed']}",
        (
            "JEE planning lens today: JEE Main scoring remains the first priority, with one smaller JEE Advanced touch if energy and schedule allow."
            if jee_track_mode in {"mains_priority", "dual_track"}
            else "JEE planning lens today: keep deeper Advanced reasoning active while protecting clean execution and revision rhythm."
            if jee_track_mode == "advanced_only"
            else ""
        ),
        "",
    ]

    for task in today_plan["tasks"]:
        lines.append(
            f"- {task['exam']} | {task['subject']}: {task['hours']} hours on {task.get('topic', task['subject'])} with revision touch {task.get('revision_topic', task.get('topic', task['subject']))}"
        )

    lines.extend(
        [
            "",
            mock_notice if mock_notice else "Mock baseline note: your current plan is using the available profile, behavior, and progress data.",
            "",
            f"Remaining backlog after today's allocation: {backlog_total} hours",
            f"Coach note: {insight_snapshot.get('coach_note', 'Keep moving steadily and review carefully.')}",
            "Rule: finish at least one practice block or mock-style drill today if the schedule allows.",
            "",
            "Student state route:",
            format_student_state_route(route),
            "",
            "Use these commands to keep the plan accurate:",
            "- Mark today's work complete",
            "- I missed today's work",
            "- Update mock scores",
            "- Update exam goals",
        ]
    )

    return "\n".join(lines)


def format_weekly_schedule(profile):
    weekly_data = get_weekly_schedule_data(profile)
    if "message" in weekly_data:
        return weekly_data["message"]

    insight_snapshot = get_student_insight_snapshot(profile)
    task_learning_context = weekly_data.get("task_learning_context", "")
    task_learning_notes = weekly_data.get("task_learning_notes", [])

    lines = [
        f"Weekly Plan for {profile['name']}",
        "",
        "Weekly overview:",
        f"- Recommended core study time: {weekly_data['weekly_core_hours']} hours",
        f"- Scheduled study time including backlog recovery: {weekly_data['weekly_scheduled_hours']} hours",
        f"- Practice-test blocks this week: {weekly_data.get('weekly_test_blocks', 4)}",
        f"- Current planner bias: {weekly_data.get('planner_bias_label', 'balanced')}",
        "",
        "Why this plan looks this way:",
    ]

    for item in weekly_data.get("weekly_strategy", [])[:4]:
        lines.append(f"- {item['title']}: {item['detail']}")

    if task_learning_notes:
        lines.append("- Task-learning notes:")
        for note in task_learning_notes[:4]:
            lines.append(f"  - {note}")

    if task_learning_context:
        lines.append("- Mode learning context:")
        for line in task_learning_context.splitlines()[:6]:
            lines.append(f"  {line}")

    lines.extend(["", "Exam-wise weekly allocation:"])

    for exam in weekly_data["exam_totals"]:
        lines.append(f"- {exam['exam']}: {exam['hours']} hours this week")

    lines.extend(["", "Suggested day-by-day structure:"])

    for day in weekly_data["days"]:
        lines.append(f"- {day['label']} ({day['date']}): {day['total_hours']} hours total")
        lines.append(f"  Theme: {day['theme']}")
        lines.append(f"  Main focus: {day['main_focus']}")
        for task in day["tasks"]:
            lines.append(
                f"  - {task['exam']} | {task['subject']}: {task['hours']} hours on {task.get('topic', task['subject'])} "
                f"({task.get('session_type', 'study')}, revision touch: {task.get('revision_topic', task.get('topic', task['subject']))})"
            )
        lines.append("")

    lines.extend(
        [
            "",
            "Weekly notes:",
            "- This weekly plan adapts to your exam dates, weaknesses, and backlog.",
            f"- Current practice trend: {insight_snapshot.get('trend_signal', 'building')}.",
            f"- Current focus recommendation: {insight_snapshot.get('focus_recommendation', 'Keep balancing concept review and practice.')}",
            "- The plan deliberately cycles topics so revision comes back again and again.",
            f"- Practice tests are mandatory across the week, not optional extras, and this week uses {weekly_data.get('weekly_test_blocks', 4)} of them.",
            "- If you miss a day, ask for today's plan again and the backlog will be redistributed.",
            "- Update mock scores after each trial mock to refresh next week's allocation.",
        ]
    )

    return "\n".join(lines)


def get_weekly_schedule_data(profile):
    if not has_exam_entries(profile):
        return {
            "message": (
                "Add your first exam in the exam setup section to unlock a weekly adaptive schedule."
            )
        }

    state = load_planner_state(profile["name"])
    missing_subjects = get_missing_mock_subjects(profile, state)
    mock_notice = ""
    if missing_subjects:
        labels = ", ".join(
            _task_label(item["exam"], item["subject"]) for item in missing_subjects
        )
        mock_notice = (
            "Trial mock scores are still missing for "
            f"{labels}. Astra is using a provisional baseline, and the weekly plan will get sharper after the first diagnostic mock."
        )

    today_plan, state = ensure_today_plan(profile)
    adaptive_profile = get_adaptive_learning_profile(profile)
    insight_snapshot = get_student_insight_snapshot(profile)
    planner_bias = _get_task_learning_bias(profile, insight_snapshot)
    weekly_core_hours = round(today_plan["recommended_hours"] * 7, 2)
    weekly_scheduled_hours = round(today_plan.get("scheduled_hours", today_plan["recommended_hours"]) * 7, 2)
    exam_totals = {}
    task_rows = _task_pressure_rows(profile, state)
    route = build_student_state_route(
        profile,
        conversation_mode="tutor",
        tutor_level=profile.get("default_tutor_level", 3) or 3,
        support_style=insight_snapshot.get("support_style"),
        insight_snapshot=insight_snapshot,
    )
    jee_track_mode = get_jee_track_mode(profile)

    days = _build_weekly_day_rows(profile, state, today_plan, planner_bias=planner_bias)
    for day in days:
        for task in day["tasks"]:
            exam_totals.setdefault(task["exam"], 0.0)
            exam_totals[task["exam"]] += task["hours"]

    strongest_sections = [row for row in task_rows if row["mock_score"] >= 75][:3]
    weakest_sections = [row for row in task_rows if row["mock_score"] < 60][:3]
    if is_jee_profile(profile):
        if jee_track_mode == "dual_track":
            jee_track_label = "JEE Main first, JEE Advanced continuously in touch"
        elif jee_track_mode == "advanced_only":
            jee_track_label = "JEE Advanced heavy with Main-style execution discipline"
        else:
            jee_track_label = "JEE Main first with weekly Advanced touch"
        weekly_strategy = [
            {
                "title": "Treat JEE Main as the first scoring milestone",
                "detail": "The weekly rhythm protects direct scoring, cleaner execution, and faster accuracy first, because JEE Main has to become dependable before the heavier Advanced push takes over.",
            },
            {
                "title": "Keep JEE Advanced alive every single week",
                "detail": "Instead of postponing Advanced completely, the plan adds smaller depth bridges so tougher reasoning never disappears from the student's thinking.",
            },
            {
                "title": "Repair Main-level weak spots before adding more depth",
                "detail": "Low-score and backlog-heavy PCM topics are brought forward early so the student does not pile Advanced difficulty on top of shaky Main fundamentals.",
            },
            {
                "title": "Use mock review to decide when Advanced load can grow",
                "detail": "As JEE Main accuracy and speed stabilize, the Advanced share of the week can gradually expand without overwhelming the student.",
            },
        ]
        notes = [
            f"This weekly plan is JEE-oriented and follows the track: {jee_track_label}.",
            "The week is intentionally split between scoring-first JEE Main work and smaller JEE Advanced depth bridges so the student does not lose contact with higher-level thinking.",
            "If you miss a day, ask for today's plan again and the backlog will be redistributed.",
            "Update mock scores after each test so the app can decide when to keep protecting Main more heavily and when to increase the Advanced push.",
            "Difficulty and teaching pace rise gradually as your adherence and mock performance improve.",
        ]
    else:
        weekly_strategy = [
            {
                "title": "Begin with the weakest, not the easiest",
                "detail": "The plan opens with weaker and nearer topics first so confidence builds where the marks upside are highest.",
            },
            {
                "title": "Use retrieval and timed practice mid-week",
                "detail": "A dedicated timed-accuracy block is placed mid-week so recall and speed improve together instead of only reading notes.",
            },
            {
                "title": "Close the week with revision and reset",
                "detail": "The final day is lighter so backlog, unsure topics, and revision can be cleaned up before the next cycle starts.",
            },
        ]
        notes = [
            "This weekly plan adapts to your exam dates, weaknesses, and backlog.",
            "The week is intentionally varied: concept rebuild, practice, timed work, revision, and mock-style review are separated so learning does not feel flat.",
            "If you miss a day, ask for today's plan again and the backlog will be redistributed.",
            "Update mock scores after each trial mock to refresh next week's allocation.",
            "Difficulty and teaching pace rise gradually as your adherence and mock performance improve.",
        ]

    notes.extend(planner_bias.get("summary", []))

    practice_rules = [
        "At least 4 practice-test blocks every week: sectional, timed, mixed, and full mock.",
        "Every subject should revisit key topics within 2 to 3 days so concepts stay fresh.",
        "Each study day should combine new learning with a revision touch, not just fresh reading.",
        "Weak topics stay in rotation until they move from pending to revise and then to done.",
    ]

    if planner_bias.get("weekly_test_blocks", 4) > 4:
        practice_rules[0] = "At least 5 practice-test blocks this week: the usual sectional, timed, mixed, and full mock flow plus one extra correction-focused test touch."
    if planner_bias.get("practice_priority") == "high":
        practice_rules.append("Each practice block should end with a short mistake review so the same errors do not carry forward.")
    if planner_bias.get("tutor_support") == "high":
        practice_rules.append("Concept blocks should stay shorter and more guided so confusion is handled before it spreads.")

    return {
        "student_name": profile["name"],
        "weekly_core_hours": weekly_core_hours,
        "weekly_scheduled_hours": weekly_scheduled_hours,
        "mock_notice": mock_notice,
        "weekly_test_blocks": planner_bias.get("weekly_test_blocks", 4),
        "planner_bias_label": planner_bias.get("practice_priority", "balanced"),
        "practice_rules": practice_rules,
        "exam_totals": [
            {"exam": exam["name"], "hours": round(exam_totals.get(exam["name"], 0.0), 2)}
            for exam in get_exam_entries(profile)
        ],
        "days": days,
        "notes": notes,
        "adaptive_profile": adaptive_profile,
        "jee_track_mode": jee_track_mode,
        "student_state_route": route,
        "student_state_route_text": format_student_state_route(route),
        "section_progress": get_section_progress(profile),
        "weekly_strategy": weekly_strategy,
        "task_learning_context": build_task_learning_context(profile["name"]),
        "task_learning_notes": planner_bias.get("summary", []),
        "strongest_sections": [
            f"{item['exam']} | {item['subject']} ({int(item['mock_score'])}/100)"
            for item in strongest_sections
        ],
        "weakest_sections": [
            f"{item['exam']} | {item['subject']} ({int(item['mock_score'])}/100)"
            for item in weakest_sections
        ],
    }


def generate_study_plan(tool_context: ToolContext):
    """Generate a multi-exam study plan from the saved student profile."""

    profile = tool_context.state.get("profile")

    if not profile:
        return (
            "I couldn't find your saved profile in this session. "
            "Please restart the app and enter your details again."
        )

    return format_study_plan(profile)


JOURNEY_FOLDER = Path("app_data") / "planner"


def _journey_path(student_id, suffix):
    JOURNEY_FOLDER.mkdir(parents=True, exist_ok=True)
    safe_id = str(student_id or "student").strip() or "student"
    return JOURNEY_FOLDER / f"{safe_id}_{suffix}.json"


def _load_json_file(path, default):
    try:
        if not Path(path).exists():
            return default
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default


def _save_json_file(path, payload):
    atomic_write_json(str(path), payload)


def _build_unit_index():
    units = []
    for subject, unit in iter_all_units():
        units.append(
            {
                "subject": subject,
                "unit_number": unit["unit_number"],
                "unit_name": unit["name"],
                "topics": list(unit["topics"]) or [unit["name"]],
                "jee_main_weightage_percent": unit["jee_main_weightage_percent"],
                "jee_advanced_weightage_percent": unit["jee_advanced_weightage_percent"],
                "prerequisite_unit_numbers": list(unit["prerequisite_unit_numbers"]),
                "estimated_learn_days": unit["estimated_learn_days"],
                "estimated_revise_days": unit["estimated_revise_days"],
                "difficulty": unit["difficulty"],
            }
        )
    return units


def _confidence_from_score(score):
    try:
        value = float(score)
    except (TypeError, ValueError):
        value = 0.0
    if value >= TOPIC_CONFIDENCE_THRESHOLDS["strong"]:
        return "strong"
    if value >= TOPIC_CONFIDENCE_THRESHOLDS["good"]:
        return "good"
    if value >= TOPIC_CONFIDENCE_THRESHOLDS["medium"]:
        return "medium"
    if value >= TOPIC_CONFIDENCE_THRESHOLDS["low"]:
        return "low"
    return "new"


def _revision_dates_from_confidence(confidence, start_date=None):
    start = start_date or datetime.today().date()
    intervals = SPACED_REPETITION_INTERVALS.get(confidence, SPACED_REPETITION_INTERVALS["low"])
    return [(start + timedelta(days=gap)).isoformat() for gap in intervals]


def _topic_slots_from_unit(unit):
    topics = list(unit.get("topics") or [unit["unit_name"]])
    learn_days = max(1, int(unit.get("estimated_learn_days", 1) or 1))
    slots = []
    for index in range(learn_days):
        topic = topics[index % len(topics)] if topics else unit["unit_name"]
        slots.append(
            {
                "subject": unit["subject"],
                "unit_number": unit["unit_number"],
                "unit_name": unit["unit_name"],
                "topic": topic,
                "weightage_percent": unit["jee_main_weightage_percent"],
                "advanced_weightage_percent": unit["jee_advanced_weightage_percent"],
                "difficulty": unit["difficulty"],
                "session_type": "learn",
            }
        )
    return slots


def _load_student_profile(student_id):
    from tools.profile_tools import load_profile

    return load_profile(student_id)


def _journey_defaults(student_id, exam_date_str, hours_per_day):
    today = datetime.today().date()
    try:
        exam_date = datetime.fromisoformat(str(exam_date_str)).date()
    except Exception:
        exam_date = today + timedelta(days=120)
    total_days = max(1, (exam_date - today).days)
    hours_per_day = max(2.0, min(float(hours_per_day or 6), 10.0))
    return exam_date, total_days, hours_per_day


def _build_topic_plan(profile):
    units = _build_unit_index()
    topic_plan = []
    covered = []
    for unit in units:
        for slot in _topic_slots_from_unit(unit):
            topic_plan.append(slot)
            covered.append(
                {
                    "subject": slot["subject"],
                    "unit_name": slot["unit_name"],
                    "topic": slot["topic"],
                }
            )
    return topic_plan, covered


def _topic_status_from_mastery(mastery_map, topic_key):
    topic = mastery_map.get(topic_key, {}) if mastery_map else {}
    return topic.get("status", "not_started")


def generate_journey_plan(student_id, exam_date_str, hours_per_day):
    try:
        profile = _load_student_profile(student_id)
        exam_date, total_days, hours_per_day = _journey_defaults(student_id, exam_date_str, hours_per_day)
        total_study_hours = round(total_days * hours_per_day, 2)
        topic_plan, covered_topics = _build_topic_plan(profile)
        first_pass_hours = round(total_study_hours * 0.6, 2)
        revision_hours = round(total_study_hours * 0.25, 2)
        pyq_hours = round(total_study_hours * 0.15, 2)
        per_day = hours_per_day
        morning_hours = round(per_day * (2 / 3), 2)
        evening_hours = round(per_day * (1 / 3), 2)
        start_date = datetime.today().date()

        journey_topics = []
        current_date = start_date
        topic_index = 0
        for slot in topic_plan:
            topic_index += 1
            journey_topics.append(
                {
                    **slot,
                    "order_index": topic_index,
                    "planned_date": current_date.isoformat(),
                    "status": "not_started",
                    "confidence_level": "new",
                    "next_revision_dates": _revision_dates_from_confidence("low", current_date),
                    "covered": False,
                }
            )
            current_date += timedelta(days=max(1, int(slot.get("difficulty", 3) / 2) or 1))
            if current_date > exam_date:
                current_date = exam_date

        journey = {
            "student_id": student_id,
            "student_name": profile.get("name", student_id),
            "exam_date": exam_date.isoformat(),
            "hours_per_day": hours_per_day,
            "total_days": total_days,
            "total_study_hours": total_study_hours,
            "allocation": {
                "first_pass_learning_hours": first_pass_hours,
                "revision_hours": revision_hours,
                "pyq_hours": pyq_hours,
            },
            "topics": journey_topics,
            "covered_topics": covered_topics,
            "created_at": datetime.utcnow().isoformat(timespec="seconds"),
            "updated_at": datetime.utcnow().isoformat(timespec="seconds"),
        }
        _save_json_file(_journey_path(student_id, "journey"), journey)
        weekly = generate_this_weeks_plan(student_id)
        summary = {
            "student_id": student_id,
            "days": total_days,
            "topics": len(journey_topics),
            "first_topic": journey_topics[0] if journey_topics else {},
            "first_week": weekly,
        }
        return summary
    except Exception as exc:
        print(f"WARNING: Could not generate journey plan for {student_id}: {exc}")
        return {
            "student_id": student_id,
            "days": 0,
            "topics": 0,
            "first_topic": {},
            "message": "Could not generate the journey plan right now.",
        }


def _load_journey(student_id):
    return _load_json_file(_journey_path(student_id, "journey"), {})


def _load_weekly(student_id):
    return _load_json_file(_journey_path(student_id, "weekly"), {})


def _load_today(student_id):
    return _load_json_file(_journey_path(student_id, "today"), {})


def _topic_progress_lookup(student_id):
    from tools.progress_tracker_tools import load_progress_state

    state = load_progress_state(student_id)
    lookup = {}
    for item in state.get("checkpoint_attempts", []) or []:
        key = f"{str(item.get('subject', '')).strip().lower()}::{str(item.get('topic', '')).strip().lower()}"
        data = lookup.setdefault(
            key,
            {
                "times_studied": 0,
                "best_score": 0,
                "last_studied": "",
                "confidence_level": "new",
                "next_revision_due": "",
            },
        )
        data["times_studied"] += 1
        score = float(item.get("checkpoint_score") or (100 if item.get("is_correct") else 0) or 0)
        data["best_score"] = max(data["best_score"], score)
        data["last_studied"] = item.get("timestamp", data["last_studied"])
        data["confidence_level"] = _confidence_from_score(score)
        revisions = _revision_dates_from_confidence(data["confidence_level"], datetime.today().date())
        data["next_revision_due"] = revisions[0] if revisions else ""
    return lookup


def _build_daily_entry(day_date, topic_item, revision_items, confidence_level, index, behavior_snapshot=None):
    behavior_snapshot = behavior_snapshot or {}
    engagement_low = str(behavior_snapshot.get("support_style", "")).strip().lower() in {"gentle_recovery", "reassuring_stepwise"}
    morning_minutes = 90 if not engagement_low else 60
    evening_minutes = 45 if not engagement_low else 30
    goal = f"Solve any standard JEE question on {topic_item['topic']} using the main rule and one example."
    return {
        "date": day_date.isoformat(),
        "day_name": day_date.strftime("%A"),
        "morning": {
            "subject": topic_item["subject"],
            "unit": topic_item["unit_name"],
            "topic": topic_item["topic"],
            "session_type": "learn" if topic_item.get("status") in {"not_started", "learning"} else "practice",
            "duration_minutes": morning_minutes,
            "daily_goal": goal,
            "weightage_percent": topic_item["weightage_percent"],
            "confidence_level": confidence_level,
        },
        "evening": {
            "subject": revision_items[0]["subject"] if revision_items else topic_item["subject"],
            "unit": revision_items[0]["unit_name"] if revision_items else topic_item["unit_name"],
            "topic": revision_items[0]["topic"] if revision_items else topic_item["topic"],
            "session_type": "revise" if revision_items else "practice",
            "duration_minutes": evening_minutes,
            "reason": "3-day revision due" if revision_items else "PYQ practice to solidify the concept",
        },
        "daily_motivation": (
            f"Day {index + 1} of your journey. You have covered {index + 1} topics. Keep going."
        ),
    }


def generate_this_weeks_plan(student_id):
    try:
        profile = _load_student_profile(student_id)
        journey = _load_journey(student_id)
        if not journey:
            return {"student_id": student_id, "days": [], "message": "Generate a journey first."}

        topic_plan = list(journey.get("topics", []) or [])
        if not topic_plan:
            return {"student_id": student_id, "days": [], "message": "Journey has no topics yet."}

        behavior_snapshot = get_behavior_snapshot(profile)
        start_date = datetime.today().date()
        week_days = []
        for index in range(7):
            day_date = start_date + timedelta(days=index)
            topic_item = topic_plan[min(index, len(topic_plan) - 1)]
            topic_key = f"{topic_item['subject'].lower()}::{topic_item['topic'].lower()}"
            revision_items = []
            revision_due = get_revision_due_today(student_id)
            for item in revision_due:
                if f"{item['subject'].lower()}::{item['topic'].lower()}" == topic_key:
                    revision_items.append(item)
                    break
            confidence_level = _confidence_from_score(revision_items[0].get("best_score", 0) if revision_items else 0)
            week_days.append(_build_daily_entry(day_date, topic_item, revision_items, confidence_level, index, behavior_snapshot))

        weekly = {
            "student_id": student_id,
            "student_name": profile.get("name", student_id),
            "generated_at": datetime.utcnow().isoformat(timespec="seconds"),
            "days": week_days,
        }
        _save_json_file(_journey_path(student_id, "weekly"), weekly)
        today_focus = get_todays_focus(student_id)
        return weekly
    except Exception as exc:
        print(f"WARNING: Could not generate weekly plan for {student_id}: {exc}")
        return {"student_id": student_id, "days": [], "message": "Could not generate the weekly plan right now."}


def get_revision_due_today(student_id):
    try:
        journey = _load_journey(student_id)
        today = datetime.today().date()
        due = []
        for item in journey.get("topics", []) or []:
            dates = item.get("next_revision_dates", []) or []
            if any(str(date_value) <= today.isoformat() for date_value in dates):
                due.append(
                    {
                        "subject": item.get("subject", ""),
                        "unit_name": item.get("unit_name", ""),
                        "topic": item.get("topic", ""),
                        "weightage_percent": item.get("weightage_percent", 0),
                        "confidence_level": item.get("confidence_level", "new"),
                        "next_revision_due": dates[0] if dates else "",
                        "overdue_days": max(0, (today - datetime.fromisoformat(dates[0]).date()).days) if dates else 0,
                        "best_score": item.get("best_score", 0),
                    }
                )
        due.sort(
            key=lambda item: (
                {"new": 0, "low": 1, "medium": 2, "good": 3, "strong": 4}.get(item.get("confidence_level", "new"), 0),
                -float(item.get("weightage_percent", 0) or 0),
                -int(item.get("overdue_days", 0) or 0),
            )
        )
        return due
    except Exception as exc:
        print(f"WARNING: Could not compute revision due list for {student_id}: {exc}")
        return []


def get_todays_focus(student_id):
    try:
        profile = _load_student_profile(student_id)
        weekly = _load_weekly(student_id)
        if not weekly:
            weekly = generate_this_weeks_plan(student_id)
        today = datetime.today().date().isoformat()
        today_entry = None
        for item in weekly.get("days", []) or []:
            if item.get("date") == today:
                today_entry = item
                break
        if not today_entry:
            days = weekly.get("days", []) or []
            today_entry = days[0] if days else {}

        revision_due = get_revision_due_today(student_id)
        behavior_snapshot = get_behavior_snapshot(profile)
        engagement_low = behavior_snapshot.get("support_style") in {"gentle_recovery", "reassuring_stepwise"}
        if today_entry:
            morning = dict(today_entry.get("morning", {}) or {})
            evening = dict(today_entry.get("evening", {}) or {})
            if engagement_low:
                morning["duration_minutes"] = max(45, int(morning.get("duration_minutes", 90) * 0.8))
                evening["duration_minutes"] = max(20, int(evening.get("duration_minutes", 45) * 0.8))
            mastery_map = get_student_mastery_map(student_id)
            topic_key = f"{str(morning.get('subject', '')).lower()}::{str(morning.get('topic', '')).lower()}"
            confidence = mastery_map.get(topic_key, {}).get("confidence_level", "new")
            morning["confidence_level"] = confidence
            focus = {
                "student_id": student_id,
                "date": today_entry.get("date", today),
                "morning": morning,
                "evening": evening,
                "primary": morning,
                "secondary": evening,
                "confidence_level": confidence,
                "revision_due": revision_due[:5],
                "daily_motivation": today_entry.get("daily_motivation", ""),
                "behind_schedule": False,
                "missed_sessions": 0,
            }
            _save_json_file(_journey_path(student_id, "today"), focus)
            return focus
        return {
            "student_id": student_id,
            "date": today,
            "morning": {},
            "evening": {},
            "primary": {},
            "secondary": {},
            "confidence_level": "new",
            "revision_due": revision_due[:5],
            "daily_motivation": "Build one small win today.",
            "behind_schedule": False,
            "missed_sessions": 0,
        }
    except Exception as exc:
        print(f"WARNING: Could not compute today's focus for {student_id}: {exc}")
        return {
            "student_id": student_id,
            "date": datetime.today().date().isoformat(),
            "morning": {},
            "evening": {},
            "primary": {},
            "secondary": {},
            "confidence_level": "new",
            "revision_due": [],
            "daily_motivation": "",
            "behind_schedule": False,
            "missed_sessions": 0,
        }


def get_student_mastery_map(student_id):
    try:
        progress = load_progress_state(student_id)
        analytics = _load_json_file(_journey_path(student_id, "analytics"), {})
        journey = _load_journey(student_id)
        lookup = _topic_progress_lookup(student_id)
        mastery = {}
        for item in journey.get("topics", []) or []:
            key = f"{str(item.get('subject', '')).lower()}::{str(item.get('topic', '')).lower()}"
            progress_info = lookup.get(key, {})
            attempts = int(progress_info.get("times_studied", 0) or 0)
            best_score = float(progress_info.get("best_score", 0) or 0)
            last_studied = progress_info.get("last_studied", "")
            confidence_level = progress_info.get("confidence_level") or _confidence_from_score(best_score)
            next_revision = progress_info.get("next_revision_due") or ""
            if not next_revision:
                nexts = item.get("next_revision_dates", []) or []
                next_revision = nexts[0] if nexts else ""
            mastery[key] = {
                "subject": item.get("subject", ""),
                "unit_name": item.get("unit_name", ""),
                "topic": item.get("topic", ""),
                "confidence_level": confidence_level,
                "times_studied": attempts,
                "best_score": round(best_score, 1),
                "last_studied": last_studied,
                "next_revision_due": next_revision,
                "status": "strong" if confidence_level in {"good", "strong"} else "revising" if confidence_level in {"low", "medium"} else "not_started",
                "weightage_percent": item.get("weightage_percent", 0),
            }
        return mastery
    except Exception as exc:
        print(f"WARNING: Could not build mastery map for {student_id}: {exc}")
        return {}


def record_topic_outcome(student_id, topic, subject, unit_name, checkpoint_score, duration_minutes, session_type):
    try:
        from tools.analytics_tools import record_engagement, record_session_analytics
        from tools.behavior_tools import record_behavior_event
        from tools.personal_memory_tools import add_memory
        from tools.progress_tracker_tools import log_topic_completion
        from tools.student_state_router import update_state

        profile = _load_student_profile(student_id)
        topic = str(topic or "").strip()
        subject = str(subject or "").strip()
        unit_name = str(unit_name or "").strip()
        session_type = str(session_type or "learn").strip().lower()
        score = float(checkpoint_score or 0)
        confidence_level = _confidence_from_score(score)
        revision_dates = _revision_dates_from_confidence(confidence_level)
        journey = _load_journey(student_id)
        updated = False

        for item in journey.get("topics", []) or []:
            if item.get("topic", "").strip().lower() == topic.strip().lower() and item.get("subject", "").strip().lower() == subject.strip().lower():
                item["confidence_level"] = confidence_level
                item["status"] = "strong" if score >= 85 else "learning" if score >= 60 else "revising"
                item["covered"] = True
                item["last_studied"] = datetime.now().isoformat(timespec="seconds")
                item["next_revision_dates"] = revision_dates
                item["best_score"] = max(float(item.get("best_score", 0) or 0), score)
                updated = True
                if score < 60:
                    item["priority_revision"] = True
                else:
                    item.pop("priority_revision", None)
                break
        if updated:
            journey["updated_at"] = datetime.utcnow().isoformat(timespec="seconds")
            _save_json_file(_journey_path(student_id, "journey"), journey)
            weekly = _load_weekly(student_id)
            if weekly:
                for day in weekly.get("days", []) or []:
                    if day.get("morning", {}).get("topic", "").strip().lower() == topic.strip().lower():
                        day["morning"]["confidence_level"] = confidence_level
                        day["morning"]["session_type"] = session_type
                        day["evening"]["reason"] = "3-day revision due" if score < 60 else day["evening"].get("reason", "PYQ practice to solidify the concept")
                _save_json_file(_journey_path(student_id, "weekly"), weekly)

        progress_result = log_topic_completion(student_id, topic, subject, score, session_type, unit_name=unit_name)
        record_session_analytics(student_id, topic, duration_minutes, score, session_type, subject=subject, exam=(profile.get("exams") or [{}])[0].get("name", "JEE MAIN"))
        record_engagement(student_id, topic, duration_minutes, session_type=session_type)
        record_behavior_event(
            student_id,
            event_type="session_completed",
            user_input=f"Studied {topic}",
            tutor_response="Session recorded.",
            metadata={
                "topic": topic,
                "subject": subject,
                "unit_name": unit_name,
                "score": score,
                "confidence_level": confidence_level,
            },
        )
        add_memory(
            student_id,
            f"Studied {topic} on {datetime.today().date().isoformat()}. Score: {round(score, 1)}%. Confidence: {confidence_level}. Next revision: {revision_dates[0] if revision_dates else ''}"
        )
        route = update_state(student_id)
        return {
            "student_id": student_id,
            "topic": topic,
            "subject": subject,
            "unit_name": unit_name,
            "checkpoint_score": round(score, 1),
            "confidence_level": confidence_level,
            "next_revision_dates": revision_dates,
            "weekly_plan_updated": updated,
            "progress": progress_result,
            "state_route": route,
            "next_steps": "Keep the revision loop active and return for the next scheduled session.",
        }
    except Exception as exc:
        print(f"WARNING: Could not record topic outcome for {student_id}: {exc}")
        return {
            "student_id": student_id,
            "topic": topic,
            "subject": subject,
            "confidence_level": "new",
            "next_revision_dates": [],
            "weekly_plan_updated": False,
            "next_steps": "Keep going gently and try again later.",
        }
