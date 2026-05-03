from tools.analytics_tools import get_analytics_summary
from tools.behavior_tools import get_behavior_snapshot, load_behavior_state
from tools.chat_history_tools import get_chat_counts
from tools.chat_outcome_tracker import (
    build_task_learning_context,
    get_difficult_topics,
    get_recurring_pain_points,
    get_teaching_effectiveness,
    get_task_learning_profiles,
    load_outcome_state,
)
from backend.storage import get_storage_status
from tools.learning_sources_tools import get_learning_source_pack
from tools.personal_memory_tools import load_personal_memory
from tools.progress_tracker_tools import get_progress_snapshot
from tools.student_state_router import build_student_state_route, format_student_state_route


def _recent_emotion_signal(memory):
    checkins = (memory or {}).get("recent_checkins", [])[-5:]
    if not checkins:
        return {"tone": "neutral", "confidence": "low", "keywords": []}

    negative_keywords = {
        "stress", "stressed", "anxious", "worried", "upset", "tired", "drained", "overwhelmed", "panic", "scared",
    }
    positive_keywords = {
        "ready", "calm", "good", "better", "confident", "motivated", "excited", "fresh",
    }

    neg_hits = 0
    pos_hits = 0
    matched = []
    for item in checkins:
        note = str(item.get("note", "")).lower()
        for keyword in negative_keywords:
            if keyword in note:
                neg_hits += 1
                matched.append(keyword)
        for keyword in positive_keywords:
            if keyword in note:
                pos_hits += 1
                matched.append(keyword)

    if neg_hits >= pos_hits + 2:
        tone = "negative"
    elif pos_hits >= neg_hits + 2:
        tone = "positive"
    else:
        tone = "mixed"

    return {
        "tone": tone,
        "confidence": "medium" if checkins else "low",
        "keywords": sorted(set(matched))[:8],
    }


def _emotional_state(behavior, analytics, emotion_signal):
    support_style = behavior.get("support_style", "balanced_support")
    recent_counts = behavior.get("recent_signal_counts", {})
    if recent_counts.get("burnout", 0) >= 2 or support_style == "gentle_recovery":
        return "overwhelmed"
    if recent_counts.get("anxiety", 0) >= 2 or emotion_signal["tone"] == "negative":
        return "strained"
    if analytics.get("recent_accuracy", 0) >= 75 and behavior.get("pacing_style") == "stretch":
        return "confident"
    if recent_counts.get("motivation", 0) >= 2 or emotion_signal["tone"] == "positive":
        return "energized"
    return "steady"


def _academic_risk(behavior, analytics, progress):
    risk_points = 0
    if behavior.get("dropout_risk") == "high":
        risk_points += 3
    elif behavior.get("dropout_risk") == "medium":
        risk_points += 1

    if analytics.get("recent_accuracy", 0) and analytics.get("recent_accuracy", 0) < 55:
        risk_points += 2
    if analytics.get("speed_signal") == "slow":
        risk_points += 1

    counts = progress.get("counts", {})
    if counts.get("pending", 0) >= 8:
        risk_points += 2
    elif counts.get("pending", 0) >= 4:
        risk_points += 1
    if counts.get("revise", 0) >= 6:
        risk_points += 1

    if risk_points >= 5:
        return "high"
    if risk_points >= 2:
        return "medium"
    return "low"


def _coaching_actions(behavior, analytics, progress, emotional_state):
    actions = []
    counts = progress.get("counts", {})
    topic_momentum = progress.get("topic_momentum", {})
    mastery_signal = topic_momentum.get("mastery_signal", "starting")

    if emotional_state in {"overwhelmed", "strained"}:
        actions.append("Use a calmer tone, smaller study blocks, and reassurance before increasing difficulty.")
    if counts.get("pending", 0):
        actions.append("Bring pending topics back into the next plan before adding too many new areas.")
    if counts.get("revise", 0):
        actions.append("Schedule explicit revision passes for brown-mark topics so they do not quietly decay.")
    if analytics.get("recent_accuracy", 0) and analytics.get("recent_accuracy", 0) < 60:
        actions.append("Prioritize accuracy rebuild before pushing speed or harder question difficulty.")
    if analytics.get("speed_signal") == "slow":
        actions.append("Add timed mini-sets and short pressure drills to improve speed without panic.")
    if mastery_signal in {"fragile", "starting"} and counts.get("done", 0):
        actions.append("Reinforce recently done topics with short recall checks so they do not fade.")
    if topic_momentum.get("weakest_topics"):
        actions.append("Begin the next explanation from the weakest tracked topic and check understanding early.")
    if not actions:
        actions.append("Keep a balanced rhythm of concept learning, practice, and revision.")

    return actions[:4]


