import json
import re
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

from tools.visual_learning_tools import build_video_explanation, build_visual_learning_aid

VIDEO_BRIEFS_ROOT = Path("app_data") / "video_briefs"
VIDEO_REQUESTS_ROOT = Path("app_data") / "video_requests"


def _normalize_text(value):
    return " ".join(str(value or "").strip().split())


def _ensure_video_roots():
    VIDEO_BRIEFS_ROOT.mkdir(parents=True, exist_ok=True)
    VIDEO_REQUESTS_ROOT.mkdir(parents=True, exist_ok=True)


def _slugify(value):
    return re.sub(r"[^a-z0-9]+", "_", _normalize_text(value).lower()).strip("_") or "topic"


def _topic_slug(topic):
    return _slugify(topic)


def _brief_path(student_id, topic_slug):
    safe_student_id = str(student_id or "student").strip() or "student"
    return VIDEO_BRIEFS_ROOT / f"{safe_student_id}_{_topic_slug(topic_slug)}.json"


def _requested_path(student_id):
    safe_student_id = str(student_id or "student").strip() or "student"
    return VIDEO_REQUESTS_ROOT / f"{safe_student_id}.json"


def _safe_load_json(path, default):
    try:
        if path.exists():
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
    except Exception:
        pass
    return default


def _safe_save_json(path, payload):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
    except Exception:
        return False
    return True


def _infer_subject_from_topic(topic):
    lower = _normalize_text(topic).lower()
    if any(word in lower for word in ["chem", "mole", "reaction", "bond", "equilibrium", "electrochem", "organic"]):
        return "Chemistry"
    if any(word in lower for word in ["math", "integral", "derivative", "probability", "matrix", "vector", "geometry", "calculus"]):
        return "Mathematics"
    return "Physics"


def _make_profile(student_id):
    return {"name": student_id or "student"}


def generate_video_brief(
    profile,
    question,
    answer_text="",
    conversation_mode="tutor",
    tutor_level=3,
    response_language="English",
    tutor_brain=None,
    avatar=None,
):
    return build_video_answer_brief(
        profile,
        question,
        answer_text=answer_text,
        conversation_mode=conversation_mode,
        tutor_level=tutor_level,
        response_language=response_language,
        tutor_brain=tutor_brain,
        avatar=avatar,
    )


class TutorScript(BaseModel):
    opening: str = ""
    concept_explanation: str = ""
    worked_example: str = ""
    checkpoint_question: str = ""
    recap: str = ""
    gesture_notes: list[str] = Field(default_factory=list)
    voice_style: str = "warm, clear, and stepwise"
    estimated_duration_seconds: int = 90


def _split_sentences(text, limit=3):
    cleaned = _normalize_text(text)
    if not cleaned:
        return []
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    return [part.strip() for part in parts if part.strip()][:limit]


def _topic_from_text(text):
    lower = _normalize_text(text).lower()
    topic_hints = [
        ("projectile motion", ["projectile", "trajectory", "parabola"]),
        ("probability", ["probability", "sample space", "event", "dice", "coin"]),
        ("electrostatics", ["electrostatics", "electric field", "field lines", "charge"]),
        ("mathematics", ["calculus", "integration", "differentiation", "limits", "probability", "algebra"]),
        ("chemistry", ["chemistry", "mole", "bond", "equilibrium", "reaction"]),
        ("physics", ["physics", "motion", "force", "energy", "momentum", "current"]),
    ]
    for label, hints in topic_hints:
        if any(hint in lower for hint in hints):
            return label
    return "the requested concept"


def _topic_subject(topic):
    lower = _normalize_text(topic).lower()
    if "chem" in lower:
        return "Chemistry"
    if "math" in lower or "probability" in lower or "algebra" in lower or "calculus" in lower:
        return "Mathematics"
    return "Physics"


def _voice_style_from_brain(tutor_brain, avatar):
    voice_profile = (tutor_brain or {}).get("voice_profile", {})
    avatar_name = (avatar or {}).get("name", "Astra Tutor")
    assistant_voice_family = voice_profile.get("assistant_voice_family", "female")
    speaking_style = voice_profile.get("speaking_style", "warm, articulate, and easy to interrupt")
    return {
        "avatar_name": avatar_name,
        "assistant_voice_family": assistant_voice_family,
        "speaking_style": speaking_style,
        "rate_hint": voice_profile.get("rate", 1.0),
    }


