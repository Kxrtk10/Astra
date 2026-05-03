import html
import html
import re
import urllib.request
from functools import lru_cache

from tools.knowledge_base_tools import search_knowledge_base
from tools.student_state_router import build_student_state_route


LEARNING_SOURCE_REGISTRY = {
    "GRE": [
        {
            "title": "ETS GRE Official Preparation",
            "source": "ETS",
            "url": "https://www.ets.org/gre/test-takers/general-test/prepare.html",
            "kind": "official_exam",
            "why": "Official prep guidance, format familiarity, and baseline practice material.",
            "tags": ["gre", "official", "format", "verbal", "quant", "writing"],
        },
        {
            "title": "Khan Academy Grammar",
            "source": "Khan Academy",
            "url": "https://www.khanacademy.org/humanities/grammar",
            "kind": "open_textbook",
            "why": "Useful for GRE verbal fundamentals and sentence-level clarity.",
            "tags": ["grammar", "verbal", "language", "sentence correction"],
        },
    ],
    "GMAT": [
        {
            "title": "GMAT Official Prep",
            "source": "mba.com",
            "url": "https://www.mba.com/exams/gmat-exam/prep",
            "kind": "official_exam",
            "why": "Best starting point for official format, prep direction, and timing familiarity.",
            "tags": ["gmat", "official", "format", "quant", "verbal", "data insights"],
        },
        {
            "title": "Khan Academy Statistics And Probability",
            "source": "Khan Academy",
            "url": "https://www.khanacademy.org/math/statistics-probability",
            "kind": "open_course",
            "why": "Supports quant foundations in a structured way.",
            "tags": ["statistics", "probability", "math", "quant"],
        },
    ],
    "JEE MAIN": [
        {
            "title": "NTA JEE Main Official Website",
            "source": "NTA",
            "url": "https://jeemain.nta.nic.in/",
            "kind": "official_exam",
            "why": "Official pattern, updates, and exam information.",
            "tags": ["jee", "official", "format", "physics", "chemistry", "math"],
        },
        {
            "title": "NPTEL Course Catalogue",
            "source": "NPTEL",
            "url": "https://nptel.ac.in/course.html",
            "kind": "open_course",
            "why": "Great public lectures for engineering-style concept strengthening.",
            "tags": ["engineering", "physics", "chemistry", "math", "mechanics", "electrical", "thermodynamics"],
        },
    ],
    "JEE ADVANCED": [
        {
            "title": "JEE Advanced Official Website",
            "source": "JEE Advanced",
            "url": "https://jeeadv.ac.in/",
            "kind": "official_exam",
            "why": "Official source for advanced-stage exam expectations and updates.",
            "tags": ["jee advanced", "official", "physics", "chemistry", "math"],
        },
        {
            "title": "MIT OpenCourseWare Physics",
            "source": "MIT OCW",
            "url": "https://ocw.mit.edu/search/?d=Physics",
            "kind": "open_course",
            "why": "Excellent for deeper conceptual physics understanding.",
            "tags": ["physics", "mechanics", "kinematics", "motion", "projectile", "dynamics", "fields"],
        },
    ],
    "ENGINEERING": [
        {
            "title": "NPTEL Course Catalogue",
            "source": "NPTEL",
            "url": "https://nptel.ac.in/course.html",
            "kind": "open_course",
            "why": "Strong public engineering lectures across core branches.",
            "tags": ["engineering", "mechanics", "electronics", "civil", "computer science", "math"],
        },
        {
            "title": "MIT OpenCourseWare",
            "source": "MIT OCW",
            "url": "https://ocw.mit.edu/",
            "kind": "open_course",
            "why": "Open university-level engineering and science learning material.",
            "tags": ["engineering", "physics", "math", "signals", "mechanics", "thermodynamics"],
        },
        {
            "title": "LibreTexts Engineering Library",
            "source": "LibreTexts",
            "url": "https://eng.libretexts.org/",
            "kind": "open_textbook",
            "why": "Open textbooks and structured engineering topic explanations.",
            "tags": ["engineering", "textbook", "mechanics", "thermodynamics", "circuits"],
        },
    ],
    "MEDICAL": [
        {
            "title": "MedlinePlus Medical Encyclopedia",
            "source": "NIH",
            "url": "https://medlineplus.gov/encyclopedia.html",
            "kind": "open_reference",
            "why": "Reliable public reference for many medical topics.",
            "tags": ["medical", "disease", "anatomy", "physiology", "pathology"],
        },
        {
            "title": "WHO Health Topics",
            "source": "WHO",
            "url": "https://www.who.int/health-topics",
            "kind": "open_reference",
            "why": "Public topic summaries useful for overview and recall.",
            "tags": ["medical", "health", "public health", "disease"],
        },
        {
            "title": "TeachMeAnatomy",
            "source": "TeachMe Series",
            "url": "https://teachmeanatomy.info/",
            "kind": "public_medical_learning",
            "why": "Useful visual public anatomy material for student revision.",
            "tags": ["anatomy", "medical", "human body", "organs", "systems"],
        },
    ],
    "MBA": [
        {
            "title": "GMAT Official Prep",
            "source": "mba.com",
            "url": "https://www.mba.com/exams/gmat-exam/prep",
            "kind": "official_exam",
            "why": "Strong official starting point for MBA-entry exam prep.",
            "tags": ["mba", "gmat", "official", "management", "quant", "verbal"],
        },
        {
            "title": "OpenStax Principles of Management",
            "source": "OpenStax",
            "url": "https://openstax.org/details/books/principles-management",
            "kind": "open_textbook",
            "why": "Public management reading for MBA-related academic grounding.",
            "tags": ["management", "mba", "business", "organization"],
        },
    ],
    "CA": [
        {
            "title": "ICAI Self Study Portal",
            "source": "ICAI",
            "url": "https://www.icai.org/post/study-material-nset",
            "kind": "official_exam",
            "why": "Official CA-related study material source.",
            "tags": ["ca", "accounting", "tax", "audit", "official"],
        },
        {
            "title": "ICAI BOS Knowledge Portal",
            "source": "ICAI",
            "url": "https://boslive.icai.org/",
            "kind": "official_exam",
            "why": "Useful for CA syllabus support and official material access.",
            "tags": ["ca", "accounting", "official", "study material"],
        },
    ],
    "COLLEGE": [
        {
            "title": "MIT OpenCourseWare",
            "source": "MIT OCW",
            "url": "https://ocw.mit.edu/",
            "kind": "open_course",
            "why": "Broad public course material across many college subjects.",
            "tags": ["college", "course", "physics", "math", "engineering", "science"],
        },
        {
            "title": "OpenStax Textbooks",
            "source": "OpenStax",
            "url": "https://openstax.org/subjects",
            "kind": "open_textbook",
            "why": "Free textbooks across science, math, business, and social sciences.",
            "tags": ["college", "textbook", "science", "math", "business", "biology"],
        },
        {
            "title": "LibreTexts Library",
            "source": "LibreTexts",
            "url": "https://libretexts.org/",
            "kind": "open_textbook",
            "why": "Wide public learning material across many academic disciplines.",
            "tags": ["college", "textbook", "engineering", "chemistry", "physics", "math"],
        },
    ],
}

