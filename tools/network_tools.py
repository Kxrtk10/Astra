import os
from collections import Counter

from tools.analytics_tools import get_analytics_summary
from tools.behavior_tools import get_behavior_snapshot
from tools.personal_memory_tools import load_personal_memory
from tools.planner_tools import get_adaptive_learning_profile, get_exam_entries, load_planner_state
from tools.profile_tools import PROFILE_FOLDER, load_profile


def _all_profiles():
    if not os.path.exists(PROFILE_FOLDER):
        return []

    profiles = []
    seen_names = set()
    for filename in os.listdir(PROFILE_FOLDER):
        if not filename.lower().endswith(".json"):
            continue
        name = os.path.splitext(filename)[0]
        profile = load_profile(name)
        if not profile:
            continue
        profile_name = profile.get("name", "").strip()
        if not profile_name or profile_name.lower() in seen_names:
            continue
        seen_names.add(profile_name.lower())
        profiles.append(profile)
    return profiles


def _safe_peer_label(name):
    parts = [part for part in str(name or "").split() if part]
    if not parts:
        return "Peer learner"
    initials = [part[0].upper() for part in parts[:3] if part]
    suffix = sum(ord(char) for char in str(name)) % 100
    return f"{'.'.join(initials)}. #{suffix:02d}"


def _interest_display_name(interest):
    cleaned = " ".join(str(interest or "").replace(",", " ").split()).strip()
    if not cleaned:
        return "General"
    words = cleaned.split()
    return " ".join(words[:2]).title()


def _normalize_interests(memory):
    interests = memory.get("interests", []) if isinstance(memory, dict) else []
    return {
        str(interest).strip().lower()
        for interest in interests
        if str(interest).strip()
    }


def _flatten_mock_scores(mock_scores):
    flattened = {}
    if not isinstance(mock_scores, dict):
        return flattened

    for exam_or_subject, score in mock_scores.items():
        if isinstance(score, dict):
            for subject, subject_score in score.items():
                key = f"{exam_or_subject} | {subject}"
                try:
                    flattened[key] = float(subject_score)
                except (TypeError, ValueError):
                    continue
        else:
            try:
                flattened[exam_or_subject] = float(score)
            except (TypeError, ValueError):
                continue
    return flattened


def _extract_weak_areas(profile):
    state = load_planner_state(profile["name"])
    weak_areas = []

    for label, score in _flatten_mock_scores(state.get("mock_scores", {})).items():
        if score < 60:
            weak_areas.append((label, round(score, 1), "low_mock"))

    for label, hours in (state.get("backlog_hours") or {}).items():
        try:
            backlog_hours = float(hours)
        except (TypeError, ValueError):
            continue
        if backlog_hours >= 3:
            pretty_label = str(label).replace("::", " | ")
            weak_areas.append((pretty_label, round(backlog_hours, 1), "backlog"))

    ranked = sorted(weak_areas, key=lambda item: item[1], reverse=True)
    seen = set()
    deduped = []
    for label, value, source in ranked:
        if label in seen:
            continue
        seen.add(label)
        deduped.append({"label": label, "value": value, "source": source})
        if len(deduped) >= 4:
            break
    return deduped


def _build_snapshot(profile):
    exams = get_exam_entries(profile)
    exam_names = [exam["name"] for exam in exams if exam.get("name")]
    subjects = sorted(
        {
            subject
            for exam in exams
            for subject in exam.get("subjects", [])
            if str(subject).strip()
        }
    )
    memory = load_personal_memory(profile["name"])
    analytics = get_analytics_summary(profile["name"])
    adaptive = get_adaptive_learning_profile(profile)
    behavior = get_behavior_snapshot(profile)

    return {
        "name": profile["name"],
        "label": _safe_peer_label(profile["name"]),
        "exam_names": exam_names,
        "subjects": subjects,
        "interests": _normalize_interests(memory),
        "analytics": analytics,
        "adaptive": adaptive,
        "behavior": behavior,
        "max_study_hours_per_day": float(profile.get("max_study_hours_per_day", profile.get("study_hours_per_day", 4))),
        "weak_areas": _extract_weak_areas(profile),
    }