def _topic_memory_summary(hard_topics, pain_points, progress):
    topic_momentum = progress.get("topic_momentum", {})
    mastery_signal = topic_momentum.get("mastery_signal", "starting")
    next_focus = topic_momentum.get("next_focus", "")
    weak_topics = topic_momentum.get("weakest_topics", [])
    strong_topics = topic_momentum.get("strongest_topics", [])

    if pain_points:
        primary = pain_points[0]["key"]
        return {
            "mastery_signal": mastery_signal,
            "primary_weak_topic": primary,
            "weak_topics": [item["key"] for item in pain_points[:3]],
            "strong_topics": [item["key"] for item in hard_topics[:3] if item.get("difficulty_score", 0) < 45] or strong_topics[:3],
            "next_teaching_adjustment": (
                f"Revisit {primary} with smaller steps, a different analogy, and one comprehension check at the end."
            ),
            "next_focus": next_focus,
        }

    if weak_topics:
        primary = weak_topics[0]
        return {
            "mastery_signal": mastery_signal,
            "primary_weak_topic": primary,
            "weak_topics": weak_topics[:3],
            "strong_topics": strong_topics[:3],
            "next_teaching_adjustment": f"Start from {primary} and keep the explanation short, visual, and check-backed.",
            "next_focus": next_focus,
        }

    if strong_topics:
        return {
            "mastery_signal": mastery_signal,
            "primary_weak_topic": "",
            "weak_topics": [],
            "strong_topics": strong_topics[:3],
            "next_teaching_adjustment": "The student looks stable here. Use a slightly higher challenge and one stretch question.",
            "next_focus": next_focus,
        }

    return {
        "mastery_signal": mastery_signal,
        "primary_weak_topic": "",
        "weak_topics": [],
        "strong_topics": [],
        "next_teaching_adjustment": next_focus or "Keep the next step small and clear.",
        "next_focus": next_focus,
    }


def get_student_insight_snapshot(profile):
    name = profile["name"]
    behavior = get_behavior_snapshot(profile)
    analytics = get_analytics_summary(name)
    progress = get_progress_snapshot(name)
    memory = load_personal_memory(name)
    emotion_signal = _recent_emotion_signal(memory)
    emotional_state = _emotional_state(behavior, analytics, emotion_signal)
    academic_risk = _academic_risk(behavior, analytics, progress)

    # Self-learning signals
    teaching_eff = get_teaching_effectiveness(name)
    hard_topics = get_difficult_topics(name, max_topics=3)
    pain_points = get_recurring_pain_points(name, min_re_asks=2)
    task_profiles = get_task_learning_profiles(name)
    topic_memory = _topic_memory_summary(hard_topics, pain_points, progress)

    return {
        "student_name": name,
        "support_style": behavior.get("support_style", "balanced_support"),
        "pacing_style": behavior.get("pacing_style", "steady"),
        "dropout_risk": behavior.get("dropout_risk", "low"),
        "sentiment_trend": emotion_signal["tone"],
        "emotional_state": emotional_state,
        "emotion_keywords": emotion_signal["keywords"],
        "academic_risk": academic_risk,
        "recent_accuracy": analytics.get("recent_accuracy", 0),
        "recent_speed_signal": analytics.get("speed_signal", "steady"),
        "difficulty_signal": analytics.get("difficulty_signal", "foundation"),
        "trend_signal": analytics.get("trend_signal", "building"),
        "focus_recommendation": analytics.get("focus_recommendation", ""),
        "top_exam_focus": analytics.get("top_exam_focus", ""),
        "top_mode_focus": analytics.get("top_mode_focus", ""),
        "pending_topics": progress.get("counts", {}).get("pending", 0),
        "revise_topics": progress.get("counts", {}).get("revise", 0),
        "done_topics": progress.get("counts", {}).get("done", 0),
        "coach_note": analytics.get("coach_note", ""),
        "progress_reminders": progress.get("reminders", []),
        "coaching_actions": _coaching_actions(behavior, analytics, progress, emotional_state),
        "teaching_quality": teaching_eff.get("quality_signal", "building"),
        "comprehension_rate": teaching_eff.get("comprehension_rate", 0),
        "re_ask_rate": teaching_eff.get("re_ask_rate", 0),
        "hardest_topics": [t["key"] for t in hard_topics],
        "pain_point_topics": [t["key"] for t in pain_points],
        "topic_mastery": topic_memory,
        "task_learning_profiles": task_profiles,
        "task_learning_summary": build_task_learning_context(name) if task_profiles else "",
    }


