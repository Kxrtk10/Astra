import json
import os
import time
from collections import defaultdict
from datetime import datetime, timedelta
from statistics import mean

from backend.database import execute_query, fetch_json_record, upsert_json_record
from backend.storage import atomic_write_json
from tools.jee_syllabus import build_chapter_ready_syllabus

try:
    from google import genai
except Exception:  # pragma: no cover - optional dependency
    genai = None

ANALYTICS_FOLDER = "analytics_state"


def _analytics_path(name):
    if not os.path.exists(ANALYTICS_FOLDER):
        os.makedirs(ANALYTICS_FOLDER)
    return os.path.join(ANALYTICS_FOLDER, f"{name}.json")


def _timestamp():
    return datetime.utcnow().isoformat(timespec="seconds")


def _normalize_mode_key(mode):
    return str(mode or "general").strip().lower() or "general"


def _default_state():
    return {
        "practice_attempts": [],
        "attempts_by_mode": {},
        "attempts_by_exam": {},
        "checkpoint_attempts": [],
        "checkpoint_attempts_by_topic": {},
        "checkpoint_attempts_by_exam": {},
        "last_updated": "",
    }


def _normalize_state(state):
    state.setdefault("practice_attempts", [])
    state.setdefault("attempts_by_mode", {})
    state.setdefault("attempts_by_exam", {})
    state.setdefault("checkpoint_attempts", [])
    state.setdefault("checkpoint_attempts_by_topic", {})
    state.setdefault("checkpoint_attempts_by_exam", {})
    state.setdefault("last_updated", "")
    return state


def _load_state_from_db(name):
    raw = fetch_json_record("student_analytics", "student_name", name, "state_json")
    if not raw:
        return None
    return _normalize_state(json.loads(raw))


def _save_state_to_db(name, state):
    upsert_json_record(
        "student_analytics",
        "student_name",
        name,
        "state_json",
        json.dumps(state, indent=2),
        _timestamp(),
    )


def load_analytics_state(name):
    state = _load_state_from_db(name)
    if state is not None:
        return state

    filepath = _analytics_path(name)
    if not os.path.exists(filepath):
        return _default_state()

    with open(filepath, "r", encoding="utf-8") as file:
        state = json.load(file)

    state = _normalize_state(state)
    _save_state_to_db(name, state)
    return state


def save_analytics_state(name, state):
    filepath = _analytics_path(name)
    state = _normalize_state(state)
    atomic_write_json(filepath, state)
    _save_state_to_db(name, state)


def record_checkpoint_attempt(
    name,
    topic,
    subject,
    is_correct,
    question="",
    student_answer="",
    correct_answer="",
    explanation_level=3,
    exam="",
    feedback="",
):
    state = load_analytics_state(name)
    attempt = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "topic": str(topic or "").strip(),
        "subject": str(subject or "").strip(),
        "exam": str(exam or "").strip(),
        "question": str(question or "").strip(),
        "student_answer": str(student_answer or "").strip(),
        "correct_answer": str(correct_answer or "").strip(),
        "explanation_level": int(explanation_level or 3),
        "is_correct": bool(is_correct),
        "feedback": str(feedback or "").strip(),
    }
    state["checkpoint_attempts"].append(attempt)
    state["checkpoint_attempts"] = state["checkpoint_attempts"][-120:]
    topic_key = attempt["topic"].strip().lower() or "general"
    exam_key = attempt["exam"].strip().upper() or "GENERAL"
    state["checkpoint_attempts_by_topic"][topic_key] = int(state["checkpoint_attempts_by_topic"].get(topic_key, 0) or 0) + 1
    state["checkpoint_attempts_by_exam"][exam_key] = int(state["checkpoint_attempts_by_exam"].get(exam_key, 0) or 0) + 1
    state["last_updated"] = attempt["timestamp"]
    save_analytics_state(name, state)
    return state