def _shared_items(left, right):
    return sorted(set(left) & set(right))


def _compatibility_label(score):
    if score >= 75:
        return "Strong fit"
    if score >= 50:
        return "Good fit"
    return "Light overlap"


def _score_similarity(current, peer):
    score = 0
    reasons = []

    shared_exams = _shared_items(current["exam_names"], peer["exam_names"])
    if shared_exams:
        score += min(45, 18 * len(shared_exams))
        reasons.append(f"shared exams: {', '.join(shared_exams[:3])}")

    shared_subjects = _shared_items(current["subjects"], peer["subjects"])
    if shared_subjects:
        score += min(16, 4 * len(shared_subjects))
        reasons.append(f"similar sections: {', '.join(shared_subjects[:3])}")

    if current["behavior"].get("support_style") == peer["behavior"].get("support_style"):
        score += 10
        reasons.append(f"same support style: {current['behavior'].get('support_style', 'balanced_support').replace('_', ' ')}")

    if current["adaptive"].get("question_difficulty") == peer["adaptive"].get("question_difficulty"):
        score += 8
        reasons.append(f"same challenge band: {current['adaptive'].get('question_difficulty', 'moderate')}")

    if current["analytics"].get("speed_signal") == peer["analytics"].get("speed_signal"):
        score += 6
        reasons.append(f"similar pace: {current['analytics'].get('speed_signal', 'steady')}")

    shared_interests = _shared_items(current["interests"], peer["interests"])
    if shared_interests:
        score += min(12, 6 * len(shared_interests))
        reasons.append(f"shared interests: {', '.join(shared_interests[:2])}")

    hours_gap = abs(current["max_study_hours_per_day"] - peer["max_study_hours_per_day"])
    if hours_gap <= 1:
        score += 6
        reasons.append("similar daily capacity")
    elif hours_gap <= 2:
        score += 3

    return min(score, 100), reasons


def _style_display(value):
    return str(value or "").replace("_", " ").strip() or "balanced support"


def _build_student_matches(current, peers):
    matches = []
    for peer in peers:
        score, reasons = _score_similarity(current, peer)
        if score < 18:
            continue
        matches.append(
            {
                "name": peer["name"],
                "label": peer["label"],
                "compatibility_score": score,
                "compatibility_band": _compatibility_label(score),
                "shared_exams": _shared_items(current["exam_names"], peer["exam_names"]),
                "shared_traits": reasons[:4],
                "study_style": (
                    f"{_style_display(peer['behavior'].get('support_style'))}, "
                    f"{peer['analytics'].get('speed_signal', 'steady')} pace, "
                    f"{peer['adaptive'].get('question_difficulty', 'moderate')} difficulty"
                ),
            }
        )

    matches.sort(key=lambda item: item["compatibility_score"], reverse=True)
    return matches[:5]


def _normalize_group_study_preferences(profile):
    prefs = profile.get("group_study_preferences", {}) if isinstance(profile, dict) else {}
    if not isinstance(prefs, dict):
        prefs = {}

    mode = str(prefs.get("mode", "solo")).strip().lower() or "solo"
    if mode not in {"solo", "friends", "random", "mixed"}:
        mode = "mixed" if prefs.get("enabled") else "solo"

    try:
        group_size = int(prefs.get("group_size", 3) or 3)
    except (TypeError, ValueError):
        group_size = 3
    group_size = max(2, min(5, group_size))

    try:
        session_minutes = int(prefs.get("session_minutes", 60) or 60)
    except (TypeError, ValueError):
        session_minutes = 60
    session_minutes = max(30, min(120, session_minutes))

    try:
        rotation_index = int(prefs.get("rotation_index", 0) or 0)
    except (TypeError, ValueError):
        rotation_index = 0

    return {
        "enabled": bool(prefs.get("enabled", False)),
        "mode": mode,
        "group_size": group_size,
        "session_minutes": session_minutes,
        "focus": str(prefs.get("focus", "")).strip(),
        "rotation_index": max(0, rotation_index),
    }


