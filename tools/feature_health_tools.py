from tools.analytics_tools import get_analytics_summary
from tools.behavior_tools import get_behavior_snapshot
from tools.chat_history_tools import get_chat_counts
from tools.engagement_tools import get_engagement_snapshot
from tools.personal_memory_tools import load_personal_memory
from tools.progress_tracker_tools import get_progress_snapshot
from tools.student_insight_tools import get_student_architecture_snapshot, get_student_insight_snapshot
from tools.student_state_router import build_student_state_route, format_student_state_route
from backend.storage import get_storage_status


def _status_label(ok, warn=False):
    if ok and not warn:
        return "pass"
    if ok and warn:
        return "warn"
    return "fail"


def _count_memory_items(memory):
    return sum(
        len(memory.get(key, []))
        for key in ("known_people", "interests", "life_notes", "recent_checkins")
    )


def get_feature_health_snapshot(profile):
    name = profile["name"]
    memory = load_personal_memory(name)
    progress = get_progress_snapshot(name)
    analytics = get_analytics_summary(name)
    behavior = get_behavior_snapshot(profile)
    engagement = get_engagement_snapshot(name)
    chats = get_chat_counts(name)
    insight = get_student_insight_snapshot(profile)
    architecture = get_student_architecture_snapshot(profile)
    route = build_student_state_route(
        profile,
        conversation_mode="tutor",
        tutor_level=int(profile.get("default_tutor_level", 3) or 3),
        support_style=insight.get("support_style"),
        insight_snapshot=insight,
    )
    storage = get_storage_status()

    checks = [
        {
            "feature": "auth_profile",
            "status": _status_label(bool(profile.get("name")) and bool(profile.get("exams"))),
            "detail": f"Profile loaded for {name} with {len(profile.get('exams', []))} exam(s).",
        },
        {
            "feature": "tutor_memory",
            "status": _status_label(_count_memory_items(memory) > 0, warn=_count_memory_items(memory) < 3),
            "detail": f"Memory items: {_count_memory_items(memory)} | teaching quality: {insight.get('teaching_quality', 'building')}",
        },
        {
            "feature": "progress_tracking",
            "status": _status_label(progress.get("counts", {}).get("total", 0) > 0, warn=progress.get("topic_momentum", {}).get("mastery_signal") == "starting"),
            "detail": f"Total topics: {progress.get('counts', {}).get('total', 0)} | mastery: {progress.get('topic_momentum', {}).get('mastery_signal', 'starting')}",
        },
        {
            "feature": "practice_analytics",
            "status": _status_label(analytics.get("total_attempts", 0) > 0, warn=analytics.get("recent_accuracy", 0) < 55 if analytics.get("total_attempts", 0) else True),
            "detail": f"Attempts: {analytics.get('total_attempts', 0)} | recent accuracy: {analytics.get('recent_accuracy', 0)} | trend: {analytics.get('trend_signal', 'building')}",
        },
        {
            "feature": "behavior_model",
            "status": _status_label(len(behavior.get("events", [])) > 0, warn=behavior.get("last_analysis", {}).get("dropout_risk", "low") != "low"),
            "detail": f"Behavior events: {len(behavior.get('events', []))} | support: {behavior.get('last_analysis', {}).get('support_style', 'balanced_support')}",
        },
        {
            "feature": "engagement_loop",
            "status": _status_label(engagement.get("points", 0) > 0 or engagement.get("bond_messages", 0) > 0, warn=engagement.get("current_streak", 0) == 0),
            "detail": f"Points: {engagement.get('points', 0)} | streak: {engagement.get('current_streak', 0)} | league: {engagement.get('current_league', 'Bronze 1')}",
        },
        {
            "feature": "conversation_store",
            "status": _status_label(chats.get("total", 0) > 0, warn=chats.get("total", 0) < 5),
            "detail": f"Chats: {chats.get('total', 0)} | by mode: {', '.join(f'{k}:{v}' for k, v in (chats.get('by_mode') or {}).items()) or 'none'}",
        },
        {
            "feature": "routing_and_prompting",
            "status": _status_label(bool(route and route.get("teaching_adjustment")), warn=route.get("student_state", {}).get("academic_risk") == "high"),
            "detail": f"Next step: {route.get('next_step', '')} | teaching adjustment: {route.get('teaching_adjustment', '')}",
        },
        {
            "feature": "storage_backend",
            "status": _status_label(storage.get("ready", False)),
            "detail": f"Backend: {storage.get('backend', 'local')} | root: {storage.get('root', '')}",
        },
        {
            "feature": "architecture_view",
            "status": _status_label(bool(architecture.get("summary_line"))),
            "detail": architecture.get("summary_line", ""),
        },
    ]

    health_score = round(
        sum(1 for item in checks if item["status"] == "pass") / len(checks) * 100,
        1,
    ) if checks else 0

    return {
        "student_name": name,
        "health_score": health_score,
        "checks": checks,
        "summary": "Use this view as the feature-by-feature recheck panel: it highlights what is healthy, what is just starting, and what needs attention.",
    }