def record_practice_attempt(
    name,
    mode,
    time_taken_minutes,
    accuracy_percent,
    exam="",
    notes="",
    question_count=0,
):
    state = load_analytics_state(name)
    attempt = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "mode": mode,
        "exam": exam,
        "time_taken_minutes": round(float(time_taken_minutes), 2),
        "accuracy_percent": round(float(accuracy_percent), 2),
        "question_count": int(question_count or 0),
        "notes": notes.strip(),
    }
    state["practice_attempts"].append(attempt)
    state["practice_attempts"] = state["practice_attempts"][-60:]
    mode_key = str(mode or "general").strip().lower() or "general"
    exam_key = str(exam or "").strip().upper() or "GENERAL"
    state["attempts_by_mode"][mode_key] = int(state["attempts_by_mode"].get(mode_key, 0) or 0) + 1
    state["attempts_by_exam"][exam_key] = int(state["attempts_by_exam"].get(exam_key, 0) or 0) + 1
    state["last_updated"] = attempt["timestamp"]
    save_analytics_state(name, state)
    return state


def record_engagement(student_id, topic, duration_minutes, session_type="learn"):
    state = load_analytics_state(student_id)
    state.setdefault("engagement_log", [])
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "topic": str(topic or "").strip(),
        "duration_minutes": round(float(duration_minutes or 0), 2),
        "session_type": str(session_type or "learn").strip().lower(),
    }
    state["engagement_log"].append(entry)
    state["engagement_log"] = state["engagement_log"][-120:]
    state["last_updated"] = entry["timestamp"]
    save_analytics_state(student_id, state)
    return state


def record_session_analytics(student_id, topic, duration_minutes, score, session_type, subject="", exam=""):
    state = load_analytics_state(student_id)
    state.setdefault("session_analytics", [])
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "topic": str(topic or "").strip(),
        "subject": str(subject or "").strip(),
        "exam": str(exam or "").strip(),
        "duration_minutes": round(float(duration_minutes or 0), 2),
        "score": round(float(score or 0), 1),
        "session_type": str(session_type or "learn").strip().lower(),
        "confidence_level": "strong" if float(score or 0) >= 85 else "good" if float(score or 0) >= 75 else "medium" if float(score or 0) >= 60 else "low",
    }
    state["session_analytics"].append(entry)
    state["session_analytics"] = state["session_analytics"][-180:]
    mode_key = _normalize_mode_key(session_type)
    state["attempts_by_mode"][mode_key] = int(state["attempts_by_mode"].get(mode_key, 0) or 0) + 1
    state["last_updated"] = entry["timestamp"]
    save_analytics_state(student_id, state)
    return state


def record_subtopic_score(student_id, unit_name, subtopic_id, score, duration_minutes, subject="", session_type="chapter"):
    state = load_analytics_state(student_id)
    state.setdefault("subtopic_scores", [])
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "unit_name": str(unit_name or "").strip(),
        "subtopic_id": str(subtopic_id or "").strip(),
        "subject": str(subject or "").strip(),
        "score": round(float(score or 0), 1),
        "duration_minutes": round(float(duration_minutes or 0), 2),
        "session_type": str(session_type or "chapter").strip().lower(),
    }
    state["subtopic_scores"].append(entry)
    state["subtopic_scores"] = state["subtopic_scores"][-240:]
    state["last_updated"] = entry["timestamp"]
    save_analytics_state(student_id, state)
    return state


def record_chapter_completion(student_id, unit_name, subject, score, mastery_level, time_taken_minutes, answers=None):
    state = load_analytics_state(student_id)
    state.setdefault("chapter_completions", [])
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "unit_name": str(unit_name or "").strip(),
        "subject": str(subject or "").strip(),
        "score": round(float(score or 0), 1),
        "mastery_level": str(mastery_level or "developing").strip().lower(),
        "time_taken_minutes": round(float(time_taken_minutes or 0), 2),
        "answers_count": len(answers) if isinstance(answers, (list, dict)) else 0,
    }
    state["chapter_completions"].append(entry)
    state["chapter_completions"] = state["chapter_completions"][-120:]
    state["last_updated"] = entry["timestamp"]
    save_analytics_state(student_id, state)
    return state


