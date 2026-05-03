import asyncio
import base64
import json
import logging
import os
import re
from uuid import uuid4
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, File, Form, Header, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.events.event import Event
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google import genai
from google.genai.types import Content
from pydantic import BaseModel, Field

from backend.auth import (
    authenticate_user,
    create_user as create_auth_user,
    get_user_by_email,
    get_user_by_student_name,
    issue_session,
    require_bearer_token,
)
from backend.config import settings
from backend.database import init_db
from backend.storage import atomic_write_json, get_storage_status, save_binary_file
from agents.supervisor_agent import supervisor_agent
from tools.analytics_tools import (
    get_analytics_summary,
    load_analytics_state,
    record_checkpoint_attempt as record_analytics_checkpoint_attempt,
    record_practice_attempt,
    record_chapter_completion,
    record_subtopic_score,
)
from tools.app_guide_tools import build_app_guide_reply
from tools.behavior_tools import format_behavior_report, record_behavior_event
from tools.chat_history_tools import (
    create_conversation,
    delete_chat_history,
    get_chat_counts,
    get_chat_history,
    list_conversations,
    list_deleted_conversations,
    resolve_conversation_id,
    restore_conversation,
    save_chat_message,
    update_conversation_metadata,
)
from tools.engagement_tools import (
    award_points,
    format_points_summary,
    get_engagement_snapshot,
    record_bond_interaction,
)
from tools.knowledge_base_tools import (
    KB_SOURCES_ROOT,
    add_document_to_kb,
    add_pyq_database,
    fetch_and_add_web_source,
    get_kb_stats,
    get_topic_coverage,
    init_knowledge_base,
    search_knowledge_base,
)
from tools.feature_health_tools import get_feature_health_snapshot
from tools.fun_fact_tools import get_daily_fun_fact
from tools.live_context_tools import build_live_context_bundle, should_fetch_live_context
from tools.last_minute_tools import build_last_minute_revision_context
from tools.learning_sources_tools import (
    build_learning_sources_context,
    get_learning_sources,
    get_learning_source_pack,
    retrieve_learning_source_bundle,
    should_retrieve_learning_sources,
)
from tools.motivation_tools import (
    ensure_motivation_store,
    get_all_stories,
    get_daily_motivation,
    get_story_by_index,
)
from tools.network_tools import build_network_snapshot
from tools.planner_tools import (
    DEFAULT_EXAM_SUBJECTS,
    format_study_plan,
    format_today_schedule,
    format_weekly_schedule,
    generate_journey_plan,
    generate_this_weeks_plan,
    get_adaptive_learning_profile,
    get_revision_due_today,
    get_student_mastery_map,
    get_todays_focus,
    get_weekly_schedule_data,
    save_mock_scores,
    record_topic_outcome,
)
from tools.jee_syllabus import build_chapter_ready_syllabus
from tools.prompt_instruction_tools import (
    MODE_RESPONSE_SHAPES,
    build_personality_summary,
    build_tutor_prompt,
    build_prompt_instruction_block,
    build_chapter_test_prompt,
    build_subtopic_explanation_prompt,
    evaluate_checkpoint_answer,
    generate_checkpoint_question,
)
from tools.personal_memory_tools import (
    add_memory_item,
    build_tutor_brief_memory_context,
    format_personal_memory_context,
    load_personal_memory,
    remove_memory_item,
    update_personal_memory,
)
from tools.behavior_tools import load_behavior_state
from tools.chapter_session_tools import (
    complete_subtopic,
    get_active_chapter_session,
    get_all_chapter_summaries,
    get_chapter_summary,
    get_current_subtopic,
    get_resume_summary,
    record_chapter_test,
    reset_chapter_session,
    start_chapter_session,
)
from tools.profile_tools import create_profile, load_profile, save_profile
from tools.progress_tracker_tools import (
    get_progress_snapshot,
    load_progress_state,
    get_chapter_mastery_board,
    get_chapter_score_summary,
    log_checkpoint,
    record_checkpoint_attempt as record_progress_checkpoint_attempt,
    log_chapter_score,
    update_progress_status,
    upsert_progress_item,
)
from tools.question_bank_tools import build_grounded_quiz_prompt
from tools.syllabus_tools import (
    build_syllabus_context,
    delete_syllabus_document,
    get_syllabus_documents,
    retrieve_syllabus_context,
    save_syllabus_document,
)
from tools.student_insight_tools import (
    build_student_insight_context,
    build_tutor_brief_insight_context,
    get_student_architecture_snapshot,
    get_student_insight_snapshot,
)
from tools.student_state_router import build_student_state_route, format_student_state_route
from tools.tips_tools import build_tips_context, get_tips_resources
from tools.video_library_tools import get_video_library_snapshot
from tools.video_answer_tools import TutorScript, build_tutor_script, build_video_answer_brief, build_video_render_request
from tools.video_answer_tools import (
    generate_video_brief,
    pre_generate_video_briefs,
    get_video_brief_for_topic,
    load_video_preplan_status,
    load_requested_videos,
    save_requested_video,
    update_requested_video_status,
)
from tools.visual_learning_tools import build_video_explanation, build_visual_learning_aid
from tools.chat_outcome_tracker import build_self_learning_context, load_outcome_state, record_chat_outcome

load_dotenv()
if os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
if os.getenv("GOOGLE_API_KEY") and os.getenv("GEMINI_API_KEY"):
    os.environ.pop("GEMINI_API_KEY", None)

logging.getLogger("google_genai.types").setLevel(logging.ERROR)
logging.getLogger("google.adk.sessions.in_memory_session_service").setLevel(logging.ERROR)

APP_NAME = "adaptive_learning_tutor_web"
USER_ID = "student"
WEB_DIR = Path("web")
VIDEO_RENDER_JOB_DIR = Path("app_data") / "render_jobs"
VIDEO_AUDIO_DIR = Path("app_data") / "audio"
APP_DATA_DIRECTORIES = [
    Path("app_data") / "render_jobs",
    Path("app_data") / "audio",
    Path("app_data") / "profiles",
    Path("app_data") / "planner",
    Path("app_data") / "sessions",
    Path("app_data") / "behavior",
    Path("app_data") / "progress",
    Path("app_data") / "analytics",
    Path("app_data") / "memory",
    Path("app_data") / "video_briefs",
    Path("app_data") / "video_requests",
]
RELOAD_EXCLUDES = [
    "personal_memory/*",
    "behavior_state/*",
    "planner_state/*",
    "profiles/*",
    "__pycache__/*",
]

app = FastAPI(title=settings.app_title, version="1.0.0")
print(f"VERSION: {app.version}", flush=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _ensure_app_data_directories():
    for directory in APP_DATA_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)


