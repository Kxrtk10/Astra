import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta

from fastapi import HTTPException

from backend.config import settings
from backend.database import db_cursor


def _timestamp(hours=0):
    return (datetime.utcnow() + timedelta(hours=hours)).isoformat(timespec="seconds")


def hash_password(password):
    salt = os.urandom(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120000)
    return f"{salt.hex()}${derived.hex()}"


def verify_password(password, stored_hash):
    try:
        salt_hex, derived_hex = stored_hash.split("$", 1)
    except ValueError:
        return False
    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(derived_hex)
    computed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120000)
    return hmac.compare_digest(computed, expected)


def _hash_token(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_user(email, password, display_name, student_name):
    created_at = _timestamp()
    password_hash = hash_password(password)
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO users (email, password_hash, display_name, student_name, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (email.strip().lower(), password_hash, display_name.strip(), student_name.strip(), created_at),
        )
        user_id = cursor.lastrowid
    return get_user_by_id(user_id)


def get_user_by_id(user_id):
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT id, email, display_name, student_name, created_at, last_login_at
            FROM users WHERE id = ?
            """,
            (user_id,),
        )
        row = cursor.fetchone()
    return dict(row) if row else None


def get_user_by_email(email):
    with db_cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),))
        row = cursor.fetchone()
    return dict(row) if row else None


def get_user_by_student_name(student_name):
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT id, email, display_name, student_name, created_at, last_login_at
            FROM users WHERE lower(student_name) = lower(?)
            """,
            (student_name.strip(),),
        )
        row = cursor.fetchone()
    return dict(row) if row else None


def issue_session(user_id):
    token = secrets.token_urlsafe(32)
    token_hash = _hash_token(token)
    created_at = _timestamp()
    expires_at = _timestamp(settings.token_ttl_hours)
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO sessions (user_id, token_hash, created_at, expires_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, token_hash, created_at, expires_at),
        )
        cursor.execute(
            """
            UPDATE users SET last_login_at = ? WHERE id = ?
            """,
            (created_at, user_id),
        )
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_at": expires_at,
    }


def authenticate_user(email, password):
    user = get_user_by_email(email)
    if not user or not verify_password(password, user["password_hash"]):
        return None
    return get_user_by_id(user["id"])


def get_user_from_token(token):
    token_hash = _hash_token(token)
    now = datetime.utcnow().isoformat(timespec="seconds")
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT users.id, users.email, users.display_name, users.student_name, users.created_at, users.last_login_at
            FROM sessions
            JOIN users ON users.id = sessions.user_id
            WHERE sessions.token_hash = ? AND sessions.expires_at >= ?
            """,
            (token_hash, now),
        )
        row = cursor.fetchone()
    return dict(row) if row else None


def require_bearer_token(authorization_header):
    if not authorization_header or not authorization_header.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token.")
    token = authorization_header.split(" ", 1)[1].strip()
    user = get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return user


def revoke_session(token):
    token_hash = _hash_token(token)
    with db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))
        return cursor.rowcount > 0
