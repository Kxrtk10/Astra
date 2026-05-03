import os
import sqlite3
from contextlib import contextmanager

from backend.config import settings


def _ensure_db_directory():
    directory = os.path.dirname(settings.database_path)
    if directory:
        os.makedirs(directory, exist_ok=True)


def get_connection():
    _ensure_db_directory()
    connection = sqlite3.connect(settings.database_path)
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def db_cursor(commit=False):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        yield cursor
        if commit:
            connection.commit()
    finally:
        connection.close()


def init_db():
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                display_name TEXT NOT NULL,
                student_name TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL,
                last_login_at TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token_hash TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_sessions_user_id
            ON sessions(user_id)
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS student_profiles (
                student_name TEXT PRIMARY KEY,
                profile_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS student_progress (
                student_name TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                conversation_mode TEXT NOT NULL,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                deleted_at TEXT,
                pinned_at TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_chat_conversations_student_mode_updated
            ON chat_conversations(student_name, conversation_mode, updated_at DESC, id DESC)
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                conversation_id INTEGER,
                conversation_mode TEXT NOT NULL,
                role TEXT NOT NULL,
                message_text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_chat_messages_student_mode
            ON chat_messages(student_name, conversation_mode, id)
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS student_behavior (
                student_name TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS student_planner (
                student_name TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS student_analytics (
                student_name TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS student_memory (
                student_name TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS student_syllabus_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                title TEXT NOT NULL,
                source_type TEXT NOT NULL,
                file_name TEXT,
                stored_path TEXT,
                extracted_text TEXT NOT NULL,
                topic_summary TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_student_syllabus_documents_student
            ON student_syllabus_documents(student_name, id)
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS student_chat_outcomes (
                student_name TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        cursor.execute("PRAGMA table_info(chat_messages)")
        chat_message_columns = {row[1] for row in cursor.fetchall()}
        if "conversation_id" not in chat_message_columns:
            cursor.execute("ALTER TABLE chat_messages ADD COLUMN conversation_id INTEGER")
        cursor.execute("PRAGMA table_info(chat_conversations)")
        chat_conversation_columns = {row[1] for row in cursor.fetchall()}
        if "deleted_at" not in chat_conversation_columns:
            cursor.execute("ALTER TABLE chat_conversations ADD COLUMN deleted_at TEXT")
        if "pinned_at" not in chat_conversation_columns:
            cursor.execute("ALTER TABLE chat_conversations ADD COLUMN pinned_at TEXT")
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_chat_messages_conversation
            ON chat_messages(student_name, conversation_id, id)
            """
        )


def fetch_json_record(table_name, key_column, key_value, json_column):
    query = f"SELECT {json_column} FROM {table_name} WHERE {key_column} = ?"
    with db_cursor() as cursor:
        cursor.execute(query, (key_value,))
        row = cursor.fetchone()
    return row[json_column] if row else None


def upsert_json_record(table_name, key_column, key_value, json_column, json_value, updated_at):
    query = f"""
        INSERT INTO {table_name} ({key_column}, {json_column}, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT({key_column}) DO UPDATE SET
            {json_column} = excluded.{json_column},
            updated_at = excluded.updated_at
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(query, (key_value, json_value, updated_at))
