import json
import re
import os
from datetime import datetime, timedelta

from tools.analytics_tools import get_analytics_summary
from tools.progress_tracker_tools import get_progress_snapshot
from backend.storage import atomic_write_json

ENGAGEMENT_FOLDER = "engagement_state"
LEAGUE_ORDER = [
    "Bronze 1",
    "Bronze 2",
    "Bronze 3",
    "Silver 1",
    "Silver 2",
    "Silver 3",
    "Gold 1",
    "Gold 2",
    "Gold 3",
    "Platinum 1",
    "Platinum 2",
    "Platinum 3",
    "Diamond 1",
    "Diamond 2",
    "Diamond 3",
    "Champion",
]
LEAGUE_STEP_POINTS = 150


def _engagement_path(name):
    if not os.path.exists(ENGAGEMENT_FOLDER):
        os.makedirs(ENGAGEMENT_FOLDER)
    return os.path.join(ENGAGEMENT_FOLDER, f"{name}.json")


def load_engagement_state(name):
    filepath = _engagement_path(name)

    if not os.path.exists(filepath):
        return {
            "points": 0,
            "level": 1,
            "current_streak": 0,
            "last_completion_date": "",
            "bond_messages": 0,
            "milestones": [],
        }

    with open(filepath, "r") as file:
        state = json.load(file)

    state.setdefault("points", 0)
    state.setdefault("level", 1)
    state.setdefault("current_streak", 0)
    state.setdefault("last_completion_date", "")
    state.setdefault("bond_messages", 0)
    state.setdefault("milestones", [])
    return state


def save_engagement_state(name, state):
    filepath = _engagement_path(name)
    atomic_write_json(filepath, state)


