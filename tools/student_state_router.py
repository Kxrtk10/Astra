import json
import os
from pathlib import Path

from backend.storage import atomic_write_json
from tools.chat_outcome_tracker import get_task_learning_profiles


def _clamp_level(value, low=1, high=5):
    try:
        return max(low, min(int(value), high))
    except (TypeError, ValueError):
        return 3


def _choose_focus(conversation_mode, insight):
    mode = (conversation_mode or "tutor").strip().lower()
    emotional_state = str((insight or {}).get("emotional_state", "steady")).strip().lower()
    academic_risk = str((insight or {}).get("academic_risk", "low")).strip().lower()

    if mode == "lounge":
        return "emotional safety and bonding"
    if mode == "practice":
        return "question quality, accuracy, and exam discipline"
    if mode == "last_minute":
        return "high-yield rescue revision"
    if mode == "tips":
        return "exam strategy and decision rules"
    if mode == "guide":
        return "product guidance and app navigation"

    if emotional_state in {"overwhelmed", "strained"} or academic_risk == "high":
        return "calming recovery and one-step progress"
    if emotional_state in {"confident", "energized"}:
        return "momentum, deeper learning, and stretch"
    return "balanced academic clarity"


def _choose_tone(conversation_mode, insight, support_style):
    mode = (conversation_mode or "tutor").strip().lower()
    emotional_state = str((insight or {}).get("emotional_state", "steady")).strip().lower()
    support_style = str(support_style or "balanced_support").strip().lower()

    if mode == "lounge":
        return "warm, casual, supportive"
    if mode == "practice":
        return "focused, exam-like, efficient"
    if mode == "last_minute":
        return "urgent but calming"
    if mode == "tips":
        return "strategic and practical"
    if mode == "guide":
        return "clear and product-focused"

    if emotional_state in {"overwhelmed", "strained"}:
        return "gentle, steady, reassuring"
    if emotional_state in {"confident", "energized"}:
        return "encouraging, goal-oriented, slightly firmer"
    if support_style in {"gentle_recovery", "reassuring_stepwise"}:
        return "calm, step-by-step, reassuring"
    if support_style in {"challenging_coach", "accountability_focused"}:
        return "firm, motivating, accountability-driven"
    return "balanced, clear, supportive"


def _choose_pressure(conversation_mode, insight):
    mode = (conversation_mode or "tutor").strip().lower()
    emotional_state = str((insight or {}).get("emotional_state", "steady")).strip().lower()
    academic_risk = str((insight or {}).get("academic_risk", "low")).strip().lower()

    if mode in {"lounge", "guide"}:
        return "low"
    if mode == "last_minute":
        return "medium-high"
    if mode == "practice":
        return "medium"
    if emotional_state in {"overwhelmed", "strained"}:
        return "low"
    if academic_risk == "high":
        return "low-medium"
    if emotional_state in {"confident", "energized"}:
        return "medium-high"
    return "medium"


def _choose_source_policy(conversation_mode, insight, tutor_level):
    mode = (conversation_mode or "tutor").strip().lower()
    level = _clamp_level(tutor_level)
    academic_risk = str((insight or {}).get("academic_risk", "low")).strip().lower()

    if mode == "lounge":
        return "no academic source retrieval unless the student asks"
    if mode == "guide":
        return "no learning-source retrieval; app only"
    if mode == "last_minute":
        return "syllabus-first plus high-yield public sources"
    if mode == "tips":
        return "trusted exam-strategy sources only"
    if mode == "practice":
        return "exam-pattern and chapter-specific source support"

    if academic_risk == "high":
        return "syllabus-first, then only the most relevant trusted public sources"
    if level >= 4:
        return "topic-specific sources plus syllabus context"
    return "curated topic-specific sources only when useful"


def _choose_avoid(conversation_mode, insight):
    mode = (conversation_mode or "tutor").strip().lower()
    emotional_state = str((insight or {}).get("emotional_state", "steady")).strip().lower()

    avoid = []
    if mode == "tutor":
        avoid.append("casual drift")
        avoid.append("overly chatty small talk")
    elif mode == "lounge":
        avoid.append("heavy academic lecturing")
    elif mode == "practice":
        avoid.append("long theory dumps")
    elif mode == "last_minute":
        avoid.append("deep diversions")
    elif mode == "tips":
        avoid.append("generic advice without application")
    elif mode == "guide":
        avoid.append("academic tutoring")

    if emotional_state in {"overwhelmed", "strained"}:
        avoid.append("pressure-heavy or guilt-heavy language")

    return avoid


