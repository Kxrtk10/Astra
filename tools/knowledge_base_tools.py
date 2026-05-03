import hashlib
import html
import json
import math
import os
import re
import threading
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import httpx

try:
    import chromadb
except Exception:  # pragma: no cover - optional dependency
    chromadb = None

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover - optional dependency
    SentenceTransformer = None

try:
    from PyPDF2 import PdfReader
except Exception:  # pragma: no cover - optional dependency
    try:
        from pypdf import PdfReader
    except Exception:  # pragma: no cover - optional dependency
        PdfReader = None


KB_ROOT = Path("app_data") / "knowledge_base"
KB_CHROMA_ROOT = KB_ROOT / "chroma"
KB_SOURCES_ROOT = KB_ROOT / "sources"
KB_COLLECTION_NAMES = {
    "physics": "physics",
    "chemistry": "chemistry",
    "mathematics": "mathematics",
    "general_jee": "general_jee",
}
PYQ_QUERY_HINTS = (
    "previous year",
    "pyq",
    "jee question",
    "asked in jee",
    "previous-year",
)
PYQ_TOPICS = {
    "physics": [
        "projectile motion",
        "laws of motion",
        "work energy theorem",
        "electrostatics",
        "modern physics",
        "waves",
        "thermodynamics",
    ],
    "chemistry": [
        "mole concept",
        "organic reactions",
        "chemical equilibrium",
        "electrochemistry",
        "coordination compounds",
    ],
    "mathematics": [
        "limits",
        "integrals",
        "matrices",
        "probability",
        "complex numbers",
        "coordinate geometry",
    ],
}
KB_VECTOR_SIZE = 384

_kb_lock = threading.Lock()
_kb_client = None
_kb_backend = "uninitialized"
_kb_model = None
_kb_model_error = None


def _ensure_kb_directories():
    KB_CHROMA_ROOT.mkdir(parents=True, exist_ok=True)
    KB_SOURCES_ROOT.mkdir(parents=True, exist_ok=True)


def _normalize_text(value):
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _normalize_subject(subject):
    text = _normalize_text(subject)
    if "phys" in text or "motion" in text or "mechanic" in text or "electro" in text:
        return "physics"
    if "chem" in text or "organic" in text or "reaction" in text:
        return "chemistry"
    if "math" in text or "calculus" in text or "integral" in text or "derivative" in text or "limit" in text:
        return "mathematics"
    return "general_jee"


def _split_words(text):
    return re.findall(r"\S+", str(text or ""))


def _chunk_text(text, chunk_size=500, overlap=50):
    words = _split_words(text)
    if not words:
        return []
    chunk_size = max(int(chunk_size or 500), 1)
    overlap = max(min(int(overlap or 0), chunk_size - 1), 0)
    step = max(chunk_size - overlap, 1)
    chunks = []
    for start in range(0, len(words), step):
        chunk_words = words[start:start + chunk_size]
        if not chunk_words:
            break
        chunks.append(" ".join(chunk_words))
        if start + chunk_size >= len(words):
            break
    return chunks


def _load_pdf_text(file_path):
    if PdfReader is None:
        return ""
    reader = PdfReader(str(file_path))
    pages = []
    for page in getattr(reader, "pages", []):
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pages.append("")
    return "\n".join(pages)


def _load_source_text(file_path):
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _load_pdf_text(path)
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    raise ValueError("Only PDF and text files are supported.")


def _load_model():
    global _kb_model, _kb_model_error
    if _kb_model is not None or _kb_model_error is not None:
        return _kb_model
    if SentenceTransformer is None:
        _kb_model_error = "sentence-transformers unavailable"
        return None
    try:
        _kb_model = SentenceTransformer("all-MiniLM-L6-v2")
    except Exception as exc:  # pragma: no cover - optional dependency path
        _kb_model_error = str(exc)
        _kb_model = None
    return _kb_model


