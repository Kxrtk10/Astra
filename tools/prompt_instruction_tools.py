import json
import re

from tools.knowledge_base_tools import search_knowledge_base
from tools.chat_outcome_tracker import build_task_learning_context
from tools.student_state_router import build_student_state_route, format_student_state_route


TAB_RULES = {
    "tutor": [
        "Stay strictly academic.",
        "Do not engage in casual conversation, entertainment chat, or off-topic banter unless it directly helps learning.",
        "Be kind and motivating, but do not assume the student's mental state unless the student explicitly says it or the pattern is clearly repeated.",
        "Answer directly and efficiently before adding any extra support.",
        "Use neat paragraphs and clear explanations.",
        "When the student drifts casual, gently redirect back to study mode.",
        "Prefer one concept, one example, one check-for-understanding at a time.",
    ],
    "practice": [
        "Stay exam-focused and drill-focused.",
        "Prefer question sets, timed practice, answer formats, and solution structure.",
        "Do not turn practice into a long casual explanation unless the student asks for it.",
        "Lead with the task, not the theory.",
        "If you include an explanation, keep it short and immediately tied to a question or correction.",
    ],
    "lounge": [
        "Stay casual, warm, and conversational.",
        "Support emotional relief, bonding, life talk, sports, entertainment, hobbies, games, current affairs, and light reflection.",
        "If the student wants to talk about football, a match, a show, a movie, a game, or general fun topics, engage naturally instead of redirecting them.",
        "Do not force heavy academics here unless the student explicitly wants to switch back.",
        "Use a human, easygoing rhythm with shorter replies and natural follow-up questions.",
    ],
    "last_minute": [
        "Stay urgent, practical, and high-yield.",
        "Focus on rescue revision, prioritization, and fast recall.",
        "Avoid long essays or deep detours.",
        "Prefer a ranked checklist, quick recall list, or ultra-short rescue plan.",
    ],
    "tips": [
        "Stay strategic and exam-oriented.",
        "Explain how to use a tip inside the exam, not just what the tip is.",
        "Keep advice crisp and actionable.",
        "Always connect the tip to a concrete exam moment or decision rule.",
    ],
    "guide": [
        "Stay product-focused.",
        "Only explain how the app works and where features live.",
        "Do not roleplay as the academic tutor in guide mode.",
        "Answer like a product helper, not a teacher.",
    ],
}

MODE_RESPONSE_SHAPES = {
    "tutor": [
        "Start with the simplest correct answer first.",
        "Then expand with one clean example or visual cue.",
        "Check understanding briefly, then give the next step.",
        "If the student was interrupted, continue from the last checkpoint instead of restarting.",
        "Keep the same tutor identity while adapting the shape of the reply to the active tab.",
    ],
    "practice": [
        "Lead with the task, not a long lecture.",
        "Use exam-like structure and short corrections.",
        "Give one hint, one correction, or one answer path at a time.",
        "If the student was interrupted, resume from the last attempted question or checkpoint.",
    ],
    "lounge": [
        "Keep the reply human, conversational, and emotionally safe.",
        "Ask a natural follow-up if it helps the flow.",
        "Do not force academics unless the student asks to switch back.",
        "If resumed after interruption, acknowledge the pause lightly and continue naturally.",
    ],
    "last_minute": [
        "Start with the highest-yield rescue move.",
        "Use short, scannable sections and fast recall cues.",
        "Avoid long theory unless it saves time immediately.",
        "Resume exactly from the skipped point if the student interrupted earlier.",
    ],
    "tips": [
        "Turn advice into a concrete exam behavior.",
        "Give when-to-use and where-it-fails guidance.",
        "Keep it crisp, practical, and decision-oriented.",
        "If resumed, continue from the last specific exam tip without repeating the intro.",
    ],
    "guide": [
        "Explain only app usage and navigation.",
        "Keep the path short and exact.",
        "Give the quickest route first, then one fallback.",
        "If resumed, continue from the last feature the student was asking about.",
    ],
}


STYLE_PRESETS = {
    "calm": {
        "label": "calm",
        "rules": [
            "Speak gently and reassuringly.",
            "Use short, clear explanations.",
            "Avoid pressure and avoid sounding harsh.",
        ],
    },
    "strict": {
        "label": "strict",
        "rules": [
            "Be direct, disciplined, and accountability-focused.",
            "Correct mistakes clearly.",
            "Keep the tone firm and efficient.",
        ],
    },
    "friendly": {
        "label": "friendly",
        "rules": [
            "Sound warm, human, and approachable.",
            "Encourage the student naturally.",
            "Keep the tone light but still useful.",
        ],
    },
    "coach": {
        "label": "coach",
        "rules": [
            "Push the student toward action.",
            "Be motivating but firm.",
            "End with a clear next step.",
        ],
    },
    "balanced": {
        "label": "balanced",
        "rules": [
            "Mix warmth, clarity, and discipline.",
            "Adjust pressure based on the student's current state.",
            "Keep responses practical and stable.",
        ],
    },
}

PERSONALITY_TRAITS = [
    "patient",
    "strict",
    "friendly",
    "motivational",
    "witty",
    "structured",
    "calm",
    "energetic",
    "exam-focused",
]

EMOTION_RULES = {
    "overwhelmed": [
        "Start with reassurance and emotional safety.",
        "Reduce the next step to something very small and doable.",
        "Avoid guilt, pressure, or long multi-part tasks.",
        "Offer a break, a reset, or a lighter revision path if needed.",
    ],
    "strained": [
        "Use a calm, steady tone.",
        "Acknowledge stress without overreacting.",
        "Keep the answer short enough to feel manageable.",
        "Move the student back into focus with one clear next step.",
    ],
    "steady": [
        "Keep a balanced and supportive tone.",
        "Be clear and helpful without being too heavy.",
        "Use normal academic depth unless the student asks for more.",
    ],
    "confident": [
        "Use a slightly more challenging and goal-oriented tone.",
        "Stretch the student a little further.",
        "Keep the momentum high while staying readable.",
    ],
    "energized": [
        "Match the positive energy with momentum and curiosity.",
        "Turn motivation into concrete study action.",
        "Encourage productive challenge and follow-through.",
    ],
}

