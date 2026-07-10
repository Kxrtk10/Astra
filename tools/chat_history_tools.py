from datetime import datetime

from backend.database import db_cursor


def _timestamp():
    return datetime.utcnow().isoformat(timespec="seconds")


def _clean_text(value):
    return str(value or "").strip()


def _build_title(seed_text):
    clean = " ".join(_clean_text(seed_text).split())
    if not clean:
        return "New chat"
    return clean[:72]


def _adopt_legacy_messages(student_name, conversation_mode):
    clean_name = _clean_text(student_name)
    clean_mode = _clean_text(conversation_mode or "tutor")
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            SELECT id
            FROM chat_conversations
            WHERE student_name = ? AND conversation_mode = ?
            LIMIT 1
            """,
            (clean_name, clean_mode),
        )
        existing = cursor.fetchone()
        cursor.execute(
            """
            SELECT COUNT(*) AS message_count
            FROM chat_messages
            WHERE student_name = ? AND conversation_mode = ? AND conversation_id IS NULL
            """,
            (clean_name, clean_mode),
        )
        orphan_count = cursor.fetchone()["message_count"]
        if existing or not orphan_count:
            return

        now = _timestamp()
        cursor.execute(
            """
            INSERT INTO chat_conversations (student_name, conversation_mode, title, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (clean_name, clean_mode, "Imported chat", now, now),
        )
        conversation_id = cursor.lastrowid
        cursor.execute(
            """
            UPDATE chat_messages
            SET conversation_id = ?
            WHERE student_name = ? AND conversation_mode = ? AND conversation_id IS NULL
            """,
            (conversation_id, clean_name, clean_mode),
        )


def list_conversations(student_name, conversation_mode, limit=30, query_text=""):
    clean_name = _clean_text(student_name)
    clean_mode = _clean_text(conversation_mode or "tutor")
    clean_query = _clean_text(query_text)
    if not clean_name:
        return []
    _adopt_legacy_messages(clean_name, clean_mode)

    with db_cursor() as cursor:
        if clean_query:
            cursor.execute(
                """
                SELECT id, student_name, conversation_mode, title, created_at, updated_at, pinned_at
                FROM chat_conversations
                WHERE student_name = ? AND conversation_mode = ? AND deleted_at IS NULL AND title LIKE ?
                ORDER BY (pinned_at IS NOT NULL) DESC, pinned_at DESC, updated_at DESC, id DESC
                LIMIT ?
                """,
                (clean_name, clean_mode, f"%{clean_query}%", int(limit)),
            )
        else:
            cursor.execute(
                """
                SELECT id, student_name, conversation_mode, title, created_at, updated_at, pinned_at
                FROM chat_conversations
                WHERE student_name = ? AND conversation_mode = ? AND deleted_at IS NULL
                ORDER BY (pinned_at IS NOT NULL) DESC, pinned_at DESC, updated_at DESC, id DESC
                LIMIT ?
                """,
                (clean_name, clean_mode, int(limit)),
            )
        rows = cursor.fetchall()
    return [dict(row) for row in rows]


def list_deleted_conversations(student_name, conversation_mode, limit=20):
    clean_name = _clean_text(student_name)
    clean_mode = _clean_text(conversation_mode or "tutor")
    if not clean_name:
        return []

    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT id, student_name, conversation_mode, title, created_at, updated_at, deleted_at, pinned_at
            FROM chat_conversations
            WHERE student_name = ? AND conversation_mode = ? AND deleted_at IS NOT NULL
            ORDER BY deleted_at DESC, id DESC
            LIMIT ?
            """,
            (clean_name, clean_mode, int(limit)),
        )
        rows = cursor.fetchall()
    return [dict(row) for row in rows]


def create_conversation(student_name, conversation_mode, title="New chat"):
    clean_name = _clean_text(student_name)
    clean_mode = _clean_text(conversation_mode or "tutor")
    clean_title = _build_title(title)
    now = _timestamp()
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO chat_conversations (student_name, conversation_mode, title, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (clean_name, clean_mode, clean_title, now, now),
        )
        conversation_id = cursor.lastrowid
    return {
        "id": conversation_id,
        "student_name": clean_name,
        "conversation_mode": clean_mode,
        "title": clean_title,
        "created_at": now,
        "updated_at": now,
    }


def get_conversation(student_name, conversation_mode, conversation_id):
    clean_name = _clean_text(student_name)
    clean_mode = _clean_text(conversation_mode or "tutor")
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT id, student_name, conversation_mode, title, created_at, updated_at
            FROM chat_conversations
            WHERE student_name = ? AND conversation_mode = ? AND id = ?
            """,
            (clean_name, clean_mode, int(conversation_id)),
        )
        row = cursor.fetchone()
    return dict(row) if row else None


