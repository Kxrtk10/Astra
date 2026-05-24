import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.knowledge_base_tools import fetch_and_add_web_source


WEB_SOURCES = [
    ("physics", "NCERT Physics Class 11 Chapter 1", "https://ncert.nic.in/textbook/pdf/leph101.pdf"),
    ("physics", "NCERT Physics Class 11 Chapter 2", "https://ncert.nic.in/textbook/pdf/leph201.pdf"),
    ("physics", "NCERT Physics Class 11 Chapter 3", "https://ncert.nic.in/textbook/pdf/leph102.pdf"),
    ("physics", "NCERT Physics Class 11 Chapter 4", "https://ncert.nic.in/textbook/pdf/leph103.pdf"),
    ("physics", "NCERT Physics Class 12 Chapter 1", "https://ncert.nic.in/textbook/pdf/leph202.pdf"),
    ("physics", "NCERT Physics Class 12 Chapter 2", "https://ncert.nic.in/textbook/pdf/leph203.pdf"),
    ("physics", "NCERT Physics Class 12 Volume 1", "https://ncert.nic.in/textbook/pdf/leph1dd.pdf"),
    ("physics", "NCERT Physics Class 12 Volume 2", "https://ncert.nic.in/textbook/pdf/leph2dd.pdf"),
    ("physics", "NCERT Physics Topic Sheet 104", "https://ncert.nic.in/textbook/pdf/leph104.pdf"),
    ("physics", "NCERT Physics Topic Sheet 105", "https://ncert.nic.in/textbook/pdf/leph105.pdf"),
    ("physics", "NCERT Physics Topic Sheet 106", "https://ncert.nic.in/textbook/pdf/leph106.pdf"),
    ("physics", "NCERT Physics Topic Sheet 204", "https://ncert.nic.in/textbook/pdf/leph204.pdf"),
    ("physics", "NCERT Physics Topic Sheet 205", "https://ncert.nic.in/textbook/pdf/leph205.pdf"),
    ("chemistry", "NCERT Chemistry Class 11 Chapter 1", "https://ncert.nic.in/textbook/pdf/lech101.pdf"),
    ("chemistry", "NCERT Chemistry Class 11 Chapter 2", "https://ncert.nic.in/textbook/pdf/lech201.pdf"),
    ("chemistry", "NCERT Chemistry Class 11 Chapter 3", "https://ncert.nic.in/textbook/pdf/lech102.pdf"),
    ("chemistry", "NCERT Chemistry Class 12 Chapter 1", "https://ncert.nic.in/textbook/pdf/lech202.pdf"),
    ("chemistry", "NCERT Chemistry Class 12 Chapter 2", "https://ncert.nic.in/textbook/pdf/lech203.pdf"),
    ("chemistry", "NCERT Chemistry Topic Sheet 103", "https://ncert.nic.in/textbook/pdf/lech103.pdf"),
    ("chemistry", "NCERT Chemistry Topic Sheet 104", "https://ncert.nic.in/textbook/pdf/lech104.pdf"),
    ("chemistry", "NCERT Chemistry Topic Sheet 203", "https://ncert.nic.in/textbook/pdf/lech203.pdf"),
    ("chemistry", "NCERT Chemistry Topic Sheet 204", "https://ncert.nic.in/textbook/pdf/lech204.pdf"),
    ("mathematics", "NCERT Mathematics Class 11 Chapter 1", "https://ncert.nic.in/textbook/pdf/lemh101.pdf"),
    ("mathematics", "NCERT Mathematics Class 11 Chapter 2", "https://ncert.nic.in/textbook/pdf/lemh201.pdf"),
    ("mathematics", "NCERT Mathematics Class 11 Chapter 3", "https://ncert.nic.in/textbook/pdf/lemh102.pdf"),
    ("mathematics", "NCERT Mathematics Class 11 Chapter 4", "https://ncert.nic.in/textbook/pdf/lemh103.pdf"),
    ("mathematics", "NCERT Mathematics Class 12 Chapter 1", "https://ncert.nic.in/textbook/pdf/lemh202.pdf"),
    ("mathematics", "NCERT Mathematics Topic Sheet 104", "https://ncert.nic.in/textbook/pdf/lemh104.pdf"),
    ("mathematics", "NCERT Mathematics Topic Sheet 105", "https://ncert.nic.in/textbook/pdf/lemh105.pdf"),
    ("mathematics", "NCERT Mathematics Topic Sheet 203", "https://ncert.nic.in/textbook/pdf/lemh203.pdf"),
    ("mathematics", "NCERT Mathematics Topic Sheet 204", "https://ncert.nic.in/textbook/pdf/lemh204.pdf"),
]


def main():
    success = 0
    failed = 0
    chunks_added = 0
    for subject, source_name, url in WEB_SOURCES:
        print(f"Fetching: {url}")
        try:
            result = fetch_and_add_web_source(url, subject, source_name)
            if result.get("ok"):
                success += 1
                chunks_added += int(result.get("chunks_added", 0) or 0)
                print(f"Added chunks: {result.get('chunks_added', 0)} | Source: {source_name}")
            else:
                failed += 1
                print(f"Error: {result.get('message', 'Unknown error')}")
        except Exception as exc:
            failed += 1
            print(f"Error: {exc}")
    print(f"Successfully indexed: {success} sources")
    print(f"Failed: {failed} sources")
    print(f"Total chunks added: {chunks_added}")


if __name__ == "__main__":
    main()