def _choose_feel(conversation_mode, insight, task_profile):
    mode = (conversation_mode or "tutor").strip().lower()
    emotional_state = str((insight or {}).get("emotional_state", "steady")).strip().lower()
    practice_accuracy = float((task_profile or {}).get("recent_accuracy", 0) or 0)
    practice_trend = str((task_profile or {}).get("trend_signal", "building")).strip().lower()

    if mode == "lounge":
        return "warm, human, and light"
    if mode == "guide":
        return "clear, calm, and product-focused"
    if mode == "practice":
        if practice_accuracy < 55 or practice_trend == "dipping":
            return "firm, corrective, and structured"
        if practice_accuracy >= 75 and practice_trend == "improving":
            return "focused, energetic, and exam-ready"
        return "focused, steady, and exam-like"
    if mode == "last_minute":
        return "urgent but reassuring"
    if mode == "tips":
        return "strategic and practical"

    if emotional_state in {"overwhelmed", "strained"}:
        return "gentle, steady, and reassuring"
    if emotional_state in {"confident", "energized"}:
        return "encouraging and slightly sharper"
    return "balanced and supportive"


def _choose_say(conversation_mode, insight, task_profile):
    mode = (conversation_mode or "tutor").strip().lower()
    emotional_state = str((insight or {}).get("emotional_state", "steady")).strip().lower()
    practice_accuracy = float((task_profile or {}).get("recent_accuracy", 0) or 0)
    practice_speed = str((task_profile or {}).get("speed_signal", "steady")).strip().lower()

    if mode == "lounge":
        return "Keep replies conversational, natural, and easy to continue."
    if mode == "guide":
        return "Explain only what the user needs to navigate the product clearly."
    if mode == "practice":
        if practice_accuracy < 55:
            return "Ask one question or give one drill at a time, then correct the mistake immediately."
        if practice_speed == "slow":
            return "Keep the drill tight, timed, and easy to self-check."
        return "Stay exam-like, concise, and focused on accuracy plus pace."
    if mode == "last_minute":
        return "Give short rescue steps, high-yield recall, and fast review cues."
    if mode == "tips":
        return "Turn strategy into concrete exam behavior."

    if emotional_state in {"overwhelmed", "strained"}:
        return "Break the idea into smaller steps and reassure before pushing forward."
    if emotional_state in {"confident", "energized"}:
        return "Stretch the student a little and keep momentum visible."
    return "Explain clearly, then move to the next useful step."


def _choose_source_pack_hint(conversation_mode, insight, task_profile, profile):
    mode = (conversation_mode or "tutor").strip().lower()
    academic_risk = str((insight or {}).get("academic_risk", "low")).strip().lower()
    top_exam = ""
    exams = profile.get("exams", []) or []
    if exams:
        top_exam = str(exams[0].get("name", "")).strip().upper()

    if mode == "lounge":
        return "No academic source pack unless the student explicitly asks."
    if mode == "guide":
        return "No source pack; explain only app navigation and product behavior."
    if mode == "last_minute":
        return "Syllabus-first rescue pack with high-yield exam references."
    if mode == "tips":
        return "Trusted exam-strategy source pack only."
    if mode == "practice":
        return f"{top_exam or 'exam'} pattern pack with focused chapter support."

    if academic_risk == "high":
        return "Syllabus-first source pack with only the most relevant public references."
    if (task_profile or {}).get("recent_accuracy", 0) and float((task_profile or {}).get("recent_accuracy", 0) or 0) >= 75:
        return f"{top_exam or 'topic'} deepening pack plus exam context."
    return "Curated topic-specific source pack only when useful."