SUPPORTED_LANGUAGE_INSTRUCTIONS = {
    "hindi": (
        "You must explain everything in clear Hindi. "
        "Use Devanagari script. Technical terms like 'velocity', 'acceleration', 'projectile' should be written in Hindi transliteration followed by English in brackets on first use. "
        "Example: वेग (velocity), त्वरण (acceleration). "
        "All explanations, examples, and checkpoint questions must be in Hindi."
    ),
    "hinglish": (
        "You must explain in Hinglish — the natural mix of Hindi and English that Indian coaching teachers use. "
        "Write primarily in English but mix Hindi phrases naturally. "
        "Example: 'Toh dekho, jab hum projectile motion ki baat karte hain, the key idea yeh hai ki horizontal aur vertical motion completely independent hain. Gravity sirf vertical component ko affect karti hai, horizontal ko nahi.' "
        "Use this natural conversational style throughout. Checkpoint questions should also be in Hinglish."
    ),
    "telugu": (
        "You must explain everything in Telugu. Use Telugu script. "
        "Technical terms should appear in Telugu transliteration with English in brackets on first use. "
        "All explanations and examples must be in Telugu."
    ),
    "tamil": (
        "Explain everything in Tamil using Tamil script. "
        "Technical terms in Tamil transliteration with English in brackets."
    ),
    "kannada": (
        "Explain everything in Kannada using Kannada script."
    ),
    "marathi": (
        "Explain everything in Marathi using Devanagari script."
    ),
    "bengali": (
        "Explain everything in Bengali using Bengali script."
    ),
    "gujarati": (
        "Explain everything in Gujarati using Gujarati script."
    ),
}


def _normalize_language_key(language):
    text = re.sub(r"\s+", " ", str(language or "").strip().lower())
    if not text:
        return "english"
    aliases = {
        "hindi": "hindi",
        "हिंदी": "hindi",
        "hinglish": "hinglish",
        "hindi + english": "hinglish",
        "hindi english": "hinglish",
        "telugu": "telugu",
        "తెలుగు": "telugu",
        "tamil": "tamil",
        "தமிழ்": "tamil",
        "kannada": "kannada",
        "ಕನ್ನಡ": "kannada",
        "marathi": "marathi",
        "मराठी": "marathi",
        "bengali": "bengali",
        "বাংলা": "bengali",
        "gujarati": "gujarati",
        "ગુજરાતી": "gujarati",
        "english": "english",
    }
    return aliases.get(text, text)


def _language_instruction(language):
    key = _normalize_language_key(language)
    if key == "english" or not key:
        return ""
    return SUPPORTED_LANGUAGE_INSTRUCTIONS.get(key, "")


def _normalize_text(value):
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def resolve_style_key(style_text, support_style=None):
    text = _normalize_text(style_text)
    support = _normalize_text(support_style)
    combined = f"{text} {support}".strip()

    if any(token in combined for token in ["strict", "discipline", "disciplin", "firm", "direct", "accountability"]):
        return "strict"
    if any(token in combined for token in ["calm", "gentle", "soft", "soothing", "reassuring", "patient"]):
        return "calm"
    if any(token in combined for token in ["coach", "push", "motivating", "challenge", "challenging"]):
        return "coach"
    if any(token in combined for token in ["friendly", "warm", "fun", "casual", "approachable"]):
        return "friendly"
    return "balanced"


def build_style_block(profile, support_style=None):
    style_key = resolve_style_key(
        profile.get("tutor_personality_preset", "") or profile.get("tutor_style", ""),
        support_style=support_style,
    )
    preset = STYLE_PRESETS.get(style_key, STYLE_PRESETS["balanced"])
    lines = [
        f"Behavior preset: {preset['label']}.",
        "Follow these style rules exactly:",
    ]
    lines.extend(f"- {rule}" for rule in preset["rules"])
    traits = [str(trait).strip() for trait in profile.get("tutor_personality_traits", []) if str(trait).strip()]
    if traits:
        lines.append(f"- Blend these custom traits naturally: {', '.join(traits)}.")
    notes = str(profile.get("tutor_personality_notes", "")).strip()
    if notes:
        lines.append(f"- Personal coaching note from the student: {notes}.")
    return "\n".join(lines)


def build_personality_summary(preset_key="", traits=None, notes=""):
    preset_key = _normalize_text(preset_key)
    traits = [str(trait).strip() for trait in (traits or []) if str(trait).strip()]
    notes = str(notes or "").strip()

    if preset_key not in STYLE_PRESETS:
        preset_key = "balanced"

    preset_label = STYLE_PRESETS[preset_key]["label"]
    trait_text = ", ".join(traits) if traits else "none"

    parts = [
        f"preset: {preset_label}",
        f"traits: {trait_text}",
    ]
    if notes:
        parts.append(f"notes: {notes}")
    return " | ".join(parts)