def _fallback_embedding(text):
    vector = [0.0] * KB_VECTOR_SIZE
    tokens = re.findall(r"[a-z0-9]+", _normalize_text(text))
    if not tokens:
        return vector
    for token in tokens:
        digest = hashlib.sha1(token.encode("utf-8")).digest()
        bucket = int.from_bytes(digest[:4], "big") % KB_VECTOR_SIZE
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[bucket] += sign
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def _embed_texts(texts):
    payload = [str(text or "") for text in texts]
    model = _load_model()
    if model is not None:
        embeddings = model.encode(payload, normalize_embeddings=True)
        if hasattr(embeddings, "tolist"):
            return embeddings.tolist()
        return [list(vector) for vector in embeddings]
    return [_fallback_embedding(text) for text in payload]


def _load_fallback_collection_payload(name):
    path = KB_CHROMA_ROOT / f"{name}.json"
    if not path.exists():
        return {"records": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"records": []}


def _save_fallback_collection_payload(name, payload):
    path = KB_CHROMA_ROOT / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _record_matches_where(record, where):
    if not where:
        return True
    for key, value in where.items():
        if record.get("metadata", {}).get(key) != value:
            return False
    return True


class _FallbackCollection:
    def __init__(self, name):
        self.name = name
        self._payload = _load_fallback_collection_payload(name)

    def _records(self):
        return list(self._payload.get("records", []))

    def _save(self, records):
        self._payload["records"] = records
        _save_fallback_collection_payload(self.name, self._payload)

    def count(self):
        return len(self._records())

    def delete(self, where=None):
        records = [record for record in self._records() if not _record_matches_where(record, where)]
        self._save(records)

    def add(self, documents, metadatas=None, embeddings=None, ids=None):
        documents = list(documents or [])
        metadatas = list(metadatas or [{} for _ in documents])
        embeddings = list(embeddings or [])
        ids = list(ids or [])
        records = self._records()
        for index, document in enumerate(documents):
            record_id = ids[index] if index < len(ids) else f"{self.name}-{index}"
            metadata = dict(metadatas[index] if index < len(metadatas) else {})
            embedding = embeddings[index] if index < len(embeddings) else _fallback_embedding(document)
            records = [record for record in records if record.get("id") != record_id]
            records.append(
                {
                    "id": record_id,
                    "document": document,
                    "metadata": metadata,
                    "embedding": list(embedding),
                }
            )
        self._save(records)

    def query(self, query_embeddings, n_results=5, **_kwargs):
        query_vector = list((query_embeddings or [[0.0] * KB_VECTOR_SIZE])[0])
        records = self._records()
        scored = []
        for record in records:
            embedding = list(record.get("embedding") or [])
            if not embedding:
                continue
            score = sum(float(a) * float(b) for a, b in zip(query_vector, embedding))
            scored.append((score, record))
        scored.sort(key=lambda item: item[0], reverse=True)
        selected = scored[: max(int(n_results or 5), 1)]
        return {
            "documents": [[item[1].get("document", "") for item in selected]],
            "metadatas": [[item[1].get("metadata", {}) for item in selected]],
            "ids": [[item[1].get("id", "") for item in selected]],
            "distances": [[1.0 - float(item[0]) for item in selected]],
        }


class _FallbackClient:
    def __init__(self):
        self._collections = {}

    def get_or_create_collection(self, name):
        collection = self._collections.get(name)
        if collection is None:
            collection = _FallbackCollection(name)
            self._collections[name] = collection
        return collection


def init_knowledge_base():
    global _kb_client, _kb_backend
    with _kb_lock:
        _ensure_kb_directories()
        if chromadb is None:
            _kb_backend = "fallback"
            _kb_client = _FallbackClient()
            for collection_name in KB_COLLECTION_NAMES.values():
                _kb_client.get_or_create_collection(collection_name)
            return _kb_client
        try:
            _kb_client = chromadb.PersistentClient(path=str(KB_CHROMA_ROOT))
            for collection_name in KB_COLLECTION_NAMES.values():
                _kb_client.get_or_create_collection(collection_name)
            _kb_backend = "chromadb"
            return _kb_client
        except Exception:
            _kb_backend = "fallback"
            _kb_client = _FallbackClient()
            for collection_name in KB_COLLECTION_NAMES.values():
                _kb_client.get_or_create_collection(collection_name)
            return _kb_client