def _warn_missing_startup_env_vars():
    checks = [
        ("GEMINI_API_KEY", "Gemini-backed tutor responses", lambda: os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")),
        ("ELEVENLABS_API_KEY", "voice synthesis", lambda: os.getenv("ELEVENLABS_API_KEY")),
        ("DID_API_KEY", "avatar video rendering", lambda: os.getenv("DID_API_KEY")),
        ("BASE_URL", "public audio/video URLs", lambda: os.getenv("BASE_URL") or os.getenv("VIDEO_BASE_URL")),
    ]
    for env_name, feature_name, resolver in checks:
        if not resolver():
            print(f"WARNING: Missing env variable: {env_name} — feature {feature_name} will not work")


@app.middleware("http")
async def guard_unhandled_backend_errors(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        print(f"ERROR: {request.method} {request.url.path} failed — {exc}")
        logging.exception("Unhandled backend error on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error. Please try again."},
        )


@app.middleware("http")
async def disable_static_caching(request: Request, call_next):
    response: Response = await call_next(request)
    if settings.app_env == "development":
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


@app.on_event("startup")
def startup_event():
    init_db()
    _ensure_app_data_directories()
    _warn_missing_startup_env_vars()
    _ensure_video_job_dirs()
    ensure_motivation_store()
    try:
        init_knowledge_base()
        kb_stats = get_kb_stats()
        if kb_stats.get("backend") == "fallback":
            print(f"WARNING: Knowledge base unavailable via ChromaDB; using fallback storage. Stats: {kb_stats}")
        else:
            print(f"Knowledge base initialized: {kb_stats}")
    except Exception as exc:
        print(f"WARNING: Knowledge base initialization failed: {exc}")


@app.get("/app-config.js", include_in_schema=False)
def app_config_js():
    runtime_config = {
        "app_title": settings.app_title,
        "app_env": settings.app_env,
        "api_base_url": settings.api_base_url,
        "default_exam": settings.frontend_default_exam,
        "default_exam_family": _exam_family_label(settings.frontend_default_exam),
        "default_language": settings.frontend_default_language,
        "default_tutor_level": settings.frontend_default_tutor_level,
        "default_tab_order": list(settings.frontend_default_tab_order),
        "video_library_media_root": settings.video_library_media_root,
        "video_library_manifest_path": settings.video_library_manifest_path,
        "avatar_presets": AVATAR_PRESETS,
        "exam_catalog": EXAM_CATALOG,
    }
    payload = "window.APP_CONFIG = " + json.dumps(runtime_config, ensure_ascii=False) + ";"
    return Response(content=payload, media_type="application/javascript")

session_service = InMemorySessionService()
runner = Runner(
    app_name=APP_NAME,
    agent=supervisor_agent,
    session_service=session_service,
    auto_create_session=False,
)
genai_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY")) if os.getenv("GOOGLE_API_KEY") else None

AVATAR_PRESETS = [
    {
        "id": "calm-mentor",
        "name": "Calm Mentor",
        "tagline": "Warm, patient, grounded, and reassuring.",
        "portrait_url": "/media/tutor-faces/GeniusStrategistGuideFemaleMain1.png",
        "accent": "#1f7a6d",
        "secondary_accent": "#8fd2c9",
        "voice_keywords": ["zira", "aria", "female"],
        "voice_rate": 0.92,
        "voice_pitch": 0.92,
        "featured_video_ids": ["female-homepage-hero", "welcome-back-female-tutor"],
        "sample_line": "We will take this step by step, keep the learning calm, and stay with you if you need to pause or ask a doubt.",
        "style_prompt": (
            "Respond like a calm, warm, deeply reassuring female mentor. "
            "Use grounded language, gentle encouragement, clear stepwise explanations, and a natural human rhythm. "
            "Switch structure by mode: Tutor should teach clearly, Practice should stay crisp and corrective, Lounge should feel relaxed and human, "
            "Tips should stay strategic, and Last Minute should stay fast and high-yield. "
            "If the student interrupts, pause cleanly and resume from the last useful checkpoint without repeating the opening."
        ),
    },
    {
        "id": "sharp-strategist",
        "name": "Sharp Strategist",
        "tagline": "Exam-focused, clear, structured, and ambitious.",
        "portrait_url": "/media/tutor-faces/GeniusStrategistGuideMaleMain1.png",
        "accent": "#a14f2a",
        "secondary_accent": "#f3b46b",
        "voice_keywords": ["david", "guy", "male"],
        "voice_rate": 1.0,
        "voice_pitch": 0.98,
        "featured_video_ids": ["strategy-focus-male-tutor", "problem-solving-male-tutor"],
        "sample_line": "Let us lock in on the highest impact move and execute it cleanly.",
        "style_prompt": (
            "Respond like a sharp exam strategist. Be clear, concise, structured, and outcome-focused."
        ),
    },
    {
        "id": "friendly-senior",
        "name": "Friendly Senior",
        "tagline": "Supportive, casual, relatable, and motivating.",
        "portrait_url": "/media/tutor-faces/EnergeticGuideFemaleMain1.png",
        "accent": "#355cbe",
        "secondary_accent": "#9bb4ff",
        "voice_keywords": ["zira", "aria", "female"],
        "voice_rate": 0.98,
        "voice_pitch": 1.03,
        "sample_line": "You are doing better than you think, so let us make this feel lighter, clearer, and easier to continue from here.",
        "style_prompt": (
            "Respond like a friendly female senior guiding a student she genuinely cares about. "
            "Be relatable, natural, and encouraging without losing clarity. "
            "Make the reply feel like a real one-to-one conversation that can switch between voice and text smoothly. "
            "Adapt the reply shape to the active mode so Tutor, Practice, Lounge, Tips, and Last Minute each feel distinct."
        ),
    },
]

EXAM_PRIORITY_ORDER = [
    "JEE MAIN",
    "JEE ADVANCED",
]

JEE_MVP_PRIMARY_EXAM = {
    "name": "JEE MAIN",
    "exam_date": "2026-01-15",
    "subjects": ["Physics", "Chemistry", "Mathematics"],
    "portion": "",
}

EXAM_CATALOG = [
    {"name": "JEE MAIN", "subjects": DEFAULT_EXAM_SUBJECTS["JEE MAIN"]},
    {"name": "JEE ADVANCED", "subjects": DEFAULT_EXAM_SUBJECTS["JEE ADVANCED"]},
]


def _normalize_exam_name(exam_name: str) -> str:
    return str(exam_name or "").strip()


def _exam_family_label(exam_name: str) -> str:
    normalized = _normalize_exam_name(exam_name).upper()
    if not normalized:
        return "JEE"
    if "JEE" in normalized:
        return "JEE"
    return "JEE"


def _ensure_video_job_dirs():
    VIDEO_RENDER_JOB_DIR.mkdir(parents=True, exist_ok=True)
    VIDEO_AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def _video_job_path(job_id: str) -> Path:
    _ensure_video_job_dirs()
    return VIDEO_RENDER_JOB_DIR / f"{job_id}.json"


def _load_video_job(job_id: str) -> dict:
    path = _video_job_path(job_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Video job not found.")
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_json_safe(path: Path, default):
    try:
        if not Path(path).exists():
            return default
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default


def _save_video_job(job_id: str, payload: dict):
    atomic_write_json(str(_video_job_path(job_id)), payload)
    return payload


def _base_url() -> str:
    base_url = (os.getenv("VIDEO_BASE_URL") or os.getenv("BASE_URL") or settings.api_base_url or "").strip().rstrip("/")
    if base_url:
        return base_url
    return f"http://{settings.host}:{settings.port}"


def _resolve_public_url(url: str) -> str:
    value = str(url or "").strip()
    if not value:
        return ""
    if value.startswith("http://") or value.startswith("https://"):
        return value
    if not value.startswith("/"):
        value = f"/{value}"
    return f"{_base_url()}{value}"


def _build_audio_public_url(job_id: str) -> str:
    return f"{_base_url()}/audio/{job_id}.mp3"


def _build_audio_relative_url(job_id: str) -> str:
    return f"/audio/{job_id}.mp3"


def _did_auth_header() -> str:
    api_key = (os.getenv("DID_API_KEY") or "").strip()
    if not api_key:
        return ""
    token = base64.b64encode(api_key.encode("utf-8")).decode("utf-8")
    return f"Basic {token}"


def _write_audio_file(job_id: str, audio_bytes: bytes) -> str:
    _ensure_video_job_dirs()
    audio_path = VIDEO_AUDIO_DIR / f"{job_id}.mp3"
    with open(audio_path, "wb") as handle:
        handle.write(audio_bytes)
    return str(audio_path)


class ChatRequest(BaseModel):
    student_name: str
    message: str
    voice_chat_mode: bool = False
    response_language: str = "English"
    conversation_mode: str = "tutor"
    tutor_mode: str = "calm"
    tutor_level: int = 3
    reading_comfort_mode: bool = False
    chunked_reply_mode: bool = True
    response_pacing: str = "gentle"
    conversation_id: int | None = None


class AvatarSelectionRequest(BaseModel):
    student_name: str
    avatar_id: str


class TutorCustomizationRequest(BaseModel):
    student_name: str
    tutor_name: str = ""
    tutor_personality_preset: str = ""
    tutor_personality_traits: list[str] = Field(default_factory=list)
    tutor_personality_notes: str = ""
    tutor_style: str = ""
    appearance_description: str = ""


class MemoryUpdateRequest(BaseModel):
    student_name: str
    value: str
    category: str


class ExamRequest(BaseModel):
    name: str
    exam_date: str
    subjects: list[str]
    portion: str = ""


class SignupRequest(BaseModel):
    name: str
    max_study_hours_per_day: float = 4
    exams: list[ExamRequest] = Field(default_factory=list)
    exam: str = ""
    exam_date: str = ""
    subjects: list[str] = Field(default_factory=list)
    onboarding_why_astra: str = ""
    onboarding_interests: str = ""
    onboarding_dislikes: str = ""
    onboarding_conversation_style: str = ""
    onboarding_preferred_language: str = ""
    onboarding_explanation_depth: str = ""
    onboarding_stress_support: str = ""
    onboarding_goals_summary: str = ""
    onboarding_astra_question: str = ""
    onboarding_astra_question_answer: str = ""


class ExamUpdateRequest(BaseModel):
    student_name: str
    exams: list[ExamRequest]


class ImageChatRequest(BaseModel):
    student_name: str
    message: str = ""
    image_base64: str
    mime_type: str
    response_language: str = "English"
    conversation_id: int | None = None


class PracticeAnalyticsRequest(BaseModel):
    student_name: str
    mode: str
    time_taken_minutes: float
    accuracy_percent: float
    exam: str = ""
    question_count: int = 0
    notes: str = ""


class MockScoreRequest(BaseModel):
    student_name: str
    exam: str
    physics: float | None = None
    chemistry: float | None = None
    mathematics: float | None = None
    subject_scores: dict[str, float] | None = None


class MockTestGenerateRequest(BaseModel):
    student_name: str
    exam: str = ""
    question_count: int = 9
    mode: str = "diagnostic"


class ProgressItemRequest(BaseModel):
    student_name: str
    exam: str = ""
    subject: str = ""
    topic: str
    status: str = "pending"
    note: str = ""


class ProgressStatusRequest(BaseModel):
    student_name: str
    item_id: str
    status: str


class GroupStudyPreferencesRequest(BaseModel):
    student_name: str
    enabled: bool = True
    mode: str = "mixed"
    group_size: int = 3
    session_minutes: int = 60
    focus: str = ""
    rotation_index: int = 0
    action: str = "save"


class SummarizeRequest(BaseModel):
    student_name: str
    answer_text: str
    response_language: str = "English"
    conversation_mode: str = "tutor"


class CheckpointGenerateRequest(BaseModel):
    student_name: str = ""
    topic: str
    subject: str = ""
    explanation_level: int = 3
    original_explanation: str = ""
    practice_count: int = 0


class CheckpointEvaluateRequest(BaseModel):
    student_name: str = ""
    question: str
    correct_answer: str
    student_answer: str
    topic: str
    subject: str = ""
    explanation_level: int = 3
    original_explanation: str = ""


class VideoAnswerBriefRequest(BaseModel):
    student_name: str
    question: str
    answer_text: str = ""
    response_language: str = "English"
    conversation_mode: str = "tutor"
    tutor_level: int = 3


class VideoAnswerRenderRequest(BaseModel):
    student_name: str
    question: str
    answer_text: str = ""
    response_language: str = "English"
    conversation_mode: str = "tutor"
    tutor_level: int = 3


class VideoGenerateVoiceRequest(BaseModel):
    script_text: str
    voice_id: str = ""
    job_id: str


class VideoRenderJobRequest(BaseModel):
    job_id: str
    tutor_face_url: str
    audio_url: str
    script: TutorScript


class VideoGenerateRequest(BaseModel):
    student_id: str
    question: str
    topic: str
    subject: str
    tutor_face_url: str
    tutor_personality: str


class VideoPrePlanRequest(BaseModel):
    student_id: str
    days_ahead: int = 7


class VideoBriefRequest(BaseModel):
    student_id: str
    topic: str
    subject: str = ""


class VideoRequestSaveRequest(BaseModel):
    student_id: str
    topic: str
    subject: str = ""
    source: str = "request"
    status: str = "requested"
    job_id: str = ""
    video_url: str = ""


class ChatDeleteRequest(BaseModel):
    student_name: str
    conversation_mode: str = ""
    conversation_id: int | None = None


class ConversationCreateRequest(BaseModel):
    student_name: str
    conversation_mode: str = "tutor"
    title: str = "New chat"


class ConversationRestoreRequest(BaseModel):
    student_name: str
    conversation_mode: str = "tutor"
    conversation_id: int


class ConversationUpdateRequest(BaseModel):
    student_name: str
    conversation_mode: str = "tutor"
    conversation_id: int
    title: str | None = None
    pinned: bool | None = None


class AuthRegisterRequest(BaseModel):
    email: str
    password: str
    display_name: str
    student_name: str = ""
    max_study_hours_per_day: float = 4
    onboarding_why_astra: str = ""
    onboarding_interests: str = ""
    onboarding_dislikes: str = ""
    onboarding_conversation_style: str = ""
    onboarding_preferred_language: str = ""
    onboarding_explanation_depth: str = ""
    onboarding_stress_support: str = ""
    onboarding_goals_summary: str = ""
    onboarding_astra_question: str = ""
    onboarding_astra_question_answer: str = ""


class AuthLoginRequest(BaseModel):
    email: str
    password: str


class OnboardingUpdateRequest(BaseModel):
    student_name: str
    onboarding_why_astra: str = ""
    onboarding_interests: str = ""
    onboarding_dislikes: str = ""
    onboarding_conversation_style: str = ""
    onboarding_preferred_language: str = ""
    onboarding_explanation_depth: str = ""
    onboarding_stress_support: str = ""
    onboarding_goals_summary: str = ""
    onboarding_astra_question: str = ""
    onboarding_astra_question_answer: str = ""
    intro_completed: bool = True


class SyllabusUploadRequest(BaseModel):
    student_name: str
    title: str = ""
    text_content: str = ""
    file_base64: str = ""
    file_name: str = ""
    mime_type: str = ""


class SyllabusDeleteRequest(BaseModel):
    student_name: str
    document_id: int


class KnowledgeBaseUrlRequest(BaseModel):
    url: str
    subject: str
    source_name: str = ""


class PlannerSetupRequest(BaseModel):
    student_id: str
    exam_date: str
    hours_per_day: float = 6


class TutorCompleteSessionRequest(BaseModel):
    student_id: str
    topic: str
    subject: str
    unit_name: str = ""
    checkpoint_score: float = 0
    duration_minutes: float = 0
    session_type: str = "learn"
    understood: bool = False


class ChapterStartRequest(BaseModel):
    student_id: str
    unit_name: str
    subject: str


class ChapterSubtopicCompleteRequest(BaseModel):
    student_id: str
    subtopic_id: str
    checkpoint_score: float = 0
    time_spent_minutes: float = 0


class ChapterTestSubmitRequest(BaseModel):
    student_id: str
    unit_name: str
    subject: str
    score: float = 0
    answers: dict | list = Field(default_factory=dict)
    time_taken_minutes: float = 0


class ChapterPracticeRequest(BaseModel):
    student_id: str
    unit_name: str
    practice_type: str


def _session_id_for(name):
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "student-session"


def _build_quiz_request(user_input):
    question_match = re.search(r"(\d+)\s+questions?", user_input, re.IGNORECASE)
    return int(question_match.group(1)) if question_match else 3


def _extract_json_payload(text):
    cleaned = (text or "").strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in model output.")
    return json.loads(cleaned[start : end + 1])


def _normalize_subject_name(subject):
    return re.sub(r"\s+", " ", str(subject or "").strip()).upper()


def _build_mock_question(subject, question_text, options, correct_answer, explanation, difficulty="medium", skill_tag=""):
    return {
        "subject": subject,
        "type": "mcq",
        "difficulty": difficulty,
        "question": question_text,
        "options": options,
        "correct_answer": correct_answer,
        "explanation": explanation,
        "skill_tag": skill_tag,
    }


def _fallback_mock_question(exam_name, subject, index):
    subject_key = _normalize_subject_name(subject)
    difficulty_cycle = ["easy", "medium", "medium", "hard"]
    difficulty = difficulty_cycle[index % len(difficulty_cycle)]

    templates = {
        "PHYSICS": [
            _build_mock_question(
                subject,
                "A body moving with constant velocity has which of the following?",
                ["Zero acceleration", "Zero speed", "Infinite force", "Zero displacement"],
                "Zero acceleration",
                "Constant velocity means the velocity is not changing, so acceleration is zero.",
                difficulty,
                "motion",
            ),
            _build_mock_question(
                subject,
                "What is the SI unit of force?",
                ["Joule", "Watt", "Newton", "Pascal"],
                "Newton",
                "Force is measured in newtons.",
                difficulty,
                "units",
            ),
            _build_mock_question(
                subject,
                "If the net force on a body is zero, the body will most likely...",
                ["Always stop instantly", "Remain at rest or move uniformly", "Reverse direction", "Gain mass"],
                "Remain at rest or move uniformly",
                "Zero net force means no acceleration, so motion stays unchanged.",
                difficulty,
                "newtons-laws",
            ),
            _build_mock_question(
                subject,
                "Which of the following is a scalar quantity?",
                ["Force", "Velocity", "Speed", "Acceleration"],
                "Speed",
                "Speed has magnitude only, so it is scalar.",
                difficulty,
                "scalars-vectors",
            ),
            _build_mock_question(
                subject,
                "A 2 kg body experiences a net force of 6 N. What is its acceleration?",
                ["2 m/s²", "3 m/s²", "4 m/s²", "6 m/s²"],
                "3 m/s²",
                "Using F = ma, a = 6/2 = 3 m/s².",
                difficulty,
                "newtons-laws",
            ),
            _build_mock_question(
                subject,
                "Light travels from air into glass. Which change is most expected?",
                ["Speed increases", "Speed decreases", "Frequency decreases", "Wavelength increases"],
                "Speed decreases",
                "Light slows down in a denser medium like glass.",
                difficulty,
                "optics",
            ),
        ],
        "CHEMISTRY": [
            _build_mock_question(
                subject,
                "Atomic number of an element is equal to the number of...",
                ["Neutrons", "Protons", "Electrons plus neutrons", "Shells"],
                "Protons",
                "Atomic number is defined by the number of protons.",
                difficulty,
                "atomic-structure",
            ),
            _build_mock_question(
                subject,
                "The pH of a neutral solution at 25°C is usually...",
                ["1", "5", "7", "14"],
                "7",
                "Neutral water has pH 7 at room temperature.",
                difficulty,
                "acids-bases",
            ),
            _build_mock_question(
                subject,
                "The valency of oxygen is usually...",
                ["1", "2", "3", "4"],
                "2",
                "Oxygen typically forms two bonds.",
                difficulty,
                "bonding",
            ),
            _build_mock_question(
                subject,
                "Which of the following is a noble gas?",
                ["Nitrogen", "Neon", "Sodium", "Chlorine"],
                "Neon",
                "Neon belongs to Group 18, the noble gases.",
                difficulty,
                "periodic-table",
            ),
            _build_mock_question(
                subject,
                "The chemical formula of water is...",
                ["H2O", "CO2", "NaCl", "O2"],
                "H2O",
                "Water contains two hydrogen atoms and one oxygen atom.",
                difficulty,
                "basic-chemistry",
            ),
            _build_mock_question(
                subject,
                "Which bond is formed by transfer of electrons?",
                ["Covalent bond", "Ionic bond", "Hydrogen bond", "Metallic bond"],
                "Ionic bond",
                "Electron transfer typically leads to ionic bonding.",
                difficulty,
                "chemical-bonding",
            ),
        ],
        "MATHEMATICS": [
            _build_mock_question(
                subject,
                "What is 20% of 150?",
                ["20", "25", "30", "35"],
                "30",
                "20% of 150 equals 30.",
                difficulty,
                "percentages",
            ),
            _build_mock_question(
                subject,
                "Solve: x + 5 = 12",
                ["5", "6", "7", "8"],
                "7",
                "Subtract 5 from both sides.",
                difficulty,
                "linear-equations",
            ),
            _build_mock_question(
                subject,
                "What is the ratio 2:3 written as a fraction?",
                ["1/2", "2/3", "3/2", "4/5"],
                "2/3",
                "A ratio of 2:3 is equivalent to the fraction 2/3.",
                difficulty,
                "ratios",
            ),
            _build_mock_question(
                subject,
                "What is the area of a circle with radius 3?",
                ["6π", "9π", "12π", "18π"],
                "9π",
                "Area = πr² = 9π.",
                difficulty,
                "mensuration",
            ),
            _build_mock_question(
                subject,
                "Solve: x² = 16. What is the positive root?",
                ["2", "4", "8", "16"],
                "4",
                "The positive square root of 16 is 4.",
                difficulty,
                "quadratic-equations",
            ),
            _build_mock_question(
                subject,
                "If A:B = 2:5 and A = 14, what is B?",
                ["28", "30", "35", "42"],
                "35",
                "If 2 parts = 14, then 1 part = 7 and 5 parts = 35.",
                difficulty,
                "ratios",
            ),
        ],
        "MATH": [],
        "BIOLOGY": [
            _build_mock_question(
                subject,
                "Which organelle is known as the powerhouse of the cell?",
                ["Nucleus", "Mitochondria", "Ribosome", "Golgi body"],
                "Mitochondria",
                "Mitochondria produce most of the cell's energy.",
                difficulty,
                "cell-biology",
            ),
            _build_mock_question(
                subject,
                "Photosynthesis primarily occurs in the...",
                ["Nucleus", "Chloroplast", "Mitochondria", "Vacuole"],
                "Chloroplast",
                "Chloroplasts contain chlorophyll and run photosynthesis.",
                difficulty,
                "photosynthesis",
            ),
            _build_mock_question(
                subject,
                "DNA is mainly found in the...",
                ["Cell membrane", "Cytoplasm", "Nucleus", "Ribosome"],
                "Nucleus",
                "In eukaryotic cells, DNA is stored in the nucleus.",
                difficulty,
                "genetics",
            ),
        ],
        "QUANT": [
            _build_mock_question(
                subject,
                "If x is 20% greater than y, then y is what percent less than x?",
                ["10%", "15%", "16.67%", "20%"],
                "16.67%",
                "If x = 1.2y, then y = 5/6 of x, so it is 16.67% less than x.",
                difficulty,
                "percentages",
            ),
            _build_mock_question(
                subject,
                "The ratio of red balls to blue balls is 3:5. If there are 24 red balls, how many blue balls are there?",
                ["30", "32", "36", "40"],
                "40",
                "3 parts correspond to 24, so 1 part is 8 and 5 parts are 40.",
                difficulty,
                "ratios",
            ),
            _build_mock_question(
                subject,
                "Solve: 2x + 3 = 11",
                ["2", "3", "4", "5"],
                "4",
                "Subtract 3, then divide by 2.",
                difficulty,
                "algebra",
            ),
        ],
        "VERBAL": [
            _build_mock_question(
                subject,
                "Choose the word closest in meaning to 'audacious'.",
                ["Bold", "Tired", "Tiny", "Silent"],
                "Bold",
                "Audacious means bold or daring.",
                difficulty,
                "vocabulary",
            ),
            _build_mock_question(
                subject,
                "The sentence is most likely about someone who is 'reluctant'. What does that mean?",
                ["Eager", "Unwilling", "Confused", "Generous"],
                "Unwilling",
                "Reluctant means unwilling or hesitant.",
                difficulty,
                "vocabulary",
            ),
            _build_mock_question(
                subject,
                "Which option best improves clarity in a sentence?",
                ["Make it longer with more adjectives", "Use simpler wording", "Add unrelated examples", "Hide the main point"],
                "Use simpler wording",
                "Clear writing usually benefits from simpler wording.",
                difficulty,
                "writing",
            ),
        ],
        "AWA": [
            _build_mock_question(
                subject,
                "Which choice best identifies a flaw in the argument: 'Sales fell, so the city should add more parking.'",
                ["It assumes parking causes sales", "It proves parking is too expensive", "It compares two different cities", "It mentions too many numbers"],
                "It assumes parking causes sales",
                "The argument does not establish causation.",
                difficulty,
                "argument-analysis",
            ),
            _build_mock_question(
                subject,
                "What is the strongest evidence that would support an argument?",
                ["A relevant statistic", "A random opinion", "A joke", "A distraction"],
                "A relevant statistic",
                "Relevant evidence strengthens an argument best.",
                difficulty,
                "reasoning",
            ),
            _build_mock_question(
                subject,
                "Which statement is most persuasive in an essay?",
                ["Clear claim with support", "No claim at all", "Repeated filler", "Irrelevant facts"],
                "Clear claim with support",
                "A persuasive essay needs a clear claim and supporting evidence.",
                difficulty,
                "writing",
            ),
        ],
        "GENERAL": [
            _build_mock_question(
                subject,
                "Which approach is best when you are unsure about a question in a mock test?",
                ["Guess wildly without reading", "Skip it and return after easier questions", "Leave the paper immediately", "Change answers randomly"],
                "Skip it and return after easier questions",
                "Smart question selection is part of baseline test strategy.",
                difficulty,
                "test-strategy",
            ),
            _build_mock_question(
                subject,
                "Which habit most helps baseline improvement?",
                ["Ignoring mistakes", "Reviewing weak areas after the test", "Avoiding practice", "Rushing every question"],
                "Reviewing weak areas after the test",
                "The report is useful only if you review weak areas afterward.",
                difficulty,
                "improvement",
            ),
            _build_mock_question(
                subject,
                "What is the main purpose of a diagnostic mock test?",
                ["To memorize answers only", "To understand current strengths and weak spots", "To finish fastest no matter what", "To avoid learning"],
                "To understand current strengths and weak spots",
                "A diagnostic mock is meant to reveal the starting point.",
                difficulty,
                "diagnostic",
            ),
        ],
    }

    key_templates = templates.get(subject_key)
    if not key_templates:
        if subject_key in {"MATHS", "MATHEMATICS"}:
            key_templates = templates["MATHEMATICS"]
        else:
            key_templates = templates["GENERAL"]

    template = key_templates[index % len(key_templates)]
    return {
        "id": f"fallback_{index + 1}",
        "subject": subject,
        "type": "mcq",
        "difficulty": template["difficulty"],
        "question": template["question"],
        "options": template["options"],
        "correct_answer": template["correct_answer"],
        "explanation": template["explanation"],
        "skill_tag": template["skill_tag"],
    }


def _fallback_mock_test_payload(exam_name, subjects, question_count, mode):
    fallback_questions = []
    subject_cycle = subjects or ["General"]
    for index in range(question_count):
        subject = subject_cycle[index % len(subject_cycle)]
        fallback_questions.append(_fallback_mock_question(exam_name, subject, index))

    return {
        "student_name": "",
        "exam": exam_name,
        "title": f"{exam_name} Diagnostic Mock Test",
        "time_limit_minutes": 60,
        "instructions": "Solve one question at a time. Choose the best option. This mock is for baseline analysis, not judgment.",
        "subjects": subjects or ["General"],
        "questions": fallback_questions,
        "mode": mode,
    }


def _load_profile_or_404(name):
    profile = load_profile(name)
    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found. Please create or load the profile in the CLI first.",
        )
    return _ensure_jee_mvp_profile_scope(profile)


def _fallback_video_profile(student_name: str, tutor_face_url: str = "", tutor_personality: str = ""):
    cleaned_name = str(student_name or "Student").strip() or "Student"
    return _ensure_jee_mvp_profile_scope(
        {
            "name": cleaned_name,
            "exam": JEE_MVP_PRIMARY_EXAM["name"],
            "exam_date": JEE_MVP_PRIMARY_EXAM["exam_date"],
            "subjects": list(JEE_MVP_PRIMARY_EXAM["subjects"]),
            "study_hours_per_day": 3,
            "max_study_hours_per_day": 6,
            "preferred_persona": "",
            "preferred_voice": "",
            "voice_rate": -2,
            "selected_avatar": "calm-mentor",
            "tutor_name": "Astra",
            "tutor_style": str(tutor_personality or "positive, encouraging, and easy to talk to").strip(),
            "tutor_personality_preset": "balanced",
            "tutor_personality_traits": [],
            "tutor_personality_notes": str(tutor_personality or "").strip(),
            "appearance_description": "friendly, fun, and human-like",
            "avatar_visuals": {
                "portrait_url": str(tutor_face_url or "").strip(),
            },
            "default_response_language": "English",
            "default_tutor_level": 3,
            "onboarding_profile": {
                "intro_completed": False,
                "why_astra": "",
                "interests": "",
                "dislikes": "",
                "conversation_style": "",
                "preferred_language": "",
                "explanation_depth": "",
                "stress_support": "",
                "goals_summary": "",
                "astra_question": "",
                "astra_question_answer": "",
            },
            "group_study_preferences": {
                "enabled": False,
                "mode": "solo",
                "group_size": 3,
                "session_minutes": 60,
                "focus": "",
                "rotation_index": 0,
            },
            "exams": [
                {
                    "name": JEE_MVP_PRIMARY_EXAM["name"],
                    "exam_date": JEE_MVP_PRIMARY_EXAM["exam_date"],
                    "subjects": list(JEE_MVP_PRIMARY_EXAM["subjects"]),
                }
            ],
            "jee_mvp_initialized": True,
        }
    )


def _clean_exam_entries(raw_exams):
    cleaned = []
    for exam in raw_exams or []:
        if isinstance(exam, BaseModel):
            exam = exam.model_dump()
        name = str(exam.get("name", "")).strip().upper()
        if name == "JEE":
            name = "JEE MAIN"
        if name not in {"JEE MAIN", "JEE ADVANCED"}:
            continue
        exam_date = str(exam.get("exam_date", "")).strip()
        subjects = [str(subject).strip() for subject in exam.get("subjects", []) if str(subject).strip()]
        portion = str(exam.get("portion", "")).strip()
        if not name or not exam_date or not subjects:
            continue
        cleaned.append(
            {
                "name": name,
                "exam_date": exam_date,
                "subjects": subjects,
                "portion": portion,
            }
        )
    return cleaned


def _sync_profile_exam_fields(profile):
    exams = _clean_exam_entries(profile.get("exams", []))
    if not exams:
        profile["exams"] = [dict(JEE_MVP_PRIMARY_EXAM)]
        profile["exam"] = JEE_MVP_PRIMARY_EXAM["name"]
        profile["exam_date"] = JEE_MVP_PRIMARY_EXAM["exam_date"]
        profile["subjects"] = list(JEE_MVP_PRIMARY_EXAM["subjects"])
        if "study_hours_per_day" not in profile:
            profile["study_hours_per_day"] = profile.get("max_study_hours_per_day", 4)
        return profile

    primary_exam = exams[0]
    profile["exams"] = exams
    profile["exam"] = primary_exam["name"]
    profile["exam_date"] = primary_exam["exam_date"]
    profile["subjects"] = primary_exam["subjects"]
    if "study_hours_per_day" not in profile:
        profile["study_hours_per_day"] = profile.get("max_study_hours_per_day", 4)
    return profile


def _ensure_jee_mvp_profile_scope(profile):
    profile = _sync_profile_exam_fields(profile)
    exam_names = {str(exam.get("name", "")).strip().upper() for exam in profile.get("exams", [])}
    if any(name in {"JEE", "JEE MAIN", "JEE ADVANCED"} for name in exam_names):
        return profile

    if profile.get("jee_mvp_initialized"):
        return profile

    legacy_exams = profile.get("exams", [])
    if legacy_exams:
        profile["legacy_exam_scope"] = legacy_exams

    profile["exams"] = [dict(JEE_MVP_PRIMARY_EXAM)]
    profile["exam"] = JEE_MVP_PRIMARY_EXAM["name"]
    profile["exam_date"] = JEE_MVP_PRIMARY_EXAM["exam_date"]
    profile["subjects"] = list(JEE_MVP_PRIMARY_EXAM["subjects"])
    profile["jee_mvp_initialized"] = True
    save_profile(profile)
    return profile


async def _ensure_session(profile, conversation_mode="tutor", tutor_level=3):
    session_id = f"{_session_id_for(profile['name'])}-{conversation_mode}"
    existing = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )
    if existing is None:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
            state={
                "profile": profile,
                "conversation_mode": conversation_mode,
                "tutor_level": tutor_level,
            },
        )
    else:
        existing.state["profile"] = profile
        existing.state["conversation_mode"] = conversation_mode
        existing.state["tutor_level"] = tutor_level
    return session_id


_TUTOR_HISTORY_REDACTION_PHRASES = (
    "let's work through",
    "start with the main idea",
    "i will explain",
    "let me",
    "we will",
    "i want to keep",
    "start with the smallest",
    "step by step",
    "i'll continue from here",
)
_TUTOR_HISTORY_REDACTION_PLACEHOLDER = "[Concept was explained here]"
_TUTOR_HISTORY_KEEP_LAST_MESSAGES = 10
_TUTOR_INSTRUCTION_MARKERS = (
    "you are astra",
    "preferred persona",
    "global mode guardrails",
    "do not blend tutor",
    "never describe what you are about to do",
    "never start your response with a plan",
)


def _event_text(event) -> str:
    content = getattr(event, "content", None)
    if not content or not getattr(content, "parts", None):
        return ""
    parts = []
    for part in content.parts:
        text = getattr(part, "text", None)
        if text:
            parts.append(str(text))
    return " ".join(parts).strip()


def _is_instruction_event(event) -> bool:
    author = str(getattr(event, "author", "") or "").strip().lower()
    if author == "user":
        return False
    text = _event_text(event).lower()
    if not text:
        return False
    return any(marker in text for marker in _TUTOR_INSTRUCTION_MARKERS)


