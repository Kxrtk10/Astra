import json
import os
import sqlite3
import threading
from contextlib import contextmanager

from backend.config import settings

_local = threading.local()
_write_lock = threading.Lock()


def _ensure_db_directory():
    directory = os.path.dirname(settings.database_path)
    if directory:
        os.makedirs(directory, exist_ok=True)


def get_db_connection():
    _ensure_db_directory()
    if not hasattr(_local, "conn") or _local.conn is None:
        _local.conn = sqlite3.connect(settings.database_path, check_same_thread=False)
        _local.conn.row_factory = sqlite3.Row
        try:
            _local.conn.execute("PRAGMA foreign_keys = ON")
        except Exception:
            pass
    return _local.conn


def get_connection():
    return get_db_connection()


def execute_query(query, params=(), fetchone=False):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        statement = str(query or "").strip().lower()
        if statement.startswith(("insert", "update", "delete", "replace", "alter", "create", "drop")):
            connection.commit()
            return cursor.lastrowid
        if statement.startswith("select"):
            return cursor.fetchone() if fetchone else cursor.fetchall()
        connection.commit()
        return cursor.rowcount
    except Exception as exc:
        print(f"ERROR: Database query failed: {exc}")
        try:
            get_db_connection().rollback()
        except Exception:
            pass
        return None


def safe_write(query, params=()):
    with _write_lock:
        return execute_query(query, params)


@contextmanager
def db_cursor(commit=False):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        yield cursor
        if commit:
            connection.commit()
    except Exception:
        try:
            connection.rollback()
        except Exception:
            pass
        raise
    finally:
        pass


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

        cursor.execute("PRAGMA table_info(student_profiles)")
        student_profile_columns = {row[1] for row in cursor.fetchall()}
        if student_profile_columns and ("student_id" not in student_profile_columns or "profile_data" not in student_profile_columns):
            cursor.execute("ALTER TABLE student_profiles RENAME TO student_profiles_legacy")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS student_profiles (
                student_id TEXT PRIMARY KEY,
                profile_data TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                learning_phase TEXT DEFAULT 'phase1_coverage',
                phase2_cycle INTEGER DEFAULT 1,
                phase1_completed_at TIMESTAMP
            )
            """
        )
        cursor.execute("PRAGMA table_info(student_profiles)")
        student_profile_columns = {row[1] for row in cursor.fetchall()}
        if "learning_phase" not in student_profile_columns:
            cursor.execute("ALTER TABLE student_profiles ADD COLUMN learning_phase TEXT DEFAULT 'phase1_coverage'")
        if "phase2_cycle" not in student_profile_columns:
            cursor.execute("ALTER TABLE student_profiles ADD COLUMN phase2_cycle INTEGER DEFAULT 1")
        if "phase1_completed_at" not in student_profile_columns:
            cursor.execute("ALTER TABLE student_profiles ADD COLUMN phase1_completed_at TIMESTAMP")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS planner_state (
                student_id TEXT PRIMARY KEY,
                journey_data TEXT,
                weekly_data TEXT,
                today_data TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chapter_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                unit_name TEXT,
                subject TEXT,
                session_data TEXT,
                status TEXT,
                started_at TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS progress_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                topic TEXT,
                subject TEXT,
                unit_name TEXT,
                session_type TEXT,
                score INTEGER,
                duration_minutes INTEGER,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chapter_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                unit_name TEXT,
                subject TEXT,
                subtopic_scores TEXT,
                chapter_test_score INTEGER,
                mastery_level TEXT,
                attempts INTEGER DEFAULT 1,
                time_spent_minutes INTEGER,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                conversation_mode TEXT,
                conversation_id TEXT,
                messages TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS analytics_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                event_type TEXT,
                event_data TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS confusion_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                topic TEXT,
                unit TEXT,
                confusion_type TEXT,
                missing_prerequisite TEXT,
                recovery_action TEXT,
                session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS mock_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                exam_type TEXT,
                total_score INTEGER,
                max_score INTEGER,
                percentage REAL,
                physics_score INTEGER,
                chemistry_score INTEGER,
                maths_score INTEGER,
                time_taken INTEGER,
                analysis TEXT,
                taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge_base_docs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT,
                source_name TEXT,
                chunk_index INTEGER,
                content TEXT,
                embedding TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS group_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                subject TEXT,
                exam TEXT,
                pace_band TEXT NOT NULL,
                scheduled_time TEXT,
                status TEXT NOT NULL DEFAULT 'scheduled' CHECK(status IN ('scheduled', 'live', 'ended')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS group_session_members (
                session_id INTEGER NOT NULL,
                user_id TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'in_main' CHECK(status IN ('in_main', 'in_breakout', 'left')),
                joined_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (session_id, user_id),
                FOREIGN KEY(session_id) REFERENCES group_sessions(id) ON DELETE CASCADE
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS group_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                channel TEXT NOT NULL CHECK(channel IN ('main', 'breakout')),
                breakout_owner_id TEXT,
                sender_type TEXT NOT NULL CHECK(sender_type IN ('tutor', 'student')),
                sender_id TEXT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(session_id) REFERENCES group_sessions(id) ON DELETE CASCADE
            )
            """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_group_sessions_match
            ON group_sessions(topic, subject, exam, pace_band, status, scheduled_time)
            """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_group_members_user
            ON group_session_members(user_id, status, session_id)
            """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_group_messages_session_channel
            ON group_messages(session_id, channel, breakout_owner_id, id)
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
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_progress_records_student_topic
            ON progress_records(student_id, topic, recorded_at DESC)
            """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_chapter_scores_student
            ON chapter_scores(student_id, unit_name, completed_at DESC)
            """
        )