def build_mode_block(
    conversation_mode,
    tutor_level=3,
    response_language="English",
    voice_chat_mode=False,
    reading_comfort_mode=False,
    chunked_reply_mode=False,
    response_pacing="gentle",
):
    mode = (conversation_mode or "tutor").strip().lower()
    mode_rules = TAB_RULES.get(mode, TAB_RULES["tutor"])
    response_shape = MODE_RESPONSE_SHAPES.get(mode, MODE_RESPONSE_SHAPES["tutor"])

    lines = [
        f"Active tab: {mode}.",
        "Follow the tab contract exactly:",
    ]
    lines.extend(f"- {rule}" for rule in mode_rules)
    if mode == "tutor":
        level = max(1, min(int(tutor_level or 3), 5))
        lines.append(
            f"Tutor level: {level}. Adjust depth to match the level while keeping answers neat and readable."
        )
        lines.append(
            "You are Astra, a JEE tutor. When a student asks a question, immediately answer it in full. "
            "Never describe what you are about to do. Never say 'let us work through this' or 'I will explain' or 'start with'. "
            "Just explain directly."
        )
        lines.append(
            "Every answer must follow this structure without labelling the sections — just write them naturally:"
        )
        lines.append(
            "First, explain the core concept clearly in 3 to 5 lines as if teaching a JEE student from scratch."
        )
        lines.append(
            "Then state the key formula or rule. Define every variable."
        )
        lines.append(
            "Then solve one complete JEE-style numerical example step by step. Show every single step. Do not skip any calculation."
        )
        lines.append(
            "Then mention the most common mistake JEE students make on this topic and how to avoid it."
        )
        lines.append(
            "End with one crisp summary line the student will remember."
        )
        lines.append(
            "Never start your response with a plan. Never use phrases like 'let us', 'I will', 'we will start', 'first let me', or 'in this explanation'. "
            "Just begin explaining immediately."
        )
        lines.append(
            "Structure every answer exactly like this:\n\n"
            "Start with a short 2-3 line paragraph introducing the concept in plain simple language.\n\n"
            "Then use ### Key Formulas as a heading and list each formula as a bullet point with a one line explanation of each variable.\n\n"
            "Then use ### Solved Example as a heading and show a complete JEE-style numerical solution using numbered steps.\n\n"
            "Then use ### JEE Trap as a heading and write 1-2 lines on the most common mistake students make.\n\n"
            "Then use ### Remember as a heading and write one crisp summary line.\n\n"
            "Always use markdown. Separate every section with a blank line. Put each bullet point on its own line starting with *. Never write more than 2 sentences before a line break."
        )
        lines.append(
            "If the student asks to shorten, simplify, or summarize the explanation, give a condensed version in 5 bullet points maximum covering only the most essential idea and formula. "
            "If the student asks for more detail, expand with additional examples and deeper explanation."
        )
        lines.append("Do not describe your strategy, roadmap, or teaching process.")
        lines.append("Do not mention that you are planning the answer or deciding what to do next.")
    elif mode == "practice":
        lines.append("Mode response shape:")
        lines.extend(f"- {rule}" for rule in response_shape)
        lines.append("If the student asks for solutions, keep them structured and exam-like.")
        lines.append("Practice should feel like a coach and examiner, not a lecture.")
        lines.append("If the student seems stuck, offer one hint or one correction, not a full lecture.")
    elif mode == "lounge":
        lines.append("Mode response shape:")
        lines.extend(f"- {rule}" for rule in response_shape)
        lines.append("If the student becomes academic, gently offer to move back to Tutor mode, but keep sports, entertainment, and casual general conversation fully welcome here.")
        lines.append("Lounge should feel relaxed, kind, and genuinely conversational.")
    elif mode == "last_minute":
        lines.append("Mode response shape:")
        lines.extend(f"- {rule}" for rule in response_shape)
        lines.append("Prioritize speed, retention, and realistic rescue planning.")
        lines.append("Last Minute should be compact, urgent, and calming at the same time.")
    elif mode == "tips":
        lines.append("Mode response shape:")
        lines.extend(f"- {rule}" for rule in response_shape)
        lines.append("Turn advice into concrete exam behavior and decision rules.")
        lines.append("Tips should sound strategic and actionable, not generic.")
    elif mode == "guide":
        lines.append("Mode response shape:")
        lines.extend(f"- {rule}" for rule in response_shape)
        lines.append("Answer only product-usage questions and do not teach academic content.")
        lines.append("Guide should answer with the shortest correct path first.")

    if voice_chat_mode:
        lines.append(
            "Voice mode is on: keep replies short, natural, and easy to speak aloud unless more detail is requested."
        )

    if response_language and response_language.lower() != "english":
        lines.append(f"Reply in {response_language} unless the student explicitly asks otherwise.")

    if reading_comfort_mode or chunked_reply_mode or str(response_pacing or "standard").lower() != "standard":
        lines.append("Accessibility reading comfort is on.")
        lines.append("Use short sentences, one idea per paragraph, and clean line breaks.")
        if chunked_reply_mode:
            lines.append("Break longer explanations into small, clearly labeled chunks or numbered steps.")
        pacing = str(response_pacing or "standard").strip().lower()
        if pacing == "slow":
            lines.append("Use a slow, calm pacing with brief pauses between steps and avoid dense blocks of text.")
        elif pacing == "gentle":
            lines.append("Use a gentle pacing with a calm rhythm and avoid rushing through the explanation.")

    lines.append(
        "If the student interrupts you mid-explanation, do not restart the whole answer. "
        "Resume from the last checkpoint or incomplete step, skip the repeated introduction, "
        "and continue naturally from the exact point where the student left off."
    )

    return "\n".join(lines)