def _group_mode_label(mode):
    labels = {
        "solo": "Solo study",
        "friends": "Friends-first group",
        "random": "Random matched room",
        "mixed": "Mixed study room",
    }
    return labels.get(mode, "Mixed study room")


def _group_focus_label(current, prefs):
    if prefs.get("focus"):
        return prefs["focus"]
    if current["weak_areas"]:
        return current["weak_areas"][0]["label"]
    if current["subjects"]:
        return current["subjects"][0]
    if current["exam_names"]:
        return current["exam_names"][0]
    return "general revision"


def _build_group_session_plan(current, members, prefs):
    session_minutes = prefs["session_minutes"]
    focus = _group_focus_label(current, prefs)
    member_count = max(1, len(members))
    blocks = [
        {
            "title": "Warm-up check-in",
            "minutes": max(5, round(session_minutes * 0.12)),
            "detail": "Each student gives one quick update so Astra can set the room tone and keep it comfortable.",
        },
        {
            "title": "Shared concept core",
            "minutes": max(10, round(session_minutes * 0.33)),
            "detail": f"The room studies {focus} together through a single clean explanation and one real-life example.",
        },
        {
            "title": "Turn-based solve round",
            "minutes": max(8, round(session_minutes * 0.27)),
            "detail": "Each student solves one step or one short question while Astra keeps the pace calm and focused.",
        },
        {
            "title": "Mixed drill or quiz",
            "minutes": max(6, round(session_minutes * 0.16)),
            "detail": "The group does a quick check to make sure the concept is sticking for everyone, not just one person.",
        },
        {
            "title": "Personal wrap-up",
            "minutes": max(5, round(session_minutes * 0.12)),
            "detail": "Astra sends each student a private follow-up step so the group session still improves individual progress.",
        },
    ]
    if session_minutes >= 80:
        blocks.insert(
            3,
            {
                "title": "Short recovery break",
                "minutes": max(5, round(session_minutes * 0.08)),
                "detail": "A brief pause keeps the room fresh and prevents one student from getting overloaded.",
            },
        )

    total_minutes = sum(block["minutes"] for block in blocks)
    if total_minutes != session_minutes and blocks:
        blocks[-1]["minutes"] = max(5, blocks[-1]["minutes"] + (session_minutes - total_minutes))

    return blocks, focus, member_count