def _redact_poisoned_assistant_event(event):
    author = str(getattr(event, "author", "") or "").strip().lower()
    if author == "user":
        return event
    text = _event_text(event).lower()
    if not text:
        return event
    if any(phrase in text for phrase in _TUTOR_HISTORY_REDACTION_PHRASES):
        role = getattr(getattr(event, "content", None), "role", "model") or "model"
        event.content = Content(
            role=role,
            parts=[{"text": _TUTOR_HISTORY_REDACTION_PLACEHOLDER}],
        )
    return event


def _sanitize_tutor_session_history(session_id: str) -> None:
    if not hasattr(session_service, "sessions"):
        return
    stored_session = (
        session_service.sessions.get(APP_NAME, {})
        .get(USER_ID, {})
        .get(session_id)
    )
    if stored_session is None or not getattr(stored_session, "events", None):
        return

    events = list(stored_session.events)
    protected_prefix = []
    for event in events:
        if len(protected_prefix) >= 2:
            break
        if _is_instruction_event(event):
            protected_prefix.append(event)
        else:
            break

    history_events = events[len(protected_prefix):]
    trimmed_history = history_events[-_TUTOR_HISTORY_KEEP_LAST_MESSAGES:]
    sanitized_history = [_redact_poisoned_assistant_event(event) for event in trimmed_history]
    stored_session.events = protected_prefix + sanitized_history


def _build_onboarding_profile_from_request(
    why_astra="",
    interests="",
    dislikes="",
    conversation_style="",
    preferred_language="",
    explanation_depth="",
    stress_support="",
    goals_summary="",
    astra_question="",
    astra_question_answer="",
    intro_completed=False,
):
    return {
        "intro_completed": bool(intro_completed),
        "why_astra": str(why_astra).strip(),
        "interests": str(interests).strip(),
        "dislikes": str(dislikes).strip(),
        "conversation_style": str(conversation_style).strip(),
        "preferred_language": str(preferred_language).strip(),
        "explanation_depth": str(explanation_depth).strip(),
        "stress_support": str(stress_support).strip(),
        "goals_summary": str(goals_summary).strip(),
        "astra_question": str(astra_question).strip(),
        "astra_question_answer": str(astra_question_answer).strip(),
    }


def _apply_onboarding_profile(profile, onboarding_profile):
    normalized = _build_onboarding_profile_from_request(
        why_astra=onboarding_profile.get("why_astra", ""),
        interests=onboarding_profile.get("interests", ""),
        dislikes=onboarding_profile.get("dislikes", ""),
        conversation_style=onboarding_profile.get("conversation_style", ""),
        preferred_language=onboarding_profile.get("preferred_language", ""),
        explanation_depth=onboarding_profile.get("explanation_depth", ""),
        stress_support=onboarding_profile.get("stress_support", ""),
        goals_summary=onboarding_profile.get("goals_summary", ""),
        astra_question=onboarding_profile.get("astra_question", ""),
        astra_question_answer=onboarding_profile.get("astra_question_answer", ""),
        intro_completed=onboarding_profile.get("intro_completed", False),
    )
    profile["onboarding_profile"] = normalized
    save_profile(profile)
    if normalized["preferred_language"]:
        profile["default_response_language"] = normalized["preferred_language"]
    if normalized["explanation_depth"]:
        depth_text = normalized["explanation_depth"].lower()
        if any(word in depth_text for word in ["short", "brief", "quick"]):
            profile["default_tutor_level"] = 1
        elif any(word in depth_text for word in ["simple", "easy"]):
            profile["default_tutor_level"] = 2
        elif any(word in depth_text for word in ["deep", "detailed", "expert"]):
            profile["default_tutor_level"] = 5
        else:
            profile["default_tutor_level"] = 3
    save_profile(profile)
    if normalized["interests"]:
        update_personal_memory(profile["name"], "interests", normalized["interests"])
    if normalized["dislikes"]:
        update_personal_memory(profile["name"], "life_notes", f"Avoid: {normalized['dislikes']}")
    if normalized["conversation_style"]:
        update_personal_memory(profile["name"], "life_notes", f"Preferred conversation style: {normalized['conversation_style']}")
    if normalized["stress_support"]:
        update_personal_memory(profile["name"], "life_notes", f"Support when stressed: {normalized['stress_support']}")
    if normalized["goals_summary"]:
        update_personal_memory(profile["name"], "life_notes", f"Goals: {normalized['goals_summary']}")
    if normalized["preferred_language"]:
        update_personal_memory(profile["name"], "life_notes", f"Preferred language: {normalized['preferred_language']}")
    if normalized["explanation_depth"]:
        update_personal_memory(profile["name"], "life_notes", f"Preferred explanation depth: {normalized['explanation_depth']}")
    if normalized["astra_question"]:
        add_memory_item(profile["name"], "life_notes", f"Asked Astra: {normalized['astra_question']}")
    if normalized["astra_question_answer"]:
        add_memory_item(profile["name"], "life_notes", f"Astra answered: {normalized['astra_question_answer']}")
    return profile


_CONFUSION_PHRASES = [
    "i don't understand", "i dont understand", "confused", "what do you mean",
    "can you explain again", "explain again", "still don't get", "still dont get",
    "not clear", "huh", "what?", "that doesn't make sense", "lost me",
    "i'm lost", "im lost", "too complex", "too complicated",
]
_UNDERSTOOD_PHRASES = [
    "got it", "i understand", "makes sense", "oh i see", "thank you",
    "thanks", "clear now", "that helps", "understood", "ah okay", "ohh",
    "now i get it", "perfect", "great explanation",
]
_NEGATIVE_SENTIMENT = [
    "stressed", "anxious", "worried", "tired", "overwhelmed", "scared",
    "hate", "frustrated", "i can't", "i cant", "hopeless",
]
_POSITIVE_SENTIMENT = [
    "good", "great", "confident", "motivated", "excited", "ready",
    "easy", "happy", "relieved", "calm", "fresh",
]


def _detect_topic_from_message(message):
    """Extract a rough topic keyword from the student message."""
    lowered = message.lower().strip()
    for prefix in ["explain ", "teach me ", "what is ", "how does ", "tell me about "]:
        if lowered.startswith(prefix):
            return lowered[len(prefix):].strip("?.! ")[:60]
    words = lowered.split()
    if len(words) <= 5:
        return lowered.strip("?.! ")[:60]
    return ""


def _detect_re_ask(message, name):
    """Check if the student is re-asking a topic that was recently explained."""
    topic = _detect_topic_from_message(message)
    if not topic:
        return False, topic
    from tools.chat_outcome_tracker import get_recent_topic_outcomes
    recent = get_recent_topic_outcomes(name, last_n=15)
    for outcome in recent:
        if outcome.get("topic") and topic and outcome["topic"] in topic or topic in outcome.get("topic", ""):
            return True, topic
    return False, topic


def _record_chat_outcome_from_reply(name, user_message, tutor_reply, conversation_mode):
    """Infer a chat outcome from the user message and record it."""
    msg_lower = (user_message or "").lower()

    # Detect outcome
    is_confused = any(phrase in msg_lower for phrase in _CONFUSION_PHRASES)
    is_understood = any(phrase in msg_lower for phrase in _UNDERSTOOD_PHRASES)

    if is_confused:
        outcome = "confused"
    elif is_understood:
        outcome = "understood"
    else:
        outcome = "neutral"

    # Detect sentiment
    has_negative = any(phrase in msg_lower for phrase in _NEGATIVE_SENTIMENT)
    has_positive = any(phrase in msg_lower for phrase in _POSITIVE_SENTIMENT)
    sentiment = "negative" if has_negative else "positive" if has_positive else "neutral"

    # Detect topic and re-ask
    is_re_ask, topic = _detect_re_ask(user_message, name)
    if is_re_ask and outcome == "neutral":
        outcome = "confused"

    follow_up = any(
        phrase in msg_lower
        for phrase in ["more detail", "explain more", "go deeper", "elaborate", "one more example"]
    )

    record_chat_outcome(
        name=name,
        topic=topic,
        outcome=outcome,
        user_sentiment_before=sentiment,
        user_sentiment_after="neutral",
        follow_up_needed=follow_up,
        re_ask=is_re_ask,
        conversation_mode=conversation_mode,
    )


def _handle_local_command(profile, user_input):
    normalized = user_input.strip().lower()

    if normalized in {"generate study plan", "create study plan"}:
        return format_study_plan(profile), "study_plan_request"
    if normalized == "what should i study today?":
        return format_today_schedule(profile), "today_plan_request"
    if normalized == "show weekly plan":
        return format_weekly_schedule(profile), "weekly_plan_request"
    if normalized in {
        "how am i doing behaviorally?",
        "how am i doing behaviorally",
        "show behavior report",
    }:
        return format_behavior_report(profile), "behavior_report_request"
    if normalized == "show my points":
        return format_points_summary(profile), "motivation_dashboard_request"

    return None, None


def _get_avatar_preset(profile):
    selected_avatar = profile.get("selected_avatar")
    return next((avatar for avatar in AVATAR_PRESETS if avatar["id"] == selected_avatar), None)


def _appearance_visuals_from_description(description, avatar=None):
    text = (description or "").lower()
    accent = (avatar or {}).get("accent", "#1f7a6d")
    visuals = {
        "skin": "#f4d1b4",
        "hair": "#3b2a22",
        "eyes": "#2a2017",
        "outfit": accent,
        "glasses": False,
        "hoodie": False,
    }

    if any(word in text for word in ["dark skin", "brown skin", "dusky"]):
        visuals["skin"] = "#9b6a4c"
    elif any(word in text for word in ["fair", "light skin", "pale"]):
        visuals["skin"] = "#f5dbc8"

    if any(word in text for word in ["blonde", "golden hair"]):
        visuals["hair"] = "#b68a32"
    elif any(word in text for word in ["blue hair"]):
        visuals["hair"] = "#355cbe"
    elif any(word in text for word in ["brown hair"]):
        visuals["hair"] = "#5a3c28"
    elif any(word in text for word in ["red hair"]):
        visuals["hair"] = "#9e4b2e"

    if any(word in text for word in ["green eyes"]):
        visuals["eyes"] = "#2f6b4f"
    elif any(word in text for word in ["blue eyes"]):
        visuals["eyes"] = "#355cbe"

    if "glasses" in text or "spectacles" in text:
        visuals["glasses"] = True
    if "hoodie" in text or "hooded" in text:
        visuals["hoodie"] = True

    if any(word in text for word in ["sporty", "sports", "athletic"]):
        visuals["outfit"] = "#d16f2d"
    elif any(word in text for word in ["tech", "futuristic", "cyber"]):
        visuals["outfit"] = "#355cbe"
    elif any(word in text for word in ["calm", "minimal", "soft"]):
        visuals["outfit"] = "#1f7a6d"

    return visuals


def _build_tutor_brain_snapshot(
    profile,
    avatar,
    student_insight_snapshot,
    conversation_mode,
    tutor_level,
    voice_chat_mode,
    reading_comfort_mode=False,
    chunked_reply_mode=False,
    response_pacing="gentle",
):
    route = build_student_state_route(
        profile,
        conversation_mode=conversation_mode,
        tutor_level=tutor_level,
        support_style=(student_insight_snapshot or {}).get("support_style"),
        insight_snapshot=student_insight_snapshot,
    )
    preset_name = (avatar or {}).get("name", "Calm Mentor")
    is_female_voice = "female" in " ".join((avatar or {}).get("voice_keywords", [])).lower() or (avatar or {}).get("id") in {"calm-mentor", "friendly-senior"}
    voice_profile = {
        "preferred_voice": profile.get("preferred_voice") or "",
        "rate": profile.get("voice_rate", -2),
        "assistant_voice_family": "female" if is_female_voice else "neutral",
        "speaking_style": "warm, articulate, and easy to interrupt" if is_female_voice else "clear and structured",
    }
    if conversation_mode == "tutor":
        if is_female_voice:
            teaching_identity = "Female tutor brain: warm, composed, and human-like."
        else:
            teaching_identity = f"{preset_name} tutor brain: focused and supportive."
    elif conversation_mode == "practice":
        teaching_identity = "Practice brain: concise, exam-like, and correction-first."
    elif conversation_mode == "lounge":
        teaching_identity = "Lounge brain: casual, safe, and conversational."
    elif conversation_mode == "last_minute":
        teaching_identity = "Last Minute brain: high-yield, urgent, and calming."
    elif conversation_mode == "tips":
        teaching_identity = "Tips brain: strategic, practical, and exam-action driven."
    else:
        teaching_identity = "Guide brain: product-focused and clear."

    return {
        "brain_label": preset_name,
        "mode": conversation_mode,
        "tutor_level": tutor_level,
        "voice_chat_mode": voice_chat_mode,
        "reading_comfort_mode": reading_comfort_mode,
        "chunked_reply_mode": chunked_reply_mode,
        "response_pacing": response_pacing,
        "identity": teaching_identity,
        "mode_response_shape": MODE_RESPONSE_SHAPES.get(conversation_mode, MODE_RESPONSE_SHAPES["tutor"]),
        "tone": route.get("tone", "balanced, clear, supportive"),
        "feel": route.get("feel", "balanced and supportive"),
        "pressure": route.get("pressure", "medium"),
        "focus": route.get("focus", "balanced academic clarity"),
        "teaching_adjustment": route.get("teaching_adjustment", "Keep the explanation small, clear, and check understanding before moving on."),
        "next_step": route.get("next_step", "Start with the smallest useful action and grow from there."),
        "avoid": route.get("avoid", []),
        "voice_profile": voice_profile,
        "resume_hint": "If the student interrupts, continue from the exact last checkpoint or incomplete step, do not repeat the opening, and keep the continuation natural.",
        "three_d_hint": "Use the 3D tutor board as the visible tutor room, and shift into the concept board when a visual scene helps more.",
    }


def _build_mode_aware_fallback_reply(
    user_input,
    conversation_mode,
    tutor_level,
    tutor_brain,
    student_insight_snapshot,
    reading_comfort_mode=False,
    chunked_reply_mode=False,
    response_pacing="gentle",
):
    mode = (conversation_mode or "tutor").strip().lower()
    topic_hint = _detect_topic_from_message(user_input) or "this topic"
    topic_label = re.sub(r"\s+", " ", topic_hint).strip("?.! ")[:80] or "this topic"
    insight = student_insight_snapshot or {}
    topic_mastery = insight.get("topic_mastery") or {}
    weak_topics = list(topic_mastery.get("weak_topics") or [])
    primary_weak = weak_topics[0] if weak_topics else ""
    emotional_state = str(insight.get("emotional_state", "steady")).strip().lower()
    teaching_adjustment = (tutor_brain or {}).get("teaching_adjustment", "").strip()
    next_step = (tutor_brain or {}).get("next_step", "Start with the smallest useful action and grow from there.").strip()
    mode_shape = MODE_RESPONSE_SHAPES.get(mode, MODE_RESPONSE_SHAPES["tutor"])
    level = max(1, min(int(tutor_level or 3), 5))

    if mode == "guide":
        return build_app_guide_reply(user_input)

    if mode == "lounge":
        return (
            f"That sounds like something we can keep calm and easy. "
            f"If you want, tell me more about {topic_label}, and I’ll stay with you at your pace."
        )

    pacing_label = str(response_pacing or "standard").strip().lower()
    accessibility_suffix = ""
    if reading_comfort_mode or chunked_reply_mode or pacing_label != "standard":
        accessibility_suffix = " I’ll keep it short, broken into small parts, and easy to scan."

    if mode == "tips":
        return (
            f"Tip for {topic_label}: use it as a decision rule, not just as theory. "
            f"Apply it at the moment you choose what to attempt, what to skip, or what to revisit.{accessibility_suffix} "
            f"If you want, I can turn this into a quick exam strategy checklist next."
        )

    if mode == "last_minute":
        lines = [
            f"Last-minute rescue for {topic_label}:",
            f"1. Focus on the core idea first.",
            f"2. Remember the most common trap or formula link.",
            f"3. Use one quick recall check before moving on.",
        ]
        if primary_weak:
            lines.append(f"4. Revisit {primary_weak} only if it is blocking scoring.")
        return "\n".join(lines)

    if mode == "practice":
        lines = [
            f"Practice mode for {topic_label}:",
            "1. Identify the concept the question is testing.",
            "2. Solve it in one clean path and keep the working exam-like.",
            "3. Check the answer against the expected condition or option.",
        ]
        if primary_weak:
            lines.append(f"Focus note: {primary_weak} has needed extra support before, so keep the first attempt small and accurate.")
        return "\n".join(lines)

    tutor_intro = f"Let’s work through {topic_label} step by step."
    if level <= 2:
        core = "The simplest way to think about it is to identify what is given, choose the key rule, and apply it once carefully."
    elif level == 3:
        core = "Start with the main idea, then use one clean example or visual cue, and finish with a quick check so the logic stays clear."
    else:
        core = "Start with the main idea, connect it to the underlying rule or formula, and then extend it once more if the student wants a deeper or exam-level version."

    follow_up = f"If you send the exact question, I’ll continue from here without restarting the whole explanation. {next_step}"
    if primary_weak:
        follow_up = (
            f"I also want to keep a careful eye on {primary_weak} because it has shown up as a weak area before. "
            f"{follow_up}"
        )
    if teaching_adjustment:
        follow_up = f"{teaching_adjustment} {follow_up}"
    if emotional_state in {"overwhelmed", "strained"}:
        tutor_intro = f"Let’s keep {topic_label} small and calm."
        core = "I’ll keep this short, clear, and easy to follow so the next step feels manageable."

    if len(mode_shape) >= 4:
        return "\n".join([tutor_intro, core, follow_up])
    return f"{tutor_intro} {core} {follow_up}"