def _get_client():
    if _kb_client is None:
        return init_knowledge_base()
    return _kb_client


def _get_collection(subject):
    client = _get_client()
    if client is None:
        return None
    return client.get_or_create_collection(KB_COLLECTION_NAMES.get(_normalize_subject(subject), "general_jee"))


def _store_documents_in_collection(collection, documents, metadatas, ids):
    if collection is None:
        return
    collection.add(documents=documents, metadatas=metadatas, embeddings=_embed_texts(documents), ids=ids)


def _query_wants_pyq(query):
    text = _normalize_text(query)
    return any(hint in text for hint in PYQ_QUERY_HINTS)


def _score_kb_result(result, query, wants_pyq=False):
    text = str(result.get("text", ""))
    metadata = result.get("metadata", {}) or {}
    score = 0.0
    query_tokens = set(re.findall(r"[a-z0-9]+", _normalize_text(query)))
    text_tokens = set(re.findall(r"[a-z0-9]+", _normalize_text(text)))
    score += len(query_tokens & text_tokens) * 2.0
    if wants_pyq and metadata.get("type") == "pyq":
        score += 8.0
    if metadata.get("type") == "pyq":
        score += 2.0
    if metadata.get("type") == "concept":
        score += 1.0
    topic = _normalize_text(metadata.get("topic", ""))
    if topic and topic in _normalize_text(query):
        score += 3.0
    return score


def add_document_to_kb(file_path, subject, source_name):
    try:
        client = _get_client()
        if client is None:
            return {"ok": False, "message": "Knowledge base unavailable", "subject": _normalize_subject(subject)}
        canonical_subject = _normalize_subject(subject)
        collection = client.get_or_create_collection(KB_COLLECTION_NAMES.get(canonical_subject, "general_jee"))
        text = _load_source_text(file_path)
        chunks = _chunk_text(text, chunk_size=500, overlap=50)
        if not chunks:
            return {
                "ok": False,
                "message": "No extractable text found in the file.",
                "subject": canonical_subject,
                "source_name": source_name,
                "chunks_added": 0,
            }
        try:
            collection.delete(where={"source_name": source_name})
        except Exception:
            pass
        embeddings = _embed_texts(chunks)
        metadatas = [
            {
                "source_name": source_name,
                "subject": canonical_subject,
                "chunk_index": index,
                "file_path": str(file_path),
            }
            for index in range(len(chunks))
        ]
        ids = [
            f"{canonical_subject}:{source_name}:{index}:{hashlib.sha1(chunk.encode('utf-8')).hexdigest()[:12]}"
            for index, chunk in enumerate(chunks)
        ]
        _store_documents_in_collection(collection, chunks, metadatas, ids)
        return {
            "ok": True,
            "message": "Document added to knowledge base.",
            "subject": canonical_subject,
            "source_name": source_name,
            "chunks_added": len(chunks),
            "backend": _kb_backend,
        }
    except Exception as exc:
        return {
            "ok": False,
            "message": str(exc),
            "subject": _normalize_subject(subject),
            "source_name": source_name,
            "chunks_added": 0,
        }


