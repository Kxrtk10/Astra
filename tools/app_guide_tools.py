GUIDE_FEATURES = [
    {
        "name": "Tutor",
        "tab": "Tutor",
        "keywords": ["tutor", "concept", "explain", "visual", "doubt", "image", "camera", "learn"],
        "description": "Use Tutor for academic explanations, visual breakdowns, image-doubt solving, and structured concept teaching.",
    },
    {
        "name": "Lounge",
        "tab": "Lounge",
        "keywords": ["lounge", "casual", "talk", "relax", "stress", "life", "current affairs", "general knowledge"],
        "description": "Use Lounge for casual conversation, decompression, general knowledge, current affairs, and emotional breathing room.",
    },
    {
        "name": "Practice",
        "tab": "Practice",
        "keywords": ["practice", "quiz", "pyq", "paper", "rapid fire", "timed", "questions", "accuracy"],
        "description": "Use Practice for quick drills, timed sets, PYQ-style question practice, rapid-fire quizzes, and paper-style sessions.",
    },
    {
        "name": "Assist",
        "tab": "Assist",
        "keywords": ["assist", "feature health", "health", "recheck", "qa", "check system", "working", "bug", "error"],
        "description": "Use Assist to inspect feature health, recheck core app systems, review live learning signals, and confirm the app is behaving correctly.",
    },
    {
        "name": "Last Minute",
        "tab": "Last Minute",
        "keywords": ["last minute", "one night", "one day before", "revision", "crash course", "high yield", "tomorrow exam"],
        "description": "Use Last Minute for JEE one-night revision plans, one-day-before rescue schedules, high-yield checklists, and fast final revision.",
    },
    {
        "name": "Guide",
        "tab": "Guide",
        "keywords": ["guide", "how", "where", "feature", "use app", "help", "navigate"],
        "description": "Use Guide when you are confused about features, tabs, workflows, or how to use the app efficiently.",
    },
    {
        "name": "Tips",
        "tab": "Tips",
        "keywords": ["tips", "strategy", "time management", "hack", "attempt strategy"],
        "description": "Use Tips for exam strategy, paper navigation, time management, and smart test-taking habits.",
    },
    {
        "name": "Network",
        "tab": "Network",
        "keywords": ["network", "circle", "peer", "student", "community", "similar learners"],
        "description": "Use Network to explore similar learners, tutor-network insights, and focused study-circle suggestions.",
    },
    {
        "name": "Weekly Plan",
        "tab": "Weekly Plan",
        "keywords": ["weekly", "plan", "schedule", "today", "progress", "section progress"],
        "description": "Use Weekly Plan to review the 7-day schedule, section progress, strengths, weaknesses, and focus breakdown.",
    },
    {
        "name": "Progress",
        "tab": "Progress",
        "keywords": ["progress tab", "green tick", "brown mark", "red mark", "done", "pending", "needs revision", "chapter tracker", "topic tracker"],
        "description": "Use Progress to mark topics as done, pending, or needing revision, and to see what still deserves attention.",
    },
    {
        "name": "Personalize",
        "tab": "Personalize",
        "keywords": ["personalize", "customize", "theme", "night mode", "voice", "avatar", "exam", "memory"],
        "description": "Use Personalize to edit your JEE track, customize the tutor, change theme or night mode, and manage saved preferences.",
    },
]


GUIDE_QUICK_START = [
    "If you want to understand a topic, start in Tutor.",
    "If you want only questions or a paper, go to Practice.",
    "If your JEE exam is tomorrow and you need a rescue plan, go to Last Minute.",
    "If you need your schedule, open Weekly Plan.",
    "If you want to recheck whether a feature is working, open Assist.",
    "If you want to change your tutor or theme, open Personalize.",
    "If you just want to talk or reset mentally, use Lounge.",
]


def _normalize(text):
    return " ".join((text or "").lower().strip().split())


def _matching_features(user_input):
    text = _normalize(user_input)
    matches = []
    for feature in GUIDE_FEATURES:
        if any(keyword in text for keyword in feature["keywords"]):
            matches.append(feature)
    return matches


def build_app_guide_reply(user_input):
    text = _normalize(user_input)
    if not text:
        return (
            "I am the App Guide. Ask me things like: where do I upload a doubt image, which tab should I use for PYQs, where is night mode, or how do I change my tutor."
        )

    if any(phrase in text for phrase in ["what can you do", "what does this app do", "how should i use this app", "overview of app"]):
        lines = ["Here is the simplest way to use the app well:"]
        lines.extend(f"- {item}" for item in GUIDE_QUICK_START)
        return "\n".join(lines)

    if any(phrase in text for phrase in ["too many features", "confusing", "simplify", "how to start", "where should i begin"]):
        return (
            "Use this app in a simple order: Tutor for learning, Practice for questions, Weekly Plan for scheduling, and Personalize only when you want to change settings. "
            "You do not need every tab on day one."
        )

    if any(phrase in text for phrase in ["feature health", "recheck the app", "check the app", "system health", "is it working", "qa check", "test the feature", "debug feature"]):
        return (
            "Use Assist for feature health checks. It shows whether core systems like Tutor, Practice, Progress, analytics, storage, routing, and engagement are healthy or need attention. "
            "If a feature looks off, that is the best place to start before changing anything else."
        )

    if "night mode" in text or ("dark" in text and "mode" in text):
        return "Night mode is in Personalize -> Layout Controls -> Night mode. You can also use the Midnight theme in Color vibe."

    if "basic mode" in text or "advanced mode" in text or "workspace mode" in text:
        return (
            "Go to Personalize -> Layout Controls -> Workspace mode. Basic mode keeps only the most important tabs visible, "
            "while Advanced mode reveals the full studio."
        )

    matches = _matching_features(text)
    if matches:
        lines = []
        for feature in matches[:3]:
            lines.append(f"{feature['tab']}: {feature['description']}")
        lines.append("If you want, I can also tell you the fastest path for your goal, like learn a concept, practice questions, or change settings.")
        return "\n".join(lines)

    if "image" in text or "upload" in text or "scan" in text:
        return "Go to Tutor, upload your doubt image below the message box, then click Scan doubt image."

    if "voice" in text:
        return "Voice controls are on the left sidebar. Personalize is where you tune the look and feel, while the sidebar lets you speak or stop replies quickly."

    if "exam" in text and ("add" in text or "change" in text or "drop" in text):
        return "Open Personalize -> Manage Your Exams. That is where you add, remove, or update exams, and your plan adapts after that."

    if any(phrase in text for phrase in ["tomorrow exam", "one night", "last minute", "one day before", "revision rescue"]):
        return "Use the Last Minute tab for JEE one-night revision plans, high-yield checklists, and final rescue schedules."

    if any(phrase in text for phrase in ["green tick", "brown mark", "red mark", "track progress", "topic status", "chapter status"]):
        return "Use the Progress tab to mark topics as Done, Needs Revision, or Pending. It also gives gentle reminders about what still deserves attention."

    if "source" in text or "current affairs" in text:
        return "Use Lounge for current affairs or general knowledge. When live grounding is used, the supporting sources appear in Assist."

    return (
        "The fastest layout is: Tutor for learning, Practice for questions, Weekly Plan for scheduling, Lounge for casual talk, and Personalize for settings. "
        "Ask me about any feature by name and I will point you to the right place."
    )
