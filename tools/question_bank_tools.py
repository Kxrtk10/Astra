import json
import os
import re
from functools import lru_cache

from tools.planner_tools import get_exam_entries, load_planner_state

os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")

QUESTION_BANK_PATH = os.path.join("data", "exam_question_bank.json")
MODEL_CACHE_DIR = "model_cache"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def _normalize_text(value):
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


@lru_cache(maxsize=1)
def _load_question_bank():
    with open(QUESTION_BANK_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=1)
def _load_embedder():
    try:
        from sentence_transformers import SentenceTransformer
        from transformers.utils import logging as transformers_logging

        transformers_logging.set_verbosity_error()

        local_snapshot_path = _resolve_local_embedding_model_path()
        model_path = local_snapshot_path or EMBEDDING_MODEL_NAME

        return SentenceTransformer(
            model_path,
            cache_folder=MODEL_CACHE_DIR,
            local_files_only=bool(local_snapshot_path),
        )
    except Exception:
        return None


def _resolve_local_embedding_model_path():
    repo_dir = os.path.join(
        MODEL_CACHE_DIR,
        "models--sentence-transformers--all-MiniLM-L6-v2",
    )
    refs_main = os.path.join(repo_dir, "refs", "main")
    snapshots_dir = os.path.join(repo_dir, "snapshots")

    if os.path.exists(refs_main):
        with open(refs_main, "r", encoding="utf-8") as file:
            snapshot_hash = file.read().strip()
        snapshot_path = os.path.join(snapshots_dir, snapshot_hash)
        if os.path.exists(snapshot_path):
            return snapshot_path

    if os.path.exists(snapshots_dir):
        children = sorted(os.listdir(snapshots_dir))
        if children:
            fallback_path = os.path.join(snapshots_dir, children[-1])
            if os.path.exists(fallback_path):
                return fallback_path

    return None


@lru_cache(maxsize=1)
def _get_bank_embeddings():
    embedder = _load_embedder()
    bank = _load_question_bank()
    if embedder is None:
        return None

    texts = [
        f"{item['exam']} {item['section']} {item['topic']} {item['difficulty']} {item['question']}"
        for item in bank
    ]
    return embedder.encode(texts, normalize_embeddings=True)


def _cosine_scores(query):
    embedder = _load_embedder()
    bank_embeddings = _get_bank_embeddings()
    if embedder is None or bank_embeddings is None:
        return None

    query_embedding = embedder.encode(query, normalize_embeddings=True)
    return bank_embeddings @ query_embedding


def _token_overlap_score(query, item):
    query_tokens = set(_normalize_text(query).split())
    item_tokens = set(
        _normalize_text(
            f"{item['exam']} {item['section']} {item['topic']} {item['difficulty']} {item['question']}"
        ).split()
    )
    if not query_tokens:
        return 0
    return len(query_tokens & item_tokens) / len(query_tokens)


def _preferred_exams(profile):
    return {exam["name"] for exam in get_exam_entries(profile)}


def _weak_sections(profile):
    state = load_planner_state(profile["name"])
    weaknesses = []

    for exam in get_exam_entries(profile):
        for subject in exam["subjects"]:
            exam_scores = state.get("mock_scores", {}).get(exam["name"], {})
            score = exam_scores.get(subject)
            if score is not None:
                weaknesses.append((score, exam["name"], subject))

    weaknesses.sort(key=lambda item: item[0])
    return {(exam_name, subject) for _, exam_name, subject in weaknesses[:3]}


def retrieve_exam_style_examples(profile, topic, top_k=4):
    bank = _load_question_bank()
    exams = _preferred_exams(profile)
    weak_sections = _weak_sections(profile)
    query = f"{' '.join(sorted(exams))} {topic}"
    scores = _cosine_scores(query)

    ranked = []
    for index, item in enumerate(bank):
        score = float(scores[index]) if scores is not None else _token_overlap_score(query, item)

        if item["exam"] in exams:
            score += 1.5
        if (item["exam"], item["section"]) in weak_sections:
            score += 0.75
        if _normalize_text(topic) in _normalize_text(item["topic"]):
            score += 1.0
        if _normalize_text(topic) in _normalize_text(item["question"]):
            score += 0.5

        ranked.append((score, item))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return [item for _, item in ranked[:top_k]]