def _gesture_notes(conversation_mode, level, visual):
    gesture_map = {
        "tutor": [
            "Open with a calm smile and a small welcoming hand motion.",
            "Point toward the key step when the concept breaks into parts.",
            "Use a gentle nod at the end of the explanation to signal the checkpoint.",
        ],
        "practice": [
            "Use a brisk, focused hand motion to keep the pace tight.",
            "Point briefly to the answer choice or main trap.",
            "Wrap up with a concise confirmation gesture.",
        ],
        "last_minute": [
            "Keep the hands steady and minimal so the urgency feels calm, not rushed.",
            "Use one firm emphasis gesture for the most important formula or rule.",
            "End with a short recall cue and a reassuring nod.",
        ],
    }
    notes = list(gesture_map.get(conversation_mode, gesture_map["tutor"]))
    if int(level or 3) >= 4:
        notes.insert(1, "Add a board-pointing gesture while unpacking the deeper idea.")
    if visual:
        notes.append("Mirror the visual scene with a subtle open-palm gesture when the scene changes.")
    return notes[:4]


def _fallback_tutor_script(question_text, topic, subject, conversation_mode, level, voice_style):
    title = topic if topic and topic != "the requested concept" else "this concept"
    opening = f"Let us walk through {title} step by step."
    concept_explanation = (
        f"The key idea behind {title} is to keep the concept small, visual, and connected to the JEE {subject.lower()} flow. "
        f"Focus on the core rule first, then see how it behaves in a real question."
    )
    worked_example = (
        f"For a simple example, take the main pattern in {title} and apply the rule one step at a time. "
        "This keeps the method clear and prevents careless mistakes."
    )
    checkpoint_question = (
        f"Before we continue, can you tell me what the first idea is that you should check in {title}?"
    )
    recap = (
        f"Quick recap: {title} works best when you identify the rule, apply it carefully, and then verify the final result."
    )
    gesture_notes = _gesture_notes(conversation_mode, level, visual={"title": topic, "scenario": question_text})
    duration = max(60, min(180, 75 + level * 12))
    return TutorScript(
        opening=opening,
        concept_explanation=concept_explanation,
        worked_example=worked_example,
        checkpoint_question=checkpoint_question,
        recap=recap,
        gesture_notes=gesture_notes,
        voice_style=voice_style or "warm, clear, and stepwise",
        estimated_duration_seconds=duration,
    )


def _extract_json_candidate(text):
    cleaned = _normalize_text(text)
    if not cleaned:
        return ""
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        return cleaned[start : end + 1]
    return cleaned


def _coerce_tutor_script(payload, fallback_script):
    fallback_script = fallback_script or TutorScript()
    data = dict(payload or {}) if isinstance(payload, dict) else {}
    gesture_notes = data.get("gesture_notes")
    if isinstance(gesture_notes, str):
        gesture_notes = [item.strip() for item in re.split(r"[\n,;]+", gesture_notes) if item.strip()]
    elif not isinstance(gesture_notes, list):
        gesture_notes = list(fallback_script.gesture_notes)
    try:
        duration_seconds = int(data.get("estimated_duration_seconds") or fallback_script.estimated_duration_seconds or 90)
    except (TypeError, ValueError):
        duration_seconds = fallback_script.estimated_duration_seconds or 90
    parsed = TutorScript(
        opening=_normalize_text(data.get("opening") or fallback_script.opening),
        concept_explanation=_normalize_text(data.get("concept_explanation") or fallback_script.concept_explanation),
        worked_example=_normalize_text(data.get("worked_example") or fallback_script.worked_example),
        checkpoint_question=_normalize_text(data.get("checkpoint_question") or fallback_script.checkpoint_question),
        recap=_normalize_text(data.get("recap") or fallback_script.recap),
        gesture_notes=[_normalize_text(item) for item in gesture_notes if _normalize_text(item)] or list(fallback_script.gesture_notes),
        voice_style=_normalize_text(data.get("voice_style") or fallback_script.voice_style),
        estimated_duration_seconds=max(30, min(300, duration_seconds)),
    )
    if not parsed.concept_explanation:
        parsed.concept_explanation = fallback_script.concept_explanation
    if not parsed.opening:
        parsed.opening = fallback_script.opening
    if not parsed.worked_example:
        parsed.worked_example = fallback_script.worked_example
    if not parsed.checkpoint_question:
        parsed.checkpoint_question = fallback_script.checkpoint_question
    if not parsed.recap:
        parsed.recap = fallback_script.recap
    if not parsed.gesture_notes:
        parsed.gesture_notes = list(fallback_script.gesture_notes)
    if not parsed.voice_style:
        parsed.voice_style = fallback_script.voice_style
    return parsed