def _json_loads_safe(raw, fallback=None):
    try:
        return json.loads(raw) if raw else (fallback if fallback is not None else {})
    except Exception:
        return fallback if fallback is not None else {}


def _legacy_json_candidates(student_id, folder_name):
    safe = str(student_id or "").strip()
    if not safe:
        return []
    return [
        os.path.join(folder_name, f"{safe}.json"),
        os.path.join("app_data", folder_name, f"{safe}.json"),
    ]


def _first_existing_path(paths):
    for path in paths:
        if path and os.path.exists(path):
            return path
    return None


def get_student_profile(student_id):
    try:
        row = execute_query(
            "SELECT profile_data FROM student_profiles WHERE student_id = ?",
            (student_id,),
            fetchone=True,
        )
        if row:
            profile = _json_loads_safe(row["profile_data"], {})
            if profile:
                return profile
        legacy_path = _first_existing_path(_legacy_json_candidates(student_id, "profiles"))
        if legacy_path:
            with open(legacy_path, "r", encoding="utf-8-sig") as file:
                profile = _json_loads_safe(file.read(), {})
            if profile:
                save_student_profile(student_id, profile)
                return profile
    except Exception as exc:
        print(f"WARNING: Could not load student profile for {student_id}: {exc}")
    return {}


def save_student_profile(student_id, profile_data):
    try:
        student_name = str((profile_data or {}).get("name") or student_id).strip() or str(student_id or "").strip()
        safe_write(
            """
            INSERT OR IGNORE INTO students (student_id, name, created_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            """,
            (student_id, student_name),
        )
        payload = json.dumps(profile_data or {}, indent=2)
        safe_write(
            """
            UPDATE students
            SET name = ?, last_active = CURRENT_TIMESTAMP
            WHERE student_id = ?
            """,
            (student_name, student_id),
        )
        safe_write(
            """
            INSERT INTO student_profiles (student_id, profile_data, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(student_id) DO UPDATE SET
                profile_data = excluded.profile_data,
                updated_at = CURRENT_TIMESTAMP
            """,
            (student_id, payload),
        )
        return profile_data
    except Exception as exc:
        print(f"WARNING: Could not save student profile for {student_id}: {exc}")
        return profile_data