SUBJECT_SOURCE_HINTS = {
    "physics": [
        {
            "title": "Khan Academy Physics",
            "source": "Khan Academy",
            "url": "https://www.khanacademy.org/science/physics",
            "kind": "open_course",
            "why": "Good conceptual physics lessons and visual intuition.",
            "tags": ["physics", "motion", "projectile", "kinematics", "mechanics", "energy", "fields"],
        }
    ],
    "chemistry": [
        {
            "title": "Khan Academy Chemistry",
            "source": "Khan Academy",
            "url": "https://www.khanacademy.org/science/chemistry",
            "kind": "open_course",
            "why": "Useful for reaction, structure, and chemistry basics.",
            "tags": ["chemistry", "reactions", "equilibrium", "organic", "inorganic"],
        }
    ],
    "biology": [
        {
            "title": "Khan Academy Biology",
            "source": "Khan Academy",
            "url": "https://www.khanacademy.org/science/biology",
            "kind": "open_course",
            "why": "Strong for foundation biology and recall support.",
            "tags": ["biology", "cells", "genetics", "human biology", "ecology"],
        }
    ],
    "math": [
        {
            "title": "Khan Academy Math",
            "source": "Khan Academy",
            "url": "https://www.khanacademy.org/math",
            "kind": "open_course",
            "why": "Wide math support from basics to advanced topics.",
            "tags": ["math", "algebra", "geometry", "calculus", "probability", "statistics"],
        }
    ],
    "anatomy": [
        {
            "title": "TeachMeAnatomy",
            "source": "TeachMe Series",
            "url": "https://teachmeanatomy.info/",
            "kind": "public_medical_learning",
            "why": "Useful anatomy visuals and structured explanations.",
            "tags": ["anatomy", "medical", "organs", "human body", "systems"],
        }
    ],
}