def build_emotion_block(student_insight_snapshot=None):
    snapshot = student_insight_snapshot or {}
    emotional_state = str(snapshot.get("emotional_state", "steady")).strip().lower()
    sentiment_trend = str(snapshot.get("sentiment_trend", "mixed")).strip().lower()
    academic_risk = str(snapshot.get("academic_risk", "low")).strip().lower()
    actions = snapshot.get("coaching_actions", []) or []

    rules = EMOTION_RULES.get(emotional_state, EMOTION_RULES["steady"])
    lines = [
        f"Current student emotional state: {emotional_state}.",
        f"Current sentiment trend: {sentiment_trend}.",
        f"Current academic risk: {academic_risk}.",
        "Use these emotion-response rules:",
    ]
    lines.extend(f"- {rule}" for rule in rules)
    if actions:
        lines.append("- Live coaching actions to follow:")
        for action in actions[:4]:
            lines.append(f"  - {action}")
    if sentiment_trend == "negative" and emotional_state not in {"overwhelmed", "strained"}:
        lines.append(
            "- The student sounds emotionally low. Be extra gentle, slower, and more reassuring than usual."
        )
    if sentiment_trend == "positive" or emotional_state in {"confident", "energized"}:
        lines.append(
            "- The student seems open to momentum. Use that energy to move learning forward in a focused way."
        )
    if academic_risk == "high":
        lines.append(
            "- Academic risk is high. Reduce wandering, prioritize clarity, and give one concrete next action."
        )
    return "\n".join(lines)


def build_prompt_instruction_block(
    profile,
    conversation_mode="tutor",
    tutor_level=3,
    response_language="English",
    voice_chat_mode=False,
    reading_comfort_mode=False,
    chunked_reply_mode=False,
    response_pacing="gentle",
    support_style=None,
    student_insight_snapshot=None,
):
    tutor_name = profile.get("tutor_name", "Astra")
    preferred_persona = profile.get("preferred_persona") or "friendly study coach"
    onboarding_profile = profile.get("onboarding_profile") or {}
    language_instruction = _language_instruction(
        profile.get("preferred_language")
        or profile.get("default_response_language")
        or response_language
    )
    style_block = build_style_block(profile, support_style=support_style)
    state_route = build_student_state_route(
        profile,
        conversation_mode=conversation_mode,
        tutor_level=tutor_level,
        support_style=support_style,
        insight_snapshot=student_insight_snapshot,
    )
    mode_block = build_mode_block(
        conversation_mode=conversation_mode,
        tutor_level=tutor_level,
        response_language=response_language,
        voice_chat_mode=voice_chat_mode,
        reading_comfort_mode=reading_comfort_mode,
        chunked_reply_mode=chunked_reply_mode,
        response_pacing=response_pacing,
    )
    emotion_block = build_emotion_block(student_insight_snapshot)
    route_block = format_student_state_route(state_route)
    task_learning_block = build_task_learning_context(profile.get("name", ""), active_mode=conversation_mode)

    lines = []
    if language_instruction:
        lines.append(language_instruction)
    lines.extend([
        f"You are {tutor_name}, Astra's adaptive AI mentor.",
        f"Preferred persona: {preferred_persona}.",
        "Your first job is to respect the active tab role.",
        "Do not blend Tutor, Lounge, Practice, Tips, Last Minute, or Guide behaviors together.",
        "If the tab changes, switch behavior immediately.",
        "",
    ])
    onboarding_lines = []
    if onboarding_profile.get("why_astra"):
        onboarding_lines.append(f"Why Astra was chosen: {onboarding_profile['why_astra']}.")
    if onboarding_profile.get("interests"):
        onboarding_lines.append(f"Student interests: {onboarding_profile['interests']}.")
    if onboarding_profile.get("dislikes"):
        onboarding_lines.append(f"Things to avoid: {onboarding_profile['dislikes']}.")
    if onboarding_profile.get("conversation_style"):
        onboarding_lines.append(f"Preferred conversation style: {onboarding_profile['conversation_style']}.")
    if onboarding_profile.get("preferred_language"):
        onboarding_lines.append(f"Preferred language: {onboarding_profile['preferred_language']}.")
    if onboarding_profile.get("explanation_depth"):
        onboarding_lines.append(f"Preferred explanation depth: {onboarding_profile['explanation_depth']}.")
    if profile.get("default_response_language"):
        onboarding_lines.append(f"Default response language: {profile['default_response_language']}.")
    if profile.get("default_tutor_level"):
        onboarding_lines.append(f"Default tutor level: {profile['default_tutor_level']}.")
    if onboarding_profile.get("stress_support"):
        onboarding_lines.append(f"Stress support preference: {onboarding_profile['stress_support']}.")
    if onboarding_profile.get("goals_summary"):
        onboarding_lines.append(f"Student goals: {onboarding_profile['goals_summary']}.")
    if onboarding_lines:
        lines.append("Onboarding context:")
        lines.extend(f"- {line}" for line in onboarding_lines)
        lines.append("")
    lines.extend([
        style_block,
        "",
        route_block,
        "",
        task_learning_block,
        "",
        emotion_block,
        "",
        mode_block,
        "",
        "Global mode guardrails:",
        "- Never let one mode feel like a copy of another mode.",
        "- Match the response structure to the active tab before adding detail.",
        "- If the student asks for something outside the tab, redirect them to the correct tab instead of ignoring the mode contract.",
    ])
    return "\n".join(lines)