def _trend_signal(recent_accuracy, earlier_accuracy):
    if earlier_accuracy <= 0:
        return "building"
    delta = round(recent_accuracy - earlier_accuracy, 1)
    if delta >= 6:
        return "improving"
    if delta <= -6:
        return "dipping"
    return "steady"


def _build_mode_profiles(attempts):
    grouped = {}
    for attempt in attempts:
        mode_key = _normalize_mode_key(attempt.get("mode"))
        grouped.setdefault(mode_key, []).append(attempt)

    profiles = {}
    for mode_key, mode_attempts in grouped.items():
        total = len(mode_attempts)
        average_time = round(sum(item["time_taken_minutes"] for item in mode_attempts) / total, 2) if total else 0
        average_accuracy = round(sum(item["accuracy_percent"] for item in mode_attempts) / total, 2) if total else 0
        recent = mode_attempts[-5:]
        recent_accuracy = round(sum(item["accuracy_percent"] for item in recent) / len(recent), 2) if recent else 0
        recent_time = round(sum(item["time_taken_minutes"] for item in recent) / len(recent), 2) if recent else 0
        earlier = mode_attempts[-10:-5]
        earlier_accuracy = (
            round(sum(item["accuracy_percent"] for item in earlier) / len(earlier), 2)
            if earlier
            else 0
        )
        trend = _trend_signal(recent_accuracy, earlier_accuracy)

        if recent_accuracy >= 82:
            difficulty_signal = "stretch"
        elif recent_accuracy >= 68:
            difficulty_signal = "challenging"
        elif recent_accuracy >= 52:
            difficulty_signal = "moderate"
        else:
            difficulty_signal = "foundation"

        if recent_time <= 8:
            speed_signal = "fast"
        elif recent_time <= 18:
            speed_signal = "steady"
        else:
            speed_signal = "slow"

        if recent_accuracy < 55:
            coach_note = "This mode still needs simpler steps, shorter sets, and clearer correction."
        elif speed_signal == "slow":
            coach_note = "This mode is accurate enough, but it needs more time discipline and shorter drills."
        elif trend == "improving":
            coach_note = "This mode is improving. Astra can raise the challenge a little."
        elif trend == "dipping":
            coach_note = "This mode is dipping. Astra should reduce pressure and rebuild confidence."
        else:
            coach_note = "This mode looks stable. Keep the current rhythm and refine the details."

        if recent_accuracy < 55:
            focus_recommendation = "Rebuild accuracy with smaller, easier sets in this mode."
        elif speed_signal == "slow":
            focus_recommendation = "Use tighter timed work to improve pace in this mode."
        elif trend == "improving":
            focus_recommendation = "Keep the momentum and add a little more challenge in this mode."
        else:
            focus_recommendation = "Keep a balanced mix of practice, review, and correction in this mode."

        profiles[mode_key] = {
            "attempts": total,
            "average_time_minutes": average_time,
            "average_accuracy": average_accuracy,
            "recent_accuracy": recent_accuracy,
            "recent_time_minutes": recent_time,
            "difficulty_signal": difficulty_signal,
            "speed_signal": speed_signal,
            "trend_signal": trend,
            "focus_recommendation": focus_recommendation,
            "coach_note": coach_note,
        }

    return profiles