def _run_agent_reply(
    profile,
    user_input,
    voice_chat_mode=False,
    response_language="English",
    conversation_mode="tutor",
    tutor_mode="calm",
    tutor_level=3,
    reading_comfort_mode=False,
    chunked_reply_mode=False,
    response_pacing="gentle",
):
    session_id = asyncio.run(_ensure_session(profile, conversation_mode, tutor_level))
    if conversation_mode == "tutor":
        _sanitize_tutor_session_history(session_id)
    exam_names = {str(exam.get("name", "")).strip().upper() for exam in profile.get("exams", [])}
    is_jee_track = any(name in {"JEE", "JEE MAIN", "JEE ADVANCED"} for name in exam_names)
    avatar = _get_avatar_preset(profile)
    personal_memory = (
        build_tutor_brief_memory_context(profile["name"])
        if conversation_mode == "tutor"
        else format_personal_memory_context(profile["name"])
    )
    student_insight_context = (
        build_tutor_brief_insight_context(profile)
        if conversation_mode == "tutor"
        else build_student_insight_context(profile)
    )
    student_insight_snapshot = get_student_insight_snapshot(profile)
    tutor_brain = _build_tutor_brain_snapshot(
        profile,
        avatar,
        student_insight_snapshot,
        conversation_mode,
        tutor_level,
        voice_chat_mode,
        reading_comfort_mode,
        chunked_reply_mode,
        response_pacing,
    )
    syllabus_context = build_syllabus_context(profile["name"])
    syllabus_retrieval_bundle = {"text": "", "sources": []}
    tutor_name = profile.get("tutor_name", "Astra")
    tutor_style = profile.get("tutor_style", "positive, encouraging, and easy to talk to")
    adaptive_profile = get_adaptive_learning_profile(profile)
    todays_focus = get_todays_focus(profile["name"]) if conversation_mode == "tutor" else {}
    revision_due_today = get_revision_due_today(profile["name"]) if conversation_mode == "tutor" else []
    mastery_map = get_student_mastery_map(profile["name"]) if conversation_mode == "tutor" else {}
    active_chapter_subtopic = get_current_subtopic(profile["name"]) if conversation_mode == "tutor" else {}
    student_state_route = build_student_state_route(
        profile,
        conversation_mode=conversation_mode,
        tutor_level=tutor_level,
        support_style=student_insight_snapshot.get("support_style"),
        insight_snapshot=student_insight_snapshot,
        todays_focus=todays_focus.get("primary") if isinstance(todays_focus, dict) else {},
        revision_due=revision_due_today,
        mastery_map=mastery_map,
    )
    if conversation_mode == "tutor":
        tutor_mode_label = str(tutor_mode or "calm").strip().lower()
        if tutor_mode_label == "motivating":
            tutor_mode_hint = "Tutor mode preference: motivating. Keep the teaching warm, uplifting, and confidence-building while staying clear."
        elif tutor_mode_label == "strict":
            tutor_mode_hint = "Tutor mode preference: strict. Keep the teaching concise, direct, and exam-focused with minimal extra padding."
        else:
            tutor_mode_hint = "Tutor mode preference: calm. Keep the teaching steady, reassuring, and easy to follow."
        instruction_block = build_tutor_prompt(
            profile,
            conversation_mode=conversation_mode,
            tutor_level=tutor_level,
            response_language=response_language,
            voice_chat_mode=voice_chat_mode,
            support_style=student_insight_snapshot.get("support_style"),
            student_insight_snapshot=student_insight_snapshot,
            reading_comfort_mode=reading_comfort_mode,
            chunked_reply_mode=chunked_reply_mode,
            response_pacing=response_pacing,
            todays_focus=todays_focus,
            memory_context=personal_memory,
            session_type=(todays_focus.get("primary", {}) or {}).get("session_type", "learn") if isinstance(todays_focus, dict) else "learn",
            knowledge_query=user_input,
            student_state_snapshot=student_state_route.get("planner_state", {}),
        )
        if active_chapter_subtopic:
            chapter_kb = search_knowledge_base(
                f"{active_chapter_subtopic.get('subtopic_name', '')} {active_chapter_subtopic.get('unit_name', '')}",
                active_chapter_subtopic.get("subject", ""),
                n_results=5,
                session_type=active_chapter_subtopic.get("session_type", "learn"),
            )
            chapter_block = build_subtopic_explanation_prompt(
                profile["name"],
                active_chapter_subtopic.get("unit_name", ""),
                active_chapter_subtopic.get("subtopic_name", ""),
                active_chapter_subtopic.get("concepts", []),
                active_chapter_subtopic.get("subject", ""),
                active_chapter_subtopic.get("session_type", "learn"),
                chapter_kb,
            )
            instruction_block = "\n\n".join([instruction_block, chapter_block])
    else:
        instruction_block = build_prompt_instruction_block(
            profile,
            conversation_mode=conversation_mode,
            tutor_level=tutor_level,
            response_language=response_language,
            voice_chat_mode=voice_chat_mode,
            support_style=student_insight_snapshot.get("support_style"),
            student_insight_snapshot=student_insight_snapshot,
            reading_comfort_mode=reading_comfort_mode,
            chunked_reply_mode=chunked_reply_mode,
            response_pacing=response_pacing,
        )

    live_context_bundle = {"text": "", "sources": []}
    learning_retrieval_bundle = {"text": "", "sources": []}

    if user_input.lower().startswith("generate quiz"):
        question_count = _build_quiz_request(user_input)
        practice_route = build_student_state_route(
            profile,
            conversation_mode="practice",
            tutor_level=tutor_level,
            support_style=student_insight_snapshot.get("support_style"),
            insight_snapshot=student_insight_snapshot,
        )
        outgoing_message = build_grounded_quiz_prompt(profile, user_input, question_count, practice_route)
    elif conversation_mode == "guide":
        return {
            "reply": build_app_guide_reply(user_input),
            "live_sources": [],
            "visual_learning": None,
            "video_explanation": None,
            "adaptive_profile": None,
        }
    else:
        outgoing_message = instruction_block
        outgoing_message += f"\n\nStudent message:\n{user_input}"
        outgoing_message += (
            "\n\nCore support policy for this tutor: stay academically focused, clear, and efficient by default. "
            "Be kind and motivating, but do not assume the student's mental state unless the student clearly expresses it or the pattern is repeated over time. "
            "If support is needed, keep it brief and practical, then return to the concept or task quickly."
        )
        outgoing_message += (
            "\n\nRelationship policy: be warm enough to feel human, but keep the tutor role primary. "
            "Do not drift into casual conversation or emotional speculation inside the tutor tab. "
            "If the student wants to vent or chat casually, suggest the Lounge tab instead."
        )
        outgoing_message += (
            "\n\nDo not invent personal facts, family members, relationships, emotions, support systems, or life events. "
            "Only mention personal details that are explicitly present in the current user message or in the supplied personal memory context."
        )
        outgoing_message += (
            f"\n\nThe tutor's chosen name is {tutor_name}. It may occasionally refer to itself by that name in a natural way."
        )
        outgoing_message += (
            f"\n\nThe tutor's custom personality style is: {tutor_style}. "
            "Honor this naturally while staying supportive, clear, and helpful."
        )
        outgoing_message += (
            "\n\nTutor brain contract: "
            f"{tutor_brain['identity']} "
            f"Tone: {tutor_brain['tone']}. "
            f"Feel: {tutor_brain['feel']}. "
            f"Pressure: {tutor_brain['pressure']}. "
            f"Teaching adjustment: {tutor_brain['teaching_adjustment']}. "
            f"Next step: {tutor_brain['next_step']}. "
            f"Voice profile: {tutor_brain['voice_profile']['speaking_style']}. "
            f"Resume rule: {tutor_brain['resume_hint']}."
        )
        outgoing_message += f"\n\nPersonal memory context:\n{personal_memory}"
        outgoing_message += f"\n\n{student_insight_context}"
        self_learning_ctx = build_self_learning_context(profile["name"])
        if self_learning_ctx:
            outgoing_message += f"\n\n{self_learning_ctx}"
        if conversation_mode in {"last_minute", "tips"} and syllabus_context:
            outgoing_message += f"\n\nSyllabus / uploaded portion context:\n{syllabus_context}"
        syllabus_query = user_input.lower()
        syllabus_needs_retrieval = conversation_mode in {"last_minute", "tips"} or any(
            term in syllabus_query for term in ["syllabus", "portion", "chapter", "uploaded", "course"]
        )
        if syllabus_needs_retrieval:
            syllabus_retrieval_bundle = retrieve_syllabus_context(profile["name"], user_input, max_chunks=2)
            if syllabus_retrieval_bundle["text"]:
                outgoing_message += f"\n\nRetrieved syllabus context:\n{syllabus_retrieval_bundle['text']}"
        include_learning_sources = should_retrieve_learning_sources(
            user_input,
            conversation_mode,
            student_state_route=student_state_route,
        )
        if include_learning_sources:
            learning_sources_context = build_learning_sources_context(
                profile,
                student_state_route=student_state_route,
                user_input=user_input,
            )
            if learning_sources_context:
                outgoing_message += f"\n\nTrusted learning-source context:\n{learning_sources_context}"
        if include_learning_sources:
            learning_retrieval_bundle = retrieve_learning_source_bundle(
                profile,
                user_input,
                max_sources=1 if conversation_mode == "tutor" else 2,
                student_state_route=student_state_route,
            )
            if learning_retrieval_bundle["text"]:
                outgoing_message += (
                    "\n\nRetrieved source material. Use it quietly to sharpen the answer, but do not mention source titles or the source library unless the student specifically asks about sources. "
                    "Integrate these insights into a clean teaching answer, and strictly obey the CRITICAL SOURCE POLICY below if one is present.\n"
                    f"{learning_retrieval_bundle['text']}"
                )
            else:
                outgoing_message += (
                    "\n\nNo external source snippet was retrieved for this question. "
                    "Do not mention that as a technical issue. Answer using your local JEE teaching knowledge, the syllabus, and the tutor brain rules so the student still gets a clear explanation."
                )
        if avatar:
            outgoing_message += (
                f"\n\nActive tutor avatar style: {avatar['name']}. "
                f"{avatar['style_prompt']}"
            )
        if conversation_mode == "tutor":
            outgoing_message += (
                "\n\nThis is the academic tutor tab. Keep the conversation focused on learning, explanations, study strategy, problem solving, "
                "visual understanding, and structured academic support. Avoid drifting into general current affairs, entertainment, or casual life chat "
                "unless it directly helps learning."
            )
            outgoing_message += f"\n\n{tutor_mode_hint}"
        if is_jee_track:
            outgoing_message += (
                "\n\nThis student is on a JEE track. Distinguish clearly between JEE Main preparation and JEE Advanced preparation. "
                "Treat JEE Main as the first scoring milestone that needs clean execution, speed, and dependable accuracy. "
                    "At the same time, keep a smaller continuous bridge to JEE Advanced through deeper reasoning, tougher extensions, and concept depth where useful. "
                    "Use Physics, Chemistry, and Mathematics framing, exam-relevant shortcuts only when conceptually justified, and clear distinction between intuition, formula, and question application."
                )
            outgoing_message += (
                "\n\nWhen teaching a concept, prefer real-life visualization, mini case studies, and scene-based explanations so the student can picture "
                "what is happening in 3D or in everyday life instead of memorizing mechanically."
            )
            outgoing_message += (
                "\n\nYour answer must be neat and easy to understand. Prefer clean paragraphs over messy bullet dumps. "
                "Use short headings only when truly helpful. Avoid markdown clutter. If a formula or equation matters, place it on its own line and then explain it in prose."
            )
            outgoing_message += (
                "\n\nIf the student has uploaded syllabus or portion documents, prioritize those topics and scope when answering. "
                "Keep the scope JEE-only and stay aligned with the student's Physics, Chemistry, and Mathematics plan."
            )
            outgoing_message += (
                "\n\nAdaptive teaching profile for this student: "
                f"question difficulty = {adaptive_profile['question_difficulty']}, "
                f"concept depth = {adaptive_profile['concept_depth']}, "
                f"teaching speed = {adaptive_profile['teaching_speed']}, "
                f"readiness band = {adaptive_profile['percentile_band']}. "
                "Increase challenge gradually over time without overwhelming the student."
            )
            level = max(1, min(int(tutor_level or 3), 5))
            if level == 1:
                outgoing_message += (
                    "\n\nTutor level is 1. Explain in simple layman terms, very clearly, with short sentences and minimal jargon. "
                    "Use 1 to 2 short paragraphs. Keep it crisp and reassuring."
                )
            elif level == 2:
                outgoing_message += (
                    "\n\nTutor level is 2. Keep the explanation simple and friendly, with only light technical detail. "
                    "Use 2 short readable paragraphs."
                )
            elif level == 3:
                outgoing_message += (
                    "\n\nTutor level is 3. Give a balanced explanation with clarity first and enough detail to build solid understanding. "
                    "Use 2 to 4 clean paragraphs."
                )
            elif level == 4:
                outgoing_message += (
                    "\n\nTutor level is 4. Give deeper detail, stronger reasoning, and more complete explanation steps. "
                    "Use 3 to 5 organized paragraphs, and include formulas only when useful."
                )
            else:
                outgoing_message += (
                    "\n\nTutor level is 5. Give a deep and detailed explanation for a highly curious learner, while staying structured and readable. "
                    "Use 4 to 6 well-organized paragraphs with strong conceptual clarity."
                )
        elif conversation_mode == "practice":
            outgoing_message += (
                "\n\nThis is the practice tab. Focus only on questions, drills, timed practice, previous-year-question style sets, "
                "and full-paper style exam practice. Avoid turning this into a teaching conversation unless the user explicitly asks for solutions."
            )
            if is_jee_track:
                outgoing_message += (
                    "\n\nFor JEE practice, distinguish clearly between JEE Main and JEE Advanced. "
                    "JEE Main sets should emphasize cleaner scoring, speed, direct application, and familiar exam pressure. "
                    "JEE Advanced sets should emphasize deeper reasoning, multi-concept linkage, and tougher conceptual traps."
                )
            outgoing_message += (
                "\n\nPrefer exam-style structure. When useful, mention suggested time limits, section labels, answer format, and whether the set is quick practice, "
                "time-bound, PYQ-style, or mini-paper style."
            )
            outgoing_message += (
                "\n\nGround the question style in public exam patterns and the active exam profile. Do not claim a question is a real copyrighted previous-year paper "
                "unless it truly is; instead say 'PYQ-style' or 'public-pattern style' when generating new material."
            )
            outgoing_message += (
                "\n\nAdaptive practice profile for this student: "
                f"question difficulty = {adaptive_profile['question_difficulty']}, "
                f"concept depth = {adaptive_profile['concept_depth']}, "
                f"teaching speed = {adaptive_profile['teaching_speed']}. "
                "Increase challenge gradually over time."
            )
            outgoing_message += (
                "\n\nFormat every practice response in a clean exam sheet style, never as one long paragraph. "
                "Use short sections like: Title, Time Limit, Instructions, Questions, and if needed Answer Format. "
                "Put each question on its own numbered line. Keep spacing clean and readable."
            )
        elif conversation_mode == "last_minute":
            outgoing_message += (
                "\n\nThis is the Last Minute tab. Focus on one-night-before, one-day-before, and last-minute revision rescue."
            )
            outgoing_message += (
                "\n\nThe goal is not perfect completeness. The goal is practical coverage, fast revision, high-yield retention, "
                "exam survival strategy, and confidence under time pressure."
            )
            outgoing_message += (
                "\n\nFormat the answer clearly with short sections such as: Portion Coverage Map, Priority Order, Fast Revision Plan, What To Memorize, "
                "What To Skip If Short On Time, Final Recall Checklist, and Exam-Day Warnings."
            )
            outgoing_message += (
                "\n\nStay tightly aligned to JEE Main and JEE Advanced final revision."
            )
            outgoing_message += (
                "\n\nNever make the answer look like a long essay. Make it scannable and urgent but calming."
            )
            outgoing_message += (
                "\n\nDo not claim full coverage unless the specified subjects and portion are actually available. "
                "If details are missing, state that clearly and show the best possible partial rescue plan."
            )
            outgoing_message += (
                "\n\nWhen details are available, make sure the answer covers the entire stated portion subject by subject so the student can track what has been revised and what is still left."
            )
            outgoing_message += "\n\n" + build_last_minute_revision_context(profile, user_input)
        elif conversation_mode == "tips":
            outgoing_message += (
                "\n\nThis is the tips and tricks tab. Focus on time management, smart question selection, exam strategy, paper navigation, "
                "elimination techniques, revision tricks, and how to apply public exam advice in practice."
            )
            outgoing_message += (
                "\n\nDo not just list generic tips. Explain how the student should use the tip inside the exam, when it helps, and where it can go wrong."
            )
            tips_context = build_tips_context(profile)
            if tips_context:
                outgoing_message += f"\n\n{tips_context}"
        elif conversation_mode == "guide":
            outgoing_message += (
                "\n\nThis is the app guide tab. Answer only product-usage questions about where features live, what each tab is for, how to use them efficiently, "
                "and what the simplest path is for a student. Do not roleplay as the academic tutor here."
            )
        else:
            outgoing_message += (
                "\n\nThis is the lounge tab. Focus on casual talk, general knowledge, current affairs, sports, entertainment, hobbies, daily life reflection, emotional support, and light conversation. "
                "If the student wants to talk about football, a match, a movie, a show, a game, or any other fun topic, engage naturally instead of redirecting them."
            )
            outgoing_message += (
                "\n\nThe tutor should feel warm and human rather than robotic. "
                "It can discuss general knowledge, life perspective, and supportive reflection when useful."
            )
            outgoing_message += (
                "\n\nWhen the student seems emotionally heavy, listen first, reflect gently, and only then offer perspective or a soft next step. "
                "The goal in Lounge is trust, relief, and emotional safety."
            )
        if voice_chat_mode:
            outgoing_message += (
                "\n\nVoice chat mode is on. Reply in a short, natural, conversational way. "
                "Keep the response easy to speak aloud, ideally within 3 to 5 short sentences "
                "unless the user explicitly asks for more detail."
            )
        pacing_label = str(response_pacing or "standard").strip().lower()
        if reading_comfort_mode or chunked_reply_mode or pacing_label != "standard":
            outgoing_message += (
                "\n\nReading comfort mode is on. Keep sentences short, break ideas into smaller chunks, and make the flow easy to scan."
            )
            if chunked_reply_mode:
                outgoing_message += (
                    "\n\nBreak longer explanations into small labeled chunks or numbered steps so the student can follow one idea at a time."
                )
            if pacing_label == "slow":
                outgoing_message += (
                    "\n\nUse a slow, calm pacing with gentle transitions and clear pauses between steps."
                )
            elif pacing_label == "gentle":
                outgoing_message += (
                    "\n\nUse a gentle pacing with a calm rhythm and avoid rushing the explanation."
                )
        if response_language and response_language.lower() != "english":
            outgoing_message += (
                f"\n\nReply in {response_language} unless the user explicitly asks you to switch languages."
            )
        if should_fetch_live_context(user_input):
            live_context_bundle = build_live_context_bundle(user_input)
            if live_context_bundle["text"]:
                outgoing_message += (
                    "\n\nUse this live context when answering current or real-world questions. "
                    "If the live context is incomplete, be honest about uncertainty instead of pretending.\n"
                    f"{live_context_bundle['text']}"
                )

    content = Content(role="user", parts=[{"text": outgoing_message}])
    run_config = RunConfig(streaming_mode=StreamingMode.NONE)
    response_text = ""
    response_source = "model"

    try:
        for event in runner.run(
            user_id=USER_ID,
            session_id=session_id,
            new_message=content,
            run_config=run_config,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                response_text = "".join(part.text or "" for part in event.content.parts).strip()
    except Exception as exc:
        logging.warning("Tutor model call fell back to local response: %s", exc)
        response_text = ""
        response_source = "fallback"

    sanitized_response = response_text.strip().lower()
    apology_markers = (
        "technical issue",
        "trusted learning resources",
        "unable to retrieve information from sources",
        "i am very sorry",
        "i'm very sorry",
        "could not access",
        "cannot access",
        "preventing me from explaining",
    )
    if not response_text.strip() or any(marker in sanitized_response for marker in apology_markers):
        response_text = _build_mode_aware_fallback_reply(
            user_input,
            conversation_mode,
            tutor_level,
            tutor_brain,
            student_insight_snapshot,
            reading_comfort_mode,
            chunked_reply_mode,
            response_pacing,
        )
        response_source = "fallback"

    return {
        "reply": response_text or "I could not generate a response just now.",
        "live_sources": live_context_bundle["sources"]
        + syllabus_retrieval_bundle["sources"]
        + learning_retrieval_bundle["sources"],
        "visual_learning": build_visual_learning_aid(user_input)
        if conversation_mode == "tutor"
        else None,
        "video_explanation": build_video_explanation(user_input, response_language)
        if conversation_mode == "tutor"
        else None,
        "adaptive_profile": adaptive_profile if conversation_mode in {"tutor", "practice"} else None,
        "reply_source": response_source,
    }


def _run_image_tutor_reply(profile, user_input, image_base64, mime_type, response_language="English"):
    if not genai_client:
        return {
            "reply": "Image analysis is not available right now because the model client is not configured.",
            "visual_learning": None,
            "video_explanation": None,
            "adaptive_profile": get_adaptive_learning_profile(profile),
        }

    prompt = user_input.strip() or "Analyze this study doubt image carefully and explain the concept, method, and likely mistake."
    adaptive_profile = get_adaptive_learning_profile(profile)
    prompt += (
        "\n\nThis is an academic tutor image-analysis request. Explain the doubt clearly, identify the likely topic, "
        "walk through the logic step by step, and point out any common trap or mistake visible in the working."
    )
    prompt += (
        f"\n\nAdaptive teaching profile: question difficulty = {adaptive_profile['question_difficulty']}, "
        f"concept depth = {adaptive_profile['concept_depth']}, teaching speed = {adaptive_profile['teaching_speed']}."
    )
    if response_language and response_language.lower() != "english":
        prompt += f"\n\nReply in {response_language}."

    image_bytes = base64.b64decode(image_base64)
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                genai.types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            ],
        )
        reply = (response.text or "").strip() or "I could not read that image clearly. Please try a sharper photo."
    except Exception as exc:
        logging.warning("Image tutor call fell back to local response: %s", exc)
        reply = _build_mode_aware_fallback_reply(
            prompt,
            "tutor",
            int(profile.get("default_tutor_level", 3) or 3),
            _build_tutor_brain_snapshot(
                profile,
                _get_avatar_preset(profile),
                get_student_insight_snapshot(profile),
                "tutor",
                int(profile.get("default_tutor_level", 3) or 3),
                False,
            ),
            get_student_insight_snapshot(profile),
        )
    return {
        "reply": reply,
        "visual_learning": build_visual_learning_aid(prompt),
        "video_explanation": build_video_explanation(prompt, response_language),
        "adaptive_profile": adaptive_profile,
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "environment": settings.app_env,
        "database_path": settings.database_path,
        "storage": get_storage_status(),
    }


@app.get("/api/readiness")
def readiness():
    return {
        "database": "ready",
        "storage": get_storage_status(),
        "environment": settings.app_env,
        "host": settings.host,
        "port": settings.port,
    }


@app.get("/api/video-library")
def video_library(student_name: str = ""):
    return get_video_library_snapshot(student_name.strip() or None)