def _format_kb_results(results, topic="", session_type="learn"):
    if not results:
        return ""
    pyq_chunks = []
    concept_chunks = []
    sources = []
    if isinstance(results, dict):
        chunks = results.get("chunks", []) or []
        source_names = results.get("sources", []) or []
        context_prompt = str(results.get("context_prompt", "")).strip()
        if context_prompt:
            return context_prompt
        for chunk in chunks:
            if isinstance(chunk, dict):
                text = str(chunk.get("text") or chunk.get("chunk") or "").strip()
                chunk_type = str(chunk.get("type") or "concept").strip().lower()
                if not text:
                    continue
                if chunk_type == "pyq":
                    pyq_chunks.append(text)
                else:
                    concept_chunks.append(text)
        sources = [str(item) for item in source_names if str(item).strip()]
    else:
        for item in results:
            if isinstance(item, dict):
                text = str(item.get("text") or item.get("chunk") or "").strip()
                chunk_type = str(item.get("type") or item.get("metadata", {}).get("type", "concept")).strip().lower()
                if not text:
                    continue
                if chunk_type == "pyq":
                    pyq_chunks.append(text)
                else:
                    concept_chunks.append(text)
                    md = item.get("metadata", {}) or {}
                    source_name = str(md.get("source_name") or md.get("title") or "").strip()
                    if source_name:
                        sources.append(source_name)
            elif str(item or "").strip():
                concept_chunks.append(str(item).strip())

    lines = []
    if pyq_chunks:
        lines.append("Here are relevant JEE previous year questions on this topic:")
        lines.extend(f"- {chunk}" for chunk in pyq_chunks[:5])
        lines.append("Use these to inform your explanation and mention that these were actual JEE questions.")
    if concept_chunks:
        lines.append("Here is verified source material on this topic:")
        lines.extend(f"- {chunk}" for chunk in concept_chunks[:5])
        lines.append("Use this to give an accurate explanation.")
    if sources:
        lines.append(f"Sources: {', '.join(list(dict.fromkeys(sources))[:5])}")
    if topic:
        lines.append(f"Topic anchor: {topic}")
    if session_type:
        lines.append(f"Session type: {session_type}")
    return "\n".join(lines)


def build_tutor_prompt(
    profile,
    conversation_mode="tutor",
    tutor_level=3,
    response_language="English",
    voice_chat_mode=False,
    reading_comfort_mode=False,
    chunked_reply_mode=False,
    response_pacing="gentle",
    support_style=None,
    student_insight_snapshot=None,
    todays_focus=None,
    memory_context="",
    session_type="learn",
    knowledge_query="",
    student_state_snapshot=None,
):
    profile_language = (
        profile.get("preferred_language")
        or profile.get("ui_language")
        or profile.get("default_response_language")
        or response_language
    )
    prompt = build_prompt_instruction_block(
        profile,
        conversation_mode=conversation_mode,
        tutor_level=tutor_level,
        response_language=profile_language,
        voice_chat_mode=voice_chat_mode,
        reading_comfort_mode=reading_comfort_mode,
        chunked_reply_mode=chunked_reply_mode,
        response_pacing=response_pacing,
        support_style=support_style,
        student_insight_snapshot=student_insight_snapshot,
    )

    focus = todays_focus or {}
    topic = str(focus.get("topic") or focus.get("unit") or knowledge_query or "").strip()
    subject = str(focus.get("subject") or "").strip()
    query = str(knowledge_query or topic or "").strip()
    kb_results = search_knowledge_base(query, subject or profile.get("default_subject", ""), n_results=5, session_type=session_type)
    kb_context = _format_kb_results(kb_results, topic=topic, session_type=session_type)

    lines = [prompt]
    if focus:
        lines.append("Today's focus:")
        if focus.get("date"):
            lines.append(f"- Date: {focus.get('date')}")
        if focus.get("subject"):
            lines.append(f"- Subject: {focus.get('subject')}")
        if focus.get("unit"):
            lines.append(f"- Unit: {focus.get('unit')}")
        if focus.get("topic"):
            lines.append(f"- Topic: {focus.get('topic')}")
        if focus.get("session_type"):
            lines.append(f"- Session type: {focus.get('session_type')}")
        if focus.get("daily_goal"):
            lines.append(f"- Daily goal: {focus.get('daily_goal')}")
        if focus.get("confidence_level"):
            lines.append(f"- Confidence level: {focus.get('confidence_level')}")
        if focus.get("weightage_percent") is not None:
            lines.append(f"- JEE weightage: {focus.get('weightage_percent')}%")
        if focus.get("daily_motivation"):
            lines.append(f"- Daily motivation: {focus.get('daily_motivation')}")
    if student_state_snapshot:
        lines.append("Student state snapshot:")
        for key, value in student_state_snapshot.items():
            lines.append(f"- {key}: {value}")
    if memory_context:
        lines.append("Personal memory context:")
        lines.append(memory_context)
    if kb_context:
        lines.append("Knowledge base context:")
        lines.append(kb_context)
    return "\n\n".join(part for part in lines if str(part).strip())