SOURCE_PACKS = {
    "default": {
        "label": "Balanced source pack",
        "reason": "General-purpose sources for broad academic support.",
        "kind_priority": ["official_exam", "open_course", "open_textbook", "open_reference"],
        "max_sources": 2,
    },
    "concept_bridge": {
        "label": "Concept bridge pack",
        "reason": "Helpful for visual explanations and concept-by-concept teaching.",
        "kind_priority": ["official_exam", "open_course", "open_textbook"],
        "max_sources": 2,
    },
    "projectile_bridge": {
        "label": "Projectile bridge pack",
        "reason": "Focused support for motion, roof-drop, and projectile-style real-life scenes.",
        "kind_priority": ["official_exam", "open_course", "open_textbook"],
        "max_sources": 2,
    },
    "electrostatics_depth": {
        "label": "Electrostatics depth pack",
        "reason": "Deeper support for charge, field, and field-line understanding.",
        "kind_priority": ["official_exam", "open_course", "open_textbook"],
        "max_sources": 2,
    },
    "probability_bridge": {
        "label": "Probability bridge pack",
        "reason": "Helpful for probability and statistics problems built from real-life examples.",
        "kind_priority": ["official_exam", "open_course", "open_textbook"],
        "max_sources": 2,
    },
    "jee_main_fast": {
        "label": "JEE Main quick pack",
        "reason": "Fast, exam-safe sources for clean mains-first preparation.",
        "kind_priority": ["official_exam", "open_course", "open_textbook"],
        "max_sources": 1,
    },
    "jee_advanced_depth": {
        "label": "JEE Advanced depth pack",
        "reason": "Deeper sources for advanced reasoning and tougher concept stretching.",
        "kind_priority": ["official_exam", "open_course", "open_textbook"],
        "max_sources": 2,
    },
    "practice_exam": {
        "label": "Practice exam pack",
        "reason": "Question-format sources for drills, mocks, and answer discipline.",
        "kind_priority": ["official_exam", "open_course", "open_textbook"],
        "max_sources": 1,
    },
    "last_minute": {
        "label": "Last minute rescue pack",
        "reason": "High-yield sources for fast revision and rescue planning.",
        "kind_priority": ["official_exam", "open_textbook", "open_reference"],
        "max_sources": 1,
    },
    "tips": {
        "label": "Strategy pack",
        "reason": "Strategy sources for exam decisions, pacing, and method.",
        "kind_priority": ["official_exam", "public_strategy", "official_partner", "open_course"],
        "max_sources": 2,
    },
}

STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "for", "of", "in", "on", "with", "by", "from", "is", "are", "be",
    "me", "my", "this", "that", "it", "as", "at", "if", "then", "how", "what", "why", "does", "do", "can",
    "please", "clearly", "properly", "explain", "teach", "about", "using",
}

TOPIC_SUBJECT_HINTS = {
    "physics": {"projectile", "motion", "kinematics", "velocity", "acceleration", "force", "energy", "momentum", "field", "charge", "current"},
    "chemistry": {"reaction", "molecule", "bond", "organic", "inorganic", "equilibrium", "acid", "base", "enthalpy"},
    "biology": {"cell", "organ", "dna", "genetics", "anatomy", "physiology", "ecology", "enzyme"},
    "math": {"algebra", "probability", "statistics", "geometry", "calculus", "matrix", "trigonometry", "percentage"},
    "anatomy": {"anatomy", "skeleton", "muscle", "organ", "artery", "vein", "nerve"},
}

LOCAL_TOPIC_NOTES = {
    "projectile motion": {
        "scope": "Physics concept fallback",
        "title": "Projectile Motion Core Idea",
        "source": "Astra Local JEE Notes",
        "kind": "local_fallback",
        "why": "Local concept fallback used when external source fetch is unavailable.",
        "url": "",
        "text": (
            "Projectile motion splits cleanly into horizontal motion with constant velocity and vertical motion with gravity. "
            "For JEE, treat the two axes separately, then combine them to understand the curved path, time of flight, maximum height, and range."
        ),
    },
    "probability": {
        "scope": "Math concept fallback",
        "title": "Probability Core Idea",
        "source": "Astra Local JEE Notes",
        "kind": "local_fallback",
        "why": "Local concept fallback used when external source fetch is unavailable.",
        "url": "",
        "text": (
            "Probability is favorable outcomes divided by total outcomes. For JEE, count the sample space carefully, define the event clearly, "
            "and keep track of independence, complement, and conditional cases step by step."
        ),
    },
    "electrostatics": {
        "scope": "Physics concept fallback",
        "title": "Electrostatics Core Idea",
        "source": "Astra Local JEE Notes",
        "kind": "local_fallback",
        "why": "Local concept fallback used when external source fetch is unavailable.",
        "url": "",
        "text": (
            "Electrostatics focuses on charge, field, force, and potential. For JEE, visualize how field lines spread from positive charge and toward negative charge, "
            "then use superposition to build the final picture."
        ),
    },
    "chemistry": {
        "scope": "Chemistry concept fallback",
        "title": "Chemistry Core Idea",
        "source": "Astra Local JEE Notes",
        "kind": "local_fallback",
        "why": "Local concept fallback used when external source fetch is unavailable.",
        "url": "",
        "text": (
            "Chemistry questions usually work best when you identify the core idea first, then apply the rule, equilibrium, or reaction trend step by step. "
            "For JEE, keep the physical meaning visible rather than memorizing isolated facts."
        ),
    },
    "math": {
        "scope": "Mathematics concept fallback",
        "title": "Mathematics Core Idea",
        "source": "Astra Local JEE Notes",
        "kind": "local_fallback",
        "why": "Local concept fallback used when external source fetch is unavailable.",
        "url": "",
        "text": (
            "Mathematics for JEE works best when you map symbols to meaning first, then manipulate formulas carefully. "
            "For limits, calculus, algebra, and probability, keep the sequence of steps explicit and avoid skipping the reason behind each move."
        ),
    },
}