def resolve_conversation_id(student_name, conversation_mode, conversation_id=None, seed_title="New chat"):
    clean_name = _clean_text(student_name)
    clean_mode = _clean_text(conversation_mode or "tutor")
    _adopt_legacy_messages(clean_name, clean_mode)
    if conversation_id:
        existing = get_conversation(clean_name, clean_mode, conversation_id)
        if existing:
            return existing["id"]

    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT id
            FROM chat_conversations
            WHERE student_name = ? AND conversation_mode = ? AND deleted_at IS NULL
            ORDER BY updated_at DESC, id DESC
            LIMIT 1
            """,
            (clean_name, clean_mode),
        )
        row = cursor.fetchone()
    if row:
        return row["id"]
    return create_conversation(clean_name, clean_mode, seed_title)["id"]


def save_chat_message(student_name, conversation_mode, role, message_text, conversation_id=None):
    clean_name = _clean_text(student_name)
    clean_mode = _clean_text(conversation_mode or "tutor")
    clean_role = _clean_text(role or "tutor")
    clean_text = _clean_text(message_text)
    if not clean_name or not clean_text:
        return None

    resolved_conversation_id = resolve_conversation_id(
        clean_name,
        clean_mode,
        conversation_id=conversation_id,
        seed_title=clean_text if clean_role == "student" else "New chat",
    )
    now = _timestamp()
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO chat_messages (student_name, conversation_id, conversation_mode, role, message_text, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (clean_name, resolved_conversation_id, clean_mode, clean_role, clean_text, now),
        )
        next_title = _conversation_title_from_messages(cursor, resolved_conversation_id)
        cursor.execute(
            """
            UPDATE chat_conversations
            SET updated_at = ?,
                title = CASE
                    WHEN (? = 'student') AND lower(trim(title)) = 'new chat' THEN ?
                    ELSE title
                END
            WHERE id = ?
            """,
            (now, clean_role, next_title, resolved_conversation_id),
        )
    return resolved_conversation_id


def _conversation_title_from_messages(cursor, conversation_id):
    cursor.execute(
        """
        SELECT message_text
        FROM chat_messages
        WHERE conversation_id = ? AND role = 'student'
        ORDER BY id ASC
        LIMIT 3
        """,
        (int(conversation_id),),
    )
    student_messages = [row["message_text"] for row in cursor.fetchall() if _clean_text(row["message_text"])]
    if not student_messages:
        return "New chat"
    if len(student_messages) == 1:
        return _build_title(student_messages[0])
    combined = " | ".join(student_messages[:2])
    return _build_title(combined)


def get_chat_history(student_name, conversation_mode=None, conversation_id=None, limit=120):
    clean_name = _clean_text(student_name)
    clean_mode = _clean_text(conversation_mode or "")
    if not clean_name:
        return []
    if clean_mode:
        _adopt_legacy_messages(clean_name, clean_mode)

    params = [clean_name]
    query = """
        SELECT id, conversation_id, student_name, conversation_mode, role, message_text, created_at
        FROM chat_messages
        WHERE student_name = ?
    """
    if conversation_id:
        query += " AND conversation_id = ?"
        params.append(int(conversation_id))
    elif clean_mode:
        query += " AND conversation_mode = ?"
        params.append(clean_mode)
    query += " ORDER BY id DESC LIMIT ?"
    params.append(int(limit))

    with db_cursor() as cursor:
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
    return [dict(row) for row in reversed(rows)]


def delete_chat_history(student_name, conversation_mode=None, conversation_id=None):
    clean_name = _clean_text(student_name)
    clean_mode = _clean_text(conversation_mode or "")
    if not clean_name:
        return 0

    with db_cursor(commit=True) as cursor:
        if conversation_id:
            now = _timestamp()
            cursor.execute(
                """
                UPDATE chat_conversations
                SET deleted_at = ?
                WHERE student_name = ? AND id = ?
                """,
                (now, clean_name, int(conversation_id)),
            )
            return cursor.rowcount or 0
        if clean_mode:
            cursor.execute(
                """
                DELETE FROM chat_messages
                WHERE student_name = ? AND conversation_mode = ?
                """,
                (clean_name, clean_mode),
            )
            deleted_messages = cursor.rowcount or 0
            cursor.execute(
                """
                DELETE FROM chat_conversations
                WHERE student_name = ? AND conversation_mode = ?
                """,
                (clean_name, clean_mode),
            )
            return deleted_messages
        cursor.execute(
            """
            DELETE FROM chat_messages
            WHERE student_name = ?
            """,
            (clean_name,),
        )
        deleted_messages = cursor.rowcount or 0
        cursor.execute(
            """
            DELETE FROM chat_conversations
            WHERE student_name = ?
            """,
            (clean_name,),
        )
        return deleted_messages


def restore_conversation(student_name, conversation_mode, conversation_id):
    clean_name = _clean_text(student_name)
    clean_mode = _clean_text(conversation_mode or "tutor")
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            UPDATE chat_conversations
            SET deleted_at = NULL,
                updated_at = ?
            WHERE student_name = ? AND conversation_mode = ? AND id = ?
            """,
            (_timestamp(), clean_name, clean_mode, int(conversation_id)),
        )
        return cursor.rowcount or 0