def _build_group_study_snapshot(current, peers, matches, circles):
    prefs = _normalize_group_study_preferences(current)
    current_focus = _group_focus_label(current, prefs)
    active = prefs["enabled"] and prefs["mode"] != "solo"

    if not active:
        return {
            "enabled": False,
            "mode": prefs["mode"],
            "mode_label": _group_mode_label("solo"),
            "status": "solo",
            "summary": (
                "Group study is currently off. Astra will keep the room individual unless you choose a shared session."
            ),
            "room_title": f"{current_focus} solo study",
            "group_rules": [
                "Keep the focus on your own pace.",
                "Use the tutor for private explanations.",
                "Switch into a group later if you want shared accountability.",
            ],
            "members": [
                {
                    "name": current["name"],
                    "label": current["label"],
                    "role": "You",
                    "focus": current_focus,
                    "study_style": _style_display(current["behavior"].get("support_style")),
                    "compatibility_band": "Self-paced",
                }
            ],
            "session_plan": [
                {
                    "title": "Solo focus block",
                    "minutes": prefs["session_minutes"],
                    "detail": f"Work on {current_focus} at your own pace with Astra supporting only you.",
                }
            ],
            "actions": [
                "Turn group study on when you want shared accountability.",
                "Use Change Group later to reroll matched learners.",
            ],
        }

    candidate_matches = list(matches or [])
    if not candidate_matches:
        candidate_matches = _build_student_matches(current, peers)

    if candidate_matches:
        offset = prefs["rotation_index"] % len(candidate_matches)
        candidate_matches = candidate_matches[offset:] + candidate_matches[:offset]

    target_size = max(2, prefs["group_size"])
    selected_matches = candidate_matches[: max(1, target_size - 1)]
    peer_lookup = {peer["name"]: peer for peer in peers}
    members = [
        {
            "name": current["name"],
            "label": current["label"],
            "role": "You",
            "focus": current_focus,
            "study_style": _style_display(current["behavior"].get("support_style")),
            "compatibility_band": "Anchor learner",
        }
    ]

    for match in selected_matches:
        peer = peer_lookup.get(match.get("name"))
        peer_focus = current_focus
        peer_style = match.get("study_style", "balanced support")
        if peer:
            peer_focus = peer["weak_areas"][0]["label"] if peer["weak_areas"] else current_focus
            peer_style = (
                f"{_style_display(peer['behavior'].get('support_style'))}, "
                f"{peer['analytics'].get('speed_signal', 'steady')} pace"
            )
        members.append(
            {
                "name": match.get("name", ""),
                "label": match.get("label", "Peer learner"),
                "role": "Matched peer",
                "focus": peer_focus,
                "study_style": peer_style,
                "compatibility_score": match.get("compatibility_score", 0),
                "compatibility_band": match.get("compatibility_band", "Good fit"),
                "shared_traits": match.get("shared_traits", [])[:3],
            }
        )

    session_plan, focus_label, member_count = _build_group_session_plan(current, members, prefs)
    room_label = _group_mode_label(prefs["mode"])
    room_title = f"{focus_label} {room_label.lower()}"
    return {
        "enabled": True,
        "mode": prefs["mode"],
        "mode_label": room_label,
        "status": "active",
        "room_title": room_title,
        "summary": (
            f"{room_label} built around {focus_label}. Astra keeps the room shared, but every student still gets a personal next step."
        ),
        "group_rules": [
            "One voice at a time.",
            "Stay on the agreed chapter or exam block.",
            "Every student leaves with a personal follow-up step.",
            "If the room feels off, change the group or go solo.",
        ],
        "members": members[:member_count],
        "session_plan": session_plan,
        "actions": [
            "Change group to reroll the matched learners.",
            "Go solo to return to a private study flow.",
        ],
        "session_minutes": prefs["session_minutes"],
        "focus": focus_label,
        "rotation_index": prefs["rotation_index"],
        "circle_hint": circles[0]["title"] if circles else "",
    }


def _build_study_circles(current, matches, peers):
    circles = []
    shared_exam_names = current["exam_names"][:2] or ["general learning"]
    exam_focus = " + ".join(shared_exam_names)
    circles.append(
        {
            "title": f"{exam_focus} focus circle",
            "reason": "Students here are aligned by exam goals, so shared strategy and practice pressure make sense.",
            "fit": "Exam-aligned",
            "potential_peers": max(1, sum(1 for peer in peers if set(shared_exam_names) & set(peer["exam_names"]))),
        }
    )

    circles.append(
        {
            "title": f"{_style_display(current['behavior'].get('support_style'))} study circle",
            "reason": "This circle groups learners who respond well to a similar coaching tone and pacing style.",
            "fit": "Support-style match",
            "potential_peers": max(
                1,
                sum(
                    1
                    for peer in peers
                    if peer["behavior"].get("support_style") == current["behavior"].get("support_style")
                ),
            ),
        }
    )

    circles.append(
        {
            "title": f"{current['adaptive'].get('question_difficulty', 'moderate').title()} difficulty circle",
            "reason": "This keeps students around a similar challenge level so the group stays useful instead of overwhelming.",
            "fit": "Difficulty match",
            "potential_peers": max(
                1,
                sum(
                    1
                    for peer in peers
                    if peer["adaptive"].get("question_difficulty") == current["adaptive"].get("question_difficulty")
                ),
            ),
        }
    )

    if current["interests"]:
        circles.append(
            {
                "title": f"{_interest_display_name(next(iter(sorted(current['interests']))))} motivation circle",
                "reason": "This is a lighter accountability layer based on hobbies or interests, so students stay connected without drifting off-topic.",
                "fit": "Motivation match",
                "potential_peers": max(
                    1,
                    sum(1 for peer in peers if _shared_items(current["interests"], peer["interests"])),
                ),
            }
        )

    return circles[:4]


