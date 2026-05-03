import json
import os
import uuid
from datetime import datetime

from backend.config import settings


def _ensure_storage_root():
    os.makedirs(settings.storage_root, exist_ok=True)


def ensure_parent_dir(path):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def atomic_write_json(path, payload):
    ensure_parent_dir(path)
    temp_path = f"{path}.tmp"
    with open(temp_path, "w", encoding="utf-8") as output_file:
        json.dump(payload, output_file, indent=2)
    os.replace(temp_path, path)


def get_storage_status():
    _ensure_storage_root()
    return {
        "backend": settings.storage_backend,
        "root": settings.storage_root,
        "ready": True,
    }


def save_binary_file(content, filename_hint, folder="uploads"):
    _ensure_storage_root()
    target_dir = os.path.join(settings.storage_root, folder)
    os.makedirs(target_dir, exist_ok=True)

    safe_name = os.path.basename(filename_hint or "file.bin")
    extension = os.path.splitext(safe_name)[1] or ".bin"
    generated_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:10]}{extension}"
    filepath = os.path.join(target_dir, generated_name)

    with open(filepath, "wb") as output_file:
        output_file.write(content)

    return {
        "backend": settings.storage_backend,
        "path": filepath,
        "filename": generated_name,
        "folder": folder,
    }
