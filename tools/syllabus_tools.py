import base64
import os
import re
import zipfile
from datetime import datetime
from io import BytesIO

from backend.database import db_cursor
from backend.storage import save_binary_file

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover - optional dependency fallback
    PdfReader = None


def _timestamp():
    return datetime.utcnow().isoformat(timespec="seconds")


def _clean_text(text):
    text = str(text or "")
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _truncate(text, limit=8000):
    clean = _clean_text(text)
    return clean[:limit]


def _tokenize(text):
    return re.findall(r"[a-z0-9]+", _clean_text(text).lower())


def _chunk_text(text, chunk_size=900, overlap=180):
    clean = _clean_text(text)
    if not clean:
        return []

    chunks = []
    start = 0
    text_length = len(clean)
    while start < text_length:
        end = min(text_length, start + chunk_size)
        chunk = clean[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= text_length:
            break
        start = max(end - overlap, start + 1)
    return chunks


def _score_chunk(query_text, chunk_text, title=""):
    query_tokens = set(_tokenize(query_text))
    if not query_tokens:
        return 0.0

    chunk_tokens = set(_tokenize(chunk_text))
    title_tokens = set(_tokenize(title))
    score = 0.0
    score += len(query_tokens & chunk_tokens) * 1.6
    score += len(query_tokens & title_tokens) * 2.2

    query_lower = _clean_text(query_text).lower()
    chunk_lower = _clean_text(chunk_text).lower()
    if query_lower and query_lower in chunk_lower:
        score += 4.0

    return score


def _summarize_topics(text):
    clean = _clean_text(text)
    if not clean:
        return "No syllabus topics extracted yet."

    lines = re.split(r"[.;\n]", clean)
    candidates = []
    seen = set()
    for line in lines:
        item = _clean_text(line)
        if len(item) < 6:
            continue
        lower = item.lower()
        if lower in seen:
            continue
        seen.add(lower)
        candidates.append(item)
        if len(candidates) >= 12:
            break

    if not candidates:
        return clean[:280]
    return "; ".join(candidates)


def _extract_text_from_pdf(file_bytes):
    if PdfReader is None:
        return ""
    reader = PdfReader(BytesIO(file_bytes))
    chunks = []
    for page in reader.pages[:60]:
        try:
            chunks.append(page.extract_text() or "")
        except Exception:
            continue
    return _clean_text(" ".join(chunks))


def _extract_text_from_docx(file_bytes):
    try:
        with zipfile.ZipFile(BytesIO(file_bytes)) as archive:
            xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")
    except Exception:
        return ""
    text = re.sub(r"</w:p>", "\n", xml)
    text = re.sub(r"<[^>]+>", " ", text)
    return _clean_text(text)


def _extract_text_from_txt(file_bytes):
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return _clean_text(file_bytes.decode(encoding))
        except Exception:
            continue
    return ""


def extract_document_text(file_bytes, file_name="", mime_type=""):
    lower_name = (file_name or "").lower()
    lower_mime = (mime_type or "").lower()

    if lower_name.endswith(".pdf") or "pdf" in lower_mime:
        return _extract_text_from_pdf(file_bytes)
    if lower_name.endswith(".docx") or "wordprocessingml" in lower_mime or "docx" in lower_mime:
        return _extract_text_from_docx(file_bytes)
    return _extract_text_from_txt(file_bytes)


def save_syllabus_document(student_name, title="", text_content="", file_base64="", file_name="", mime_type=""):
    clean_student = str(student_name or "").strip()
    clean_title = str(title or "").strip()
    raw_text = str(text_content or "").strip()
    stored = None

    if file_base64:
        file_bytes = base64.b64decode(file_base64)
        stored = save_binary_file(
            file_bytes,
            file_name or "syllabus-upload.bin",
            folder=os.path.join("syllabus_docs", re.sub(r"[^a-z0-9]+", "-", clean_student.lower()).strip("-") or "student"),
        )
        extracted = extract_document_text(file_bytes, file_name=file_name, mime_type=mime_type)
        raw_text = f"{raw_text}\n\n{extracted}".strip() if raw_text else extracted

    cleaned_text = _truncate(raw_text, 12000)
    if not cleaned_text:
        raise ValueError("Could not extract any usable syllabus text from that input.")

    if not clean_title:
        clean_title = file_name or "Syllabus Notes"

    source_type = "text"
    if file_name:
        source_type = "document"

    topic_summary = _summarize_topics(cleaned_text)
    created_at = _timestamp()

    with db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO student_syllabus_documents
            (student_name, title, source_type, file_name, stored_path, extracted_text, topic_summary, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                clean_student,
                clean_title[:120],
                source_type,
                file_name or "",
                (stored or {}).get("path", ""),
                cleaned_text,
                topic_summary,
                created_at,
            ),
        )
        doc_id = cursor.lastrowid

    return {
        "id": doc_id,
        "student_name": clean_student,
        "title": clean_title[:120],
        "source_type": source_type,
        "file_name": file_name or "",
        "stored_path": (stored or {}).get("path", ""),
        "topic_summary": topic_summary,
        "created_at": created_at,
    }