def _build_tutor_network(current, matches, peers):
    high_signal_peers = []
    for peer in peers:
        adherence = float(peer["adaptive"].get("adherence_ratio", 0) or 0)
        recent_accuracy = float(peer["analytics"].get("recent_accuracy", 0) or 0)
        if recent_accuracy >= 68 or adherence >= 0.65:
            high_signal_peers.append(peer)

    support_counter = Counter(
        _style_display(peer["behavior"].get("support_style"))
        for peer in high_signal_peers
    )
    weak_area_counter = Counter()
    for peer in peers:
        for area in peer["weak_areas"]:
            weak_area_counter[area["label"]] += 1

    current_weakest = current["weak_areas"][0]["label"] if current["weak_areas"] else ""
    top_network_weak = weak_area_counter.most_common(1)[0][0] if weak_area_counter else ""
    top_support = support_counter.most_common(1)[0][0] if support_counter else _style_display(current["behavior"].get("support_style"))

    insights = []
    if current_weakest:
        insights.append(
            {
                "title": "Where your tutor network would lean harder next",
                "detail": (
                    f"{current_weakest} is the strongest signal right now. A good tutor network would keep this in guided rotation, "
                    "use short feedback loops, and only raise pressure after cleaner accuracy."
                ),
                "signal": current_weakest,
            }
        )

    if top_network_weak:
        insights.append(
            {
                "title": "Pattern tutors are seeing across similar learners",
                "detail": (
                    f"Across students close to your exam mix and study style, {top_network_weak} shows up repeatedly as a sticking point. "
                    "That makes it a strong candidate for extra visuals, case studies, and timed drills."
                ),
                "signal": top_network_weak,
            }
        )

    insights.append(
        {
            "title": "Coaching style that is working best in the network",
            "detail": (
                f"Tutors helping comparable students are getting the best traction with {top_support} support. "
                "Your personal tutor can borrow that tone without losing your one-to-one personalization."
            ),
            "signal": top_support,
        }
    )

    if matches:
        insights.append(
            {
                "title": "How your tutor stays personal even inside a network",
                "detail": (
                    f"Your tutor still belongs only to you. The network layer just shares anonymized teaching wins from {len(matches)} similar learners "
                    "so your explanations, pacing, and recovery plans improve faster."
                ),
                "signal": f"{len(matches)} similar learners found",
            }
        )

    return {
        "summary": (
            "Personal tutors stay separate, but they can safely borrow anonymized coaching wins from the wider tutor network."
        ),
        "insights": insights[:4],
    }


def build_network_snapshot(profile):
    current = _build_snapshot(profile)
    peer_profiles = [
        peer_profile
        for peer_profile in _all_profiles()
        if peer_profile.get("name", "").strip().lower() != profile["name"].strip().lower()
    ]
    peer_snapshots = [_build_snapshot(peer_profile) for peer_profile in peer_profiles]
    matches = _build_student_matches(current, peer_snapshots)
    circles = _build_study_circles(current, matches, peer_snapshots)
    tutor_network = _build_tutor_network(current, matches, peer_snapshots)
    group_study = _build_group_study_snapshot(current, peer_snapshots, matches, circles)

    return {
        "privacy_mode": "private_by_default",
        "network_note": (
            "This first version uses anonymized matching, opt-in group study, and tutor-insight sharing, not open social chat. "
            "That keeps the product focused on learning instead of distraction."
        ),
        "stats": {
            "peer_count": len(peer_snapshots),
            "match_count": len(matches),
            "circle_count": len(circles),
            "tutor_network_ready": "yes" if peer_snapshots else "starter",
            "group_study_ready": "yes" if group_study.get("enabled") else "starter",
        },
        "student_matches": matches,
        "study_circles": circles,
        "tutor_network": tutor_network,
        "group_study": group_study,
    }