def build_tutor_script(
    profile,
    question,
    answer_text="",
    conversation_mode="tutor",
    tutor_level=3,
    response_language="English",
    tutor_brain=None,
    avatar=None,
    tutor_personality="",
    genai_client=None,
):
    question_text = _normalize_text(question)
    source_text = _normalize_text(answer_text) or question_text
    visual = build_visual_learning_aid(source_text or question_text)
    topic = visual.get("title") if visual else _topic_from_text(question_text or source_text)
    subject = _topic_subject(topic)
    voice_style = _voice_style_from_brain(tutor_brain, avatar)
    try:
        level = int(tutor_level or 3)
    except (TypeError, ValueError):
        level = 3
    level = max(1, min(level, 5))
    fallback_script = _fallback_tutor_script(question_text, topic, subject, conversation_mode, level, voice_style.get("speaking_style", "warm, clear, and stepwise"))

    prompt = (
        "You are Astra, a JEE tutor video script writer. Return ONLY valid JSON with these exact keys: "
        "opening, concept_explanation, worked_example, checkpoint_question, recap, gesture_notes, voice_style, estimated_duration_seconds. "
        "gesture_notes must be an array of short strings. The explanation must be crystal clear, warm, direct, and JEE-focused. "
        "Use the student's answer if helpful, but keep the result concise enough for a speaking video. "
        "Do not add markdown fences or extra commentary.\n\n"
        f"Student name: {profile.get('name', '')}\n"
        f"Conversation mode: {conversation_mode}\n"
        f"Tutor level: {level}\n"
        f"Response language: {response_language}\n"
        f"Subject: {subject}\n"
        f"Topic: {topic}\n"
        f"Question: {question_text}\n"
        f"Tutor personality: {_normalize_text(tutor_personality) or (tutor_brain or {}).get('tone', 'clear and warm')}\n"
        f"Teacher style: {(tutor_brain or {}).get('tone', 'clear and warm')}\n"
        f"Voice style hint: {fallback_script.voice_style}\n"
        f"Student answer context: {source_text}\n"
        f"Opening idea: {fallback_script.opening}\n"
        f"Worked example idea: {fallback_script.worked_example}\n"
        f"Checkpoint idea: {fallback_script.checkpoint_question}\n"
        f"Recap idea: {fallback_script.recap}\n"
    )

    if genai_client:
        try:
            response = genai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            raw_text = _normalize_text(getattr(response, "text", "") or "")
            candidate = _extract_json_candidate(raw_text)
            parsed_payload = json.loads(candidate) if candidate else {}
            return _coerce_tutor_script(parsed_payload, fallback_script)
        except Exception:
            return fallback_script

    return fallback_script