def get_analytics_summary(name):
    state = load_analytics_state(name)
    attempts = state.get("practice_attempts", [])
    checkpoint_attempts = state.get("checkpoint_attempts", [])
    if not attempts:
        checkpoint_total = len(checkpoint_attempts)
        checkpoint_correct = sum(1 for item in checkpoint_attempts if item.get("is_correct"))
        return {
            "total_attempts": 0,
            "average_time_minutes": 0,
            "average_accuracy": 0,
            "recent_accuracy": 0,
            "recent_time_minutes": 0,
            "difficulty_signal": "foundation",
            "speed_signal": "steady",
            "trend_signal": "building",
            "focus_recommendation": "Start logging a few practice attempts to build a learning profile.",
            "top_exam_focus": "",
            "top_mode_focus": "",
            "coach_note": "No timed practice data yet. Start logging attempts to build your speed and accuracy profile.",
            "attempts": [],
            "attempts_by_exam": {},
            "attempts_by_mode": {},
            "mode_profiles": {},
            "total_checkpoint_attempts": checkpoint_total,
            "checkpoint_accuracy": round((checkpoint_correct / checkpoint_total * 100), 1) if checkpoint_total else 0,
            "checkpoint_attempts": checkpoint_attempts[-10:],
            "checkpoint_attempts_by_topic": dict(sorted((state.get("checkpoint_attempts_by_topic") or {}).items(), key=lambda item: item[1], reverse=True)),
            "checkpoint_attempts_by_exam": dict(sorted((state.get("checkpoint_attempts_by_exam") or {}).items(), key=lambda item: item[1], reverse=True)),
        }

    avg_time = round(sum(item["time_taken_minutes"] for item in attempts) / len(attempts), 2)
    avg_accuracy = round(sum(item["accuracy_percent"] for item in attempts) / len(attempts), 2)
    recent = attempts[-5:]
    recent_accuracy = round(sum(item["accuracy_percent"] for item in recent) / len(recent), 2)
    recent_time = round(sum(item["time_taken_minutes"] for item in recent) / len(recent), 2)
    earlier = attempts[-10:-5]
    earlier_accuracy = round(sum(item["accuracy_percent"] for item in earlier) / len(earlier), 2) if earlier else 0
    trend_signal = _trend_signal(recent_accuracy, earlier_accuracy)

    if recent_accuracy >= 82:
        difficulty_signal = "stretch"
    elif recent_accuracy >= 68:
        difficulty_signal = "challenging"
    elif recent_accuracy >= 52:
        difficulty_signal = "moderate"
    else:
        difficulty_signal = "foundation"

    if recent_time <= 8:
        speed_signal = "fast"
    elif recent_time <= 18:
        speed_signal = "steady"
    else:
        speed_signal = "slow"

    attempts_by_mode = dict(sorted((state.get("attempts_by_mode") or {}).items(), key=lambda item: item[1], reverse=True))
    attempts_by_exam = dict(sorted((state.get("attempts_by_exam") or {}).items(), key=lambda item: item[1], reverse=True))
    mode_profiles = _build_mode_profiles(attempts)
    if mode_profiles:
        weakest_mode = min(
            mode_profiles.items(),
            key=lambda item: (item[1].get("recent_accuracy", 0), -item[1].get("attempts", 0)),
        )[0]
        strongest_mode = max(
            mode_profiles.items(),
            key=lambda item: (item[1].get("recent_accuracy", 0), item[1].get("attempts", 0)),
        )[0]
        top_mode_focus = weakest_mode
    else:
        top_mode_focus = next(iter(attempts_by_mode.keys()), "")
        strongest_mode = top_mode_focus
    top_exam_focus = next(iter(attempts_by_exam.keys()), "")

    if recent_accuracy < 55:
        coach_note = "Accuracy is still unstable. Slow down a little, review mistakes, and rebuild confidence before increasing speed."
    elif speed_signal == "slow":
        coach_note = "Accuracy looks workable, but speed is lagging. Use more timed mini-sets and section drills."
    elif difficulty_signal == "stretch":
        coach_note = "You are handling current practice well. It is safe to increase difficulty and paper pressure gradually."
    elif trend_signal == "improving":
        coach_note = "Your recent practice trend is improving. Keep the current rhythm and add a little more challenge."
    elif trend_signal == "dipping":
        coach_note = "Recent practice is dipping a little. Reduce pressure, review weak spots, and rebuild confidence first."
    else:
        coach_note = "You are moving in the right direction. Keep balancing timed practice with careful review."

    if recent_accuracy < 55:
        focus_recommendation = "Rebuild accuracy first with easier, shorter question sets."
    elif speed_signal == "slow":
        focus_recommendation = "Use timed mini-sets to improve speed without increasing panic."
    elif trend_signal == "improving":
        focus_recommendation = "Push a little harder with a higher-quality question mix."
    else:
        focus_recommendation = "Keep a balanced mix of concept review, timed drills, and revision."

    return {
        "total_attempts": len(attempts),
        "average_time_minutes": avg_time,
        "average_accuracy": avg_accuracy,
        "recent_accuracy": recent_accuracy,
        "recent_time_minutes": recent_time,
        "difficulty_signal": difficulty_signal,
        "speed_signal": speed_signal,
        "trend_signal": trend_signal,
        "focus_recommendation": focus_recommendation,
        "top_exam_focus": top_exam_focus,
        "top_mode_focus": top_mode_focus,
        "strongest_mode_focus": strongest_mode,
        "coach_note": coach_note,
        "attempts": attempts[-10:],
        "attempts_by_exam": attempts_by_exam,
        "attempts_by_mode": attempts_by_mode,
        "mode_profiles": mode_profiles,
        "total_checkpoint_attempts": len(checkpoint_attempts),
        "checkpoint_accuracy": round((sum(1 for item in checkpoint_attempts if item.get("is_correct")) / len(checkpoint_attempts) * 100), 1) if checkpoint_attempts else 0,
        "checkpoint_attempts": checkpoint_attempts[-10:],
        "checkpoint_attempts_by_topic": dict(sorted((state.get("checkpoint_attempts_by_topic") or {}).items(), key=lambda item: item[1], reverse=True)),
        "checkpoint_attempts_by_exam": dict(sorted((state.get("checkpoint_attempts_by_exam") or {}).items(), key=lambda item: item[1], reverse=True)),
    }


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _normalize_subject_label(subject):
    label = str(subject or "").strip().lower()
    if "phys" in label:
        return "physics"
    if "chem" in label:
        return "chemistry"
    if "math" in label:
        return "mathematics"
    return label or "general"