def _gentle_architecture_suggestion(insight, route):
    trend = insight.get("trend_signal", "building")
    focus = (insight.get("focus_recommendation") or "").strip()
    route_name = (route.get("label") or route.get("next_step") or "the current rhythm").strip()

    if trend == "dipping":
        return f"Optional suggestion: keep {route_name.lower()} light for now, and try one short confidence-building practice set when you feel ready."
    if trend == "improving":
        if focus:
            return f"Optional suggestion: continue {route_name.lower()} and spend a little extra time on {focus.lower()}."
        return f"Optional suggestion: keep following {route_name.lower()} and build on the momentum you already have."
    if focus:
        return f"Optional suggestion: stay with {route_name.lower()} and gently revisit {focus.lower()} when it feels comfortable."
    return f"Optional suggestion: keep following {route_name.lower()} at a pace that feels comfortable."


def get_student_architecture_snapshot(profile):
    insight = get_student_insight_snapshot(profile)
    storage = get_storage_status()
    chats = get_chat_counts(profile["name"])
    memory = load_personal_memory(profile["name"])
    outcome_state = load_outcome_state(profile["name"])
    route = build_student_state_route(
        profile,
        conversation_mode="tutor",
        tutor_level=int(profile.get("default_tutor_level", 3) or 3),
        support_style=insight.get("support_style"),
        insight_snapshot=insight,
    )
    source_pack = get_learning_source_pack(profile, student_state_route=route)
    gentle_suggestion = _gentle_architecture_suggestion(insight, route)

    return {
        "student_name": profile["name"],
        "storage_backend": storage.get("backend", "local"),
        "storage_ready": storage.get("ready", False),
        "profile_saved": True,
        "progress_items": insight.get("done_topics", 0) + insight.get("revise_topics", 0) + insight.get("pending_topics", 0),
        "chat_messages": chats.get("total", 0),
        "practice_attempts": get_analytics_summary(profile["name"]).get("total_attempts", 0),
        "memory_items": len(memory.get("known_people", []))
        + len(memory.get("interests", []))
        + len(memory.get("life_notes", []))
        + len(memory.get("recent_checkins", [])),
        "behavior_events": len((load_behavior_state(profile["name"]) or {}).get("events", [])),
        "outcome_records": len(outcome_state.get("outcomes", [])),
        "source_pack": source_pack,
        "student_state_route": route,
        "student_state_route_text": format_student_state_route(route),
        "next_step": route.get("next_step", "Start with the smallest useful action and grow from there."),
        "focus_recommendation": insight.get("focus_recommendation", ""),
        "analytics_trend": insight.get("trend_signal", "building"),
        "gentle_suggestion": gentle_suggestion,
        "summary_line": "Astra is combining storage, behavior, progress, analytics, topic memory, and route logic into one adaptive view.",
    }


