import json
import json
import re
from pathlib import Path

from backend.config import settings
from tools.profile_tools import load_profile
from tools.visual_learning_tools import build_video_explanation, build_visual_learning_aid
from tools.progress_tracker_tools import get_progress_snapshot

SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".webm", ".m4v", ".mov"}


def _normalize_text(value):
    return " ".join(str(value or "").strip().split())


def _slugify(value):
    text = _normalize_text(value).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "video"


def _humanize_slug(value):
    text = _normalize_text(value).replace("-", " ").replace("_", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text.title() if text else "Tutor Video"


def _to_public_url(relative_path):
    parts = [part for part in str(relative_path or "").split("/") if part]
    return "/" + "/".join(re.sub(r" ", "%20", part) for part in parts)


def _load_manifest_entries(manifest_path):
    if not manifest_path.exists():
        return []
    try:
        with manifest_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return []

    if isinstance(payload, dict):
        entries = payload.get("videos") or payload.get("items") or []
    elif isinstance(payload, list):
        entries = payload
    else:
        entries = []

    return [entry for entry in entries if isinstance(entry, dict)]


def _scan_video_files(media_root):
    if not media_root.exists():
        return []

    discovered = []
    for path in sorted(media_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_VIDEO_EXTENSIONS:
            continue
        relative_path = path.relative_to(Path("web")).as_posix()
        discovered.append(
            {
                "id": _slugify(path.stem),
                "title": _humanize_slug(path.stem),
                "file_name": path.name,
                "url": _to_public_url(relative_path),
                "source_type": "local_file",
            }
        )
    return discovered


def _merge_video_entry(file_entry, manifest_entry=None):
    manifest_entry = manifest_entry or {}
    title = _normalize_text(manifest_entry.get("title")) or file_entry["title"]
    topic = _normalize_text(manifest_entry.get("topic")) or title
    summary = _normalize_text(manifest_entry.get("summary")) or (
        f"This tutor video covers {topic.lower()} and can be used as a launch point for the 3D concept board."
    )
    tags = manifest_entry.get("tags")
    if isinstance(tags, str):
        tags = [item.strip() for item in tags.split(",") if item.strip()]
    if not isinstance(tags, list):
        tags = []

    transcript_hint = _normalize_text(manifest_entry.get("transcript_hint"))
    bridge_prompt = (
        f"Explain {topic} with a concept-first, visual teaching style. "
        f"Use a real-life case study and a 3D-style visualization board. {summary}"
    )
    if transcript_hint:
        bridge_prompt = f"{bridge_prompt} {transcript_hint}"

    visual_learning = build_visual_learning_aid(bridge_prompt)
    if not visual_learning:
        visual_learning = build_visual_learning_aid(f"Explain {topic} concept with a real-life case study and 3D-style visualization.")
    video_explanation = build_video_explanation(bridge_prompt)
    if not video_explanation:
        video_explanation = build_video_explanation(f"Explain {topic} concept with a real-life case study and 3D-style visualization.")

    cue_points = manifest_entry.get("cue_points")
    if not isinstance(cue_points, list):
        cue_points = []
    cue_points = [item for item in (_normalize_text(point) for point in cue_points) if item]

    return {
        "id": manifest_entry.get("id") or file_entry["id"],
        "title": title,
        "topic": topic,
        "summary": summary,
        "tags": tags,
        "file_name": file_entry["file_name"],
        "url": file_entry["url"],
        "source_type": file_entry["source_type"],
        "duration_label": _normalize_text(manifest_entry.get("duration_label")),
        "level": _normalize_text(manifest_entry.get("level")),
        "order": manifest_entry.get("order"),
        "cue_points": cue_points,
        "transcript_hint": transcript_hint,
        "bridge_prompt": bridge_prompt,
        "visual_learning": visual_learning,
        "video_explanation": video_explanation,
    }


def _score_video(video, progress_snapshot, active_exam_label):
    score = 0
    reasons = []
    text_blobs = " ".join(
        [
            video.get("title", ""),
            video.get("topic", ""),
            video.get("summary", ""),
            " ".join(video.get("tags", [])),
        ]
    ).lower()

    if active_exam_label and active_exam_label.lower() in text_blobs:
        score += 4
        reasons.append(f"Matches {active_exam_label} study context.")

    weak_topics = []
    topic_momentum = (progress_snapshot or {}).get("topic_momentum") or {}
    for item in topic_momentum.get("weakest_topics", [])[:3]:
        if isinstance(item, dict):
            weak_topics.append(_normalize_text(item.get("topic")))
        elif isinstance(item, str):
            weak_topics.append(_normalize_text(item))

    for weak_topic in weak_topics:
        if weak_topic and weak_topic.lower() in text_blobs:
            score += 5
            reasons.append(f"Supports a weak topic: {weak_topic}.")

    if "projectile" in text_blobs or "motion" in text_blobs:
        score += 2
    if "probability" in text_blobs or "percent" in text_blobs:
        score += 2
    if "field" in text_blobs or "electro" in text_blobs:
        score += 2

    if video.get("visual_learning"):
        score += 1
    if video.get("video_explanation"):
        score += 1

    if not reasons:
        reasons.append("Available for the 3D and lesson bridge.")

    return score, reasons


def _get_active_exam_label(student_name, progress_snapshot):
    profile = load_profile(student_name) if student_name else None
    if profile:
        exams = profile.get("exams") or []
        if exams and isinstance(exams[0], dict):
            return _normalize_text(exams[0].get("name"))
        exam_name = _normalize_text(profile.get("exam"))
        if exam_name:
            return exam_name
    if progress_snapshot:
        exam_name = _normalize_text(progress_snapshot.get("active_exam") or progress_snapshot.get("exam"))
        if exam_name:
            return exam_name
    return ""


def get_video_library_snapshot(student_name=None):
    media_root = Path(settings.video_library_media_root)
    manifest_path = Path(settings.video_library_manifest_path)

    manifest_entries = _load_manifest_entries(manifest_path)
    manifest_by_file = {}
    manifest_by_id = {}
    for entry in manifest_entries:
        entry_id = _normalize_text(entry.get("id"))
        file_name = _normalize_text(entry.get("file_name") or entry.get("file"))
        if entry_id:
            manifest_by_id[entry_id] = entry
        if file_name:
            manifest_by_file[file_name] = entry

    file_entries = _scan_video_files(media_root)
    merged = []
    used_keys = set()

    for file_entry in file_entries:
        manifest_entry = manifest_by_file.get(file_entry["file_name"]) or manifest_by_id.get(file_entry["id"])
        if manifest_entry:
            used_keys.add(manifest_entry.get("id") or manifest_entry.get("file_name") or manifest_entry.get("file"))
        merged.append(_merge_video_entry(file_entry, manifest_entry))

    for entry in manifest_entries:
        entry_id = _normalize_text(entry.get("id"))
        file_name = _normalize_text(entry.get("file_name") or entry.get("file"))
        key = entry_id or file_name
        if key and key in used_keys:
            continue
        if file_name:
            url = file_name if file_name.startswith("/") else _to_public_url(f"media/tutor-videos/{file_name}")
            file_entry = {
                "id": entry_id or _slugify(file_name),
                "title": _humanize_slug(entry.get("title") or Path(file_name).stem),
                "file_name": file_name,
                "url": url,
                "source_type": "manifest",
            }
        else:
            file_entry = {
                "id": entry_id or _slugify(entry.get("title") or "video"),
                "title": _humanize_slug(entry.get("title") or entry.get("topic") or "Video"),
                "file_name": "",
                "url": _normalize_text(entry.get("url")),
                "source_type": "manifest",
            }
        if file_entry["url"]:
            merged.append(_merge_video_entry(file_entry, entry))

    progress_snapshot = get_progress_snapshot(student_name) if student_name else {}
    active_exam_label = _get_active_exam_label(student_name, progress_snapshot)
    scored = []
    for video in merged:
        score, reasons = _score_video(video, progress_snapshot, active_exam_label)
        scored.append(
            {
                **video,
                "relevance_score": score,
                "match_reasons": reasons,
                "recommended_action": "Open 3D Concept" if video.get("visual_learning") else "Use as lesson bridge",
            }
        )

    scored.sort(key=lambda item: (-int(item.get("relevance_score", 0)), item.get("order") is None, item.get("order") or 0, item.get("title", "")))

    return {
        "videos": scored,
        "count": len(scored),
        "manifest_path": str(manifest_path),
        "media_root": str(media_root),
        "student_name": student_name or "",
        "summary": "Drop tutor videos into web/media/tutor-videos and optionally add metadata in data/tutor_video_library.json.",
    }