def _load_dashboard_cache(student_id):
    state = load_analytics_state(student_id)
    cache = state.get("dashboard_insight_cache") or {}
    generated_at = cache.get("generated_at", "")
    if generated_at:
        try:
            cached_dt = datetime.fromisoformat(generated_at)
            if (datetime.utcnow() - cached_dt).total_seconds() < 3600:
                return cache
        except Exception:
            pass
    return None


def _save_dashboard_cache(student_id, insight):
    state = load_analytics_state(student_id)
    state["dashboard_insight_cache"] = {
        "insight": insight,
        "generated_at": datetime.utcnow().isoformat(timespec="seconds"),
    }
    state["last_updated"] = state["dashboard_insight_cache"]["generated_at"]
    save_analytics_state(student_id, state)


def get_performance_trends(student_id, days=30):
    try:
        rows = execute_query(
            """
            SELECT DATE(recorded_at) AS day, subject, score, duration_minutes
            FROM progress_records
            WHERE student_id = ? AND recorded_at >= datetime('now', ?)
            ORDER BY recorded_at ASC, id ASC
            """,
            (student_id, f"-{int(days or 30)} days"),
        ) or []
        daily_map = defaultdict(lambda: {"scores": [], "sessions": 0, "minutes": 0})
        subject_map = defaultdict(lambda: {"scores": [], "sessions": 0})
        total_sessions = 0
        total_minutes = 0
        for row in rows:
            day = str(row["day"] or "").strip()
            subject = _normalize_subject_label(row["subject"])
            score = _safe_float(row["score"])
            duration = _safe_float(row["duration_minutes"])
            if not day:
                continue
            daily_map[day]["scores"].append(score)
            daily_map[day]["sessions"] += 1
            daily_map[day]["minutes"] += duration
            subject_map[subject]["scores"].append(score)
            subject_map[subject]["sessions"] += 1
            total_sessions += 1
            total_minutes += duration

        daily_scores = [
            {
                "date": day,
                "avg_score": round(mean(bucket["scores"]), 1) if bucket["scores"] else 0,
                "sessions": bucket["sessions"],
                "minutes": round(bucket["minutes"], 1),
            }
            for day, bucket in sorted(daily_map.items())
        ]
        subject_averages = {
            subject: round(mean(bucket["scores"]), 1) if bucket["scores"] else 0
            for subject, bucket in subject_map.items()
        }
        recent = daily_scores[-7:]
        previous = daily_scores[-14:-7]
        recent_avg = round(mean([item["avg_score"] for item in recent]), 1) if recent else 0
        previous_avg = round(mean([item["avg_score"] for item in previous]), 1) if previous else 0
        weekly_improvement = round(recent_avg - previous_avg, 1)
        best_day = max(daily_scores, key=lambda item: (item["avg_score"], item["sessions"]))["date"] if daily_scores else ""
        consistency = get_study_consistency(student_id, days=min(7, max(int(days or 30), 7)))
        return {
            "daily_scores": daily_scores,
            "subject_averages": subject_averages,
            "weekly_improvement": weekly_improvement,
            "best_day": best_day,
            "consistency_score": consistency.get("consistency_percent", 0),
            "total_sessions": total_sessions,
            "total_time_minutes": int(round(total_minutes)),
        }
    except Exception as exc:
        print(f"WARNING: Could not build performance trends for {student_id}: {exc}")
        return {
            "daily_scores": [],
            "subject_averages": {},
            "weekly_improvement": 0,
            "best_day": "",
            "consistency_score": 0,
            "total_sessions": 0,
            "total_time_minutes": 0,
        }


