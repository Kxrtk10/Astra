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
    ("chemistry", "NCERT Chemistry Class 11 Chapter 1", "https://ncert.nic.in/textbook/pdf/lech101.pdf"),
    ("chemistry", "NCERT Chemistry Class 11 Chapter 2", "https://ncert.nic.in/textbook/pdf/lech201.pdf"),
    ("chemistry", "NCERT Chemistry Class 11 Chapter 3", "https://ncert.nic.in/textbook/pdf/lech102.pdf"),
    ("chemistry", "NCERT Chemistry Class 12 Chapter 1", "https://ncert.nic.in/textbook/pdf/lech202.pdf"),
    ("chemistry", "NCERT Chemistry Class 12 Chapter 2", "https://ncert.nic.in/textbook/pdf/lech203.pdf"),
    ("mathematics", "NCERT Mathematics Class 11 Chapter 1", "https://ncert.nic.in/textbook/pdf/lemh101.pdf"),
    ("mathematics", "NCERT Mathematics Class 11 Chapter 2", "https://ncert.nic.in/textbook/pdf/lemh201.pdf"),
    ("mathematics", "NCERT Mathematics Class 11 Chapter 3", "https://ncert.nic.in/textbook/pdf/lemh102.pdf"),
    ("mathematics", "NCERT Mathematics Class 11 Chapter 4", "https://ncert.nic.in/textbook/pdf/lemh103.pdf"),
    ("mathematics", "NCERT Mathematics Class 12 Chapter 1", "https://ncert.nic.in/textbook/pdf/lemh202.pdf"),
]


def main():
    for subject, source_name, url in WEB_SOURCES:
        print(f"Fetching: {url}")
        try:
            result = fetch_and_add_web_source(url, subject, source_name)
            if result.get("ok"):
                print(f"Added chunks: {result.get('chunks_added', 0)} | Source: {source_name}")
            else:
                print(f"Error: {result.get('message', 'Unknown error')}")
        except Exception as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