def search_knowledge_base(query, subject, n_results=5, session_type=None):
    try:
        if not query:
            return {"chunks": [], "has_pyqs": False, "sources": [], "context_prompt": ""} if session_type else []
        collection = _get_collection(subject)
        if collection is None:
            return {"chunks": [], "has_pyqs": False, "sources": [], "context_prompt": ""} if session_type else []
        query_embedding = _embed_texts([query])[0]
        response = collection.query(
            query_embeddings=[query_embedding],
            n_results=max(int(n_results or 5) * 2, 1),
        )
        documents = response.get("documents", [])
        metadatas = response.get("metadatas", [])
        if not documents:
            return {"chunks": [], "has_pyqs": False, "sources": [], "context_prompt": ""} if session_type else []
        wants_pyq = _query_wants_pyq(query)
        results = []
        for index, chunk in enumerate(documents[0]):
            if not chunk:
                continue
            metadata = metadatas[0][index] if metadatas and metadatas[0] and index < len(metadatas[0]) else {}
            results.append(
                {
                    "text": chunk,
                    "type": metadata.get("type", "concept"),
                    "metadata": metadata,
                    "score": _score_kb_result({"text": chunk, "metadata": metadata}, query, wants_pyq=wants_pyq),
                }
            )
        results.sort(key=lambda item: item.get("score", 0), reverse=True)
        selected = results[: max(int(n_results or 5), 1)]
        if not session_type:
            return selected

        normalized_session = str(session_type or "learn").strip().lower()
        has_pyqs = any(item.get("type") == "pyq" for item in selected)
        sources = []
        chunks = []

        def _append_item(item):
            metadata = item.get("metadata", {}) or {}
            source_name = str(metadata.get("source_name") or metadata.get("title") or "").strip()
            if source_name and source_name not in sources:
                sources.append(source_name)
            chunks.append(item)

        if normalized_session == "practice":
            pyqs = [item for item in selected if item.get("type") == "pyq"]
            concepts = [item for item in selected if item.get("type") != "pyq"]
            ordered = (pyqs + concepts)[: max(int(n_results or 5), 1)]
            if len(pyqs) < 3:
                extra = [item for item in results if item.get("type") == "pyq" and item not in pyqs]
                ordered.extend(extra[: max(0, 3 - len(pyqs))])
            for item in ordered[: max(int(n_results or 5), 1)]:
                _append_item(item)
        elif normalized_session == "revise":
            ordered = sorted(selected, key=lambda item: (item.get("type") == "pyq", item.get("score", 0)), reverse=True)
            for item in ordered:
                _append_item(item)
        else:  # learn and default
            concept_first = sorted(selected, key=lambda item: (item.get("type") == "concept", item.get("score", 0)), reverse=True)
            for item in concept_first:
                _append_item(item)

        context_lines = []
        pyq_chunks = [item["text"] for item in chunks if item.get("type") == "pyq"]
        concept_chunks = [item["text"] for item in chunks if item.get("type") != "pyq"]
        if normalized_session == "practice" or has_pyqs:
            if pyq_chunks:
                context_lines.append("Here are relevant JEE previous year questions on this topic:")
                context_lines.extend(f"- {chunk}" for chunk in pyq_chunks[:5])
                context_lines.append("Use these to inform your explanation and mention that these were actual JEE questions.")
        if concept_chunks:
            context_lines.append("Here is verified source material on this topic:")
            context_lines.extend(f"- {chunk}" for chunk in concept_chunks[:5])
            context_lines.append("Use this to give an accurate explanation.")
        if sources:
            context_lines.append(f"Sources: {', '.join(sources[:5])}")
        return {
            "chunks": chunks,
            "has_pyqs": has_pyqs,
            "sources": sources,
            "context_prompt": "\n".join(context_lines),
        }
    except Exception:
        return {"chunks": [], "has_pyqs": False, "sources": [], "context_prompt": ""} if session_type else []