GENERIC_JEE_LOCAL_NOTE = {
    "scope": "JEE local fallback",
    "title": "Astra JEE Core Notes",
    "source": "Astra Local JEE Notes",
    "kind": "local_fallback",
    "why": "Local concept fallback used when external source fetch is unavailable.",
    "url": "",
    "text": (
        "Astra can explain this from its local JEE knowledge: define the topic clearly, separate the known facts from the unknowns, "
        "use the standard JEE formulas or concepts carefully, and finish with one short check so the idea stays solid."
    ),
}

TOPIC_FOCUS_HINTS = {
    "projectile": {
        "subject": "physics",
        "pack": "projectile_bridge",
        "priority": ["motion", "mechanics", "kinematics"],
    },
    "kinematics": {
        "subject": "physics",
        "pack": "projectile_bridge",
        "priority": ["motion", "velocity", "acceleration"],
    },
    "force": {
        "subject": "physics",
        "pack": "concept_bridge",
        "priority": ["mechanics", "energy", "momentum"],
    },
    "field": {
        "subject": "physics",
        "pack": "electrostatics_depth",
        "priority": ["fields", "charge", "electrostatics"],
    },
    "rotation": {
        "subject": "physics",
        "pack": "jee_advanced_depth",
        "priority": ["mechanics", "momentum", "torque"],
    },
    "probability": {
        "subject": "math",
        "pack": "probability_bridge",
        "priority": ["probability", "statistics"],
    },
    "matrix": {
        "subject": "math",
        "pack": "practice_exam",
        "priority": ["algebra", "linear algebra", "equations"],
    },
    "organic": {
        "subject": "chemistry",
        "pack": "concept_bridge",
        "priority": ["reactions", "mechanism", "bonding"],
    },
    "equilibrium": {
        "subject": "chemistry",
        "pack": "jee_advanced_depth",
        "priority": ["reaction", "thermodynamics"],
    },
}


def _infer_kb_subject(user_input):
    text = _normalize_text(user_input)
    if any(term in text for term in ["physics", "projectile", "motion", "force", "energy", "rotation", "electrostatics"]):
        return "physics"
    if any(term in text for term in ["chemistry", "organic", "reaction", "mechanism", "functional group", "named reaction"]):
        return "chemistry"
    if any(term in text for term in ["math", "mathematics", "calculus", "limit", "derivative", "integral", "differential equation", "probability"]):
        return "mathematics"
    return "general_jee"

QUERY_INTENT_HINTS = {
    "revision": {"revision", "revise", "last minute", "quick recap", "formula sheet", "crash"},
    "strategy": {"strategy", "plan", "how should", "how do i prepare", "study plan", "timetable", "tactics"},
    "practice": {"question", "quiz", "practice", "mock", "drill", "test", "solve"},
    "concept": {"explain", "teach", "understand", "visual", "why", "how does", "derive"},
}


def _normalize_exam_keys(profile):
    keys = set()
    for exam in profile.get("exams", []):
        name = str(exam.get("name", "")).strip().upper()
        if not name:
            continue
        keys.add(name)
        if "ENGINEERING" in name or "SEMESTER" in name or "BTECH" in name or "BE" == name:
            keys.add("ENGINEERING")
        if "MEDICAL" in name or "MBBS" in name or "BDS" in name or "NEET" in name:
            keys.add("MEDICAL")
        if "MBA" in name:
            keys.add("MBA")
        if name == "CA" or "CHARTERED ACCOUNTANCY" in name:
            keys.add("CA")
    if not keys:
        keys.add("COLLEGE")
    return keys


