TIP_RESOURCES = {
    "JEE MAIN": [
        {
            "title": "NTA Official JEE Main Resources",
            "source": "NTA",
            "url": "https://jeemain.nta.nic.in/",
            "kind": "official",
            "tip": "Use this for official updates, structure, and exam information.",
        },
        {
            "title": "NTA Student Support And Lecture Content",
            "source": "NTA",
            "url": "https://nta.ac.in/Students",
            "kind": "official",
            "tip": "Useful for public learning support resources and structured revision input.",
        },
    ],
    "JEE ADVANCED": [
        {
            "title": "JEE Advanced Official Website",
            "source": "JEE Advanced",
            "url": "https://jeeadv.ac.in/",
            "kind": "official",
            "tip": "Keep this for official pattern awareness and exam-stage clarity.",
        },
        {
            "title": "NTA Student Support And Lecture Content",
            "source": "NTA",
            "url": "https://nta.ac.in/Students",
            "kind": "official",
            "tip": "Use this with advanced prep to strengthen concept review and revision structure.",
        },
    ],
}


def get_tips_resources(profile):
    exams = profile.get("exams", [])
    resources = []
    seen = set()

    for exam in exams:
        exam_name = str(exam.get("name", "")).strip().upper()
        for key, items in TIP_RESOURCES.items():
            if key == exam_name:
                for item in items:
                    if item["url"] in seen:
                        continue
                    resources.append(
                        {
                            "exam": exam_name,
                            **item,
                        }
                    )
                    seen.add(item["url"])

    return resources


def build_tips_context(profile):
    resources = get_tips_resources(profile)
    if not resources:
        return ""

    lines = ["Curated public strategy resources for this student's exams:"]
    for item in resources:
        lines.append(f"- {item['exam']}: {item['title']} ({item['source']}) -> {item['tip']} {item['url']}")
    return "\n".join(lines)