def _choose_teaching_adjustment(conversation_mode, insight, task_profile):
    mode = (conversation_mode or "tutor").strip().lower()
    topic_mastery = (insight or {}).get("topic_mastery", {}) or {}
    weak_topics = topic_mastery.get("weak_topics", []) or []
    next_adjustment = str(topic_mastery.get("next_teaching_adjustment", "")).strip()
    focus_recommendation = str((insight or {}).get("focus_recommendation", "")).strip()
    trend = str((task_profile or {}).get("trend_signal", "building")).strip().lower()
    recent_accuracy = float((task_profile or {}).get("recent_accuracy", 0) or 0)

    if mode == "lounge":
        return "Keep it light and supportive; do not force academic pressure."
    if mode == "guide":
        return "Stay product-focused and explain only the feature the student asked about."
    if mode == "practice":
        if weak_topics:
            return f"Start from {weak_topics[0]} and keep the drill tight, exam-like, and correction-friendly."
        if recent_accuracy < 55:
            return "Use easier questions first, then increase difficulty only after a correct response."
        if trend == "improving":
            return "Increase challenge gradually while keeping the format clean and timed."
        return "Keep the set balanced and focused on error correction."
    if mode == "last_minute":
        return "Use high-yield rescue steps, short recall loops, and no extra filler."
    if mode == "tips":
        return "Turn every tip into a concrete exam action the student can apply immediately."

    if next_adjustment:
        return next_adjustment
    if focus_recommendation:
        return f"Use this as the next anchor: {focus_recommendation}"
    return "Keep the explanation small, clear, and check understanding before moving on."


def route_student_state(
    profile,
    conversation_mode="tutor",
    tutor_level=3,
    support_style=None,
    insight_snapshot=None,
    todays_focus=None,
    revision_due=None,
    mastery_map=None,
):
    insight = insight_snapshot or {}
    mode = (conversation_mode or "tutor").strip().lower()
    level = _clamp_level(tutor_level)
    task_profiles = get_task_learning_profiles(profile["name"])
    task_profile = task_profiles.get(mode, {})
    todays_focus = todays_focus or {}
    revision_due = revision_due or []
    mastery_map = mastery_map or {}

    active_topic = str((todays_focus.get("topic") or todays_focus.get("unit") or "")).strip()
    confidence_level = str(todays_focus.get("confidence_level") or mastery_map.get("confidence_level") or "new").strip().lower()
    revision_count = len(revision_due)
    on_track = bool(todays_focus) and revision_count <= 1 and confidence_level in {"medium", "good", "strong"}
    behind_schedule = bool(todays_focus) and (todays_focus.get("behind_schedule") or todays_focus.get("missed_sessions", 0) > 0)
    revision_overdue = revision_count >= 2
    ready_for_practice = confidence_level in {"good", "strong"} and revision_count == 0 and mode in {"practice", "tutor"}

    route = {
        "tab": mode,
        "feel": _choose_feel(mode, insight, task_profile),
        "tone": _choose_tone(mode, insight, support_style),
        "say": _choose_say(mode, insight, task_profile),
        "focus": _choose_focus(mode, insight),
        "pressure": _choose_pressure(mode, insight),
        "source_policy": _choose_source_policy(mode, insight, level),
        "source_pack_hint": _choose_source_pack_hint(mode, insight, task_profile, profile),
        "teaching_adjustment": _choose_teaching_adjustment(mode, insight, task_profile),
        "avoid": _choose_avoid(mode, insight),
        "next_step": "Start with the smallest useful action and grow from there.",
        "task_learning": {
            "mode": task_profile.get("mode_label", mode.replace("_", " ").title()),
            "interactions": task_profile.get("interactions", 0),
            "recent_accuracy": task_profile.get("recent_accuracy", 0),
            "trend_signal": task_profile.get("trend_signal", "building"),
            "adaptation": task_profile.get("adaptation", ""),
        },
        "student_state": {
            "emotional_state": insight.get("emotional_state", "steady"),
            "sentiment_trend": insight.get("sentiment_trend", "mixed"),
            "academic_risk": insight.get("academic_risk", "low"),
            "support_style": support_style or insight.get("support_style", "balanced_support"),
            "pacing_style": insight.get("pacing_style", "steady"),
        },
        "planner_state": {
            "active_topic": active_topic,
            "confidence_level": confidence_level,
            "revision_due_count": revision_count,
            "state_label": "on_track_learning" if on_track else "revision_overdue" if revision_overdue else "behind_schedule" if behind_schedule else "ready_for_practice" if ready_for_practice else "on_track_learning",
            "on_track_learning": on_track,
            "behind_schedule": behind_schedule,
            "revision_overdue": revision_overdue,
            "ready_for_practice": ready_for_practice,
        },
    }

    if mode == "lounge":
        route["next_step"] = "Keep the student comfortable and present."
    elif mode == "practice":
        route["next_step"] = "Give the next question or drill in a clean exam format."
    elif mode == "last_minute":
        route["next_step"] = "Build the fastest high-yield rescue path."
    elif mode == "tips":
        route["next_step"] = "Turn the strategy into a concrete exam behavior."
    elif mode == "guide":
        route["next_step"] = "Explain where the user should click or what the feature does."
    elif route["student_state"]["emotional_state"] in {"overwhelmed", "strained"}:
        route["next_step"] = "Reassure first, then move to one small academic step."
    elif route["student_state"]["emotional_state"] in {"confident", "energized"}:
        route["next_step"] = "Use momentum to deepen the concept or increase challenge a little."

    route["planner_state"]["state_label"] = route["planner_state"].get("state_label") or "on_track_learning"
    save_student_state(profile["name"], route)
    return route