def build_video_answer_brief(
    profile,
    question,
    answer_text="",
    conversation_mode="tutor",
    tutor_level=3,
    response_language="English",
    tutor_brain=None,
    avatar=None,
):
    question_text = _normalize_text(question)
    source_text = _normalize_text(answer_text) or question_text
    visual = build_visual_learning_aid(source_text or question_text)
    video_explanation = build_video_explanation(source_text or question_text, response_language)
    if not video_explanation:
        video_explanation = build_video_explanation(question_text, response_language)
    topic = visual.get("title") if visual else _topic_from_text(question_text or source_text)
    subject = _topic_subject(topic)
    voice_style = _voice_style_from_brain(tutor_brain, avatar)
    try:
        level = int(tutor_level or 3)
    except (TypeError, ValueError):
        level = 3
    level = max(1, min(level, 5))
    tutor_script = build_tutor_script(
        profile,
        question_text,
        answer_text=source_text,
        conversation_mode=conversation_mode,
        tutor_level=level,
        response_language=response_language,
        tutor_brain=tutor_brain,
        avatar=avatar,
        genai_client=None,
    )
    explanation_lines = _split_sentences(tutor_script.concept_explanation, limit=4)
    if not explanation_lines:
        explanation_lines = [tutor_script.concept_explanation or f"We will understand {topic} clearly and step by step."]

    scene_blocks = []
    script_sections = [
        ("Opening", tutor_script.opening),
        ("Concept", tutor_script.concept_explanation),
        ("Worked Example", tutor_script.worked_example),
        ("Checkpoint", tutor_script.checkpoint_question),
        ("Recap", tutor_script.recap),
    ]
    for index, (label, text) in enumerate(script_sections, start=1):
        if not text:
            continue
        scene_blocks.append(
            {
                "label": label,
                "narration": text,
                "gesture": tutor_script.gesture_notes[min(index - 1, len(tutor_script.gesture_notes) - 1)] if tutor_script.gesture_notes else "open_palm_explain",
                "caption": text,
            }
        )

    script_blocks = [{"label": label, "text": text} for label, text in script_sections if text]
    if not script_blocks:
        script_blocks = [
            {"label": "Opening", "text": tutor_script.opening},
            {"label": "Concept", "text": tutor_script.concept_explanation},
        ]

    caption_text = " ".join(item["text"] for item in script_blocks if item.get("text")).strip()

    return {
        "contract_version": "1.0",
        "status": "brief_ready",
        "student_name": profile.get("name", ""),
        "question": question_text,
        "subject": subject,
        "topic": topic,
        "conversation_mode": conversation_mode,
        "tutor_level": level,
        "tutor_face": {
            "id": (avatar or {}).get("id", ""),
            "name": (avatar or {}).get("name", "Astra Tutor"),
            "portrait_url": (avatar or {}).get("portrait_url", ""),
            "tagline": (avatar or {}).get("tagline", ""),
        },
        "voice_style": voice_style,
        "tutor_script": tutor_script.model_dump(),
        "scene_blocks": scene_blocks,
        "gesture_notes": tutor_script.gesture_notes or _gesture_notes(conversation_mode, level, visual),
        "script_blocks": script_blocks,
        "script": caption_text,
        "caption_text": caption_text,
        "visual_reference": visual,
        "video_explanation": video_explanation,
        "expected_duration_seconds": tutor_script.estimated_duration_seconds,
        "render_next": [
            "generate voice track",
            "render avatar or full-body video",
            "combine captions and lesson board",
        ],
        "next_step": "This brief is ready to be sent to the video renderer.",
    }


def build_video_render_request(profile, video_answer_brief, avatar=None):
    brief = video_answer_brief or {}
    avatar = avatar or {}
    created_at = datetime.now(timezone.utc).isoformat()
    video_title = brief.get("caption_text") or brief.get("topic") or "Tutor answer video"
    return {
        "contract_version": brief.get("contract_version", "1.0"),
        "status": "render_ready",
        "created_at": created_at,
        "student_name": profile.get("name", ""),
        "job_id": f"render-{_slugify(profile.get('name', 'student'))}-{_slugify(brief.get('topic', 'concept'))}-{int(datetime.now().timestamp())}",
        "title": video_title[:120],
        "question": brief.get("question", ""),
        "subject": brief.get("subject", ""),
        "topic": brief.get("topic", ""),
        "conversation_mode": brief.get("conversation_mode", "tutor"),
        "tutor_level": brief.get("tutor_level", 3),
        "tutor_face": brief.get("tutor_face", {}),
        "voice_style": brief.get("voice_style", {}),
        "script_blocks": brief.get("script_blocks", []),
        "scene_blocks": brief.get("scene_blocks", []),
        "gesture_notes": brief.get("gesture_notes", []),
        "caption_text": brief.get("caption_text", ""),
        "tutor_script": brief.get("tutor_script", {}),
        "render_target": {
            "avatar_name": avatar.get("name", "Astra Tutor"),
            "portrait_url": avatar.get("portrait_url", ""),
            "reference_video_ids": avatar.get("featured_video_ids", []),
            "format": "16:9",
            "quality": "1080p",
            "captions": True,
        },
        "renderer_steps": [
            "Generate voice track from the selected tutor voice profile.",
            "Animate the tutor face or full-body avatar with matching gestures.",
            "Overlay captions and a clean lesson board if available.",
            "Return a playable tutor video URL when rendering is wired in.",
        ],
        "output_hint": "This request is ready for the actual video rendering engine.",
        "preview_text": (
            f"{video_title}. {brief.get('script', '')[:240]}".strip()
        ),
    }


def _brief_metadata(brief, source="weekly_plan", status="brief_ready", topic_slug=""):
    brief = dict(brief or {})
    brief["source"] = source
    brief["status"] = status
    brief["topic_slug"] = topic_slug or _topic_slug(brief.get("topic", "topic"))
    brief["saved_at"] = datetime.now(timezone.utc).isoformat()
    return brief


def _load_weekly_plan(student_id):
    safe_student_id = str(student_id or "student").strip() or "student"
    weekly_path = Path("app_data") / "planner" / f"{safe_student_id}_weekly.json"
    return _safe_load_json(weekly_path, {})