def update_conversation_metadata(student_name, conversation_mode, conversation_id, title=None, pinned=None):
    clean_name = _clean_text(student_name)
    clean_mode = _clean_text(conversation_mode or "tutor")
    clean_title = _build_title(title) if title is not None else None
    now = _timestamp()
    with db_cursor(commit=True) as cursor:
        if clean_title is not None and pinned is not None:
            cursor.execute(
                """
                UPDATE chat_conversations
                SET title = ?, pinned_at = ?, updated_at = ?
                WHERE student_name = ? AND conversation_mode = ? AND id = ?
                """,
                (clean_title, now if pinned else None, now, clean_name, clean_mode, int(conversation_id)),
            )
        elif clean_title is not None:
            cursor.execute(
                """
                UPDATE chat_conversations
                SET title = ?, updated_at = ?
                WHERE student_name = ? AND conversation_mode = ? AND id = ?
                """,
                (clean_title, now, clean_name, clean_mode, int(conversation_id)),
            )
        elif pinned is not None:
            cursor.execute(
                """
                UPDATE chat_conversations
                SET pinned_at = ?, updated_at = ?
                WHERE student_name = ? AND conversation_mode = ? AND id = ?
                """,
                (now if pinned else None, now, clean_name, clean_mode, int(conversation_id)),
            )
        return cursor.rowcount or 0


def get_chat_counts(student_name):
    clean_name = _clean_text(student_name)
    counts = {}
    total = 0
    if not clean_name:
        return {"total": 0, "by_mode": counts}

    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT conversation_mode, COUNT(*) AS message_count
            FROM chat_messages
            WHERE student_name = ?
            GROUP BY conversation_mode
            """,
            (clean_name,),
        )
        rows = cursor.fetchall()

    for row in rows:
        counts[row["conversation_mode"]] = row["message_count"]
        total += row["message_count"]
    return {"total": total, "by_mode": counts}
