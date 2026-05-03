from __future__ import annotations

from datetime import date, datetime


def _safe_exam_list(profile):
    exams = profile.get("exams") or []
    cleaned = []
    for exam in exams:
        name = str((exam or {}).get("name", "")).strip()
        subjects = [str(item).strip() for item in (exam or {}).get("subjects", []) if str(item).strip()]
        exam_date = str((exam or {}).get("exam_date", "")).strip()
        portion = str((exam or {}).get("portion", "")).strip()
        if name:
            cleaned.append(
                {
                    "name": name,
                    "subjects": subjects,
                    "exam_date": exam_date,
                    "portion": portion,
                }
            )
    if cleaned:
        return cleaned

    legacy_name = str(profile.get("exam", "")).strip()
    legacy_subjects = [str(item).strip() for item in profile.get("subjects", []) if str(item).strip()]
    legacy_date = str(profile.get("exam_date", "")).strip()
    if legacy_name:
        return [
            {
                "name": legacy_name,
                "subjects": legacy_subjects,
                "exam_date": legacy_date,
                "portion": "",
            }
        ]
    return []


def _days_until(exam_date):
    if not exam_date:
        return None
    try:
        parsed = datetime.strptime(exam_date, "%Y-%m-%d").date()
    except ValueError:
        return None
    return (parsed - date.today()).days


def _infer_track(name, subjects):
    return "jee"


def _track_strategy(track):
    return (
        "Focus on JEE Main and JEE Advanced first, then short revision loops, then a final recall pass. "
        "Keep it practical, time-aware, and centered on Physics, Chemistry, and Mathematics."
    )


def build_last_minute_revision_context(profile, user_input):
    exams = _safe_exam_list(profile)
    if not exams:
        return (
            "The student has not added any exam yet. Ask one short follow-up to identify the exam, "
            "the core subjects, and how much time is left, then build a last-minute revision plan."
        )

    lines = []
    lines.append(
        "This request is for the Last Minute tab. The student wants one-night-before or one-day-before revision help."
    )
    lines.append(
        "Treat this as a high-urgency revision sprint: prioritize coverage, retention, and confidence over perfect completeness."
    )
    lines.append(
        "Never overwhelm the student with a giant textbook-style explanation. Use a rescue-plan style answer with very clear headings and compact bullets."
    )
    lines.append(
        "Always include: syllabus coverage map, priority topics, revision order, what to skip if needed, what to memorize, and a final recall checklist."
    )
    lines.append(
        "The plan should aim to cover the entire specified portion. If full coverage is impossible in the available time, say that honestly and rank what must be covered first, second, and third."
    )

    max_hours = float(profile.get("max_study_hours_per_day", profile.get("study_hours_per_day", 4)) or 4)
    lines.append(f"The student's realistic upper study cap is about {round(max_hours, 1)} hours in one day.")

    tracks = []
    missing_portion_details = []
    for exam in exams:
        days_left = _days_until(exam["exam_date"])
        track = _infer_track(exam["name"], exam["subjects"])
        tracks.append(track)
        urgency = "date not set"
        if days_left is not None:
            if days_left <= 1:
                urgency = f"{days_left} day left"
            else:
                urgency = f"{days_left} days left"
        portion_note = f" Portion note: {exam['portion']}." if exam["portion"] else ""
        subject_text = ", ".join(exam["subjects"]) if exam["subjects"] else "subjects not specified yet"
        lines.append(
            f"- Exam: {exam['name']} | Track: {track} | Time left: {urgency} | Subjects: {subject_text}.{portion_note}"
        )
        if not exam["subjects"] or not exam["portion"]:
            missing_parts = []
            if not exam["subjects"]:
                missing_parts.append("subjects")
            if not exam["portion"]:
                missing_parts.append("portion")
            missing_portion_details.append(f"{exam['name']} ({', '.join(missing_parts)} missing)")

    primary_track = tracks[0] if tracks else "general"
    lines.append(f"Primary last-minute revision strategy: {_track_strategy(primary_track)}")
    lines.append(
        "For each exam, organize the answer subject by subject so the student can verify that nothing important from the stated portion is missed."
    )
    lines.append(
        "Within every subject, group the revision into: must-cover, should-cover, and if-time-remains."
    )
    lines.append(
        "End with a rapid final recall layer that helps the student revise the whole portion once more just before the exam."
    )
    if missing_portion_details:
        lines.append(
            "Some exam details are incomplete, so do not pretend the coverage is complete. "
            f"Explicitly tell the student to add the missing details for: {', '.join(missing_portion_details)}."
        )

    lowered = (user_input or "").lower()
    if "one night" in lowered or "tonight" in lowered:
        lines.append(
            "The student explicitly wants a one-night revision push. Break the plan into late-evening, midnight, early-morning, and final revision phases if helpful."
        )
    if any(word in lowered for word in ["revision", "last minute", "tomorrow", "before exam"]):
        lines.append(
            "The answer should feel like a practical revision rescue system, not a generic study plan."
        )
    if any(word in lowered for word in ["complete", "entire", "whole portion", "cover all", "everything"]):
        lines.append(
            "The student explicitly wants complete coverage of the specified portion. Build the answer like a coverage checklist and say clearly where time pressure may force prioritization."
        )

    lines.append(
        "Keep the answer user-friendly: section headers, numbered phases, and crisp bullets the student can act on immediately."
    )
    return "\n".join(lines)
