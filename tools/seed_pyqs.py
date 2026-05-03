import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.knowledge_base_tools import add_pyq_database, get_kb_stats


def main():
    pyq_file = ROOT / "app_data" / "knowledge_base" / "sources" / "jee_pyqs.json"
    result = add_pyq_database(str(pyq_file))
    if result.get("ok"):
        print(f"PYQ database ingested: {result.get('added', 0)} questions")
        for item in result.get("questions_added", []):
            print(f"Added PYQ: {item.get('exam')} {item.get('year')} | {item.get('subject')} | {item.get('topic')}")
        for subject, count in sorted((result.get("subjects") or {}).items()):
            print(f"Added {count} questions to {subject}")
        print(f"Final stats: {get_kb_stats()}")
    else:
        print(f"Error: {result.get('message', 'Could not ingest PYQ database.')}")


if __name__ == "__main__":
    main()