@app.post("/api/auth/register")
def auth_register(request: AuthRegisterRequest):
    email = request.email.strip().lower()
    display_name = request.display_name.strip()
    student_name = (request.student_name or request.display_name).strip()

    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="A valid email is required.")
    if len(request.password or "") < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters.")
    if not display_name:
        raise HTTPException(status_code=400, detail="Display name is required.")
    if not student_name:
        raise HTTPException(status_code=400, detail="Student name is required.")
    if get_user_by_email(email):
        raise HTTPException(status_code=409, detail="An account with that email already exists.")
    if get_user_by_student_name(student_name):
        raise HTTPException(status_code=409, detail="That student profile name is already linked to another account.")

    profile = load_profile(student_name)
    if not profile:
        onboarding_profile = _build_onboarding_profile_from_request(
            why_astra=request.onboarding_why_astra,
            interests=request.onboarding_interests,
            dislikes=request.onboarding_dislikes,
            conversation_style=request.onboarding_conversation_style,
            preferred_language=request.onboarding_preferred_language,
            explanation_depth=request.onboarding_explanation_depth,
            stress_support=request.onboarding_stress_support,
            goals_summary=request.onboarding_goals_summary,
            astra_question=request.onboarding_astra_question,
            astra_question_answer=request.onboarding_astra_question_answer,
            intro_completed=any(
                value.strip()
                for value in [
                    request.onboarding_why_astra,
                    request.onboarding_interests,
                    request.onboarding_dislikes,
                    request.onboarding_conversation_style,
                    request.onboarding_preferred_language,
                    request.onboarding_explanation_depth,
                    request.onboarding_stress_support,
                    request.onboarding_goals_summary,
                    request.onboarding_astra_question,
                    request.onboarding_astra_question_answer,
                ]
            ),
        )
        profile = create_profile(
            name=student_name,
            exam=JEE_MVP_PRIMARY_EXAM["name"],
            exam_date=JEE_MVP_PRIMARY_EXAM["exam_date"],
            study_hours_per_day=request.max_study_hours_per_day,
            subjects=list(JEE_MVP_PRIMARY_EXAM["subjects"]),
            exams=[dict(JEE_MVP_PRIMARY_EXAM)],
            max_study_hours_per_day=request.max_study_hours_per_day,
            onboarding_profile=onboarding_profile,
        )
        _apply_onboarding_profile(profile, onboarding_profile)

    user = create_auth_user(
        email=email,
        password=request.password,
        display_name=display_name,
        student_name=student_name,
    )
    session = issue_session(user["id"])
    return {
        "user": user,
        "session": session,
        "profile": profile,
    }


@app.post("/api/auth/login")
def auth_login(request: AuthLoginRequest):
    user = authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    session = issue_session(user["id"])
    profile = load_profile(user["student_name"])
    return {
        "user": user,
        "session": session,
        "profile": profile,
    }


@app.get("/api/auth/me")
def auth_me(authorization: str | None = Header(default=None)):
    user = require_bearer_token(authorization)
    profile = load_profile(user["student_name"])
    return {
        "user": user,
        "profile": profile,
    }


@app.get("/api/profile/{student_name}")
def get_profile(student_name: str):
    profile = _ensure_jee_mvp_profile_scope(_load_profile_or_404(student_name))
    if not profile.get("avatar_visuals"):
        profile["avatar_visuals"] = _appearance_visuals_from_description(
            profile.get("appearance_description", ""),
            _get_avatar_preset(profile),
        )
        save_profile(profile)
    avatar = _get_avatar_preset(profile)
    insight = get_student_insight_snapshot(profile)
    return {
        "profile": profile,
        "active_avatar": avatar,
        "tutor_brain": _build_tutor_brain_snapshot(
            profile,
            avatar,
            insight,
            "tutor",
            int(profile.get("default_tutor_level", 3) or 3),
            False,
        ),
        "fun_fact": get_daily_fun_fact(profile["name"]),
        "personal_memory": load_personal_memory(profile["name"]),
        "syllabus_documents": get_syllabus_documents(profile["name"]),
    }


@app.post("/api/profile/onboarding")
def update_onboarding_profile(request: OnboardingUpdateRequest):
    profile = _load_profile_or_404(request.student_name)
    onboarding_profile = _build_onboarding_profile_from_request(
        why_astra=request.onboarding_why_astra,
        interests=request.onboarding_interests,
        dislikes=request.onboarding_dislikes,
        conversation_style=request.onboarding_conversation_style,
        preferred_language=request.onboarding_preferred_language,
        explanation_depth=request.onboarding_explanation_depth,
        stress_support=request.onboarding_stress_support,
        goals_summary=request.onboarding_goals_summary,
        astra_question=request.onboarding_astra_question,
        astra_question_answer=request.onboarding_astra_question_answer,
        intro_completed=request.intro_completed,
    )
    profile = _apply_onboarding_profile(profile, onboarding_profile)
    return {"profile": profile}


@app.get("/api/avatar-presets")
def avatar_presets():
    return {"avatars": AVATAR_PRESETS}


@app.get("/api/exam-catalog")
def exam_catalog():
    return {"exams": EXAM_CATALOG}


@app.post("/api/signup")
def signup(request: SignupRequest):
    clean_name = request.name.strip()
    if not clean_name:
        raise HTTPException(status_code=400, detail="Name is required.")
    if load_profile(clean_name):
        raise HTTPException(status_code=409, detail="A profile with that name already exists.")

    exams = _clean_exam_entries(request.exams)
    if not exams and request.exam.strip() and request.exam_date.strip():
        exams = _clean_exam_entries(
            [
                {
                    "name": request.exam.strip(),
                    "exam_date": request.exam_date.strip(),
                    "subjects": request.subjects,
                }
            ]
        )
    primary_exam = exams[0] if exams else dict(JEE_MVP_PRIMARY_EXAM)

    onboarding_profile = _build_onboarding_profile_from_request(
        why_astra=request.onboarding_why_astra,
        interests=request.onboarding_interests,
        dislikes=request.onboarding_dislikes,
        conversation_style=request.onboarding_conversation_style,
        preferred_language=request.onboarding_preferred_language,
        explanation_depth=request.onboarding_explanation_depth,
        stress_support=request.onboarding_stress_support,
        goals_summary=request.onboarding_goals_summary,
        astra_question=request.onboarding_astra_question,
        astra_question_answer=request.onboarding_astra_question_answer,
        intro_completed=any(
            value.strip()
            for value in [
                request.onboarding_why_astra,
                request.onboarding_interests,
                request.onboarding_dislikes,
                request.onboarding_conversation_style,
                request.onboarding_preferred_language,
                request.onboarding_explanation_depth,
                request.onboarding_stress_support,
                request.onboarding_goals_summary,
                request.onboarding_astra_question,
                request.onboarding_astra_question_answer,
            ]
        ),
    )

    profile = create_profile(
        name=clean_name,
        exam=primary_exam["name"],
        exam_date=primary_exam["exam_date"],
        study_hours_per_day=request.max_study_hours_per_day,
        subjects=primary_exam["subjects"],
        exams=exams or [dict(JEE_MVP_PRIMARY_EXAM)],
        max_study_hours_per_day=request.max_study_hours_per_day,
        onboarding_profile=onboarding_profile,
    )
    _apply_onboarding_profile(profile, onboarding_profile)
    return {"profile": profile}


@app.post("/api/profile/exams")
def update_profile_exams(request: ExamUpdateRequest):
    profile = _load_profile_or_404(request.student_name)
    profile["exams"] = request.exams
    profile = _sync_profile_exam_fields(profile)
    save_profile(profile)
    return {"profile": profile}


@app.post("/api/avatar/select")
def select_avatar(request: AvatarSelectionRequest):
    profile = _load_profile_or_404(request.student_name)
    preset = next((avatar for avatar in AVATAR_PRESETS if avatar["id"] == request.avatar_id), None)
    if not preset:
        raise HTTPException(status_code=404, detail="Avatar preset not found.")

    profile["selected_avatar"] = preset["id"]
    profile["preferred_persona"] = preset["name"]
    save_profile(profile)
    return {
        "profile": profile,
        "avatar": preset,
        "tutor_brain": _build_tutor_brain_snapshot(
            profile,
            preset,
            get_student_insight_snapshot(profile),
            "tutor",
            int(profile.get("default_tutor_level", 3) or 3),
            False,
        ),
    }


@app.post("/api/tutor/customize")
def customize_tutor(request: TutorCustomizationRequest):
    profile = _load_profile_or_404(request.student_name)
    tutor_name = request.tutor_name.strip() or profile.get("tutor_name", "Astra")
    personality_preset = request.tutor_personality_preset.strip() or profile.get(
        "tutor_personality_preset", "balanced"
    )
    personality_traits = [trait.strip() for trait in request.tutor_personality_traits if trait.strip()]
    personality_notes = request.tutor_personality_notes.strip() or profile.get("tutor_personality_notes", "")
    appearance_description = request.appearance_description.strip() or profile.get(
        "appearance_description", "friendly, fun, and human-like"
    )
    tutor_style = request.tutor_style.strip() or build_personality_summary(
        personality_preset,
        personality_traits,
        personality_notes,
    )
    profile["tutor_name"] = tutor_name[:40]
    profile["tutor_personality_preset"] = personality_preset[:40]
    profile["tutor_personality_traits"] = personality_traits[:20]
    profile["tutor_personality_notes"] = personality_notes[:240]
    profile["tutor_style"] = tutor_style[:220]
    profile["appearance_description"] = appearance_description[:220]
    profile["avatar_visuals"] = _appearance_visuals_from_description(
        profile["appearance_description"],
        _get_avatar_preset(profile),
    )
    save_profile(profile)
    return {"profile": profile}


@app.post("/api/memory/add")
def add_memory(request: MemoryUpdateRequest):
    _load_profile_or_404(request.student_name)
    memory = add_memory_item(request.student_name, request.category, request.value)
    return {
        "personal_memory": memory,
        "fun_fact": get_daily_fun_fact(request.student_name),
    }


@app.post("/api/memory/remove")
def remove_memory(request: MemoryUpdateRequest):
    _load_profile_or_404(request.student_name)
    memory = remove_memory_item(request.student_name, request.category, request.value)
    return {
        "personal_memory": memory,
        "fun_fact": get_daily_fun_fact(request.student_name),
    }


@app.get("/api/weekly-plan/{student_name}")
def weekly_plan(student_name: str):
    profile = _load_profile_or_404(student_name)
    plan = get_weekly_schedule_data(profile)
    if "message" in plan:
        return plan

    exam_names = [str(exam.get("name", "")).strip().upper() for exam in profile.get("exams", [])]
    retrieval_query = (
        "JEE Main and JEE Advanced preparation strategy with mains-first planning, parallel advanced touch, "
        "Physics Chemistry Mathematics balance, mock analysis, formula revision, error log review, and topper-style preparation rhythm"
    )
    insight_snapshot = get_student_insight_snapshot(profile)
    route = build_student_state_route(
        profile,
        conversation_mode="tutor",
        tutor_level=profile.get("default_tutor_level", 3) or 3,
        support_style=insight_snapshot.get("support_style"),
        insight_snapshot=insight_snapshot,
    )
    source_bundle = retrieve_learning_source_bundle(
        profile,
        retrieval_query,
        max_sources=2,
        student_state_route=route,
    )
    plan["strategy_sources"] = source_bundle.get("sources", [])
    return plan


def _build_session_opening_message(profile, todays_focus):
    morning = todays_focus.get("primary") or todays_focus.get("morning") or {}
    session_type = str(morning.get("session_type") or "learn").strip().lower()
    student_name = profile.get("name", "Student")
    topic = str(morning.get("topic") or "this topic").strip()
    unit = str(morning.get("unit") or morning.get("unit_name") or "today's unit").strip()
    weightage = morning.get("weightage_percent", morning.get("jee_weightage_percent", 0))
    confidence = str(todays_focus.get("confidence_level") or morning.get("confidence_level") or "new").strip().lower()
    if session_type == "practice":
        return (
            f"{student_name}, you understand {topic} well. Today we test that understanding with actual JEE questions. "
            "This builds the exam speed you need. No explanation first - let us see what you know."
        )
    if session_type == "revise":
        return (
            f"{student_name}, we are revisiting {topic} today from {unit}. Last time the confidence level was {confidence}. "
            "This session will be shorter and more targeted, and I will use a different angle to make the weak part click."
        )
    return (
        f"{student_name}, today we start {topic} from {unit}. This topic carries {weightage}% weightage in JEE Main. "
        "By the end of today you will be able to solve any standard JEE question on this. I have pulled up the exact content you need. "
        "Let us begin."
    )


def _find_chapter_unit(subject, unit_name):
    syllabus = build_chapter_ready_syllabus()
    for unit in syllabus.get(str(subject or "").strip().lower(), []):
        if str(unit.get("name") or "").strip().lower() == str(unit_name or "").strip().lower():
            return unit
    return None


def _find_chapter_unit_with_subject(unit_name):
    syllabus = build_chapter_ready_syllabus()
    for subject, units in syllabus.items():
        for unit in units:
            if str(unit.get("name") or "").strip().lower() == str(unit_name or "").strip().lower():
                return subject, unit
    return "", None


def _chapter_test_fallback_questions(unit_name, chapter_unit, subject, kb_bundle=None):
    subtopics = list((chapter_unit or {}).get("subtopics") or [])
    questions = []
    pyq_chunks = []
    if isinstance(kb_bundle, dict):
        pyq_chunks = list(kb_bundle.get("chunks") or [])
    for index in range(15):
        subtopic = subtopics[index % len(subtopics)] if subtopics else {}
        concepts = list(subtopic.get("concepts") or [])
        concept_text = concepts[0] if concepts else f"Core idea of {unit_name}"
        topic_name = subtopic.get("name") or unit_name or "Chapter"
        prompt_context = pyq_chunks[index % len(pyq_chunks)] if pyq_chunks else ""
        correct_letter = ["A", "B", "C", "D"][index % 4]
        distractors = [
            f"Common mistake 1 for {topic_name}",
            f"Common mistake 2 for {topic_name}",
            f"Common mistake 3 for {topic_name}",
            f"Common mistake 4 for {topic_name}",
        ]
        options = list(distractors)
        options[index % 4] = f"Correct application of {concept_text}"
        questions.append(
            {
                "number": index + 1,
                "question": (
                    f"JEE-style question {index + 1} on {topic_name}: which option best applies {concept_text}?"
                    + (f" Use this reference: {prompt_context[:160]}" if prompt_context else "")
                ),
                "options": options[:4],
                "correct": correct_letter,
                "subtopic": topic_name,
                "difficulty": "easy" if index < 5 else "medium" if index < 11 else "hard",
                "solution": f"Use {concept_text} directly and eliminate the options that contradict the main rule.",
            }
        )
    return questions


def _build_planner_setup_response(request: PlannerSetupRequest, background_tasks: BackgroundTasks | None = None):
    profile = _load_profile_or_404(request.student_id)
    profile["exam_date"] = request.exam_date
    profile["max_study_hours_per_day"] = max(2, min(10, int(request.hours_per_day or 6)))
    save_profile(profile)
    summary = generate_journey_plan(profile["name"], request.exam_date, request.hours_per_day)
    weekly = generate_this_weeks_plan(profile["name"])
    if background_tasks is not None:
        print("Pre-generating video briefs for week 1 topics...")
        background_tasks.add_task(pre_generate_video_briefs, profile["name"], 7)
    todays_focus = get_todays_focus(profile["name"])
    return {
        "student_id": profile["name"],
        "plan_summary": summary,
        "weekly_plan": weekly,
        "todays_focus": todays_focus,
        "opening_message": _build_session_opening_message(profile, todays_focus),
        "message": "Your JEE journey is ready.",
    }


@app.post("/api/planner/setup")
def planner_setup(request: PlannerSetupRequest, background_tasks: BackgroundTasks):
    return _build_planner_setup_response(request, background_tasks)


@app.post("/api/planner/generate-journey")
def planner_generate_journey(request: PlannerSetupRequest, background_tasks: BackgroundTasks):
    return _build_planner_setup_response(request, background_tasks)


@app.post("/api/video/pre-plan")
def video_pre_plan(request: VideoPrePlanRequest):
    try:
        briefs = pre_generate_video_briefs(request.student_id, request.days_ahead)
        return {
            "student_id": request.student_id,
            "days_ahead": request.days_ahead,
            "briefs": briefs,
        }
    except Exception as exc:
        logging.exception("Video pre-plan generation failed: %s", exc)
        raise HTTPException(status_code=500, detail="Could not pre-generate video briefs right now.") from exc


@app.get("/api/video/pre-plan/status/{student_id}")
def video_pre_plan_status(student_id: str):
    try:
        return {
            "student_id": student_id,
            "items": load_video_preplan_status(student_id),
        }
    except Exception as exc:
        logging.exception("Video pre-plan status failed: %s", exc)
        raise HTTPException(status_code=500, detail="Could not load video pre-plan status right now.") from exc


@app.get("/api/video/brief/{student_id}/{topic_slug}")
def video_brief_for_topic(student_id: str, topic_slug: str, subject: str = ""):
    try:
        topic = str(topic_slug or "").replace("_", " ")
        brief = get_video_brief_for_topic(student_id, topic, subject)
        return {
            "student_id": student_id,
            "topic_slug": topic_slug,
            "brief": brief,
        }
    except Exception as exc:
        logging.exception("Video brief lookup failed: %s", exc)
        raise HTTPException(status_code=500, detail="Could not load that video brief right now.") from exc


@app.get("/api/video/requests/{student_id}")
def video_requested_list(student_id: str):
    try:
        return {
            "student_id": student_id,
            "requests": load_requested_videos(student_id),
        }
    except Exception as exc:
        logging.exception("Requested video list failed: %s", exc)
        raise HTTPException(status_code=500, detail="Could not load requested videos right now.") from exc


@app.post("/api/video/request")
def video_request_save(request: VideoRequestSaveRequest):
    try:
        record = save_requested_video(
            request.student_id,
            request.topic,
            request.subject,
            source=request.source,
            status=request.status,
            job_id=request.job_id,
            video_url=request.video_url,
        )
        return {
            "student_id": request.student_id,
            "request": record,
            "requests": load_requested_videos(request.student_id),
        }
    except Exception as exc:
        logging.exception("Could not save requested video: %s", exc)
        raise HTTPException(status_code=500, detail="Could not save the requested video right now.") from exc


@app.post("/api/video/request/status")
def video_request_update_status(request: VideoRequestSaveRequest):
    try:
        record = update_requested_video_status(
            request.student_id,
            request.topic or request.topic_slug,
            request.status,
            job_id=request.job_id,
            video_url=request.video_url,
        )
        return {
            "student_id": request.student_id,
            "request": record,
            "requests": load_requested_videos(request.student_id),
        }
    except Exception as exc:
        logging.exception("Could not update requested video status: %s", exc)
        raise HTTPException(status_code=500, detail="Could not update the requested video right now.") from exc


@app.get("/api/planner/today/{student_id}")
def planner_today(student_id: str):
    profile = _load_profile_or_404(student_id)
    todays_focus = get_todays_focus(profile["name"])
    morning = todays_focus.get("primary") or {}
    kb_query = f"{morning.get('topic', '')} {morning.get('unit', '')} {morning.get('subject', '')}".strip()
    kb_bundle = search_knowledge_base(kb_query, morning.get("subject", ""), n_results=5, session_type=morning.get("session_type", "learn"))
    if isinstance(kb_bundle, dict):
        retrieved = kb_bundle
    else:
        retrieved = {"chunks": kb_bundle, "has_pyqs": any(item.get("type") == "pyq" for item in kb_bundle), "sources": [], "context_prompt": ""}
    return {
        "student_id": profile["name"],
        "focus": todays_focus,
        "retrieved_content": retrieved,
        "opening_message": _build_session_opening_message(profile, todays_focus),
        "student_state": get_student_mastery_map(profile["name"]),
        "revision_due": get_revision_due_today(profile["name"]),
    }


@app.get("/api/planner/weekly/{student_id}")
def planner_weekly(student_id: str):
    profile = _load_profile_or_404(student_id)
    weekly = _load_json_safe(_journey_path(profile["name"], "weekly"), {})
    if not weekly:
        weekly = generate_this_weeks_plan(profile["name"])
    return weekly


@app.get("/api/planner/journey/{student_id}")
def planner_journey(student_id: str):
    profile = _load_profile_or_404(student_id)
    journey = _load_json_safe(_journey_path(profile["name"], "journey"), {})
    if not journey:
        journey = generate_journey_plan(profile["name"], profile.get("exam_date", ""), profile.get("max_study_hours_per_day", 6))
    return journey