def get_learning_phase(student_id):
    try:
        row = execute_query(
            """
            SELECT learning_phase, phase2_cycle
            FROM student_profiles
            WHERE student_id = ?
            """,
            (student_id,),
            fetchone=True,
        )
        if not row:
            return {"phase": "phase1_coverage", "cycle": 1}
        return {
            "phase": row["learning_phase"] or "phase1_coverage",
            "cycle": int(row["phase2_cycle"] or 1),
        }
    except Exception as exc:
        print(f"WARNING: Could not load learning phase for {student_id}: {exc}")
        return {"phase": "phase1_coverage", "cycle": 1}


def set_learning_phase(student_id, phase, cycle=1):
    try:
        phase = str(phase or "phase1_coverage").strip() or "phase1_coverage"
        cycle = max(1, int(cycle or 1))
        safe_write(
            """
            INSERT OR IGNORE INTO student_profiles (
                student_id, profile_data, updated_at, learning_phase, phase2_cycle
            )
            VALUES (?, ?, CURRENT_TIMESTAMP, 'phase1_coverage', 1)
            """,
            (student_id, "{}"),
        )
        if phase == "phase2_revision":
            safe_write(
                """
                UPDATE student_profiles
                SET learning_phase = ?,
                    phase2_cycle = ?,
                    phase1_completed_at = COALESCE(phase1_completed_at, CURRENT_TIMESTAMP),
                    updated_at = CURRENT_TIMESTAMP
                WHERE student_id = ?
                """,
                (phase, cycle, student_id),
            )
        else:
            safe_write(
                """
                UPDATE student_profiles
                SET learning_phase = ?,
                    phase2_cycle = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE student_id = ?
                """,
                (phase, cycle, student_id),
            )
        return get_learning_phase(student_id)
    except Exception as exc:
        print(f"WARNING: Could not set learning phase for {student_id}: {exc}")
        return {"phase": "phase1_coverage", "cycle": 1}


def get_planner_state(student_id):
    try:
        row = execute_query(
            "SELECT journey_data, weekly_data, today_data FROM planner_state WHERE student_id = ?",
            (student_id,),
            fetchone=True,
        )
        if row:
            return {
                "journey": _json_loads_safe(row["journey_data"], {}),
                "weekly": _json_loads_safe(row["weekly_data"], {}),
                "today": _json_loads_safe(row["today_data"], {}),
            }
        legacy_path = _first_existing_path(_legacy_json_candidates(student_id, "planner"))
        if legacy_path:
            with open(legacy_path, "r", encoding="utf-8-sig") as file:
                payload = _json_loads_safe(file.read(), {})
            if isinstance(payload, dict):
                save_planner_state(student_id, payload.get("journey", {}), payload.get("weekly", {}), payload.get("today", {}))
                return {
                    "journey": payload.get("journey", {}),
                    "weekly": payload.get("weekly", {}),
                    "today": payload.get("today", {}),
                }
    except Exception as exc:
        print(f"WARNING: Could not load planner state for {student_id}: {exc}")
    return {"journey": {}, "weekly": {}, "today": {}}