def _practice_route_policy(route):
    focus = _normalize_text(str((route or {}).get("focus", "balanced academic clarity")))
    tone = _normalize_text(str((route or {}).get("tone", "focused, exam-like, efficient")))
    pressure = _normalize_text(str((route or {}).get("pressure", "medium")))

    if "calm" in tone or "gentle" in tone or "reassuring" in tone or "small step" in focus:
        return {
            "exam_mix": "JEE Main first, with only a very small Advanced bridge if it truly helps understanding",
            "difficulty_bias": "foundation-to-main",
            "pace": "slow and confidence-building",
            "instructions": (
                "Keep the set short, cleaner, and confidence-safe. Prefer direct scoring questions and avoid heavy traps."
            ),
        }
    if "stretch" in focus or "confident" in tone or "energized" in tone:
        return {
            "exam_mix": "JEE Main plus a stronger Advanced bridge",
            "difficulty_bias": "main-to-advanced",
            "pace": "steady with a light challenge increase",
            "instructions": (
                "Keep the set manageable but slightly deeper. Add one or two advanced-style twists only when they support growth."
            ),
        }
    if "practice" in pressure or "medium" in pressure:
        return {
            "exam_mix": "JEE Main with a controlled Advanced touch",
            "difficulty_bias": "balanced",
            "pace": "steady and exam-like",
            "instructions": (
                "Keep the set focused on the active exam level. Use Advanced-style thinking only as a bridge, not as overload."
            ),
        }
    return {
        "exam_mix": "JEE Main first, Advanced bridge second",
        "difficulty_bias": "balanced",
        "pace": "steady",
        "instructions": "Keep the set exam-ready, not overwhelming.",
    }


def build_grounded_quiz_prompt(profile, user_input, question_count, student_state_route=None):
    raw_input = (user_input or "").strip()
    lowered_input = raw_input.lower()
    topic_match = re.search(
        r"(?:on|about|for)\s+(.+)$",
        raw_input,
        flags=re.IGNORECASE,
    )
    is_mock_request = any(term in lowered_input for term in ["mock", "diagnostic", "mini paper", "mini test", "full paper", "full mock"])
    topic = topic_match.group(1).strip() if topic_match else ("diagnostic baseline mock" if is_mock_request else "the requested topic")
    examples = retrieve_exam_style_examples(profile, topic)
    route = student_state_route or {}
    route_focus = route.get("focus", "balanced academic clarity")
    route_tone = route.get("tone", "focused, exam-like, efficient")
    route_pressure = route.get("pressure", "medium")
    route_source_policy = route.get("source_policy", "exam-pattern and chapter-specific source support")
    route_policy = _practice_route_policy(route)

    examples_block = []
    for index, example in enumerate(examples, start=1):
        examples_block.append(
            "\n".join(
                [
                    f"Example {index}",
                    f"Exam: {example['exam']}",
                    f"Section: {example['section']}",
                    f"Topic: {example['topic']}",
                    f"Difficulty: {example['difficulty']}",
                    f"Question style: {example['question']}",
                    f"Expected answer type: {example['answer_type']}",
                ]
            )
        )

    preferred_exams = ", ".join(sorted(_preferred_exams(profile)))
    mock_instruction = (
        "This is a diagnostic mock baseline request. Spread the questions across the active subjects, reveal strengths and weak spots, and keep the paper balanced rather than topic narrow.\n\n"
        if is_mock_request
        else ""
    )

    return (
        f"{raw_input}\n\n"
        f"The student is preparing for: {preferred_exams}.\n"
        f"Current practice route focus: {route_focus}.\n"
        f"Current practice tone: {route_tone}.\n"
        f"Current practice pressure level: {route_pressure}.\n"
        f"Current practice source policy: {route_source_policy}.\n"
        f"Practice exam mix: {route_policy['exam_mix']}.\n"
        f"Practice difficulty bias: {route_policy['difficulty_bias']}.\n"
        f"Practice pace: {route_policy['pace']}.\n"
        f"Comfort-first instruction: {route_policy['instructions']}\n"
        f"Generate exactly {question_count} original questions.\n"
        f"Keep the questions at the level and style of the grounded examples below.\n"
        "Do not copy the examples verbatim. Use them only as style anchors.\n"
        "Prefer the student's active exams and weaker sections when relevant.\n\n"
        f"{mock_instruction}"
        "Grounded exam-style examples:\n"
        + "\n\n".join(examples_block)
    )