@app.get("/api/planner/mastery/{student_id}")
def planner_mastery(student_id: str):
    profile = _load_profile_or_404(student_id)
    return {"student_id": profile["name"], "mastery_map": get_student_mastery_map(profile["name"])}


@app.get("/api/planner/revision-due/{student_id}")
def planner_revision_due(student_id: str):
    profile = _load_profile_or_404(student_id)
    return {"student_id": profile["name"], "revision_due": get_revision_due_today(profile["name"])}


@app.post("/api/planner/rebalance/{student_id}")
def planner_rebalance(student_id: str):
    profile = _load_profile_or_404(student_id)
    hours = profile.get("max_study_hours_per_day", profile.get("study_hours_per_day", 6) or 6)
    journey = _load_json_safe(_journey_path(profile["name"], "journey"), {})
    exam_date = journey.get("exam_date") or profile.get("exam_date") or ""
    summary = generate_journey_plan(profile["name"], exam_date, hours)
    weekly = generate_this_weeks_plan(profile["name"])
    return {
        "student_id": profile["name"],
        "message": "Journey rebalanced.",
        "plan_summary": summary,
        "weekly_plan": weekly,
        "todays_focus": get_todays_focus(profile["name"]),
    }


@app.get("/api/tutor/todays-session/{student_id}")
def tutor_todays_session(student_id: str):
    profile = _load_profile_or_404(student_id)
    focus = get_todays_focus(profile["name"])
    opening_message = _build_session_opening_message(profile, focus)
    morning = focus.get("primary") or {}
    kb_bundle = search_knowledge_base(
        f"{morning.get('topic', '')} {morning.get('unit', '')} {morning.get('subject', '')}",
        morning.get("subject", ""),
        n_results=5,
        session_type=morning.get("session_type", "learn"),
    )
    if not isinstance(kb_bundle, dict):
        kb_bundle = {"chunks": kb_bundle, "has_pyqs": False, "sources": [], "context_prompt": ""}
    return {
        "student_id": profile["name"],
        "opening_message": opening_message,
        "todays_focus": focus,
        "retrieved_content": kb_bundle,
        "student_state": get_student_mastery_map(profile["name"]),
        "revision_due": get_revision_due_today(profile["name"]),
    }


@app.post("/api/tutor/complete-session")
def tutor_complete_session(request: TutorCompleteSessionRequest):
    profile = _load_profile_or_404(request.student_id)
    result = record_topic_outcome(
        profile["name"],
        request.topic,
        request.subject,
        request.unit_name,
        request.checkpoint_score,
        request.duration_minutes,
        request.session_type,
    )
    return {
        "student_id": profile["name"],
        "updated_confidence": result.get("confidence_level", "new"),
        "next_topic_preview": get_todays_focus(profile["name"]).get("primary", {}),
        "weekly_plan_updated": result.get("weekly_plan_updated", False),
        "encouragement_message": "Nice work. Keep the revision loop active and come back for the next scheduled session.",
        "result": result,
    }


@app.post("/api/session/start-chapter")
def session_start_chapter(request: ChapterStartRequest):
    profile = _load_profile_or_404(request.student_id)
    session = start_chapter_session(profile["name"], request.unit_name, request.subject)
    current = get_current_subtopic(profile["name"])
    return {
        "session": session,
        "first_subtopic": current,
    }


@app.get("/api/session/current-subtopic/{student_id}")
def session_current_subtopic(student_id: str):
    profile = _load_profile_or_404(student_id)
    return {
        "student_id": profile["name"],
        "current_subtopic": get_current_subtopic(profile["name"]),
    }


@app.get("/api/session/resume-summary/{student_id}")
def session_resume_summary(student_id: str):
    profile = _load_profile_or_404(student_id)
    session = get_active_chapter_session(profile["name"])
    unit_name = str(session.get("unit_name") or "").strip()
    return get_resume_summary(profile["name"], unit_name)


@app.post("/api/session/complete-subtopic")
def session_complete_subtopic(request: ChapterSubtopicCompleteRequest):
    profile = _load_profile_or_404(request.student_id)
    chapter_result = complete_subtopic(
        profile["name"],
        request.subtopic_id,
        request.checkpoint_score,
        request.time_spent_minutes,
    )
    session_state = chapter_result.get("session", {}) or {}
    record_subtopic_score(
        profile["name"],
        session_state.get("unit_name", ""),
        request.subtopic_id,
        request.checkpoint_score,
        request.time_spent_minutes,
        subject=session_state.get("subject", ""),
        session_type="chapter",
    )
    log_checkpoint(
        profile["name"],
        session_state.get("unit_name", ""),
        session_state.get("subject", ""),
        request.subtopic_id,
        request.checkpoint_score,
        request.time_spent_minutes,
        chapter_name=session_state.get("unit_name", ""),
    )
    return chapter_result


@app.post("/api/session/reset-chapter")
def session_reset_chapter(request: ChapterStartRequest):
    profile = _load_profile_or_404(request.student_id)
    return reset_chapter_session(profile["name"], request.unit_name, request.subject)


@app.get("/api/session/generate-chapter-test/{student_id}/{unit_name}")
def session_generate_chapter_test(student_id: str, unit_name: str):
    profile = _load_profile_or_404(student_id)
    session = get_active_chapter_session(profile["name"])
    session_unit = str(session.get("unit_name") or unit_name or "").strip()
    if not session_unit:
        raise HTTPException(status_code=400, detail="No active chapter session was found for this chapter.")
    subject = str(session.get("subject") or _find_chapter_unit_with_subject(session_unit)[0] or "").strip()
    chapter_unit = _find_chapter_unit(subject, session_unit) or _find_chapter_unit_with_subject(session_unit)[1] or {}
    subtopics = list(chapter_unit.get("subtopics") or [])
    kb_bundle = search_knowledge_base(session_unit, subject, n_results=5, session_type="practice")
    prompt = build_chapter_test_prompt(session_unit, subtopics, difficulty="jee_main")

    generated_questions = []
    if genai_client:
        try:
            kb_context = kb_bundle.get("context_prompt", "") if isinstance(kb_bundle, dict) else ""
            response = genai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=(
                    f"{prompt}\n\n"
                    f"Use this relevant JEE source material and PYQs:\n{kb_context}\n\n"
                    "Return ONLY valid JSON with keys: questions, unit_name, duration_minutes, marking_scheme. "
                    "Each question object must include number, question, options, correct, subtopic, difficulty, and solution."
                ),
            )
            raw_text = str(getattr(response, "text", "") or "").strip()
            candidate = _extract_json_payload(raw_text)
            parsed = json.loads(candidate) if candidate else {}
            if isinstance(parsed, dict) and isinstance(parsed.get("questions"), list):
                for index, item in enumerate(parsed["questions"][:15], start=1):
                    if not isinstance(item, dict):
                        continue
                    options = [str(option).strip() for option in item.get("options", []) if str(option).strip()][:4]
                    if len(options) < 4:
                        options = (options + ["A", "B", "C", "D"])[:4]
                    generated_questions.append(
                        {
                            "number": index,
                            "question": str(item.get("question") or f"Question {index}").strip(),
                            "options": options,
                            "correct": str(item.get("correct") or item.get("correct_answer") or "A").strip().upper()[:1] or "A",
                            "subtopic": str(item.get("subtopic") or session_unit).strip(),
                            "difficulty": str(item.get("difficulty") or "medium").strip(),
                            "solution": str(item.get("solution") or "").strip(),
                        }
                    )
        except Exception as exc:
            print(f"WARNING: Could not generate chapter test via model for {student_id}: {exc}")
            generated_questions = []

    if len(generated_questions) < 15:
        generated_questions = _chapter_test_fallback_questions(session_unit, chapter_unit, subject, kb_bundle)

    return {
        "unit_name": session_unit,
        "questions": generated_questions[:15],
        "duration_minutes": int(chapter_unit.get("chapter_test_duration_minutes") or 30),
        "marking": "+4 correct, -1 wrong",
        "chapter_test_questions": int(chapter_unit.get("chapter_test_questions") or 15),
        "subject": subject,
    }


@app.post("/api/session/submit-chapter-test")
def session_submit_chapter_test(request: ChapterTestSubmitRequest):
    profile = _load_profile_or_404(request.student_id)
    result = record_chapter_test(
        profile["name"],
        request.unit_name,
        request.subject,
        request.score,
        request.answers,
        request.time_taken_minutes,
    )
    return {
        "mastery_report": result,
        "next_steps": result.get("revision_scheduled", []),
    }


@app.get("/api/session/chapter-summary/{student_id}/{unit_name}")
def session_chapter_summary(student_id: str, unit_name: str):
    profile = _load_profile_or_404(student_id)
    return get_chapter_summary(profile["name"], unit_name)


@app.get("/api/session/chapter-summaries/{student_id}")
def session_chapter_summaries(student_id: str):
    profile = _load_profile_or_404(student_id)
    return get_all_chapter_summaries(profile["name"])


@app.get("/api/progress/chapter-mastery/{student_id}")
def progress_chapter_mastery(student_id: str):
    profile = _load_profile_or_404(student_id)
    return get_chapter_mastery_board(profile["name"])


@app.get("/api/progress/analytics/{student_id}")
def progress_analytics(student_id: str):
    profile = _load_profile_or_404(student_id)
    return get_chapter_score_summary(profile["name"])


@app.post("/api/session/extend-practice")
def session_extend_practice(request: ChapterPracticeRequest):
    profile = _load_profile_or_404(request.student_id)
    subject, chapter_unit = _find_chapter_unit_with_subject(request.unit_name)
    chapter_unit = chapter_unit or {}
    topic_anchor = request.unit_name
    if request.practice_type == "done":
        return {"student_id": profile["name"], "practice_type": request.practice_type, "questions": [], "message": "Move to the next topic in your journey."}
    if request.practice_type == "5_questions":
        pyq_bundle = search_knowledge_base(topic_anchor, subject, n_results=5, session_type="practice")
        chunks = pyq_bundle.get("chunks", []) if isinstance(pyq_bundle, dict) else pyq_bundle
        return {
            "student_id": profile["name"],
            "practice_type": request.practice_type,
            "questions": chunks[:5],
        }
    if request.practice_type == "full_mock":
        prompt = generate_chapter_test_prompt(request.unit_name, chapter_unit.get("subtopics", []), difficulty="jee_main")
        return {
            "student_id": profile["name"],
            "practice_type": request.practice_type,
            "questions": [
                {
                    "question": "Full mock generation is ready.",
                    "prompt": prompt,
                    "time_limit_minutes": 45,
                    "count": 25,
                }
            ],
        }
    return {"student_id": profile["name"], "practice_type": request.practice_type, "questions": []}


@app.get("/api/tips/{student_name}")
def tips_resources(student_name: str):
    profile = _load_profile_or_404(student_name)
    return {"resources": get_tips_resources(profile)}


@app.get("/api/learning-sources/{student_name}")
def learning_sources(student_name: str):
    profile = _load_profile_or_404(student_name)
    route = build_student_state_route(
        profile,
        conversation_mode="tutor",
        tutor_level=int(profile.get("default_tutor_level", 3) or 3),
        support_style=profile.get("tutor_style", ""),
        insight_snapshot=get_student_insight_snapshot(profile),
    )
    return {
        "resources": get_learning_sources(profile, student_state_route=route),
        "source_pack": get_learning_source_pack(profile, student_state_route=route),
        "student_state_route_text": format_student_state_route(route),
    }


@app.get("/api/motivation/daily")
def motivation_daily():
    return get_daily_motivation()


@app.get("/api/motivation/stories")
def motivation_stories():
    return {"stories": get_all_stories()}


@app.get("/api/motivation/stories/{index}")
def motivation_story(index: int):
    story = get_story_by_index(index)
    if story is None:
        raise HTTPException(status_code=404, detail="Motivation story not found.")
    return {"index": index, "story": story}


@app.post("/api/kb/add-url")
def kb_add_url(payload: KnowledgeBaseUrlRequest):
    result = fetch_and_add_web_source(
        payload.url,
        payload.subject,
        payload.source_name or Path(urlparse(payload.url).path).stem or "web_source",
    )
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("message", "Could not ingest the web source."))
    return {
        "message": result.get("message", "Web source ingested into the knowledge base."),
        "result": result,
        "stats": get_kb_stats(),
    }


@app.get("/api/kb/stats")
def kb_stats():
    return get_kb_stats()


@app.get("/api/kb/coverage")
def kb_coverage():
    return get_topic_coverage()


@app.post("/api/kb/add-document")
async def kb_add_document(
    subject: str = Form(...),
    file: UploadFile = File(...),
    source_name: str | None = Form(None),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="A PDF or text file is required.")
    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".pdf", ".txt"}:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")
    KB_SOURCES_ROOT.mkdir(parents=True, exist_ok=True)
    safe_source_name = (source_name or Path(file.filename).stem or "kb_source").strip() or "kb_source"
    saved_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid4().hex[:10]}{suffix}"
    saved_path = KB_SOURCES_ROOT / saved_name
    saved_path.write_bytes(await file.read())
    result = add_document_to_kb(str(saved_path), subject, safe_source_name)
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("message", "Could not add document to the knowledge base."))
    return {
        "message": "Document added to the knowledge base.",
        "file_name": saved_name,
        "source_name": safe_source_name,
        "subject": result.get("subject"),
        "chunks_added": result.get("chunks_added", 0),
        "stats": get_kb_stats(),
    }


@app.get("/api/analytics/{student_name}")
def analytics_summary(student_name: str):
    _load_profile_or_404(student_name)
    return get_analytics_summary(student_name)


@app.get("/api/progress/{student_name}")
def progress_summary(student_name: str):
    _load_profile_or_404(student_name)
    return get_progress_snapshot(student_name)


@app.get("/api/storage-status/{student_name}")
def storage_status(student_name: str):
    profile = _load_profile_or_404(student_name)
    progress = get_progress_snapshot(profile["name"])
    chats = get_chat_counts(profile["name"])
    syllabus_docs = get_syllabus_documents(profile["name"])
    analytics = get_analytics_summary(profile["name"])
    memory = load_personal_memory(profile["name"])
    behavior_state = load_behavior_state(profile["name"])
    outcome_state = load_outcome_state(profile["name"])
    memory_items = sum(
        len(memory.get(key, []))
        for key in ("known_people", "interests", "life_notes", "recent_checkins")
    )
    return {
        "student_name": profile["name"],
        "profile_saved": True,
        "progress_items": progress["counts"]["total"],
        "chat_messages": chats["total"],
        "syllabus_documents": len(syllabus_docs),
        "practice_attempts": analytics.get("total_attempts", 0),
        "analytics_trend": analytics.get("trend_signal", "building"),
        "memory_items": memory_items,
        "behavior_events": len(behavior_state.get("events", [])),
        "outcome_records": len(outcome_state.get("outcomes", [])),
        "chat_by_mode": chats["by_mode"],
        "last_progress_update": progress.get("last_updated", ""),
    }


@app.get("/api/engagement/{student_name}")
def engagement_summary(student_name: str):
    profile = _load_profile_or_404(student_name)
    return {
        "student_name": profile["name"],
        "engagement": get_engagement_snapshot(profile["name"]),
    }


@app.get("/api/storage-overview/{student_name}")
def storage_overview(student_name: str):
    profile = _load_profile_or_404(student_name)
    status = storage_status(profile["name"])
    return {
        "student_name": profile["name"],
        "database_path": settings.database_path,
        "storage_root": settings.storage_root,
        "storage_backend": settings.storage_backend,
        "mvp_ready": True,
        "safety_notes": [
            "Student data is currently stored locally on this computer.",
            "SQLite plus local file storage is acceptable for an MVP and demo stage.",
            "It is not yet production-grade security because there is no encryption-at-rest or managed cloud backup by default.",
        ],
        "stored_entities": [
            "accounts and sessions",
            "student profiles",
            "progress tracker",
            "chat conversations and messages",
            "behavior state",
            "planner state",
            "analytics",
            "personal memory",
            "uploaded syllabus documents",
        ],
        "counts": status,
    }


@app.get("/api/student-insights/{student_name}")
def student_insights(student_name: str):
    profile = _load_profile_or_404(student_name)
    insight_snapshot = get_student_insight_snapshot(profile)
    architecture_snapshot = get_student_architecture_snapshot(profile)
    return {
        "student_name": profile["name"],
        "insight_snapshot": insight_snapshot,
        "architecture_snapshot": architecture_snapshot,
        "student_state_route": build_student_state_route(
            profile,
            conversation_mode="tutor",
            tutor_level=int(profile.get("default_tutor_level", 3) or 3),
            support_style=insight_snapshot.get("support_style"),
            insight_snapshot=insight_snapshot,
        ),
        "student_state_route_text": format_student_state_route(
            build_student_state_route(
                profile,
                conversation_mode="tutor",
                tutor_level=int(profile.get("default_tutor_level", 3) or 3),
                support_style=insight_snapshot.get("support_style"),
                insight_snapshot=insight_snapshot,
            )
        ),
        "storage_overview_url": f"/api/storage-overview/{profile['name']}",
    }


@app.get("/api/student-state-route/{student_name}")
def student_state_route(student_name: str, conversation_mode: str = "tutor", tutor_level: int = 3):
    profile = _load_profile_or_404(student_name)
    insight_snapshot = get_student_insight_snapshot(profile)
    route = build_student_state_route(
        profile,
        conversation_mode=conversation_mode,
        tutor_level=tutor_level,
        support_style=insight_snapshot.get("support_style"),
        insight_snapshot=insight_snapshot,
    )
    return {
        "student_name": profile["name"],
        "conversation_mode": conversation_mode,
        "student_state_route": route,
        "student_state_route_text": format_student_state_route(route),
    }


@app.get("/api/feature-health/{student_name}")
def feature_health(student_name: str):
    profile = _load_profile_or_404(student_name)
    return get_feature_health_snapshot(profile)


@app.get("/api/syllabus/{student_name}")
def syllabus_documents(student_name: str):
    profile = _load_profile_or_404(student_name)
    return {
        "student_name": profile["name"],
        "documents": get_syllabus_documents(profile["name"]),
    }


@app.post("/api/syllabus/upload")
def upload_syllabus(request: SyllabusUploadRequest):
    profile = _load_profile_or_404(request.student_name)
    try:
        document = save_syllabus_document(
            student_name=profile["name"],
            title=request.title,
            text_content=request.text_content,
            file_base64=request.file_base64,
            file_name=request.file_name,
            mime_type=request.mime_type,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "student_name": profile["name"],
        "document": document,
        "documents": get_syllabus_documents(profile["name"]),
        "storage_status": storage_status(profile["name"]),
    }


@app.post("/api/syllabus/delete")
def remove_syllabus_document(request: SyllabusDeleteRequest):
    profile = _load_profile_or_404(request.student_name)
    deleted_count = delete_syllabus_document(profile["name"], request.document_id)
    return {
        "student_name": profile["name"],
        "deleted_count": deleted_count,
        "documents": get_syllabus_documents(profile["name"]),
        "storage_status": storage_status(profile["name"]),
    }


@app.get("/api/chat-history/{student_name}")
def chat_history(student_name: str, conversation_mode: str = "", conversation_id: int | None = None):
    profile = _load_profile_or_404(student_name)
    return {
        "student_name": profile["name"],
        "conversation_mode": conversation_mode or "",
        "conversation_id": conversation_id,
        "messages": get_chat_history(profile["name"], conversation_mode or None, conversation_id=conversation_id),
    }


@app.get("/api/conversations/{student_name}")
def conversation_list(student_name: str, conversation_mode: str = "tutor", q: str = ""):
    profile = _load_profile_or_404(student_name)
    return {
        "student_name": profile["name"],
        "conversation_mode": conversation_mode,
        "conversations": list_conversations(profile["name"], conversation_mode, query_text=q),
    }


@app.get("/api/conversations/deleted/{student_name}")
def deleted_conversation_list(student_name: str, conversation_mode: str = "tutor"):
    profile = _load_profile_or_404(student_name)
    return {
        "student_name": profile["name"],
        "conversation_mode": conversation_mode,
        "conversations": list_deleted_conversations(profile["name"], conversation_mode),
    }


@app.post("/api/conversations/new")
def new_conversation(request: ConversationCreateRequest):
    profile = _load_profile_or_404(request.student_name)
    conversation = create_conversation(profile["name"], request.conversation_mode, request.title)
    return {
        "student_name": profile["name"],
        "conversation": conversation,
        "conversations": list_conversations(profile["name"], request.conversation_mode),
    }