def _normalize_subjects(profile):
    subjects = set()
    for exam in profile.get("exams", []):
        for subject in exam.get("subjects", []):
            clean = str(subject or "").strip().lower()
            if clean:
                subjects.add(clean)
    return subjects


def _infer_query_intent(user_input):
    text = _normalize_text(user_input)
    if not text:
        return {"intent": "concept", "depth": "neutral", "topic": ""}

    for intent, hints in QUERY_INTENT_HINTS.items():
        if any(hint in text for hint in hints):
            depth = "deep" if intent == "concept" else "focused"
            if intent == "revision":
                depth = "quick"
            elif intent == "practice":
                depth = "drill"
            elif intent == "strategy":
                depth = "strategic"
            return {"intent": intent, "depth": depth, "topic": next((topic for topic in TOPIC_FOCUS_HINTS if topic in text), "")}

    return {"intent": "concept", "depth": "neutral", "topic": next((topic for topic in TOPIC_FOCUS_HINTS if topic in text), "")}


def _route_allows_academic_sources(student_state_route):
    route = student_state_route or {}
    tab = _normalize_text(route.get("tab", "tutor"))
    source_policy = _normalize_text(route.get("source_policy", ""))
    if tab in {"lounge", "guide"}:
        return False
    if "no academic source retrieval" in source_policy:
        return False
    if "app only" in source_policy:
        return False
    return True


def _source_pack_for_route(profile, student_state_route=None, user_input=""):
    route = student_state_route or {}
    tab = _normalize_text(route.get("tab", "tutor"))
    pressure = _normalize_text(route.get("pressure", "medium"))
    depth = _normalize_text(route.get("focus_depth", route.get("depth", "")))
    hint = _normalize_text(route.get("source_pack_hint", ""))
    exam_names = _normalize_exam_keys(profile)
    query = _infer_query_intent(user_input)
    query_topic = query.get("topic", "")
    query_intent = query.get("intent", "")
    query_depth = query.get("depth", "")

    if tab == "last_minute":
        return SOURCE_PACKS["last_minute"]
    if tab == "tips":
        return SOURCE_PACKS["tips"]
    if tab == "practice":
        return SOURCE_PACKS["practice_exam"]
    if "rescue pack" in hint or "syllabus-first" in hint:
        return SOURCE_PACKS["last_minute"]
    if "deepening pack" in hint or "deepening" in hint or "deepen" in hint:
        if "jee advanced" in exam_names:
            return SOURCE_PACKS["jee_advanced_depth"]
        return SOURCE_PACKS["concept_bridge"]
    if "pattern pack" in hint or "exam-pattern" in hint:
        return SOURCE_PACKS["practice_exam"]
    if query_intent == "revision" or "revision" in depth or pressure in {"low", "low-medium"}:
        return SOURCE_PACKS["last_minute"]
    if query_intent == "strategy":
        return SOURCE_PACKS["tips"]
    if query_intent == "practice":
        return SOURCE_PACKS["practice_exam"]
    if query_topic and query_topic in TOPIC_FOCUS_HINTS:
        pack_key = TOPIC_FOCUS_HINTS[query_topic].get("pack", "concept_bridge")
        return SOURCE_PACKS.get(pack_key, SOURCE_PACKS["concept_bridge"])
    if "jee advanced" in exam_names or "advanced" in depth or pressure in {"medium-high", "high"}:
        return SOURCE_PACKS["jee_advanced_depth"]
    if "jee main" in exam_names:
        if query_intent == "concept" and query_depth in {"deep", "focused"}:
            return SOURCE_PACKS["concept_bridge"]
        return SOURCE_PACKS["jee_main_fast"]
    return SOURCE_PACKS["default"]


def get_learning_source_pack(profile, student_state_route=None, user_input=""):
    route = student_state_route or build_student_state_route(profile)
    pack = _source_pack_for_route(profile, student_state_route=route, user_input=user_input)
    return {
        "key": next((key for key, value in SOURCE_PACKS.items() if value.get("label") == pack.get("label")), "default"),
        "label": pack.get("label", "Balanced source pack"),
        "reason": pack.get("reason", "General-purpose sources for broad academic support."),
        "max_sources": pack.get("max_sources", 2),
        "kind_priority": list(pack.get("kind_priority", [])),
        "route_policy": route.get("source_policy", ""),
        "route_focus": route.get("focus", ""),
        "route_pressure": route.get("pressure", ""),
        "route_source_pack_hint": route.get("source_pack_hint", ""),
    }


def _route_max_sources(student_state_route, default=2):
    route = student_state_route or {}
    pressure = _normalize_text(route.get("pressure", "medium"))
    focus = _normalize_text(route.get("focus", ""))
    if pressure in {"low", "low-medium"}:
        return 1
    if "recovery" in focus:
        return 1
    if pressure == "medium-high":
        return min(default + 1, 3)
    return default