def get_syllabus_documents(student_name):
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT id, title, source_type, file_name, stored_path, topic_summary, created_at
            FROM student_syllabus_documents
            WHERE student_name = ?
            ORDER BY id DESC
            """,
            (student_name,),
        )
        rows = cursor.fetchall()
    return [dict(row) for row in rows]


def delete_syllabus_document(student_name, document_id):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            DELETE FROM student_syllabus_documents
            WHERE student_name = ? AND id = ?
            """,
            (student_name, int(document_id)),
        )
        return cursor.rowcount or 0


def build_syllabus_context(student_name):
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT title, topic_summary, extracted_text
            FROM student_syllabus_documents
            WHERE student_name = ?
            ORDER BY id DESC
            LIMIT 6
            """,
            (student_name,),
        )
        rows = cursor.fetchall()

    if not rows:
        return ""

    lines = [
        "Uploaded syllabus and portion context for this student:",
    ]
    for row in rows:
        lines.append(f"- Source: {row['title']}")
        lines.append(f"  Topic summary: {row['topic_summary']}")
        lines.append(f"  Extracted detail: {_truncate(row['extracted_text'], 1400)}")
    lines.append(
        "Use this uploaded syllabus context when answering doubts, building plans, and creating revision coverage. "
        "Prefer these uploaded topics over generic assumptions."
    )
    return "\n".join(lines)


def retrieve_syllabus_context(student_name, query_text, max_chunks=3):
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT id, title, extracted_text
            FROM student_syllabus_documents
            WHERE student_name = ?
            ORDER BY id DESC
            LIMIT 10
            """,
            (student_name,),
        )
        rows = cursor.fetchall()

    if not rows:
        return {"text": "", "sources": []}

    ranked_chunks = []
    for row in rows:
        title = row["title"]
        for chunk in _chunk_text(row["extracted_text"]):
            score = _score_chunk(query_text, chunk, title=title)
            if score <= 0:
                continue
            ranked_chunks.append(
                {
                    "score": score,
                    "document_id": row["id"],
                    "title": title,
                    "chunk": chunk,
                }
            )

    if not ranked_chunks:
        return {"text": "", "sources": []}

    ranked_chunks.sort(key=lambda item: item["score"], reverse=True)
    selected = ranked_chunks[:max_chunks]
    lines = ["Relevant retrieved syllabus/portion excerpts for this student:"]
    sources = []
    seen_sources = set()
    for item in selected:
        lines.append(f"- From {item['title']}: {_truncate(item['chunk'], 650)}")
        if item["document_id"] not in seen_sources:
            sources.append(
                {
                    "label": item["title"],
                    "url": "",
                    "kind": "student_syllabus",
                }
            )
            seen_sources.add(item["document_id"])

    lines.append(
        "Use these retrieved syllabus excerpts to keep the answer aligned with the student's actual portion and avoid drifting into unrelated topics."
    )
    return {"text": "\n".join(lines), "sources": sources}