def add_pyq_database(json_file_path):
    try:
        path = Path(json_file_path)
        if not path.exists():
            return {"ok": False, "message": "PYQ JSON file not found.", "added": 0, "subjects": {}}
        payload = json.loads(path.read_text(encoding="utf-8"))
        questions = payload.get("questions", [])
        if not isinstance(questions, list):
            return {"ok": False, "message": "Invalid PYQ file format.", "added": 0, "subjects": {}}
        client = _get_client()
        if client is None:
            return {"ok": False, "message": "Knowledge base unavailable.", "added": 0, "subjects": {}}

        added = 0
        subjects = {}
        added_questions = []
        for collection_name in KB_COLLECTION_NAMES.values():
            try:
                client.get_or_create_collection(collection_name).delete(where={"type": "pyq", "source_name": path.stem})
            except Exception:
                pass
        for question in questions:
            subject = _normalize_subject(question.get("subject", "general_jee"))
            collection = client.get_or_create_collection(KB_COLLECTION_NAMES.get(subject, "general_jee"))
            year = int(question.get("year", 0) or 0)
            exam = str(question.get("exam", "JEE")).strip() or "JEE"
            exam_label = exam if exam.upper().startswith("JEE") else f"JEE {exam}"
            topic = str(question.get("topic", "")).strip() or "General"
            question_text = str(question.get("question", "")).strip()
            options = question.get("options", [])
            solution = str(question.get("solution", "")).strip()
            key_concept = str(question.get("key_concept", "")).strip()
            correct_answer = str(question.get("correct_answer", "")).strip()
            chunk = (
                f"{exam_label} {year} | {subject} | Topic: {topic}\n"
                f"Question: {question_text}\n"
                f"Options: {json.dumps(options, ensure_ascii=False)}\n"
                f"Correct Answer: {correct_answer}\n"
                f"Solution: {solution}\n"
                f"Key Concept: {key_concept}"
            )
            metadata = {
                "type": "pyq",
                "year": year,
                "exam": exam,
                "topic": topic,
                "subject": subject,
                "source_name": path.stem,
            }
            chunk_id = f"pyq:{subject}:{year}:{exam}:{hashlib.sha1(chunk.encode('utf-8')).hexdigest()[:12]}"
            try:
                collection.add(
                    documents=[chunk],
                    metadatas=[metadata],
                    embeddings=_embed_texts([chunk]),
                    ids=[chunk_id],
                )
                added += 1
                subjects[subject] = subjects.get(subject, 0) + 1
                added_questions.append(
                    {
                        "year": year,
                        "exam": exam_label,
                        "subject": subject,
                        "topic": topic,
                    }
                )
            except Exception:
                continue
        return {
            "ok": True,
            "message": "PYQ database ingested.",
            "added": added,
            "subjects": subjects,
            "questions_added": added_questions,
            "file_path": str(path),
        }
    except Exception as exc:
        return {"ok": False, "message": str(exc), "added": 0, "subjects": {}}


def get_topic_coverage():
    coverage = {}
    pyq_file = KB_SOURCES_ROOT / "jee_pyqs.json"
    topics_by_subject = {subject: set() for subject in PYQ_TOPICS}
    if pyq_file.exists():
        try:
            payload = json.loads(pyq_file.read_text(encoding="utf-8"))
            for question in payload.get("questions", []):
                subject = _normalize_subject(question.get("subject", "general_jee"))
                topic = _normalize_text(question.get("topic", ""))
                if subject in topics_by_subject and topic:
                    topics_by_subject[subject].add(topic)
        except Exception:
            pass

    for subject, expected_topics in PYQ_TOPICS.items():
        have = sorted(topic for topic in expected_topics if topic in topics_by_subject.get(subject, set()))
        missing = sorted(topic for topic in expected_topics if topic not in topics_by_subject.get(subject, set()))
        coverage[subject] = {
            "have_pyqs": have,
            "missing_pyqs": missing,
            "covered_count": len(have),
            "expected_count": len(expected_topics),
        }

    return {
        "subjects": coverage,
        "total_covered_topics": sum(item["covered_count"] for item in coverage.values()),
        "total_expected_topics": sum(item["expected_count"] for item in coverage.values()),
        "pyq_file": str(pyq_file),
    }


