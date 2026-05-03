from tools.behavior_tools import format_behavior_context
from tools.engagement_tools import load_engagement_state
from tools.planner_tools import get_exam_entries, load_planner_state
from tools.student_state_router import build_student_state_route, format_student_state_route
from tools.student_insight_tools import get_student_insight_snapshot


def _safe_profile(tool_context):
    return tool_context.state.get("profile") or {}


def get_student_context(tool_context):
    """Return the current student's profile and adaptive planning context."""

    profile = _safe_profile(tool_context)
    if not profile:
        return "No active student profile is available in session state."

    planner_state = load_planner_state(profile["name"])
    backlog_hours = planner_state.get("backlog_hours", {})
    current_day_plan = planner_state.get("current_day_plan")

    lines = [
        f"Student: {profile['name']}",
        f"Target exams: {', '.join(exam['name'] for exam in get_exam_entries(profile))}",
        f"Maximum study hours available: {profile.get('max_study_hours_per_day', profile.get('study_hours_per_day', 6))}",
        "",
        "Exam context:",
    ]

    for exam in get_exam_entries(profile):
        lines.append(f"- {exam['name']} on {exam['exam_date']}")
        for subject in exam["subjects"]:
            score = planner_state.get("mock_scores", {}).get(exam["name"], {}).get(subject, "not yet provided")
            backlog = round(float(backlog_hours.get(f"{exam['name']}::{subject}", 0)), 2)
            lines.append(f"  {subject}: mock {score}, backlog {backlog}")

    if current_day_plan:
        lines.extend(
            [
                "",
                f"Today's plan date: {current_day_plan['date']}",
                f"Today's plan status: {current_day_plan['status']}",
                f"Recommended study hours today: {current_day_plan.get('recommended_hours', 'not set')}",
                "Today's tasks:",
            ]
        )
        for task in current_day_plan.get("tasks", []):
            lines.append(f"- {task['exam']} | {task['subject']}: {task['hours']} hours")

    return "\n".join(lines)


def get_engagement_context(tool_context):
    """Return motivation and relationship-building context for the current student."""

    profile = _safe_profile(tool_context)
    if not profile:
        return "No active student profile is available in session state."

    engagement_state = load_engagement_state(profile["name"])
    preferred_persona = profile.get("preferred_persona") or "friendly study coach"

    lines = [
        "Engagement context:",
        f"- Preferred tutor persona inspiration: {preferred_persona}",
        f"- Points: {engagement_state['points']}",
        f"- Level: {engagement_state['level']}",
        f"- Current streak: {engagement_state['current_streak']}",
        f"- Relationship touchpoints so far: {engagement_state['bond_messages']}",
        "- Teaching tone should be warm, encouraging, and lightly conversational.",
        "- The tutor should feel like a trusted study companion, not a strict examiner.",
    ]

    return "\n".join(lines)


def get_behavior_context(tool_context):
    """Return recent and long-term study-behavior context for the current student."""

    profile = _safe_profile(tool_context)
    if not profile:
        return "No active student profile is available in session state."

    return format_behavior_context(profile)


def get_weakness_summary(tool_context):
    """Summarize weak and strong sections using stored mock performance."""

    profile = _safe_profile(tool_context)
    if not profile:
        return "No active student profile is available in session state."

    planner_state = load_planner_state(profile["name"])
    ranking = []
    for exam in get_exam_entries(profile):
        for subject in exam["subjects"]:
            score = planner_state.get("mock_scores", {}).get(exam["name"], {}).get(subject)
            if score is not None:
                ranking.append((score, exam["name"], subject))

    if not ranking:
        return (
            "No mock scores are available yet. Ask the student to take a trial mock "
            "and record section-wise scores first."
        )

    ranking.sort(key=lambda item: item[0])
    weakest = ranking[0]
    strongest = ranking[-1]

    lines = [
        "Weakness summary:",
        f"- Weakest section: {weakest[1]} | {weakest[2]} ({weakest[0]}/100)",
        f"- Strongest section: {strongest[1]} | {strongest[2]} ({strongest[0]}/100)",
        "- Section ranking from weakest to strongest:",
    ]

    for score, exam_name, subject in ranking:
        lines.append(f"- {exam_name} | {subject}: {score}/100")

    return "\n".join(lines)


def get_recovery_summary(tool_context):
    """Summarize missed-work backlog and recovery pressure."""

    profile = _safe_profile(tool_context)
    if not profile:
        return "No active student profile is available in session state."

    planner_state = load_planner_state(profile["name"])
    backlog_hours = planner_state.get("backlog_hours", {})
    total_backlog = round(sum(float(hours) for hours in backlog_hours.values()), 2)

    if total_backlog == 0:
        return (
            "Recovery summary:\n"
            "- No backlog is pending.\n"
            "- The student is on track with scheduled work."
        )

    lines = [
        "Recovery summary:",
        f"- Total backlog hours: {total_backlog}",
        "- Backlog split:",
    ]

    for exam in get_exam_entries(profile):
        for subject in exam["subjects"]:
            hours = round(float(backlog_hours.get(f"{exam['name']}::{subject}", 0)), 2)
            lines.append(f"- {exam['name']} | {subject}: {hours} hours")

    lines.extend(
        [
            "- Recommendation: prioritize the largest backlog in the next few study blocks.",
            "- Recommendation: keep weaker sections protected while redistributing missed work.",
        ]
    )

    return "\n".join(lines)


def get_tutor_intelligence_route(tool_context):
    """Return the unified intelligence route dictating tone, pressure, and focus."""
    profile = _safe_profile(tool_context)
    if not profile:
        return "No active student profile is available in session state."
    
    conversation_mode = tool_context.state.get("conversation_mode", "tutor")
    tutor_level = tool_context.state.get("tutor_level", 3)
    
    insight_snapshot = get_student_insight_snapshot(profile)
    route = build_student_state_route(
        profile, 
        conversation_mode=conversation_mode, 
        tutor_level=tutor_level, 
        support_style=insight_snapshot.get("support_style"),
        insight_snapshot=insight_snapshot
    )
    
    return format_student_state_route(route)