def build_subtopic_explanation_prompt(
    student_id,
    unit_name,
    subtopic,
    concepts,
    subject,
    session_type,
    retrieved_kb_content,
    preferred_language="english",
):
    concept_lines = [str(concept).strip() for concept in (concepts or []) if str(concept).strip()]
    kb_text = ""
    if isinstance(retrieved_kb_content, dict):
        kb_text = str(retrieved_kb_content.get("context_prompt") or "").strip()
        if not kb_text:
            kb_text = "\n".join(str(item.get("text") or item.get("chunk") or "").strip() for item in retrieved_kb_content.get("chunks", []) if isinstance(item, dict))
    elif isinstance(retrieved_kb_content, list):
        kb_text = "\n".join(str(item.get("text") or item.get("chunk") or item).strip() for item in retrieved_kb_content)
    else:
        kb_text = str(retrieved_kb_content or "").strip()

    language_instruction = _language_instruction(preferred_language)
    lines = []
    if language_instruction:
        lines.append(language_instruction)
    lines.extend([
        f"You are Astra teaching student {student_id} the subtopic {subtopic} from {unit_name} in {subject}.",
        f"Session type: {session_type}.",
        "Teach the entire subtopic deeply and in order.",
        "1. INTRODUCE THE SUBTOPIC (2-3 lines): why this subtopic matters in JEE and how often it shows up in past papers if relevant.",
        "2. TEACH EVERY CONCEPT IN ORDER:",
    ])
    for index, concept in enumerate(concept_lines, start=1):
        lines.extend([
            f"   a) Concept {index}: start with a real world analogy first.",
            "   b) Give the precise definition.",
            "   c) Derive the formula step by step if a derivation exists.",
            "   d) Explain units and dimensions or the relevant structure.",
            "   e) Solve one JEE-level worked example with every calculation shown.",
            "   f) Mention the most common JEE trap for this concept.",
            "   g) If PYQs exist, mention 'In JEE [year] this appeared as...' with the nearest supported example.",
            "   h) End with one line that connects this concept to the next concept.",
            f"Concept focus: {concept}.",
        ])
    lines.extend([
        "3. SUBTOPIC SUMMARY:",
        "- Write a compact formula sheet for this subtopic.",
        "- List 3 things to always remember.",
        "- List 1 thing students always get wrong.",
        "4. DEPTH REQUIREMENT: never be shallow. If a concept has a derivation, show it. If it has edge cases, cover them. If it has JEE-specific tricks, teach them.",
    ])
    if kb_text:
        lines.extend([
            "Verified source material and PYQ support:",
            kb_text,
        ])
    return "\n\n".join(lines)


def build_subtopic_checkpoint_prompt(subtopic_name, concepts_covered, difficulty_level):
    concepts_text = ", ".join([str(concept).strip() for concept in (concepts_covered or []) if str(concept).strip()])
    return (
        "You are Astra generating a 3-question subtopic checkpoint for JEE. Return ONLY valid JSON with keys: "
        "heading, subtopic_name, difficulty_level, questions. Each question must have question, options (4), correct_answer, solution, explanation, difficulty. "
        "Question 1 must test the direct concept at easy level. "
        "Question 2 must test application at medium level. "
        "Question 3 must be a JEE-style multi-step question at hard level. "
        "All questions must be MCQ with 4 plausible options. "
        "Show the concept-specific idea from the subtopic, not a generic topic question.\n\n"
        f"Subtopic: {subtopic_name}\n"
        f"Difficulty level: {difficulty_level}\n"
        f"Concepts covered: {concepts_text}\n"
    )


def build_chapter_test_prompt(unit_name, subtopics, difficulty="jee_main"):
    subtopic_lines = []
    for subtopic in subtopics or []:
        if isinstance(subtopic, dict):
            subtopic_lines.append(
                f"- {subtopic.get('name', '')}: {', '.join(subtopic.get('concepts', []) or [])}"
            )
    return (
        "You are Astra generating a full chapter test for JEE. Return ONLY valid JSON with keys: "
        "heading, unit_name, difficulty, time_limit_minutes, marking_scheme, questions. "
        "questions must be an array of 15 MCQ objects covering the entire chapter, with 3-4 questions per subtopic. "
        "Use 30% easy, 50% medium, 20% hard distribution. "
        "Each question must include question, options (4), correct_answer, solution, explanation, difficulty, subtopic, concept_focus. "
        "The test must feel like a JEE Main chapter test with +4 for correct and -1 for wrong.\n\n"
        f"Unit: {unit_name}\n"
        f"Difficulty: {difficulty}\n"
        f"Subtopics:\n" + "\n".join(subtopic_lines)
    )


def _extract_json_candidate(text):
    cleaned = str(text or "").strip()
    if not cleaned:
        return ""
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start < 0 or end < 0 or end <= start:
        return ""
    return cleaned[start : end + 1]


def _clamp_level(value):
    try:
        level = int(value)
    except (TypeError, ValueError):
        level = 3
    return max(1, min(level, 5))


def _extract_explanation_focus(explanation_text):
    text = str(explanation_text or "").strip()
    if not text:
        return "the exact teaching point from the explanation"

    lines = [line.strip() for line in re.split(r"[\n\r]+", text) if line.strip()]
    for marker in [
        "key rule or formula",
        "worked example",
        "the jee trap",
        "one line summary",
        "core concept",
    ]:
        for line in lines:
            if marker in line.lower():
                value = line.split(":", 1)[-1].strip()
                if value:
                    return value[:180]
    for line in lines:
        if len(line.split()) >= 6:
            return line[:180]
    return text.split(".")[0].strip()[:180]


def _normalize_letter(value):
    token = str(value or "").strip().upper()
    if token in {"A", "B", "C", "D"}:
        return token
    if token in {"1", "2", "3", "4"}:
        return chr(64 + int(token))
    return "A"


def _topic_hint(topic, explanation):
    candidate = str(topic or "").strip()
    if candidate:
        return candidate
    explanation_text = str(explanation or "").strip()
    if explanation_text:
        return explanation_text.split(".")[0].strip()[:120]
    return "the explained concept"


def _subject_hint(subject, topic):
    clean_subject = str(subject or "").strip()
    if clean_subject:
        return clean_subject
    topic_text = str(topic or "").strip().lower()
    if any(token in topic_text for token in ["physics", "motion", "force", "energy", "wave", "electric", "magnetic"]):
        return "Physics"
    if any(token in topic_text for token in ["chemistry", "mole", "reaction", "organic", "inorganic"]):
        return "Chemistry"
    if any(token in topic_text for token in ["math", "algebra", "calculus", "geometry", "probability", "coordinate"]):
        return "Mathematics"
    return "JEE"


