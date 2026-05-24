import json
import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.knowledge_base_tools import add_pyq_database


def main():
    pyq_file = ROOT / "app_data" / "knowledge_base" / "sources" / "jee_pyqs.json"
    if not pyq_file.exists():
        print(f"Error: PYQ source file not found at {pyq_file}")
        return

    payload = json.loads(pyq_file.read_text(encoding="utf-8"))
    questions = payload.get("questions", []) if isinstance(payload, dict) else []
    total = len(questions)
    added = 0
    failed = 0
    for index, question in enumerate(questions, start=1):
        print(f"Seeding PYQ {index}/{total}: {question.get('subject', '')} | {question.get('topic', '')}")
        single_payload = {"questions": [question]}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as temp_file:
            temp_file.write(json.dumps(single_payload, indent=2, ensure_ascii=False))
            temp_path = temp_file.name
        try:
            result = add_pyq_database(temp_path)
            if result.get("ok"):
                added += 1 if int(result.get("added", 0) or 0) > 0 else 0
            else:
                failed += 1
                print(f"Error: {result.get('message', 'Could not ingest PYQ.')}")
        finally:
            try:
                Path(temp_path).unlink(missing_ok=True)
            except Exception:
                pass

    print(f"Successfully indexed: {added} sources")
    print(f"Failed: {failed} sources")
    print(f"Total chunks added: {added}")


if __name__ == "__main__":
    main()