def get_weak_strong_topics(student_id):
    try:
        rows = execute_query(
            """
            SELECT unit_name, subject, topic, score
            FROM progress_records
            WHERE student_id = ?
            ORDER BY recorded_at DESC, id DESC
            """,
            (student_id,),
        ) or []
        chapter_rows = execute_query(
            """
            SELECT unit_name, subject, subtopic_scores, chapter_test_score, attempts
            FROM chapter_scores
            WHERE student_id = ?
            ORDER BY completed_at DESC, id DESC
            """,
            (student_id,),
        ) or []
        topic_scores = defaultdict(list)
        attempted_topics = set()
        for row in rows:
            topic = str(row["topic"] or row["unit_name"] or "").strip()
            subject = _normalize_subject_label(row["subject"])
            score = _safe_float(row["score"])
            if topic:
                attempted_topics.add(topic.lower())
                topic_scores[(topic, subject)].append(score)
        for row in chapter_rows:
            subject = _normalize_subject_label(row["subject"])
            unit_name = str(row["unit_name"] or "").strip()
            chapter_score = _safe_float(row["chapter_test_score"])
            if unit_name:
                attempted_topics.add(unit_name.lower())
                topic_scores[(unit_name, subject)].append(chapter_score)
            try:
                subtopics = json.loads(row["subtopic_scores"] or "{}")
            except Exception:
                subtopics = {}
            if isinstance(subtopics, dict):
                for subtopic_name, subtopic_score in subtopics.items():
                    subtopic_label = str(subtopic_name or "").strip()
                    if subtopic_label:
                        attempted_topics.add(subtopic_label.lower())
                        topic_scores[(subtopic_label, subject)].append(_safe_float(subtopic_score))

        strong_topics = []
        weak_topics = []
        for (topic, subject), scores in sorted(topic_scores.items(), key=lambda item: item[0][0].lower()):
            if not scores:
                continue
            best_score = round(max(scores), 1)
            attempts = len(scores)
            entry = {
                "topic": topic,
                "subject": subject,
                "best_score": best_score,
                "attempts": attempts,
            }
            if best_score >= 80:
                strong_topics.append(entry)
            elif best_score < 60:
                entry["revision_recommended"] = True
                weak_topics.append(entry)

        syllabus = build_chapter_ready_syllabus()
        not_attempted = []
        for subject, units in syllabus.items():
            for unit in units:
                unit_name = str(unit.get("name") or "").strip()
                if unit_name and unit_name.lower() not in attempted_topics:
                    not_attempted.append(unit_name)

        return {
            "strong_topics": strong_topics[:20],
            "weak_topics": weak_topics[:20],
            "not_attempted": not_attempted[:40],
        }
    except Exception as exc:
        print(f"WARNING: Could not derive weak/strong topics for {student_id}: {exc}")
        return {"strong_topics": [], "weak_topics": [], "not_attempted": []}