def _recalculate_level(points):
    return max(1, (points // 100) + 1)


def _league_snapshot(points):
    league_index = min(points // LEAGUE_STEP_POINTS, len(LEAGUE_ORDER) - 1)
    current_league = LEAGUE_ORDER[league_index]
    max_index = len(LEAGUE_ORDER) - 1

    if league_index >= max_index:
        return {
            "current_league": current_league,
            "next_league": "Max league reached",
            "points_into_league": points - (league_index * LEAGUE_STEP_POINTS),
            "points_needed_for_next": 0,
            "promotion_progress_percent": 100,
        }

    base_points = league_index * LEAGUE_STEP_POINTS
    points_into_league = max(0, points - base_points)
    points_needed_for_next = max(0, LEAGUE_STEP_POINTS - points_into_league)
    promotion_progress = round((points_into_league / LEAGUE_STEP_POINTS) * 100)
    return {
        "current_league": current_league,
        "next_league": LEAGUE_ORDER[league_index + 1],
        "points_into_league": points_into_league,
        "points_needed_for_next": points_needed_for_next,
        "promotion_progress_percent": promotion_progress,
    }


def _contains_reason(milestones, keywords):
    for item in milestones:
        reason = str(item.get("reason", "")).lower()
        if any(keyword in reason for keyword in keywords):
            return True
    return False


def _reason_key(reason):
    return re.sub(r"\s+", " ", str(reason or "").strip().lower())


def _awarded_today(state, reason):
    target = _reason_key(reason)
    today = datetime.now().date().isoformat()
    for item in reversed(state.get("milestones", [])):
        if not item.get("timestamp", "").startswith(today):
            break
        if _reason_key(item.get("reason", "")) == target:
            return True
    return False


def _daily_missions(name, state):
    progress = get_progress_snapshot(name)
    analytics = get_analytics_summary(name)
    milestones = state.get("milestones", [])
    counts = progress.get("counts", {})

    missions = [
        {
            "title": "Visual Concept Quest",
            "detail": "Use a visual or 3D-style explanation for one concept so the idea becomes easier to picture.",
            "status": "done"
            if _contains_reason(milestones, ["visual concept", "visual explanation", "3d", "concept visualization"])
            else "active",
            "reward": 30,
        },
        {
            "title": "Practice Sprint",
            "detail": "Log one practice attempt with accuracy and timing so your speed path keeps growing.",
            "status": "done" if _contains_reason(milestones, ["practice review", "practice attempt"]) else "active",
            "reward": 25,
        },
        {
            "title": "Progress Push",
            "detail": "Move at least one topic into done or revise so the syllabus does not stay stuck in the shadows.",
            "status": "done"
            if _contains_reason(milestones, ["done lane", "revision lane", "progress tracker updated"])
            or counts.get("done", 0) + counts.get("revise", 0) > 0
            else "active",
            "reward": 20,
        },
    ]

    if analytics.get("recent_accuracy", 0):
        missions.append(
            {
                "title": "Accuracy Guard",
                "detail": "Keep improving accuracy so the tutor can safely raise challenge without overwhelming you.",
                "status": "done" if analytics.get("recent_accuracy", 0) >= 70 else "active",
                "reward": 20,
            }
        )

    return missions


def get_engagement_snapshot(name):
    state = load_engagement_state(name)
    league = _league_snapshot(state["points"])
    return {
        "points": state["points"],
        "level": state["level"],
        "current_streak": state["current_streak"],
        "bond_messages": state["bond_messages"],
        "last_completion_date": state["last_completion_date"],
        "recent_milestones": state["milestones"][-5:],
        "daily_missions": _daily_missions(name, state),
        **league,
    }


def award_points(name, points, reason):
    state = load_engagement_state(name)
    if points <= 0:
        return state
    if _awarded_today(state, reason):
        return state
    state["points"] += points
    state["level"] = _recalculate_level(state["points"])
    state["milestones"].append(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "points": points,
            "reason": reason,
        }
    )
    save_engagement_state(name, state)
    return state


def record_bond_interaction(name):
    state = load_engagement_state(name)
    state["bond_messages"] += 1
    save_engagement_state(name, state)
    return state


def record_daily_completion(name):
    today = datetime.now().date()
    state = load_engagement_state(name)
    last_completion_date = state.get("last_completion_date")

    if last_completion_date:
        last_date = datetime.strptime(last_completion_date, "%Y-%m-%d").date()
        if last_date == today:
            return state
        if last_date == today - timedelta(days=1):
            state["current_streak"] += 1
        else:
            state["current_streak"] = 1
    else:
        state["current_streak"] = 1

    state["last_completion_date"] = today.strftime("%Y-%m-%d")
    save_engagement_state(name, state)
    return state


def break_streak(name):
    state = load_engagement_state(name)
    state["current_streak"] = 0
    save_engagement_state(name, state)
    return state


def format_points_summary(profile):
    state = load_engagement_state(profile["name"])
    league = _league_snapshot(state["points"])
    persona = profile.get("preferred_persona") or "your chosen study vibe"

    lines = [
        f"Motivation Dashboard for {profile['name']}",
        "",
        f"Points: {state['points']}",
        f"Level: {state['level']}",
        f"Current league: {league['current_league']}",
        f"Next promotion: {league['next_league']}",
        f"Points needed for promotion: {league['points_needed_for_next']}",
        f"Current streak: {state['current_streak']} day(s)",
        f"Tutor persona inspiration: {persona}",
    ]

    if state["milestones"]:
        latest = state["milestones"][-3:]
        lines.extend(["", "Recent points earned:"])
        for item in latest:
            lines.append(f"- +{item['points']} for {item['reason']}")

    lines.extend(
        [
            "",
            "Point rules:",
            "- Points are for real learning actions, not repeated taps.",
            "- You earn more when you finish a topic, revise a weak topic, or complete practice with good accuracy.",
            "- Repeating the same save in the same day does not keep farming points.",
            "- Streak points stay tied to actual day-by-day consistency.",
            "",
            "How to earn points:",
            "- Complete today's work",
            "- Move pending topics into done or revision-ready status",
            "- Log practice attempts and improve accuracy",
            "- Update mock scores after a trial mock",
            "- Keep your streak alive day by day",
        ]
    )

    return "\n".join(lines)