def get_video_brief_for_topic(student_id, topic, subject):
    try:
        _ensure_video_roots()
        topic = _normalize_text(topic)
        topic_slug = _topic_slug(topic)
        brief_path = _brief_path(student_id, topic_slug)
        existing = _safe_load_json(brief_path, None)
        if isinstance(existing, dict) and existing:
            return existing
        profile = _make_profile(student_id)
        inferred_subject = _normalize_text(subject) or _infer_subject_from_topic(topic)
        question = f"Explain {topic or 'this topic'} for a JEE {inferred_subject} student using a clear video script."
        brief = generate_video_brief(
            profile,
            question,
            answer_text=topic or question,
            conversation_mode="tutor",
            tutor_level=3,
            response_language="English",
            tutor_brain={"tone": "clear and warm", "voice_profile": {"assistant_voice_family": "female", "speaking_style": "warm, articulate, and easy to interrupt"}},
            avatar=None,
        )
        brief.update(
            {
                "student_id": student_id,
                "subject": inferred_subject,
                "topic": topic or brief.get("topic", "topic"),
                "topic_slug": topic_slug,
            }
        )
        brief = _brief_metadata(brief, source="manual_request", status="brief_ready", topic_slug=topic_slug)
        _safe_save_json(brief_path, brief)
        return brief
    except Exception as exc:
        fallback_topic = _normalize_text(topic) or "topic"
        profile = _make_profile(student_id)
        brief = generate_video_brief(
            profile,
            f"Explain {fallback_topic}",
            answer_text=fallback_topic,
            conversation_mode="tutor",
            tutor_level=3,
            response_language="English",
            tutor_brain={"tone": "clear and warm", "voice_profile": {"assistant_voice_family": "female", "speaking_style": "warm, articulate, and easy to interrupt"}},
            avatar=None,
        )
        brief.update(
            {
                "student_id": student_id,
                "subject": _normalize_text(subject) or _infer_subject_from_topic(fallback_topic),
                "topic": fallback_topic,
                "topic_slug": _topic_slug(fallback_topic),
                "error": str(exc),
            }
        )
        brief = _brief_metadata(brief, source="fallback", status="brief_ready", topic_slug=brief["topic_slug"])
        return brief


def pre_generate_video_briefs(student_id, days_ahead=7):
    try:
        _ensure_video_roots()
        weekly = _load_weekly_plan(student_id)
        days = list((weekly or {}).get("days", []) or [])[: max(1, int(days_ahead or 7))]
        generated = []
        seen = set()
        for day in days:
            for slot_name in ("morning", "evening"):
                session = dict(day.get(slot_name, {}) or {})
                topic = _normalize_text(session.get("topic") or "")
                if not topic:
                    continue
                subject = _normalize_text(session.get("subject") or _infer_subject_from_topic(topic))
                topic_slug = _topic_slug(topic)
                if topic_slug in seen:
                    continue
                seen.add(topic_slug)
                brief = get_video_brief_for_topic(student_id, topic, subject)
                brief = dict(brief or {})
                brief.update(
                    {
                        "source": "weekly_plan",
                        "scheduled_day": day.get("date") or day.get("label") or "",
                        "scheduled_slot": slot_name,
                        "subject": subject,
                        "topic": topic,
                        "topic_slug": topic_slug,
                    }
                )
                brief = _brief_metadata(brief, source="weekly_plan", status=brief.get("status", "brief_ready"), topic_slug=topic_slug)
                _safe_save_json(_brief_path(student_id, topic_slug), brief)
                generated.append(brief)
        return generated
    except Exception as exc:
        print(f"WARNING: Could not pre-generate video briefs for {student_id}: {exc}")
        return []