def get_study_consistency(student_id, days=7):
    try:
        rows = execute_query(
            """
            SELECT DATE(recorded_at) AS day, SUM(duration_minutes) AS total_minutes
            FROM progress_records
            WHERE student_id = ? AND recorded_at >= datetime('now', ?)
            GROUP BY DATE(recorded_at)
            ORDER BY DATE(recorded_at) ASC
            """,
            (student_id, f"-{int(days or 7)} days"),
        ) or []
        studied_days = []
        minutes_by_day = {}
        for row in rows:
            day = str(row["day"] or "").strip()
            if day:
                studied_days.append(day)
                minutes_by_day[day] = int(round(_safe_float(row["total_minutes"])))
        studied_days_set = set(studied_days)
        total_days = max(int(days or 7), 1)
        days_studied = len(studied_days_set)
        days_missed = max(0, total_days - days_studied)
        avg_daily_minutes = round(sum(minutes_by_day.values()) / max(days_studied, 1), 1) if days_studied else 0
        consistency_percent = round((days_studied / total_days) * 100, 1)
        current_streak = 0
        longest_streak = 0
        cursor_date = datetime.utcnow().date()
        for _ in range(total_days):
            day_key = cursor_date.isoformat()
            if day_key in studied_days_set:
                current_streak += 1
            else:
                break
            cursor_date = cursor_date - timedelta(days=1)
        run = 0
        for offset in range(total_days):
            day_key = (datetime.utcnow().date() - timedelta(days=offset)).isoformat()
            if day_key in studied_days_set:
                run += 1
                longest_streak = max(longest_streak, run)
            else:
                run = 0
        return {
            "days_studied": days_studied,
            "days_missed": days_missed,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "avg_daily_minutes": avg_daily_minutes,
            "consistency_percent": consistency_percent,
        }
    except Exception as exc:
        print(f"WARNING: Could not calculate consistency for {student_id}: {exc}")
        return {
            "days_studied": 0,
            "days_missed": int(days or 7),
            "current_streak": 0,
            "longest_streak": 0,
            "avg_daily_minutes": 0,
            "consistency_percent": 0,
        }


