import os
from dataclasses import dataclass


def _env_flag(name, default=False):
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


def _env_list(name, default):
    raw_value = os.getenv(name)
    if raw_value is None:
        return list(default)
    values = [item.strip() for item in raw_value.split(",") if item.strip()]
    return values or list(default)


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "development")
    app_title: str = os.getenv("APP_TITLE", "Adaptive Learning Tutor")
    host: str = os.getenv("APP_HOST", "127.0.0.1")
    port: int = int(os.getenv("APP_PORT", "8000"))
    reload: bool = _env_flag("APP_RELOAD", os.name != "nt")
    api_base_url: str = os.getenv("API_BASE_URL", "")
    database_path: str = os.getenv("DATABASE_PATH", os.path.join("app_data", "adaptive_learning.db"))
    storage_backend: str = os.getenv("STORAGE_BACKEND", "local")
    storage_root: str = os.getenv("STORAGE_ROOT", os.path.join("app_data", "storage"))
    video_library_manifest_path: str = os.getenv(
        "VIDEO_LIBRARY_MANIFEST_PATH",
        os.path.join("data", "tutor_video_library.json"),
    )
    video_library_media_root: str = os.getenv(
        "VIDEO_LIBRARY_MEDIA_ROOT",
        os.path.join("web", "media", "tutor-videos"),
    )
    token_ttl_hours: int = int(os.getenv("AUTH_TOKEN_TTL_HOURS", "168"))
    frontend_default_exam: str = os.getenv("FRONTEND_DEFAULT_EXAM", "JEE MAIN")
    frontend_default_language: str = os.getenv("FRONTEND_DEFAULT_LANGUAGE", "English")
    frontend_default_tutor_level: int = int(os.getenv("FRONTEND_DEFAULT_TUTOR_LEVEL", "3"))
    frontend_default_tab_order: tuple[str, ...] = tuple(
        _env_list(
            "FRONTEND_DEFAULT_TAB_ORDER",
            ["overview", "tutor", "tutorroom", "practice", "mocktest", "lastminute", "tips", "weekly", "progress", "lounge", "network", "league", "personalize", "guide", "assist"],
        )
    )


settings = Settings()