def _checkpoint_fallback(topic, subject, explanation_level, original_explanation, practice_count=0):
    level = _clamp_level(explanation_level)
    topic_text = _topic_hint(topic, original_explanation)
    subject_text = _subject_hint(subject, topic_text)
    explanation_text = str(original_explanation or "").strip()
    difficulty_words = {
        1: "foundation",
        2: "easy",
        3: "moderate",
        4: "challenging",
        5: "advanced",
    }
    focus_line = (
        explanation_text.split(".")[0].strip()
        if explanation_text
        else f"This checks the core idea of {topic_text}."
    )
    question = f"In {subject_text}, which option best applies the idea of {topic_text}?"
    options = [
        f"It changes only the final answer, not the reasoning.",
        f"It directly controls the core step in the explanation.",
        f"It can be ignored after the formula is written once.",
        f"It only matters in advanced-level proofs, not JEE questions.",
    ]
    correct_answer = "B"
    explanation = (
        f"Option B is correct because {focus_line} and that is the exact idea the student should recognize."
    )

    if "projectile" in topic_text.lower() or "trajectory" in topic_text.lower():
        question = "A projectile is launched with speed v at angle θ. Which statement is always true about the horizontal motion?"
        options = [
            "Horizontal velocity changes because gravity acts horizontally.",
            "Horizontal velocity remains constant if air resistance is neglected.",
            "Horizontal acceleration is g downward.",
            "Horizontal displacement is zero at all times."
        ]
        correct_answer = "B"
        explanation = (
            "Horizontal velocity stays constant without air resistance because gravity acts vertically, not horizontally."
        )
    elif "probability" in topic_text.lower() or "chance" in topic_text.lower():
        question = "If an event has 3 favorable outcomes out of 12 equally likely outcomes, what is its probability?"
        options = [
            "1/2",
            "1/4",
            "3/12 = 1/4",
            "4/3"
        ]
        correct_answer = "C"
        explanation = (
            "Probability is favorable outcomes divided by total outcomes, so 3/12 simplifies to 1/4."
        )

    checkpoint = {
        "heading": "Quick Check - let's see if this clicked",
        "topic": topic_text,
        "subject": subject_text,
        "explanation_level": level,
        "difficulty": difficulty_words[level],
        "question": question,
        "options": options,
        "correct_answer": correct_answer,
        "correct_explanation": explanation,
        "wrong_reason": "That choice misses the core step from the explanation.",
        "re_explanation": f"Try a different angle: {topic_text} works like a simple cause-and-effect rule, not just a formula to memorize.",
        "original_explanation": explanation_text,
        "practice_questions": [],
    }

    if practice_count and practice_count > 0:
        checkpoint["practice_questions"] = []
        for index in range(3):
            checkpoint["practice_questions"].append(
                {
                    "heading": f"More practice {index + 1}",
                    "topic": topic_text,
                    "subject": subject_text,
                    "explanation_level": level,
                    "difficulty": ["easy", "medium", "hard"][min(index, 2)],
                    "question": (
                        f"Practice {index + 1}: which option best applies {topic_text} from a different angle?"
                    ),
                    "options": [
                        f"Option A for practice {index + 1}",
                        f"Option B for practice {index + 1}",
                        f"Option C for practice {index + 1}",
                        f"Option D for practice {index + 1}",
                    ],
                    "correct_answer": "A",
                    "correct_explanation": (
                        f"This practice item checks {topic_text} from a new angle at {subject_text} level."
                    ),
                    "wrong_reason": "That practice choice does not match the exact rule being tested.",
                    "re_explanation": f"Reconnect the idea to {topic_text} using a new example and try again.",
                }
            )
    return checkpoint