def load_video_preplan_status(student_id):
    try:
        _ensure_video_roots()
        weekly = _load_weekly_plan(student_id)
        briefs = {}
        safe_student_id = str(student_id or "student").strip() or "student"
        for path in VIDEO_BRIEFS_ROOT.glob(f"{safe_student_id}_*.json"):
            payload = _safe_load_json(path, {})
            if isinstance(payload, dict):
                briefs[_topic_slug(payload.get("topic_slug") or payload.get("topic") or path.stem)] = payload
        requested = load_requested_videos(student_id)
        requested_index = {
            _topic_slug(item.get("topic") or item.get("topic_slug") or ""): item for item in requested
            if isinstance(item, dict)
        }
        items = []
        for day in list((weekly or {}).get("days", []) or [])[:7]:
            for slot_name in ("morning", "evening"):
                session = dict(day.get(slot_name, {}) or {})
                topic = _normalize_text(session.get("topic") or "")
                if not topic:
                    continue
                subject = _normalize_text(session.get("subject") or _infer_subject_from_topic(topic))
                topic_slug = _topic_slug(topic)
                brief = briefs.get(topic_slug)
                request_entry = requested_index.get(topic_slug) or {}
                video_ready = bool(str(request_entry.get("status", "")).lower() in {"ready", "completed"} or request_entry.get("video_url"))
                script_ready = bool(brief)
                status = "Video Ready" if video_ready else "Script Ready" if script_ready else "Not prepared yet"
                items.append(
                    {
                        "date": day.get("date") or "",
                        "day_label": day.get("label") or day.get("date") or "",
                        "slot": slot_name,
                        "subject": subject,
                        "topic": topic,
                        "topic_slug": topic_slug,
                        "script_ready": script_ready,
                        "video_ready": video_ready,
                        "status": status,
                        "brief": brief or {},
                        "video_url": request_entry.get("video_url", ""),
                        "job_id": request_entry.get("job_id", ""),
                    }
                )
        return items
    except Exception as exc:
        print(f"WARNING: Could not load video preplan status for {student_id}: {exc}")
        return []


def load_requested_videos(student_id):
    try:
        data = _safe_load_json(_requested_path(student_id), {})
        if isinstance(data, dict):
            requests = data.get("requests", [])
            return list(requests) if isinstance(requests, list) else []
        if isinstance(data, list):
            return list(data)
        return []
    except Exception:
        return []


def save_requested_video(student_id, topic, subject, source="request", status="requested", job_id="", video_url=""):
    try:
        _ensure_video_roots()
        request_path = _requested_path(student_id)
        existing = _safe_load_json(request_path, {})
        requests = list(existing.get("requests", [])) if isinstance(existing, dict) else list(existing or [])
        topic_slug = _topic_slug(topic)
        record = {
            "student_id": student_id,
            "topic": _normalize_text(topic),
            "subject": _normalize_text(subject) or _infer_subject_from_topic(topic),
            "topic_slug": topic_slug,
            "source": source,
            "status": status,
            "job_id": job_id,
            "video_url": video_url,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        updated = False
        for index, item in enumerate(requests):
            if _topic_slug(item.get("topic") or item.get("topic_slug") or "") == topic_slug:
                requests[index] = {**item, **record}
                updated = True
                break
        if not updated:
            requests.insert(0, record)
        payload = {"student_id": student_id, "updated_at": datetime.now(timezone.utc).isoformat(), "requests": requests[:50]}
        _safe_save_json(request_path, payload)
        return record
    except Exception as exc:
        print(f"WARNING: Could not save requested video for {student_id}: {exc}")
        return {
            "student_id": student_id,
            "topic": _normalize_text(topic),
            "subject": _normalize_text(subject) or _infer_subject_from_topic(topic),
            "topic_slug": _topic_slug(topic),
            "source": source,
            "status": status,
            "job_id": job_id,
            "video_url": video_url,
            "error": str(exc),
        }


def update_requested_video_status(student_id, topic_slug, status, job_id="", video_url=""):
    try:
        _ensure_video_roots()
        request_path = _requested_path(student_id)
        existing = _safe_load_json(request_path, {})
        requests = list(existing.get("requests", [])) if isinstance(existing, dict) else list(existing or [])
        topic_slug = _topic_slug(topic_slug)
        updated = None
        for index, item in enumerate(requests):
            if _topic_slug(item.get("topic") or item.get("topic_slug") or "") == topic_slug:
                requests[index] = {
                    **item,
                    "status": status,
                    "job_id": job_id or item.get("job_id", ""),
                    "video_url": video_url or item.get("video_url", ""),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
                updated = requests[index]
                break
        payload = {"student_id": student_id, "updated_at": datetime.now(timezone.utc).isoformat(), "requests": requests[:50]}
        _safe_save_json(request_path, payload)
        return updated or {
            "student_id": student_id,
            "topic_slug": topic_slug,
            "status": status,
            "job_id": job_id,
            "video_url": video_url,
        }
    except Exception as exc:
        print(f"WARNING: Could not update requested video for {student_id}: {exc}")
        return {
            "student_id": student_id,
            "topic_slug": _topic_slug(topic_slug),
            "status": status,
            "job_id": job_id,
            "video_url": video_url,
            "error": str(exc),
        }