@app.post("/api/conversations/restore")
def restore_deleted_conversation(request: ConversationRestoreRequest):
    profile = _load_profile_or_404(request.student_name)
    restored_count = restore_conversation(profile["name"], request.conversation_mode, request.conversation_id)
    return {
        "student_name": profile["name"],
        "restored_count": restored_count,
        "conversation_mode": request.conversation_mode,
        "conversations": list_conversations(profile["name"], request.conversation_mode),
        "deleted_conversations": list_deleted_conversations(profile["name"], request.conversation_mode),
    }


@app.post("/api/conversations/update")
def update_conversation(request: ConversationUpdateRequest):
    profile = _load_profile_or_404(request.student_name)
    updated_count = update_conversation_metadata(
        profile["name"],
        request.conversation_mode,
        request.conversation_id,
        title=request.title,
        pinned=request.pinned,
    )
    return {
        "student_name": profile["name"],
        "updated_count": updated_count,
        "conversation_mode": request.conversation_mode,
        "conversations": list_conversations(profile["name"], request.conversation_mode),
        "deleted_conversations": list_deleted_conversations(profile["name"], request.conversation_mode),
    }


@app.post("/api/chat-history/delete")
def clear_chat_history(request: ChatDeleteRequest):
    profile = _load_profile_or_404(request.student_name)
    deleted_count = delete_chat_history(
        profile["name"],
        request.conversation_mode or None,
        conversation_id=request.conversation_id,
    )
    return {
        "student_name": profile["name"],
        "conversation_mode": request.conversation_mode or "",
        "conversation_id": request.conversation_id,
        "deleted_count": deleted_count,
        "conversations": list_conversations(profile["name"], request.conversation_mode or "tutor")
        if request.conversation_mode
        else [],
        "deleted_conversations": list_deleted_conversations(profile["name"], request.conversation_mode or "tutor")
        if request.conversation_mode
        else [],
        "storage_status": storage_status(profile["name"]),
    }


@app.post("/api/progress/item")
def save_progress_item(request: ProgressItemRequest):
    profile = _load_profile_or_404(request.student_name)
    before_state = load_progress_state(profile["name"])
    before_item = next(
        (
            item
            for item in before_state.get("items", [])
            if item.get("exam", "").lower() == str(request.exam or "").strip().lower()
            and item.get("subject", "").lower() == str(request.subject or "").strip().lower()
            and item.get("topic", "").lower() == str(request.topic or "").strip().lower()
        ),
        None,
    )
    snapshot = upsert_progress_item(
        name=profile["name"],
        exam=request.exam,
        subject=request.subject,
        topic=request.topic,
        status=request.status,
        note=request.note,
    )
    record_behavior_event(
        profile["name"],
        event_type="progress_item_saved",
        user_input=f"{request.topic} marked {request.status}",
        tutor_response="Progress tracker updated.",
        metadata={
            "exam": request.exam,
            "subject": request.subject,
            "status": request.status,
        },
    )
    if not before_item or before_item.get("status") != request.status:
        if request.status == "done":
            award_points(profile["name"], 25, f"completing {request.topic}")
        elif request.status == "revise":
            award_points(profile["name"], 12, f"marking {request.topic} for structured revision")
    return snapshot


@app.post("/api/progress/status")
def save_progress_status(request: ProgressStatusRequest):
    profile = _load_profile_or_404(request.student_name)
    existing_item = next(
        (
            item
            for item in load_progress_state(profile["name"]).get("items", [])
            if item.get("id") == request.item_id
        ),
        None,
    )
    snapshot = update_progress_status(profile["name"], request.item_id, request.status)
    record_behavior_event(
        profile["name"],
        event_type="progress_status_updated",
        user_input=f"progress status changed to {request.status}",
        tutor_response="Progress tracker updated.",
        metadata={"item_id": request.item_id, "status": request.status},
    )
    if not existing_item or existing_item.get("status") != request.status:
        if request.status == "done":
            award_points(profile["name"], 20, "pushing a topic into the done lane")
        elif request.status == "revise":
            award_points(profile["name"], 10, "moving a topic into the revision lane")
    return snapshot


@app.get("/api/network/{student_name}")
def network_summary(student_name: str):
    profile = _load_profile_or_404(student_name)
    return build_network_snapshot(profile)


@app.post("/api/network/group-study/preferences")
def update_group_study_preferences(request: GroupStudyPreferencesRequest):
    profile = _load_profile_or_404(request.student_name)
    current_preferences = dict(profile.get("group_study_preferences") or {})
    action = str(request.action or "save").strip().lower()

    def _safe_int(value, default, minimum=None, maximum=None):
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            parsed = default
        if minimum is not None:
            parsed = max(minimum, parsed)
        if maximum is not None:
            parsed = min(maximum, parsed)
        return parsed

    if action == "solo":
        current_preferences.update(
            {
                "enabled": False,
                "mode": "solo",
                "group_size": _safe_int(current_preferences.get("group_size", request.group_size), request.group_size or 3, minimum=2, maximum=5),
                "session_minutes": _safe_int(current_preferences.get("session_minutes", request.session_minutes), request.session_minutes or 60, minimum=30, maximum=120),
                "focus": request.focus.strip() or str(current_preferences.get("focus", "")).strip(),
            }
        )
    else:
        try:
            group_size = int(request.group_size or current_preferences.get("group_size", 3) or 3)
        except (TypeError, ValueError):
            group_size = 3
        try:
            session_minutes = int(request.session_minutes or current_preferences.get("session_minutes", 60) or 60)
        except (TypeError, ValueError):
            session_minutes = 60
        try:
            rotation_index = int(request.rotation_index or current_preferences.get("rotation_index", 0) or 0)
        except (TypeError, ValueError):
            rotation_index = 0

        current_preferences.update(
            {
                "enabled": bool(request.enabled) if action != "reroll" else True,
                "mode": str(request.mode or current_preferences.get("mode", "mixed")).strip().lower() or "mixed",
                "group_size": max(2, min(5, group_size)),
                "session_minutes": max(30, min(120, session_minutes)),
                "focus": request.focus.strip() or str(current_preferences.get("focus", "")).strip(),
                "rotation_index": max(0, rotation_index + (1 if action == "reroll" else 0)),
            }
        )
        if current_preferences["mode"] == "solo":
            current_preferences["enabled"] = False

    profile["group_study_preferences"] = current_preferences
    save_profile(profile)
    network = build_network_snapshot(profile)
    return {
        "profile": profile,
        "group_study": network.get("group_study"),
        "stats": network.get("stats"),
    }


@app.get("/api/fun-fact/{student_name}")
def fun_fact(student_name: str):
    profile = _load_profile_or_404(student_name)
    return get_daily_fun_fact(profile["name"])


@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        profile = _load_profile_or_404(request.student_name)
        student_insight_snapshot = get_student_insight_snapshot(profile)
        tutor_brain = _build_tutor_brain_snapshot(
            profile,
            _get_avatar_preset(profile),
            student_insight_snapshot,
            request.conversation_mode,
            request.tutor_level,
            request.voice_chat_mode,
        )
        personal_memory = (
            load_personal_memory(profile["name"])
            if request.conversation_mode == "guide"
            else update_personal_memory(profile["name"], request.message)
        )
        local_reply, event_type = _handle_local_command(profile, request.message)

        conversation_id = resolve_conversation_id(
            profile["name"],
            request.conversation_mode,
            conversation_id=request.conversation_id,
            seed_title=request.message,
        )

        if local_reply is None:
            record_bond_interaction(profile["name"])
            agent_result = _run_agent_reply(
                profile,
                request.message,
                voice_chat_mode=request.voice_chat_mode,
                response_language=request.response_language,
                conversation_mode=request.conversation_mode,
                tutor_mode=request.tutor_mode,
                tutor_level=request.tutor_level,
                reading_comfort_mode=request.reading_comfort_mode,
                chunked_reply_mode=request.chunked_reply_mode,
                response_pacing=request.response_pacing,
            )
            reply = agent_result["reply"]
            live_sources = agent_result["live_sources"]
            visual_learning = agent_result["visual_learning"]
            video_explanation = agent_result["video_explanation"]
            adaptive_profile = agent_result["adaptive_profile"]
            event_type = "chat"
            if request.conversation_mode == "tutor" and visual_learning:
                reward_points = int((visual_learning.get("mastery") or {}).get("reward_points", 18) or 18)
                award_points(
                    profile["name"],
                    reward_points,
                    f"unlocking a visual concept explanation for {visual_learning.get('title', 'a concept')}",
                )
            if request.conversation_mode == "tutor" and video_explanation:
                award_points(profile["name"], 10, "watching a lesson-style concept walkthrough")
        else:
            reply = local_reply
            live_sources = []
            visual_learning = build_visual_learning_aid(request.message) if request.conversation_mode == "tutor" else None
            video_explanation = (
                build_video_explanation(request.message, request.response_language)
                if request.conversation_mode == "tutor"
                else None
            )
            adaptive_profile = (
                get_adaptive_learning_profile(profile)
                if request.conversation_mode in {"tutor", "practice"}
                else None
            )
            if request.conversation_mode == "tutor" and visual_learning:
                reward_points = int((visual_learning.get("mastery") or {}).get("reward_points", 18) or 18)
                award_points(
                    profile["name"],
                    reward_points,
                    f"unlocking a visual concept explanation for {visual_learning.get('title', 'a concept')}",
                )
            if request.conversation_mode == "tutor" and video_explanation:
                award_points(profile["name"], 10, "watching a lesson-style concept walkthrough")

        if request.conversation_mode != "guide":
            record_behavior_event(
                profile["name"],
                event_type=event_type,
                user_input=request.message,
                tutor_response=reply,
            )
            # Self-learning loop: record chat outcome
            _record_chat_outcome_from_reply(
                profile["name"],
                request.message,
                reply,
                request.conversation_mode,
            )
        save_chat_message(profile["name"], request.conversation_mode, "student", request.message, conversation_id=conversation_id)
        save_chat_message(profile["name"], request.conversation_mode, "tutor", reply, conversation_id=conversation_id)
        return {
            "reply": reply,
            "student_name": profile["name"],
            "conversation_id": conversation_id,
            "conversations": list_conversations(profile["name"], request.conversation_mode),
            "reply_type": "weekly_plan" if request.message.strip().lower() == "show weekly plan" else "text",
            "active_avatar": _get_avatar_preset(profile),
            "fun_fact": get_daily_fun_fact(profile["name"]),
            "personal_memory": personal_memory,
            "live_sources": live_sources,
            "visual_learning": visual_learning,
            "video_explanation": video_explanation,
            "adaptive_profile": adaptive_profile,
            "tutor_brain": tutor_brain,
            "reply_source": agent_result.get("reply_source", "local"),
            "weekly_plan": get_weekly_schedule_data(profile)
            if request.message.strip().lower() == "show weekly plan"
            else None,
        }
    except HTTPException:
        raise
    except Exception as exc:
        logging.exception("Chat request failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="The tutor ran into a temporary issue while replying. Please try again.",
        ) from exc


@app.post("/api/checkpoint/generate")
def checkpoint_generate(request: CheckpointGenerateRequest):
    try:
        profile = _load_profile_or_404(request.student_name) if str(request.student_name or "").strip() else None
        checkpoint = generate_checkpoint_question(
            request.topic,
            request.subject,
            request.explanation_level or (profile.get("default_tutor_level", 3) if profile else 3),
            request.original_explanation,
            genai_client=genai_client,
            practice_count=request.practice_count,
        )
        if profile:
            active_exam = (profile.get("exams") or [{}])[0] if profile.get("exams") else {}
            checkpoint["student_name"] = profile["name"]
            checkpoint["active_exam"] = active_exam.get("name", "") if isinstance(active_exam, dict) else ""
        return checkpoint
    except HTTPException:
        raise
    except Exception as exc:
        logging.exception("Checkpoint generation failed: %s", exc)
        raise HTTPException(status_code=500, detail="The tutor could not build a quick check right now.") from exc


@app.post("/api/checkpoint/evaluate")
def checkpoint_evaluate(request: CheckpointEvaluateRequest):
    try:
        profile = _load_profile_or_404(request.student_name) if str(request.student_name or "").strip() else None
        evaluation = evaluate_checkpoint_answer(
            request.question,
            request.correct_answer,
            request.student_answer,
            request.topic,
            subject=request.subject,
            explanation_level=request.explanation_level or (profile.get("default_tutor_level", 3) if profile else 3),
            original_explanation=request.original_explanation,
            genai_client=genai_client,
        )

        if profile:
            active_exam = ""
            if profile.get("exams"):
                first_exam = profile.get("exams")[0]
                if isinstance(first_exam, dict):
                    active_exam = first_exam.get("name", "")
            record_analytics_checkpoint_attempt(
                profile["name"],
                request.topic,
                request.subject or "",
                evaluation["is_correct"],
                question=request.question,
                student_answer=request.student_answer,
                correct_answer=evaluation["correct_answer"],
                explanation_level=request.explanation_level or (profile.get("default_tutor_level", 3) if profile else 3),
                exam=active_exam,
                feedback=evaluation.get("feedback", ""),
            )
            record_progress_checkpoint_attempt(
                profile["name"],
                active_exam,
                request.subject or "",
                request.topic,
                evaluation["is_correct"],
                question=request.question,
                student_answer=request.student_answer,
                correct_answer=evaluation["correct_answer"],
                explanation_level=request.explanation_level or (profile.get("default_tutor_level", 3) if profile else 3),
                feedback=evaluation.get("feedback", ""),
                re_explanation=evaluation.get("re_explanation", ""),
            )

        if evaluation["is_correct"]:
            evaluation["feedback"] = evaluation.get("feedback") or "Nice work — that clicked."
            evaluation["offer_more_practice"] = True
            evaluation["more_practice_heading"] = "More practice is ready if you want it."
        else:
            evaluation["offer_more_practice"] = False
        return evaluation
    except HTTPException:
        raise
    except Exception as exc:
        logging.exception("Checkpoint evaluation failed: %s", exc)
        raise HTTPException(status_code=500, detail="The tutor could not evaluate that checkpoint right now.") from exc


@app.post("/api/summarize")
def summarize_answer(request: SummarizeRequest):
    try:
        profile = _load_profile_or_404(request.student_name)
        source_text = (request.answer_text or "").strip()
        if not source_text:
            raise HTTPException(status_code=400, detail="There is no answer available to summarize yet.")

        prompt = (
            "Summarize the following tutor answer into a crisp, student-friendly quick revision note. "
            "Keep it short, clear, and easy to scan. "
            "Use 3 to 6 short bullet points or very short lines. "
            "Preserve the core idea, formulas, warnings, and final takeaway if present, but remove repetition.\n\n"
            f"Original answer:\n{source_text}"
        )
        if request.response_language and request.response_language.lower() != "english":
            prompt += f"\n\nWrite the summary in {request.response_language}."

        result = _run_agent_reply(
            profile,
            prompt,
            voice_chat_mode=False,
            response_language=request.response_language,
            conversation_mode=request.conversation_mode if request.conversation_mode in {"tutor", "practice", "last_minute"} else "tutor",
            tutor_level=2,
        )
        return {
            "summary": result["reply"],
            "student_name": profile["name"],
        }
    except HTTPException:
        raise
    except Exception as exc:
        logging.exception("Summary request failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="The app could not summarize that answer right now. Please try again.",
        ) from exc


@app.post("/api/video-answer/brief")
def video_answer_brief(request: VideoAnswerBriefRequest):
    try:
        try:
            profile = _load_profile_or_404(request.student_name)
        except Exception as exc:
            logging.warning("Video answer brief profile lookup failed for %s; using fallback profile: %s", request.student_name, exc)
            profile = _fallback_video_profile(request.student_name)
        avatar = _get_avatar_preset(profile)
        tutor_brain = _build_tutor_brain_snapshot(
            profile,
            avatar,
            get_student_insight_snapshot(profile),
            request.conversation_mode if request.conversation_mode in {"tutor", "practice", "last_minute", "tips"} else "tutor",
            request.tutor_level,
            request.conversation_mode == "tutor",
        )
        brief = build_video_answer_brief(
            profile,
            request.question,
            answer_text=request.answer_text,
            conversation_mode=request.conversation_mode,
            tutor_level=request.tutor_level,
            response_language=request.response_language,
            tutor_brain=tutor_brain,
            avatar=avatar,
        )
        return {
            "student_name": profile["name"],
            "active_avatar": avatar,
            "tutor_brain": tutor_brain,
            "video_answer_brief": brief,
        }
    except HTTPException:
        raise
    except Exception as exc:
        logging.exception("Video answer brief request failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="The video answer brief could not be created right now. Please try again.",
        ) from exc


@app.post("/api/video-answer/render")
def video_answer_render(request: VideoAnswerRenderRequest):
    try:
        try:
            profile = _load_profile_or_404(request.student_name)
        except Exception as exc:
            logging.warning("Video answer render profile lookup failed for %s; using fallback profile: %s", request.student_name, exc)
            profile = _fallback_video_profile(request.student_name)
        avatar = _get_avatar_preset(profile)
        tutor_brain = _build_tutor_brain_snapshot(
            profile,
            avatar,
            get_student_insight_snapshot(profile),
            request.conversation_mode if request.conversation_mode in {"tutor", "practice", "last_minute", "tips"} else "tutor",
            request.tutor_level,
            request.conversation_mode == "tutor",
        )
        brief = build_video_answer_brief(
            profile,
            request.question,
            answer_text=request.answer_text,
            conversation_mode=request.conversation_mode,
            tutor_level=request.tutor_level,
            response_language=request.response_language,
            tutor_brain=tutor_brain,
            avatar=avatar,
        )
        render_job = build_video_render_request(profile, brief, avatar=avatar)
        render_job["tutor_brain"] = tutor_brain
        render_job["brief_status"] = brief.get("status", "brief_ready")
        render_folder = os.path.join("video_render_jobs", profile["name"])
        render_path = os.path.join(settings.storage_root, render_folder, f"{render_job['job_id']}.json")
        atomic_write_json(render_path, render_job)
        render_job["stored_path"] = render_path
        return {
            "student_name": profile["name"],
            "active_avatar": avatar,
            "tutor_brain": tutor_brain,
            "video_answer_brief": brief,
            "render_job": render_job,
        }
    except HTTPException:
        raise
    except Exception as exc:
        logging.exception("Video answer render request failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="The video render request could not be created right now. Please try again.",
        ) from exc


def _select_video_voice_id(profile: dict, avatar: dict, tutor_personality: str = "") -> str:
    for key in ("video_voice_id", "tutor_voice_id", "elevenlabs_voice_id", "voice_id"):
        value = str(profile.get(key, "") or "").strip()
        if value:
            return value
    personality_text = str(tutor_personality or profile.get("tutor_style", "") or avatar.get("name", "")).lower()
    if any(term in personality_text for term in ("female", "warm", "mentor", "calm")):
        return os.getenv("ELEVENLABS_FEMALE_VOICE_ID", os.getenv("ELEVENLABS_DEFAULT_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"))
    if any(term in personality_text for term in ("male", "strategist", "strict", "sharp")):
        return os.getenv("ELEVENLABS_MALE_VOICE_ID", os.getenv("ELEVENLABS_DEFAULT_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"))
    return os.getenv("ELEVENLABS_DEFAULT_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")


def _serialize_tutor_script(script) -> dict:
    if isinstance(script, TutorScript):
        return script.model_dump()
    if isinstance(script, dict):
        return TutorScript(**script).model_dump()
    return TutorScript().model_dump()