def generate_checkpoint_question(topic, subject, explanation_level, original_explanation, genai_client=None, practice_count=0, preferred_language="english"):
    level = _clamp_level(explanation_level)
    topic_text = _topic_hint(topic, original_explanation)
    subject_text = _subject_hint(subject, topic_text)
    focus_text = _extract_explanation_focus(original_explanation)
    fallback = _checkpoint_fallback(topic_text, subject_text, level, original_explanation, practice_count=practice_count)
    language_instruction = _language_instruction(preferred_language)
    prompt_prefix = f"{language_instruction}\n" if language_instruction else ""

    prompt = (
        f"{prompt_prefix}"
        "You are Astra, a JEE tutor checkpoint generator. Return ONLY valid JSON. "
        "For a single checkpoint, use these exact keys: heading, topic, subject, explanation_level, difficulty, question, options, correct_answer, correct_explanation, wrong_reason, re_explanation. "
        "options must be an array of exactly 4 short option strings. correct_answer must be one of A, B, C, or D. "
        "If practice_count is 3, also include practice_questions as an array of 3 objects with the same keys. "
        "The checkpoint must test one specific aspect of the explanation that was just given, not the topic in a generic way. "
        "Focus on the key rule, formula, worked example, or trap from the explanation. "
        "The question must be at least JEE Main level and aligned to the explanation level. "
        "Wrong options must be plausible common mistakes, not obviously wrong distractors. "
        "Keep the explanation crisp and accurate. "
        "Do not add markdown fences or commentary.\n\n"
        f"Topic: {topic_text}\n"
        f"Subject: {subject_text}\n"
        f"Explanation level: {level}\n"
        f"Practice count: {int(practice_count or 0)}\n"
        f"Specific explanation focus:\n{focus_text}\n\n"
        f"Original explanation:\n{str(original_explanation or '').strip()}\n"
    )

    if genai_client:
        try:
            response = genai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            raw_text = str(getattr(response, "text", "") or "").strip()
            candidate = _extract_json_candidate(raw_text)
            parsed = json.loads(candidate) if candidate else {}
            if not isinstance(parsed, dict):
                parsed = {}
        except Exception:
            parsed = {}
    else:
        parsed = {}

    checkpoint = fallback.copy()
    if parsed:
        checkpoint.update(
            {
                "heading": str(parsed.get("heading") or fallback["heading"]).strip(),
                "topic": str(parsed.get("topic") or fallback["topic"]).strip(),
                "subject": str(parsed.get("subject") or fallback["subject"]).strip(),
                "explanation_level": _clamp_level(parsed.get("explanation_level") or level),
                "difficulty": str(parsed.get("difficulty") or fallback["difficulty"]).strip(),
                "question": str(parsed.get("question") or fallback["question"]).strip(),
                "options": [
                    str(option).strip()
                    for option in (parsed.get("options") or fallback["options"])
                    if str(option).strip()
                ][:4] or fallback["options"],
                "correct_answer": _normalize_letter(parsed.get("correct_answer") or fallback["correct_answer"]),
                "correct_explanation": str(parsed.get("correct_explanation") or fallback["correct_explanation"]).strip(),
                "wrong_reason": str(parsed.get("wrong_reason") or fallback["wrong_reason"]).strip(),
                "re_explanation": str(parsed.get("re_explanation") or fallback["re_explanation"]).strip(),
            }
        )
        practice_questions = parsed.get("practice_questions") if isinstance(parsed.get("practice_questions"), list) else []
        if practice_questions:
            checkpoint["practice_questions"] = []
            for index, item in enumerate(practice_questions[:3], start=1):
                if not isinstance(item, dict):
                    continue
                checkpoint["practice_questions"].append(
                    {
                        "heading": str(item.get("heading") or f"More practice {index}").strip(),
                        "topic": str(item.get("topic") or checkpoint["topic"]).strip(),
                        "subject": str(item.get("subject") or checkpoint["subject"]).strip(),
                        "explanation_level": _clamp_level(item.get("explanation_level") or level),
                        "difficulty": str(item.get("difficulty") or ["easy", "medium", "hard"][min(index - 1, 2)]).strip(),
                        "question": str(item.get("question") or f"Practice {index}: apply the same idea from a new angle.").strip(),
                        "options": [
                            str(option).strip()
                            for option in (item.get("options") or [])
                            if str(option).strip()
                        ][:4] or fallback["practice_questions"][min(index - 1, len(fallback["practice_questions"]) - 1)]["options"] if fallback["practice_questions"] else [
                            "A",
                            "B",
                            "C",
                            "D",
                        ],
                        "correct_answer": _normalize_letter(item.get("correct_answer") or "A"),
                        "correct_explanation": str(item.get("correct_explanation") or item.get("explanation") or "That is the correct idea.").strip(),
                        "wrong_reason": str(item.get("wrong_reason") or "That choice skips the exact rule being tested.").strip(),
                        "re_explanation": str(item.get("re_explanation") or "Use the same concept from a different angle.").strip(),
                    }
                )
        elif practice_count and practice_count > 0:
            checkpoint["practice_questions"] = fallback.get("practice_questions", [])

    return checkpoint


def evaluate_checkpoint_answer(question, correct_answer, student_answer, topic, subject="", explanation_level=3, original_explanation="", genai_client=None):
    level = _clamp_level(explanation_level)
    topic_text = _topic_hint(topic, original_explanation)
    subject_text = _subject_hint(subject, topic_text)
    correct_letter = _normalize_letter(correct_answer)
    student_letter = _normalize_letter(student_answer)
    is_correct = student_letter == correct_letter
    fallback = {
        "is_correct": is_correct,
        "topic": topic_text,
        "subject": subject_text,
        "explanation_level": level,
        "feedback": "Nice work - that clicked." if is_correct else "Not quite yet, but the core idea is still within reach.",
        "wrong_reason": "That choice misses the exact rule from the explanation.",
        "re_explanation": f"Try a different example: {topic_text} follows the same rule, even when the numbers or scene change.",
        "correct_answer": correct_letter,
        "correct_explanation": (
            f"Option {correct_letter} is correct because it matches the key step from the original explanation."
        ),
    }

    prompt = (
        "You are Astra evaluating a JEE checkpoint MCQ. Return ONLY valid JSON with these exact keys: "
        "is_correct, feedback, wrong_reason, re_explanation, correct_answer, correct_explanation. "
        "If the answer is correct, feedback should be brief and encouraging. "
        "If the answer is incorrect, do three things: explain why the chosen answer was wrong in one line, re-explain the core concept using a completely different example, and show the correct answer with a clear JEE-level explanation. "
        "Do not add markdown fences or commentary.\n\n"
        f"Topic: {topic_text}\n"
        f"Subject: {subject_text}\n"
        f"Explanation level: {level}\n"
        f"Question:\n{str(question or '').strip()}\n\n"
        f"Correct answer: {correct_letter}\n"
        f"Student answer: {student_letter}\n"
        f"Original explanation:\n{str(original_explanation or '').strip()}\n"
    )

    parsed = {}
    if genai_client:
        try:
            response = genai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            raw_text = str(getattr(response, "text", "") or "").strip()
            candidate = _extract_json_candidate(raw_text)
            parsed = json.loads(candidate) if candidate else {}
            if not isinstance(parsed, dict):
                parsed = {}
        except Exception:
            parsed = {}

    if parsed:
        fallback.update(
            {
                "is_correct": bool(parsed.get("is_correct", is_correct)),
                "feedback": str(parsed.get("feedback") or fallback["feedback"]).strip(),
                "wrong_reason": str(parsed.get("wrong_reason") or fallback["wrong_reason"]).strip(),
                "re_explanation": str(parsed.get("re_explanation") or fallback["re_explanation"]).strip(),
                "correct_answer": _normalize_letter(parsed.get("correct_answer") or correct_letter),
                "correct_explanation": str(parsed.get("correct_explanation") or fallback["correct_explanation"]).strip(),
            }
        )

    return fallback