def _collect_topic_hints(user_input):
    query = _normalize_text(user_input)
    topics = []
    for topic, config in TOPIC_FOCUS_HINTS.items():
        if topic in query:
            topics.append((topic, config))
    return topics


def _gather_topic_resources(user_input, allowed_kinds, seen_urls):
    resources = []
    for _, config in _collect_topic_hints(user_input):
        subject = config.get("subject", "")
        pack_key = config.get("pack", "concept_bridge")
        priority_kinds = set(SOURCE_PACKS.get(pack_key, SOURCE_PACKS["default"]).get("kind_priority", []))
        subject_sources = list(SUBJECT_SOURCE_HINTS.get(subject, []))

        # Keep the list compact and only add one or two topic-specific matches.
        for item in subject_sources:
            if item["url"] in seen_urls:
                continue
            if allowed_kinds and item.get("kind") not in allowed_kinds and item.get("kind") not in priority_kinds:
                continue
            resources.append({"scope": f"{subject.title()} focus", **item})
            seen_urls.add(item["url"])
            if len(resources) >= 2:
                break
        if len(resources) >= 2:
            break
    if not resources:
        lowered = _normalize_text(user_input)
        for topic_key, note in LOCAL_TOPIC_NOTES.items():
            if topic_key in lowered:
                resources.append(note)
                break
    return resources


def get_learning_sources(profile, student_state_route=None, user_input=""):
    if not _route_allows_academic_sources(student_state_route):
        return []

    resources = []
    seen_urls = set()
    pack = _source_pack_for_route(profile, student_state_route=student_state_route)
    allowed_kinds = set(pack.get("kind_priority", []))

    for key in sorted(_normalize_exam_keys(profile)):
        for item in LEARNING_SOURCE_REGISTRY.get(key, []):
            if item["url"] in seen_urls:
                continue
            if allowed_kinds and item.get("kind") not in allowed_kinds:
                continue
            resources.append({"scope": key, **item})
            seen_urls.add(item["url"])

    for subject in sorted(_normalize_subjects(profile)):
        for hint, items in SUBJECT_SOURCE_HINTS.items():
            if hint in subject:
                for item in items:
                    if item["url"] in seen_urls:
                        continue
                    if allowed_kinds and item.get("kind") not in allowed_kinds:
                        continue
                    resources.append({"scope": subject.title(), **item})
                    seen_urls.add(item["url"])

    for item in _gather_topic_resources(user_input, allowed_kinds, seen_urls):
        resources.append(item)

    return resources


def build_learning_sources_context(profile, student_state_route=None, user_input=""):
    if not _route_allows_academic_sources(student_state_route):
        return ""

    resources = get_learning_sources(profile, student_state_route=student_state_route, user_input=user_input)
    if not resources:
        return ""
    lines = ["Trusted open learning sources available for this student:"]
    route = student_state_route or build_student_state_route(profile)
    pack = _source_pack_for_route(profile, student_state_route=route, user_input=user_input)
    if pack.get("label"):
        lines.append(f"- Source pack: {pack['label']}")
    if pack.get("reason"):
        lines.append(f"- Pack reason: {pack['reason']}")
    if route.get("source_policy"):
        lines.append(f"- Route policy: {route['source_policy']}")
    if route.get("source_pack_hint"):
        lines.append(f"- Route source-pack hint: {route['source_pack_hint']}")
    ranked = sorted(resources, key=lambda item: _score_source(item, user_input), reverse=True)
    threshold = 3.0 if user_input else 0.0
    filtered = [item for item in ranked if item.get("url") and _score_source(item, user_input) >= threshold]
    if not filtered:
        filtered = [item for item in ranked if item.get("url")]
    for item in filtered[: pack.get("max_sources", 2)]:
        url = f" {item['url']}" if item.get("url") else ""
        lines.append(f"- {item['scope']}: {item['title']} ({item['source']}) -> {item['why']}{url}")
    if len(lines) == 1:
        lowered = _normalize_text(user_input)
        for topic_key, note in LOCAL_TOPIC_NOTES.items():
            if topic_key in lowered:
                lines.append(f"- Local fallback: {note['title']} ({note['source']}) -> {note['text']}")
                break
        else:
            lines.append(f"- Local fallback: {GENERIC_JEE_LOCAL_NOTE['title']} ({GENERIC_JEE_LOCAL_NOTE['source']}) -> {GENERIC_JEE_LOCAL_NOTE['text']}")
    return "\n".join(lines)


def _normalize_text(value):
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _tokenize(value):
    tokens = re.findall(r"[a-z0-9]+", _normalize_text(value))
    return [token for token in tokens if token not in STOPWORDS and len(token) > 2]