def save_planner_state(student_id, journey, weekly, today):
    try:
        safe_write(
            """
            INSERT INTO planner_state (student_id, journey_data, weekly_data, today_data, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(student_id) DO UPDATE SET
                journey_data = excluded.journey_data,
                weekly_data = excluded.weekly_data,
                today_data = excluded.today_data,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                student_id,
                json.dumps(journey or {}, indent=2),
                json.dumps(weekly or {}, indent=2),
                json.dumps(today or {}, indent=2),
            ),
        )
    except Exception as exc:
        print(f"WARNING: Could not save planner state for {student_id}: {exc}")


def get_active_chapter_session(student_id):
    try:
        row = execute_query(
            """
            SELECT unit_name, subject, session_data, status, started_at, updated_at
            FROM chapter_sessions
            WHERE student_id = ? AND status = 'in_progress'
            ORDER BY updated_at DESC, id DESC
            LIMIT 1
            """,
            (student_id,),
            fetchone=True,
        )
        if row:
            session = _json_loads_safe(row["session_data"], {})
            if isinstance(session, dict):
                session.setdefault("unit_name", row["unit_name"] or "")
                session.setdefault("subject", row["subject"] or "")
                session.setdefault("status", row["status"] or "in_progress")
                return session
    except Exception as exc:
        print(f"WARNING: Could not load active chapter session for {student_id}: {exc}")
    return {}


def save_chapter_session(student_id, unit_name, subject, session_data, status):
    try:
        safe_write(
            """
            INSERT OR REPLACE INTO chapter_sessions (id, student_id, unit_name, subject, session_data, status, started_at, updated_at)
            VALUES (
                COALESCE(
                    (SELECT id FROM chapter_sessions WHERE student_id = ? AND unit_name = ? AND subject = ?),
                    NULL
                ),
                ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
            )
            """,
            (
                student_id,
                unit_name,
                subject,
                student_id,
                unit_name,
                subject,
                json.dumps(session_data or {}, indent=2),
                status,
            ),
        )
        return session_data
    except Exception as exc:
        print(f"WARNING: Could not save chapter session for {student_id}: {exc}")
        return session_data


def log_progress_record(student_id, topic, subject, unit_name, session_type, score, duration_minutes):
    try:
        safe_write(
            """
            INSERT INTO progress_records (student_id, topic, subject, unit_name, session_type, score, duration_minutes, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (
                student_id,
                str(topic or "").strip(),
                str(subject or "").strip(),
                str(unit_name or "").strip(),
                str(session_type or "").strip(),
                int(score or 0),
                int(duration_minutes or 0),
            ),
        )
    except Exception as exc:
        print(f"WARNING: Could not log progress record for {student_id}: {exc}")


def get_student_progress_summary(student_id):
    try:
        rows = execute_query(
            "SELECT topic, subject, score FROM progress_records WHERE student_id = ? ORDER BY recorded_at DESC, id DESC",
            (student_id,),
        ) or []
        summary = {
            "average_score_per_subject": {},
            "topics_attempted": [],
            "strong_topics": [],
            "weak_topics": [],
            "attempt_count": 0,
        }
        if not rows:
            return summary
        subject_buckets = {}
        attempted = []
        strong = []
        weak = []
        for row in rows:
            topic = str(row["topic"] or "").strip()
            subject = str(row["subject"] or "General").strip() or "General"
            score = float(row["score"] or 0)
            attempted.append(topic)
            bucket = subject_buckets.setdefault(subject, {"total": 0.0, "count": 0})
            bucket["total"] += score
            bucket["count"] += 1
            if score >= 80 and topic:
                strong.append(topic)
            if score < 60 and topic:
                weak.append(topic)
        summary["average_score_per_subject"] = {
            subject: round(bucket["total"] / bucket["count"], 1) if bucket["count"] else 0
            for subject, bucket in subject_buckets.items()
        }
        summary["topics_attempted"] = list(dict.fromkeys(attempted))
        summary["strong_topics"] = list(dict.fromkeys(strong))
        summary["weak_topics"] = list(dict.fromkeys(weak))
        summary["attempt_count"] = len(rows)
        return summary
    except Exception as exc:
        print(f"WARNING: Could not load progress summary for {student_id}: {exc}")
        return {
            "average_score_per_subject": {},
            "topics_attempted": [],
            "strong_topics": [],
            "weak_topics": [],
            "attempt_count": 0,
        }


def save_chapter_score(student_id, unit_name, subject, subtopic_scores, chapter_test_score, mastery_level, time_spent_minutes):
    try:
        safe_write(
            """
            INSERT OR REPLACE INTO chapter_scores (id, student_id, unit_name, subject, subtopic_scores, chapter_test_score, mastery_level, attempts, time_spent_minutes, completed_at)
            VALUES (
                COALESCE(
                    (SELECT id FROM chapter_scores WHERE student_id = ? AND unit_name = ? AND subject = ?),
                    NULL
                ),
                ?, ?, ?, ?, ?, ?, 1, ?, CURRENT_TIMESTAMP
            )
            """,
            (
                student_id,
                unit_name,
                subject,
                student_id,
                str(unit_name or "").strip(),
                str(subject or "").strip(),
                json.dumps(subtopic_scores or {}, indent=2),
                int(chapter_test_score or 0),
                str(mastery_level or "developing").strip(),
                int(time_spent_minutes or 0),
            ),
        )
    except Exception as exc:
        print(f"WARNING: Could not save chapter score for {student_id}: {exc}")


def get_all_chapter_scores(student_id):
    try:
        rows = execute_query(
            """
            SELECT unit_name, subject, subtopic_scores, chapter_test_score, mastery_level, attempts, time_spent_minutes, completed_at
            FROM chapter_scores
            WHERE student_id = ?
            ORDER BY completed_at DESC, id DESC
            """,
            (student_id,),
        ) or []
        results = []
        for row in rows:
            results.append(
                {
                    "unit_name": row["unit_name"],
                    "subject": row["subject"],
                    "subtopic_scores": _json_loads_safe(row["subtopic_scores"], {}),
                    "chapter_test_score": row["chapter_test_score"],
                    "mastery_level": row["mastery_level"],
                    "attempts": row["attempts"],
                    "time_spent_minutes": row["time_spent_minutes"],
                    "completed_at": row["completed_at"],
                }
            )
        return results
    except Exception as exc:
        print(f"WARNING: Could not load chapter scores for {student_id}: {exc}")
        return []


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


def _row_to_dict(row):
    if not row:
        return {}
    return {key: row[key] for key in row.keys()}


def _rows_to_dicts(rows):
    return [_row_to_dict(row) for row in (rows or [])]


def list_student_ids(limit=200):
    try:
        rows = execute_query(
            """
            SELECT student_id FROM student_profiles
            UNION
            SELECT student_id FROM students
            ORDER BY student_id
            LIMIT ?
            """,
            (int(limit or 200),),
        )
        return [str(row["student_id"] or "").strip() for row in (rows or []) if str(row["student_id"] or "").strip()]
    except Exception as exc:
        print(f"WARNING: Could not list student ids: {exc}")
        return []


def get_group_session(session_id):
    try:
        row = execute_query(
            "SELECT * FROM group_sessions WHERE id = ?",
            (int(session_id),),
            fetchone=True,
        )
        return _row_to_dict(row)
    except Exception as exc:
        print(f"WARNING: Could not load group session {session_id}: {exc}")
        return {}


def list_group_session_members(session_id):
    try:
        rows = execute_query(
            """
            SELECT session_id, user_id, status, joined_at
            FROM group_session_members
            WHERE session_id = ? AND status != 'left'
            ORDER BY joined_at, user_id
            """,
            (int(session_id),),
        )
        return _rows_to_dicts(rows)
    except Exception as exc:
        print(f"WARNING: Could not list group members for {session_id}: {exc}")
        return []


def get_active_group_session_for_user(user_id):
    try:
        row = execute_query(
            """
            SELECT gs.*
            FROM group_sessions gs
            JOIN group_session_members gsm ON gsm.session_id = gs.id
            WHERE gsm.user_id = ?
              AND gsm.status != 'left'
              AND gs.status IN ('scheduled', 'live')
            ORDER BY gs.created_at DESC, gs.id DESC
            LIMIT 1
            """,
            (str(user_id or "").strip(),),
            fetchone=True,
        )
        return _row_to_dict(row)
    except Exception as exc:
        print(f"WARNING: Could not load active group session for {user_id}: {exc}")
        return {}


def find_open_group_session(topic, subject, exam, pace_band):
    try:
        row = execute_query(
            """
            SELECT gs.*
            FROM group_sessions gs
            LEFT JOIN group_session_members gsm
              ON gsm.session_id = gs.id AND gsm.status != 'left'
            WHERE lower(gs.topic) = lower(?)
              AND lower(COALESCE(gs.subject, '')) = lower(?)
              AND lower(COALESCE(gs.exam, '')) = lower(?)
              AND gs.pace_band = ?
              AND gs.status = 'scheduled'
            GROUP BY gs.id
            HAVING COUNT(gsm.user_id) < 3
            ORDER BY gs.created_at ASC, gs.id ASC
            LIMIT 1
            """,
            (
                str(topic or "").strip(),
                str(subject or "").strip(),
                str(exam or "").strip(),
                str(pace_band or "steady").strip().lower() or "steady",
            ),
            fetchone=True,
        )
        return _row_to_dict(row)
    except Exception as exc:
        print(f"WARNING: Could not find open group session: {exc}")
        return {}


def create_group_session(topic, subject, exam, pace_band, scheduled_time=""):
    try:
        with _write_lock:
            with db_cursor(commit=True) as cursor:
                cursor.execute(
                    """
                    INSERT INTO group_sessions (topic, subject, exam, pace_band, scheduled_time, status, created_at)
                    VALUES (?, ?, ?, ?, ?, 'scheduled', CURRENT_TIMESTAMP)
                    """,
                    (
                        str(topic or "").strip(),
                        str(subject or "").strip(),
                        str(exam or "").strip(),
                        str(pace_band or "steady").strip().lower() or "steady",
                        str(scheduled_time or "").strip(),
                    ),
                )
                return cursor.lastrowid
    except Exception as exc:
        print(f"WARNING: Could not create group session: {exc}")
        return None


def add_group_session_member(session_id, user_id, status="in_main"):
    try:
        with _write_lock:
            with db_cursor(commit=True) as cursor:
                cursor.execute(
                    """
                    INSERT INTO group_session_members (session_id, user_id, status, joined_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(session_id, user_id) DO UPDATE SET
                        status = excluded.status
                    """,
                    (int(session_id), str(user_id or "").strip(), str(status or "in_main").strip() or "in_main"),
                )
                cursor.execute(
                    """
                    UPDATE group_sessions
                    SET status = CASE (
                        SELECT COUNT(*) FROM group_session_members
                        WHERE session_id = ? AND status != 'left'
                    ) WHEN 3 THEN 'live' ELSE status END
                    WHERE id = ? AND status = 'scheduled'
                    """,
                    (int(session_id), int(session_id)),
                )
        return True
    except Exception as exc:
        print(f"WARNING: Could not add group session member: {exc}")
        return False


def update_group_member_status(session_id, user_id, status):
    try:
        safe_write(
            """
            UPDATE group_session_members
            SET status = ?
            WHERE session_id = ? AND user_id = ?
            """,
            (str(status or "in_main").strip(), int(session_id), str(user_id or "").strip()),
        )
        return True
    except Exception as exc:
        print(f"WARNING: Could not update group member status: {exc}")
        return False


def add_group_message(session_id, channel, sender_type, content, sender_id=None, breakout_owner_id=None):
    try:
        with _write_lock:
            with db_cursor(commit=True) as cursor:
                cursor.execute(
                    """
                    INSERT INTO group_messages (session_id, channel, breakout_owner_id, sender_type, sender_id, content, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """,
                    (
                        int(session_id),
                        str(channel or "main").strip().lower() or "main",
                        str(breakout_owner_id).strip() if breakout_owner_id is not None else None,
                        str(sender_type or "student").strip().lower() or "student",
                        str(sender_id).strip() if sender_id is not None else None,
                        str(content or "").strip(),
                    ),
                )
                return cursor.lastrowid
    except Exception as exc:
        print(f"WARNING: Could not add group message: {exc}")
        return None


def list_group_messages(session_id, channel="main", breakout_owner_id=None, since_id=None, since_created_at=None, limit=160):
    try:
        params = [int(session_id), str(channel or "main").strip().lower() or "main"]
        query = """
            SELECT id, session_id, channel, breakout_owner_id, sender_type, sender_id, content, created_at
            FROM group_messages
            WHERE session_id = ? AND channel = ?
        """
        if breakout_owner_id is not None:
            query += " AND breakout_owner_id = ?"
            params.append(str(breakout_owner_id).strip())
        elif str(channel or "main").strip().lower() == "breakout":
            query += " AND breakout_owner_id IS NULL"
        if since_id:
            query += " AND id > ?"
            params.append(int(since_id))
        if since_created_at:
            query += " AND created_at > ?"
            params.append(str(since_created_at))
        query += " ORDER BY id ASC LIMIT ?"
        params.append(max(1, min(int(limit or 160), 300)))
        return _rows_to_dicts(execute_query(query, tuple(params)))
    except Exception as exc:
        print(f"WARNING: Could not list group messages: {exc}")
        return []