def build_student_insight_context(profile):
    insight = get_student_insight_snapshot(profile)
    lines = [
        "Student insight snapshot:",
        f"- Sentiment trend: {insight['sentiment_trend']}",
        f"- Emotional state: {insight['emotional_state']}",
        f"- Academic risk: {insight['academic_risk']}",
        f"- Support style: {insight['support_style']}",
        f"- Pacing style: {insight['pacing_style']}",
        f"- Recent accuracy: {insight['recent_accuracy']}",
        f"- Recent speed signal: {insight['recent_speed_signal']}",
        f"- Practice trend: {insight['trend_signal']}",
        f"- Practice focus recommendation: {insight['focus_recommendation']}",
        f"- Pending topics: {insight['pending_topics']}",
        f"- Needs-revision topics: {insight['revise_topics']}",
    ]
    if insight["coach_note"]:
        lines.append(f"- Analytics coach note: {insight['coach_note']}")
    topic_mastery = insight.get("topic_mastery") or {}
    if topic_mastery.get("mastery_signal"):
        lines.append(f"- Topic mastery signal: {topic_mastery.get('mastery_signal')}")
    if topic_mastery.get("next_teaching_adjustment"):
        lines.append(f"- Next teaching adjustment: {topic_mastery.get('next_teaching_adjustment')}")
    if topic_mastery.get("weak_topics"):
        lines.append(f"- Weak topic memory: {', '.join(topic_mastery.get('weak_topics', [])[:3])}")
    if topic_mastery.get("strong_topics"):
        lines.append(f"- Strong topic memory: {', '.join(topic_mastery.get('strong_topics', [])[:3])}")
    if insight["emotion_keywords"]:
        lines.append(f"- Emotion keywords seen recently: {', '.join(insight['emotion_keywords'])}")
    if insight.get("teaching_quality") and insight["teaching_quality"] != "building":
        lines.append(f"- Teaching quality: {insight['teaching_quality']} (comprehension {insight.get('comprehension_rate', 0)}%, re-ask {insight.get('re_ask_rate', 0)}%)")
    if insight.get("hardest_topics"):
        lines.append(f"- Hardest topics: {', '.join(insight['hardest_topics'][:3])}")
    if insight.get("pain_point_topics"):
        lines.append(f"- Pain points (keeps re-asking): {', '.join(insight['pain_point_topics'][:3])}")
    if insight.get("task_learning_summary"):
        lines.append("- Task learning summary:")
        for item in insight["task_learning_summary"].splitlines()[:6]:
            lines.append(f"  {item}")
    if insight["progress_reminders"]:
        lines.append("- Progress reminders:")
        for item in insight["progress_reminders"][:3]:
            lines.append(f"  - {item}")
    if insight["coaching_actions"]:
        lines.append("- Recommended coaching actions:")
        for item in insight["coaching_actions"]:
            lines.append(f"  - {item}")
    lines.append(
        "Use this snapshot to adapt tone, pacing, difficulty, reminders, and study planning so the student feels supported without being overwhelmed."
    )
    return "\n".join(lines)


def build_tutor_brief_insight_context(profile):
    insight = get_student_insight_snapshot(profile)
    lines = [
        "Student insight snapshot (tutor brief):",
        f"- Emotional state: {insight['emotional_state']}",
        f"- Academic risk: {insight['academic_risk']}",
        f"- Support style: {insight['support_style']}",
        f"- Practice trend: {insight['trend_signal']}",
    ]
    if insight["focus_recommendation"]:
        lines.append(f"- Practice focus recommendation: {insight['focus_recommendation']}")
    if insight["coach_note"]:
        lines.append(f"- Coach note: {insight['coach_note']}")
    topic_mastery = insight.get("topic_mastery") or {}
    if topic_mastery.get("next_teaching_adjustment"):
        lines.append(f"- Teaching adjustment: {topic_mastery.get('next_teaching_adjustment')}")
    if topic_mastery.get("weak_topics"):
        lines.append(f"- Weak topics to remember: {', '.join(topic_mastery.get('weak_topics', [])[:3])}")
    if insight.get("task_learning_profiles"):
        active_modes = sorted(
            insight["task_learning_profiles"].values(),
            key=lambda item: (-item.get("interactions", 0), item.get("mode", "")),
        )[:3]
        if active_modes:
            lines.append("- Task learning signals:")
            for item in active_modes:
                lines.append(
                    f"  - {item['mode_label']}: recent accuracy {item['recent_accuracy']}%, "
                    f"trend {item['trend_signal']}, adaptation {item['adaptation']}"
                )
    lines.append("Use this brief snapshot to stay academic, clear, and lightly adaptive.")
    return "\n".join(lines)