def generate_ai_insight(student_id):
    try:
        cached = _load_dashboard_cache(student_id)
        if cached and cached.get("insight"):
            return {"insight": cached["insight"], "cached": True}

        trends = get_performance_trends(student_id, days=30)
        weak_strong = get_weak_strong_topics(student_id)
        consistency = get_study_consistency(student_id, days=7)
        prompt = (
            "You are Astra's analytics coach. Write exactly 3 short sentences.\n"
            "Make the insight personalized, specific, and encouraging.\n"
            "Use the data below and mention one strength, one weak area, and one next action.\n\n"
            f"Performance trends: {json.dumps(trends, ensure_ascii=False)}\n"
            f"Weak/strong topics: {json.dumps(weak_strong, ensure_ascii=False)}\n"
            f"Consistency: {json.dumps(consistency, ensure_ascii=False)}\n"
        )
        insight = ""
        client = None
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if genai is not None and api_key:
            try:
                client = genai.Client(api_key=api_key)
            except Exception:
                client = None
        if client is not None:
            try:
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                insight = str(response.text or "").strip()
            except Exception as exc:
                print(f"WARNING: Gemini insight generation failed for {student_id}: {exc}")
        if not insight:
            strongest = (weak_strong.get("strong_topics") or [])[:1]
            weakest = (weak_strong.get("weak_topics") or [])[:1]
            strong_text = strongest[0]["topic"] if strongest else "your recent strengths"
            weak_text = weakest[0]["topic"] if weakest else "one weak area"
            insight = (
                f"You are building confidence in {strong_text}. "
                f"{weak_text} still needs focused revision. "
                f"Keep a steady rhythm and use one targeted practice block next."
            )
        _save_dashboard_cache(student_id, insight)
        return {"insight": insight, "cached": False}
    except Exception as exc:
        print(f"WARNING: Could not generate AI insight for {student_id}: {exc}")
        return {"insight": "Keep going. Astra will refine your plan as more sessions are logged.", "cached": False}


def get_subject_mastery_breakdown(student_id):
    try:
        syllabus = build_chapter_ready_syllabus()
        chapters = execute_query(
            """
            SELECT unit_name, subject, chapter_test_score, mastery_level, attempts
            FROM chapter_scores
            WHERE student_id = ?
            ORDER BY completed_at DESC, id DESC
            """,
            (student_id,),
        ) or []
        progress_rows = execute_query(
            """
            SELECT topic, subject, score
            FROM progress_records
            WHERE student_id = ?
            ORDER BY recorded_at DESC, id DESC
            """,
            (student_id,),
        ) or []
        subject_maps = {subject: {"attempted": set(), "strong": set(), "developing": set(), "weak": set()} for subject in syllabus.keys()}
        for row in progress_rows:
            subject = _normalize_subject_label(row["subject"])
            topic = str(row["topic"] or "").strip()
            score = _safe_float(row["score"])
            if subject not in subject_maps:
                continue
            if topic:
                subject_maps[subject]["attempted"].add(topic)
                if score >= 80:
                    subject_maps[subject]["strong"].add(topic)
                elif score >= 60:
                    subject_maps[subject]["developing"].add(topic)
                else:
                    subject_maps[subject]["weak"].add(topic)
        for row in chapters:
            subject = _normalize_subject_label(row["subject"])
            unit_name = str(row["unit_name"] or "").strip()
            score = _safe_float(row["chapter_test_score"])
            if subject not in subject_maps:
                continue
            if unit_name:
                subject_maps[subject]["attempted"].add(unit_name)
                if score >= 80:
                    subject_maps[subject]["strong"].add(unit_name)
                elif score >= 60:
                    subject_maps[subject]["developing"].add(unit_name)
                else:
                    subject_maps[subject]["weak"].add(unit_name)
        breakdown = {}
        for subject, units in syllabus.items():
            total_topics = len(units)
            attempted = len(subject_maps.get(subject, {}).get("attempted", set()))
            strong = len(subject_maps.get(subject, {}).get("strong", set()))
            developing = len(subject_maps.get(subject, {}).get("developing", set()))
            weak = len(subject_maps.get(subject, {}).get("weak", set()))
            not_started = max(0, total_topics - attempted)
            mastery_percent = round(((strong * 1.0 + developing * 0.6 + weak * 0.2) / max(total_topics, 1)) * 100, 1)
            breakdown[subject] = {
                "total_topics": total_topics,
                "topics_attempted": attempted,
                "topics_strong": strong,
                "topics_developing": developing,
                "topics_weak": weak,
                "topics_not_started": not_started,
                "overall_mastery_percent": mastery_percent,
            }
        return breakdown
    except Exception as exc:
        print(f"WARNING: Could not build subject mastery breakdown for {student_id}: {exc}")
        return {}