def get_kb_stats():
    client = _get_client()
    counts = {}
    for subject, collection_name in KB_COLLECTION_NAMES.items():
        count = 0
        try:
            collection = client.get_or_create_collection(collection_name) if client is not None else None
            count = collection.count() if collection is not None else 0
        except Exception:
            count = 0
        counts[subject] = count
    return {
        "available": client is not None,
        "backend": _kb_backend if client is not None else "unavailable",
        "collections": counts,
        "total_documents": sum(counts.values()),
        "root": str(KB_ROOT),
        "chroma_root": str(KB_CHROMA_ROOT),
        "sources_root": str(KB_SOURCES_ROOT),
        "model": "all-MiniLM-L6-v2" if _load_model() is not None else "fallback-hash-embeddings",
    }


def _strip_html_markup(text):
    cleaned = re.sub(r"(?is)<script.*?>.*?</script>", " ", text or "")
    cleaned = re.sub(r"(?is)<style.*?>.*?</style>", " ", cleaned)
    cleaned = re.sub(r"(?is)<noscript.*?>.*?</noscript>", " ", cleaned)
    cleaned = re.sub(r"(?i)</p>|</div>|</li>|<br\s*/?>", "\n", cleaned)
    cleaned = re.sub(r"(?is)<[^>]+>", " ", cleaned)
    cleaned = html.unescape(cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def _load_pdf_from_path(pdf_path):
    if PdfReader is None:
        return ""
    try:
        reader = PdfReader(str(pdf_path))
        pages = []
        for page in getattr(reader, "pages", []):
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                pages.append("")
        return "\n".join(pages)
    except Exception:
        return ""


def fetch_and_add_web_source(url, subject, source_name):
    try:
        if not url:
            return {"ok": False, "message": "A URL is required.", "url": url, "subject": _normalize_subject(subject), "chunks_added": 0}

        parsed = urlparse(url)
        path = (parsed.path or "").lower()
        suffix = Path(path).suffix
        response = httpx.get(url, follow_redirects=True, timeout=30.0)
        response.raise_for_status()

        if suffix == ".pdf" or "application/pdf" in response.headers.get("content-type", "").lower():
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(response.content)
                temp_pdf_path = temp_pdf.name
            try:
                cleaned_text = _load_pdf_from_path(temp_pdf_path)
            finally:
                try:
                    os.unlink(temp_pdf_path)
                except OSError:
                    pass
        else:
            response.encoding = response.encoding or "utf-8"
            cleaned_text = _strip_html_markup(response.text)

        if not cleaned_text.strip():
            return {
                "ok": False,
                "message": "No extractable text found at the source URL.",
                "url": url,
                "subject": _normalize_subject(subject),
                "chunks_added": 0,
            }

        chunks = _chunk_text(cleaned_text, chunk_size=500, overlap=50)
        if not chunks:
            return {
                "ok": False,
                "message": "No chunks could be created from the source text.",
                "url": url,
                "subject": _normalize_subject(subject),
                "chunks_added": 0,
            }

        added = 0
        source_stem = source_name or Path(parsed.path).stem or "web_source"
        for index, chunk in enumerate(chunks, start=1):
            chunk_path = KB_SOURCES_ROOT / f"{source_stem}__chunk_{index:03d}.txt"
            try:
                chunk_path.write_text(chunk, encoding="utf-8")
                result = add_document_to_kb(str(chunk_path), subject, f"{source_stem}__chunk_{index:03d}")
                if result.get("ok"):
                    added += 1
            finally:
                try:
                    os.unlink(chunk_path)
                except OSError:
                    pass

        return {
            "ok": True,
            "message": "Web source ingested into the knowledge base.",
            "url": url,
            "subject": _normalize_subject(subject),
            "source_name": source_name or source_stem,
            "chunks_added": added,
            "chunk_count": len(chunks),
            "backend": _kb_backend,
        }
    except Exception as exc:
        return {
            "ok": False,
            "message": str(exc),
            "url": url,
            "subject": _normalize_subject(subject),
            "source_name": source_name,
            "chunks_added": 0,
        }