def should_retrieve_learning_sources(user_input, conversation_mode="tutor", student_state_route=None):
    text = _normalize_text(user_input)
    route = student_state_route or {}
    if not text or conversation_mode not in {"tutor", "last_minute", "tips"}:
        return False
    if not _route_allows_academic_sources(route):
        return False
    if route.get("pressure") in {"low", "low-medium"} and len(text.split()) < 4:
        return False

    trigger_phrases = (
        "explain",
        "teach",
        "how does",
        "what is",
        "why does",
        "difference between",
        "derive",
        "concept",
        "formula",
        "revision",
        "portion",
        "syllabus",
    )
    return any(phrase in text for phrase in trigger_phrases) or len(text.split()) >= 5


def _score_source(resource, query_text):
    query_tokens = set(_tokenize(query_text))
    source_tokens = set(
        _tokenize(
            f"{resource.get('scope', '')} {resource.get('title', '')} {resource.get('source', '')} {resource.get('why', '')}"
        )
    )
    tag_tokens = set(_tokenize(" ".join(resource.get("tags", []))))
    if not query_tokens:
        return 0

    score = 0.0
    overlap = query_tokens & source_tokens
    tag_overlap = query_tokens & tag_tokens
    score += len(overlap) * 1.8
    score += len(tag_overlap) * 3.0

    inferred_subjects = set()
    for subject, hints in TOPIC_SUBJECT_HINTS.items():
      if query_tokens & hints:
        inferred_subjects.add(subject)

    resource_text = _normalize_text(f"{resource.get('scope', '')} {' '.join(resource.get('tags', []))}")
    for subject in inferred_subjects:
        if subject in resource_text:
            score += 4.0

    kind = resource.get("kind", "")
    if kind == "official_exam" and inferred_subjects:
        score -= 1.5
    if kind in {"open_course", "open_textbook", "open_reference", "public_medical_learning"} and inferred_subjects:
        score += 1.2

    return score