def build_student_state_route(profile, conversation_mode="tutor", tutor_level=3, support_style=None, insight_snapshot=None, todays_focus=None, revision_due=None, mastery_map=None):
    return route_student_state(
        profile,
        conversation_mode=conversation_mode,
        tutor_level=tutor_level,
        support_style=support_style,
        insight_snapshot=insight_snapshot,
        todays_focus=todays_focus,
        revision_due=revision_due,
        mastery_map=mastery_map,
    )


def update_state(student_id, profile=None, todays_focus=None, revision_due=None, mastery_map=None, conversation_mode="tutor"):
    if profile is None:
        from tools.profile_tools import load_profile

        profile = load_profile(student_id)
    from tools.student_insight_tools import get_student_insight_snapshot

    insight_snapshot = get_student_insight_snapshot(profile)
    route = route_student_state(
        profile,
        conversation_mode=conversation_mode,
        tutor_level=int(profile.get("default_tutor_level", 3) or 3),
        support_style=insight_snapshot.get("support_style"),
        insight_snapshot=insight_snapshot,
        todays_focus=todays_focus,
        revision_due=revision_due,
        mastery_map=mastery_map,
    )
    return route


def format_student_state_route(route):
    lines = [
        "Student state route:",
        f"- Tab: {route.get('tab', 'tutor')}",
        f"- Feel: {route.get('feel', 'balanced and supportive')}",
        f"- Tone: {route.get('tone', 'balanced')}",
        f"- Say: {route.get('say', 'Explain clearly, then move to the next useful step.')}",
        f"- Focus: {route.get('focus', 'balanced academic clarity')}",
        f"- Pressure: {route.get('pressure', 'medium')}",
        f"- Source policy: {route.get('source_policy', 'curated sources only when useful')}",
        f"- Source pack hint: {route.get('source_pack_hint', 'Curated topic-specific source pack only when useful.')}",
        f"- Teaching adjustment: {route.get('teaching_adjustment', 'Keep the explanation small, clear, and check understanding before moving on.')}",
        f"- Next step: {route.get('next_step', 'Start with the smallest useful action and grow from there.')}",
    ]
    avoid = route.get("avoid", [])
    if avoid:
        lines.append(f"- Avoid: {', '.join(avoid)}")
    state = route.get("student_state", {})
    if state:
        lines.append("- Student state:")
        lines.append(f"  - emotional_state: {state.get('emotional_state', 'steady')}")
        lines.append(f"  - sentiment_trend: {state.get('sentiment_trend', 'mixed')}")
        lines.append(f"  - academic_risk: {state.get('academic_risk', 'low')}")
        lines.append(f"  - support_style: {state.get('support_style', 'balanced_support')}")
        lines.append(f"  - pacing_style: {state.get('pacing_style', 'steady')}")
    task_learning = route.get("task_learning", {})
    if task_learning:
        lines.append("- Task learning:")
        lines.append(f"  - mode: {task_learning.get('mode', 'Tutor')}")
        lines.append(f"  - interactions: {task_learning.get('interactions', 0)}")
        lines.append(f"  - recent_accuracy: {task_learning.get('recent_accuracy', 0)}")
        lines.append(f"  - trend_signal: {task_learning.get('trend_signal', 'building')}")
        if task_learning.get("adaptation"):
            lines.append(f"  - adaptation: {task_learning.get('adaptation')}")
    return "\n".join(lines)
STATE_FOLDER = Path("app_data") / "planner"


def _state_path(name):
    STATE_FOLDER.mkdir(parents=True, exist_ok=True)
    safe_name = str(name or "student").strip() or "student"
    return STATE_FOLDER / f"{safe_name}_state.json"


def load_student_state(name):
    path = _state_path(name)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_student_state(name, state):
    path = _state_path(name)
    atomic_write_json(str(path), state)