def _generate_voice_audio(job_id: str, script_text: str, voice_id: str = "") -> str:
    api_key = (os.getenv("ELEVENLABS_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is missing.")
    try:
        from elevenlabs import ElevenLabs
    except Exception as exc:
        raise RuntimeError("The elevenlabs package is not installed.") from exc

    selected_voice_id = (voice_id or "").strip() or os.getenv("ELEVENLABS_DEFAULT_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    client = ElevenLabs(api_key=api_key)
    try:
        audio_result = client.text_to_speech.convert(
            voice_id=selected_voice_id,
            text=script_text,
            model_id=os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2"),
            output_format="mp3_44100_128",
        )
    except Exception as exc:
        raise RuntimeError(f"ElevenLabs synthesis failed: {exc}") from exc

    if isinstance(audio_result, (bytes, bytearray)):
        audio_bytes = bytes(audio_result)
    elif hasattr(audio_result, "read"):
        audio_bytes = audio_result.read()
    else:
        chunks = []
        for chunk in audio_result:
            if isinstance(chunk, (bytes, bytearray)):
                chunks.append(bytes(chunk))
            elif isinstance(chunk, str):
                chunks.append(chunk.encode("utf-8"))
        audio_bytes = b"".join(chunks)

    if not audio_bytes:
        raise RuntimeError("ElevenLabs returned an empty audio payload.")
    _write_audio_file(job_id, audio_bytes)
    return _build_audio_relative_url(job_id)


def _create_did_talk(job_id: str, tutor_face_url: str, audio_url: str, script: TutorScript) -> str:
    api_key = (os.getenv("DID_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError("DID_API_KEY is missing.")
    auth_header = _did_auth_header()
    if not auth_header:
        raise RuntimeError("DID_API_KEY is missing.")
    payload = {
        "source_url": _resolve_public_url(tutor_face_url),
        "script": {
            "type": "audio",
            "audio_url": _resolve_public_url(audio_url),
        },
        "config": {
            "stitch": True,
        },
        "user_data": json.dumps({"job_id": job_id})[:1000],
    }
    with httpx.Client(timeout=120.0) as client:
        response = client.post(
            "https://api.d-id.com/talks",
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json",
            },
            json=payload,
        )
    if response.status_code >= 400:
        raise RuntimeError(f"D-ID render request failed: {response.status_code} {response.text}")
    data = response.json()
    did_talk_id = str(data.get("id") or data.get("talk_id") or "").strip()
    if not did_talk_id:
        raise RuntimeError("D-ID did not return a talk id.")
    return did_talk_id


def _poll_did_talk(did_talk_id: str) -> dict:
    auth_header = _did_auth_header()
    if not auth_header:
        raise RuntimeError("DID_API_KEY is missing.")
    with httpx.Client(timeout=60.0) as client:
        response = client.get(
            f"https://api.d-id.com/talks/{did_talk_id}",
            headers={"Authorization": auth_header},
        )
    if response.status_code >= 400:
        raise RuntimeError(f"D-ID status request failed: {response.status_code} {response.text}")
    return response.json()


def _run_video_generation_job(job_id: str, request_payload: dict):
    def persist_job(status: str, **updates):
        job_state = _load_video_job(job_id)
        job_state.update({"status": status, **updates})
        _save_video_job(job_id, job_state)
        return job_state

    def fail_job(stage: str, exc: Exception):
        error_message = f"{stage}: {exc}"
        print(f"[video_generate] job {job_id} failed - {error_message}")
        logging.exception("Video generation job failed for %s during %s: %s", job_id, stage, exc)
        try:
            persist_job("failed", error=error_message, failed_stage=stage)
        except Exception:
            logging.exception("Could not persist failed state for video job %s", job_id)

    try:
        print(f"[video_generate] job {job_id} starting with payload: {request_payload}")
        job = persist_job("generating_script")
        student_id = str(request_payload.get("student_id") or job.get("student_id") or "").strip()
        try:
            profile = _load_profile_or_404(student_id)
        except Exception as exc:
            logging.warning("Video generation profile lookup failed for %s; using fallback profile: %s", student_id, exc)
            profile = _fallback_video_profile(
                student_id or "Student",
                request_payload.get("tutor_face_url", ""),
                request_payload.get("tutor_personality", ""),
            )

        try:
            avatar = _get_avatar_preset(profile)
            tutor_personality = str(request_payload.get("tutor_personality") or profile.get("tutor_style", "") or "").strip()
            tutor_level = int(profile.get("default_tutor_level", 3) or 3)
            tutor_brain = _build_tutor_brain_snapshot(
                profile,
                avatar,
                get_student_insight_snapshot(profile),
                "tutor",
                tutor_level,
                True,
            )
            tutor_script = build_tutor_script(
                profile,
                request_payload.get("question", ""),
                answer_text=request_payload.get("question", ""),
                conversation_mode="tutor",
                tutor_level=tutor_level,
                response_language=profile.get("default_response_language", "English"),
                tutor_brain=tutor_brain,
                avatar=avatar,
                tutor_personality=tutor_personality,
                genai_client=genai_client,
            )
            job = persist_job(
                "generating_voice",
                script=tutor_script.model_dump(),
                tutor_brain=tutor_brain,
                tutor_face_url=request_payload.get("tutor_face_url", ""),
                tutor_personality=tutor_personality,
            )
        except Exception as exc:
            fail_job("generate_script", exc)
            return

        try:
            voice_url = _generate_voice_audio(
                job_id,
                " ".join(
                    item for item in [
                        tutor_script.opening,
                        tutor_script.concept_explanation,
                        tutor_script.worked_example,
                        tutor_script.checkpoint_question,
                        tutor_script.recap,
                    ]
                    if item
                ).strip(),
                voice_id=_select_video_voice_id(profile, avatar, tutor_personality),
            )
            job = persist_job("rendering_video", audio_url=voice_url)
        except Exception as exc:
            fail_job("generate_voice", exc)
            return

        try:
            did_talk_id = _create_did_talk(
                job_id,
                request_payload.get("tutor_face_url", ""),
                voice_url,
                tutor_script,
            )
            persist_job(
                "processing",
                did_talk_id=did_talk_id,
                audio_url=voice_url,
            )
            print(f"[video_generate] job {job_id} created D-ID talk {did_talk_id}")
        except Exception as exc:
            fail_job("render_video", exc)
            return
    except Exception as exc:
        fail_job("job_runner", exc)


@app.post("/api/video/generate-voice")
def video_generate_voice(request: VideoGenerateVoiceRequest):
    try:
        job_id = request.job_id.strip()
        if not job_id:
            raise HTTPException(status_code=400, detail="job_id is required.")
        audio_url = _generate_voice_audio(job_id, request.script_text, request.voice_id)
        return {
            "audio_url": audio_url,
            "status": "ready",
        }
    except HTTPException:
        raise
    except Exception as exc:
        logging.exception("Voice generation failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/video/render")
def video_render(request: VideoRenderJobRequest):
    try:
        job = _load_video_job(request.job_id)
        script = request.script if isinstance(request.script, TutorScript) else TutorScript(**request.script)
        did_talk_id = _create_did_talk(request.job_id, request.tutor_face_url, request.audio_url, script)
        job.update(
            {
                "status": "processing",
                "did_talk_id": did_talk_id,
                "tutor_face_url": request.tutor_face_url,
                "audio_url": request.audio_url,
                "script": script.model_dump(),
            }
        )
        _save_video_job(request.job_id, job)
        return {
            "job_id": request.job_id,
            "did_talk_id": did_talk_id,
            "status": "processing",
        }
    except HTTPException:
        raise
    except Exception as exc:
        logging.exception("D-ID render creation failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/video/status/{job_id}")
def video_status(job_id: str):
    try:
        job = _load_video_job(job_id)
        current_status = str(job.get("status", "queued")).strip().lower()
        if current_status in {"failed", "queued", "generating_script", "generating_voice"}:
            return {
                "status": current_status,
                "job_id": job_id,
                "message": job.get("error", ""),
            }

        did_talk_id = str(job.get("did_talk_id") or "").strip()
        if not did_talk_id:
            if current_status == "rendering_video":
                return {
                    "status": "pending",
                    "job_id": job_id,
                }
            if current_status == "ready" and job.get("video_url"):
                return {
                    "status": "ready",
                    "video_url": job.get("video_url"),
                    "job_id": job_id,
                }
            return {
                "status": current_status or "pending",
                "job_id": job_id,
            }

        did_status = _poll_did_talk(did_talk_id)
        did_state = str(did_status.get("status", "")).strip().lower()
        if did_state == "done":
            video_url = did_status.get("result_url") or did_status.get("video_url") or ""
            job.update({"status": "ready", "video_url": video_url, "did_status": did_status})
            _save_video_job(job_id, job)
            return {
                "status": "ready",
                "video_url": video_url,
                "script": job.get("script", {}),
                "job_id": job_id,
            }
        if did_state in {"created", "started", "pending", "processing"}:
            job.update({"status": "rendering_video", "did_status": did_status})
            _save_video_job(job_id, job)
            return {
                "status": "pending",
                "job_id": job_id,
            }
        if did_state == "error":
            error_message = did_status.get("error", {}).get("message") if isinstance(did_status.get("error"), dict) else did_status.get("error", "D-ID rendering failed.")
            job.update({"status": "failed", "error": error_message, "did_status": did_status})
            _save_video_job(job_id, job)
            return {
                "status": "failed",
                "error": error_message,
                "job_id": job_id,
            }
        return {
            "status": "pending",
            "job_id": job_id,
        }
    except HTTPException:
        raise
    except Exception as exc:
        logging.exception("Video status lookup failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/video/generate")
def video_generate(request: VideoGenerateRequest, background_tasks: BackgroundTasks):
    try:
        print("[video_generate] incoming request body:", request.model_dump())
        job_id = str(uuid4())
        _ensure_video_job_dirs()
        initial_job = {
            "job_id": job_id,
            "status": "queued",
            "created_at": datetime.utcnow().isoformat(),
            "student_id": request.student_id,
            "question": request.question,
            "topic": request.topic,
            "subject": request.subject,
            "tutor_face_url": request.tutor_face_url,
            "tutor_personality": request.tutor_personality,
        }
        _save_video_job(job_id, initial_job)
        background_tasks.add_task(_run_video_generation_job, job_id, request.model_dump())
        return {
            "job_id": job_id,
            "status": "queued",
        }
    except HTTPException:
        raise
    except Exception as exc:
        logging.exception("Video generation queue creation failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/chat/image")
def image_chat(request: ImageChatRequest):
    try:
        profile = _load_profile_or_404(request.student_name)
        image_bytes = base64.b64decode(request.image_base64)
        extension = ".jpg"
        if "png" in (request.mime_type or "").lower():
            extension = ".png"
        stored_image = save_binary_file(
            image_bytes,
            f"{profile['name']}-doubt{extension}",
            folder=os.path.join("doubt_images", _session_id_for(profile["name"])),
        )
        conversation_id = resolve_conversation_id(
            profile["name"],
            "tutor",
            conversation_id=request.conversation_id,
            seed_title=request.message or "Image doubt",
        )
        result = _run_image_tutor_reply(
            profile,
            request.message,
            request.image_base64,
            request.mime_type,
            request.response_language,
        )
        reply = result["reply"]
        record_behavior_event(
            profile["name"],
            event_type="image_doubt_request",
            user_input=request.message or "image doubt",
            tutor_response=reply,
        )
        save_chat_message(profile["name"], "tutor", "student", request.message or "[Image doubt uploaded]", conversation_id=conversation_id)
        save_chat_message(profile["name"], "tutor", "tutor", reply, conversation_id=conversation_id)
        return {
            "reply": reply,
            "student_name": profile["name"],
            "conversation_id": conversation_id,
            "conversations": list_conversations(profile["name"], "tutor"),
            "active_avatar": _get_avatar_preset(profile),
            "tutor_brain": _build_tutor_brain_snapshot(
                profile,
                _get_avatar_preset(profile),
                get_student_insight_snapshot(profile),
                "tutor",
                int(profile.get("default_tutor_level", 3) or 3),
                False,
            ),
            "fun_fact": get_daily_fun_fact(profile["name"]),
            "personal_memory": load_personal_memory(profile["name"]),
            "visual_learning": result["visual_learning"],
            "video_explanation": result["video_explanation"],
            "adaptive_profile": result["adaptive_profile"],
            "reply_source": result.get("reply_source", "local"),
            "live_sources": [],
            "stored_image": stored_image,
        }
    except HTTPException:
        raise
    except Exception as exc:
        logging.exception("Image chat request failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="The tutor could not process that image right now. Please try again with a clearer image.",
        ) from exc


@app.post("/api/analytics/practice")
def practice_analytics(request: PracticeAnalyticsRequest):
    profile = _load_profile_or_404(request.student_name)
    analytics_state = load_analytics_state(profile["name"])
    mode_key = str(request.mode or "general").strip().lower() or "general"
    today_key = datetime.utcnow().date().isoformat()
    already_rewarded_today = any(
        str(item.get("timestamp", "")).startswith(today_key)
        and str(item.get("mode", "")).strip().lower() == mode_key
        for item in analytics_state.get("practice_attempts", [])
    )
    record_practice_attempt(
        name=profile["name"],
        mode=request.mode,
        time_taken_minutes=request.time_taken_minutes,
        accuracy_percent=request.accuracy_percent,
        exam=request.exam,
        notes=request.notes,
        question_count=request.question_count,
    )
    record_behavior_event(
        profile["name"],
        event_type="practice_attempt",
        user_input=f"{request.mode} attempt",
        tutor_response="Practice analytics logged.",
        metadata={
            "time_taken_minutes": request.time_taken_minutes,
            "accuracy_percent": request.accuracy_percent,
            "exam": request.exam,
            "question_count": request.question_count,
        },
    )
    earned_points = 10
    if already_rewarded_today:
        earned_points = 0
    else:
        if request.accuracy_percent >= 85:
            earned_points += 20
        elif request.accuracy_percent >= 70:
            earned_points += 14
        elif request.accuracy_percent >= 55:
            earned_points += 8
        if request.question_count >= 15:
            earned_points += 10
        elif request.question_count >= 8:
            earned_points += 5
        award_points(
            profile["name"],
            earned_points,
            f"{request.mode} practice review with {round(request.accuracy_percent, 1)}% accuracy",
        )
    summary = get_analytics_summary(profile["name"])
    summary["earned_points"] = earned_points
    summary["reward_policy"] = "One rewarded practice review per mode per day."
    return summary


@app.post("/api/planner/mock-scores")
def planner_mock_scores(request: MockScoreRequest):
    profile = _load_profile_or_404(request.student_name)
    exam_name = request.exam.strip().upper()
    if not exam_name:
        raise HTTPException(status_code=400, detail="Please choose an exam before saving mock scores.")

    score_map = {}
    if request.subject_scores:
        for subject, score in request.subject_scores.items():
            subject_name = str(subject).strip()
            if not subject_name:
                continue
            score_map[subject_name] = max(0.0, min(100.0, float(score)))
    else:
        if request.physics is not None:
            score_map["Physics"] = max(0.0, min(100.0, float(request.physics)))
        if request.chemistry is not None:
            score_map["Chemistry"] = max(0.0, min(100.0, float(request.chemistry)))
        if request.mathematics is not None:
            score_map["Mathematics"] = max(0.0, min(100.0, float(request.mathematics)))

    if not score_map:
        raise HTTPException(status_code=400, detail="Please enter at least one subject score.")

    state = save_mock_scores(profile, {exam_name: score_map})
    return {
        "student_name": profile["name"],
        "exam": exam_name,
        "saved_scores": score_map,
        "planner_state": state,
        "weekly_plan": get_weekly_schedule_data(profile),
        "today_plan": format_today_schedule(profile),
        "adaptive_profile": get_adaptive_learning_profile(profile),
    }


@app.post("/api/mock-test/generate")
def generate_mock_test(request: MockTestGenerateRequest):
    profile = _load_profile_or_404(request.student_name)
    exam_name = request.exam.strip().upper() if request.exam.strip() else next(
        (str(exam.get("name", "")).strip().upper() for exam in profile.get("exams", []) if exam.get("name")),
        "JEE MAIN",
    )
    exam_entry = next(
        (exam for exam in profile.get("exams", []) if str(exam.get("name", "")).strip().upper() == exam_name),
        None,
    )
    subjects = list(exam_entry.get("subjects", [])) if exam_entry else []
    if not subjects:
        subjects = list(DEFAULT_EXAM_SUBJECTS.get(exam_name, [])) or ["Physics", "Chemistry", "Mathematics"]

    subject_text = ", ".join(subjects)
    question_count = max(6, min(int(request.question_count or 9), 15))
    per_subject = max(1, question_count // max(1, len(subjects)))
    primary_subject = subjects[0] if subjects else "General"
    payload = None
    if genai_client:
        prompt = (
            "You are generating a clean diagnostic mock test for a student.\n"
            "Return ONLY valid JSON. No markdown. No commentary.\n\n"
            "{\n"
            '  "title": "Diagnostic Mock Test",\n'
            f'  "exam": "{exam_name}",\n'
            '  "time_limit_minutes": 60,\n'
            '  "instructions": "Solve one question at a time. Choose the best option. This mock is for baseline analysis, not judgment.",\n'
            '  "questions": [\n'
            "    {\n"
            '      "id": "q1",\n'
            f'      "subject": "{primary_subject}",\n'
            '      "type": "mcq",\n'
            '      "difficulty": "medium",\n'
            '      "question": "Question text here",\n'
            '      "options": ["Option A", "Option B", "Option C", "Option D"],\n'
            '      "correct_answer": "Option B",\n'
            '      "explanation": "Short explanation here",\n'
            '      "skill_tag": "kinematics"\n'
            "    }\n"
            "  ]\n"
            "}\n\n"
            f"Create {question_count} questions total.\n"
            f"Use the active subjects: {subject_text}.\n"
            f"Try to keep the paper roughly balanced across the subjects, about {per_subject} questions per subject where possible.\n"
            "Create MCQ-only questions. Every question must have exactly 4 options and one correct answer.\n"
            "If the exam is JEE, keep the paper JEE-style and baseline-friendly.\n"
            "If the exam is not JEE, keep it exam-like, fair, and diagnostic.\n"
            "Do not generate integer questions.\n"
            "Keep each explanation short and useful.\n"
            "Do not include any extra keys beyond title, exam, time_limit_minutes, instructions, questions."
        )

        try:
            response = genai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            payload_text = (response.text or "").strip()
            payload = _extract_json_payload(payload_text)
        except Exception as exc:
            logging.warning("Mock test generator fell back to local paper generation: %s", exc)

    if not payload:
        payload = _fallback_mock_test_payload(exam_name, subjects, question_count, request.mode.strip().lower() or "diagnostic")

    questions = payload.get("questions", [])
    if not isinstance(questions, list) or not questions:
        payload = _fallback_mock_test_payload(exam_name, subjects, question_count, request.mode.strip().lower() or "diagnostic")
        questions = payload.get("questions", [])

    normalized_questions = []
    seen_questions = set()
    for index, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            continue
        q_type = str(question.get("type", "mcq")).strip().lower()
        options = [str(option).strip() for option in question.get("options", []) if str(option).strip()]
        correct_answer = str(question.get("correct_answer") or "").strip()
        if q_type != "mcq" or len(options) != 4 or not correct_answer:
            continue
        if correct_answer not in options:
            continue
        question_text = str(question.get("question") or "").strip()
        question_key = re.sub(r"\s+", " ", question_text).lower()
        if not question_text or question_key in seen_questions:
            continue
        seen_questions.add(question_key)
        normalized_questions.append(
            {
                "id": str(question.get("id") or f"q{index}"),
                "subject": str(question.get("subject") or subjects[(index - 1) % len(subjects)]).strip(),
                "type": "mcq",
                "difficulty": str(question.get("difficulty") or "medium").strip().lower(),
                "question": question_text,
                "options": options,
                "correct_answer": correct_answer,
                "explanation": str(question.get("explanation") or "").strip(),
                "skill_tag": str(question.get("skill_tag") or "").strip(),
            }
        )

    fallback_payload = _fallback_mock_test_payload(
        exam_name,
        subjects,
        question_count,
        request.mode.strip().lower() or "diagnostic",
    )
    fallback_questions = fallback_payload.get("questions", [])

    if len(normalized_questions) < question_count:
        existing_ids = {item["id"] for item in normalized_questions if item.get("id")}
        existing_questions = {re.sub(r"\s+", " ", item["question"]).strip().lower() for item in normalized_questions if item.get("question")}
        for fallback_question in fallback_questions:
            if len(normalized_questions) >= question_count:
                break
            if fallback_question["id"] in existing_ids:
                continue
            fallback_key = re.sub(r"\s+", " ", fallback_question["question"]).strip().lower()
            if fallback_key in existing_questions:
                continue
            normalized_questions.append(fallback_question)
            existing_ids.add(fallback_question["id"])
            existing_questions.add(fallback_key)

    if not normalized_questions:
        normalized_questions = fallback_questions

    return {
        "student_name": profile["name"],
        "exam": exam_name,
        "title": payload.get("title", fallback_payload["title"]),
        "time_limit_minutes": int(payload.get("time_limit_minutes") or fallback_payload["time_limit_minutes"]),
        "instructions": payload.get("instructions", fallback_payload["instructions"]),
        "subjects": subjects,
        "questions": normalized_questions[:question_count],
        "mode": request.mode.strip().lower() or "diagnostic",
    }


VIDEO_RENDER_JOB_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

if WEB_DIR.exists():
    app.mount("/audio", StaticFiles(directory=str(VIDEO_AUDIO_DIR), html=False), name="audio")
    app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")


if __name__ == "__main__":
    import uvicorn

    reload_enabled = settings.reload and os.name != "nt"
    uvicorn_kwargs = {
        "host": settings.host,
        "port": settings.port,
        "reload": reload_enabled,
    }
    if reload_enabled:
        uvicorn_kwargs["reload_excludes"] = RELOAD_EXCLUDES

    uvicorn.run(
        "web_api:app",
        **uvicorn_kwargs,
    )