@lru_cache(maxsize=64)
def _fetch_source_excerpt(url):
    if not url:
        return {"title": "Local fallback", "excerpt": ""}
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "AdaptiveLearningTutor/1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=8) as response:
        payload = response.read().decode("utf-8", errors="ignore")

    title_match = re.search(r"<title[^>]*>(.*?)</title>", payload, flags=re.IGNORECASE | re.DOTALL)
    title = html.unescape(title_match.group(1)).strip() if title_match else ""

    cleaned = re.sub(r"(?is)<script.*?>.*?</script>", " ", payload)
    cleaned = re.sub(r"(?is)<style.*?>.*?</style>", " ", cleaned)
    cleaned = re.sub(r"(?is)<noscript.*?>.*?</noscript>", " ", cleaned)
    cleaned = re.sub(r"(?i)</p>|</div>|</li>|<br\s*/?>", "\n", cleaned)
    cleaned = re.sub(r"(?is)<[^>]+>", " ", cleaned)
    cleaned = html.unescape(cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    excerpt = cleaned[:1200]
    return {"title": title, "excerpt": excerpt}


def retrieve_learning_source_bundle(profile, user_input, max_sources=2, student_state_route=None):
    route = student_state_route or build_student_state_route(profile)
    if not _route_allows_academic_sources(route):
        return {"text": "", "sources": []}

    resources = get_learning_sources(profile, student_state_route=route, user_input=user_input)

    pack = _source_pack_for_route(profile, student_state_route=route, user_input=user_input)
    route_max_sources = min(_route_max_sources(route, default=max_sources), pack.get("max_sources", max_sources))
    ranked = sorted(resources, key=lambda item: _score_source(item, user_input), reverse=True) if resources else []
    selected = [item for item in ranked[: max(route_max_sources * 2, route_max_sources)] if item.get("url")]
    snippets = []
    sources = []

    for resource in selected:
        if not resource.get("url"):
            snippets.append(
                "\n".join(
                    [
                        f"Source scope: {resource.get('scope', '')}",
                        f"Source title: {resource.get('title', '')}",
                        f"Why useful: {resource.get('why', '')}",
                        f"Retrieved page title: Local fallback",
                        f"Retrieved excerpt: {resource.get('text', '') or resource.get('why', '')}",
                    ]
                )
            )
            sources.append(
                {
                    "label": resource.get("title", "Learning source"),
                    "url": "",
                    "kind": resource.get("kind", "local_fallback"),
                }
            )
            if len(sources) >= route_max_sources:
                break
            continue
        try:
            fetched = _fetch_source_excerpt(resource["url"])
        except Exception:
            fetched = {"title": "Local fallback", "excerpt": resource.get("why", "")}
        snippets.append(
            "\n".join(
                [
                    f"Source scope: {resource.get('scope', '')}",
                    f"Source title: {resource.get('title', '')}",
                    f"Why useful: {resource.get('why', '')}",
                    f"Retrieved page title: {fetched.get('title', '')}",
                    f"Retrieved excerpt: {fetched.get('excerpt', '') or resource.get('why', '')}",
                ]
            )
        )
        sources.append(
            {
                "label": resource.get("title", "Learning source"),
                "url": resource.get("url", ""),
                "kind": "learning_source",
            }
        )
        if len(sources) >= route_max_sources:
            break

    if not snippets:
        kb_subject = _infer_kb_subject(user_input)
        kb_chunks = search_knowledge_base(user_input, kb_subject, n_results=3, session_type="tutor")
        if isinstance(kb_chunks, dict):
            kb_items = kb_chunks.get("chunks", []) or []
            kb_context_prompt = str(kb_chunks.get("context_prompt", "")).strip()
        else:
            kb_items = kb_chunks or []
            kb_context_prompt = ""
        if kb_items:
            pyq_chunks = [item["text"] for item in kb_items if item.get("type") == "pyq"]
            concept_chunks = [item["text"] for item in kb_items if item.get("type") != "pyq"]
            if kb_context_prompt:
                kb_context = kb_context_prompt
            elif pyq_chunks:
                kb_context = (
                    "Here are relevant JEE previous year questions on this topic:\n"
                    + "\n\n".join(pyq_chunks)
                    + "\n\nUse these to inform your explanation and mention that these were actual JEE questions."
                )
            else:
                kb_context = (
                    "Here is verified source material on this topic:\n"
                    + "\n\n".join(concept_chunks)
                    + "\n\nUse this to give an accurate explanation."
                )
            snippets.append(
                "\n".join(
                    [
                        f"Source scope: {kb_subject.title()} verified local knowledge base",
                        "Source title: Astra RAG knowledge base",
                        "Why useful: Verified JEE source material stored locally for high-quality tutoring.",
                        "Retrieved page title: Local knowledge base",
                        f"Retrieved excerpt: {kb_context}",
                        f"Now answer: {user_input}",
                    ]
                )
            )
            sources.append(
                {
                    "label": "Astra RAG knowledge base",
                    "url": "",
                    "kind": "knowledge_base",
                }
            )
        else:
            lowered = _normalize_text(user_input)
            for topic_key, note in LOCAL_TOPIC_NOTES.items():
                if topic_key in lowered:
                    snippets.append(
                        "\n".join(
                            [
                                f"Source scope: {note['scope']}",
                                f"Source title: {note['title']}",
                                f"Why useful: {note['why']}",
                                "Retrieved page title: Local fallback",
                                f"Retrieved excerpt: {note['text']}",
                            ]
                        )
                    )
                    sources.append(
                        {
                            "label": note.get("title", "Local fallback"),
                            "url": "",
                            "kind": "local_fallback",
                        }
                    )
                    break
            else:
                snippets.append(
                    "\n".join(
                        [
                            f"Source scope: {GENERIC_JEE_LOCAL_NOTE['scope']}",
                            f"Source title: {GENERIC_JEE_LOCAL_NOTE['title']}",
                            f"Why useful: {GENERIC_JEE_LOCAL_NOTE['why']}",
                            "Retrieved page title: Local fallback",
                            f"Retrieved excerpt: {GENERIC_JEE_LOCAL_NOTE['text']}",
                        ]
                    )
                )
                sources.append(
                    {
                        "label": GENERIC_JEE_LOCAL_NOTE.get("title", "Local fallback"),
                        "url": "",
                        "kind": "local_fallback",
                    }
                )
    if not snippets:
        return {"text": "", "sources": []}

    strict_instruction = ""
    policy = _normalize_text(route.get("source_policy", ""))
    if "verified" in policy or "strict" in policy or "only" in policy:
        strict_instruction = "\n\nCRITICAL SOURCE POLICY: You MUST build your explanation using ONLY the information from these verified sources and any attached syllabus documents. Do not invent formulas or facts outside this scope."
    else:
        strict_instruction = "\n\nUse these retrieved source snippets to make the answer more specific, accurate, and exam-relevant."

    text = (
        "Trusted online learning retrieval for this question:\n"
        f"- Source pack: {pack.get('label', 'Balanced source pack')}\n"
        f"- Pack reason: {pack.get('reason', 'General-purpose sources for broad academic support.')}\n"
        + "\n\n".join(f"- {snippet}" for snippet in snippets)
        + strict_instruction
    )
    return {"text": text, "sources": sources}
