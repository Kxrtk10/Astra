import asyncio
import logging
import os
import re
import sys
import ctypes
import time

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content

from agents.supervisor_agent import supervisor_agent
from tools.behavior_tools import format_behavior_report, record_behavior_event
from tools.engagement_tools import (
    award_points,
    break_streak,
    format_points_summary,
    record_bond_interaction,
    record_daily_completion,
)
from tools.planner_tools import (
    DEFAULT_EXAM_SUBJECTS,
    format_study_plan,
    format_today_schedule,
    format_weekly_schedule,
    get_exam_entries,
    get_missing_mock_subjects,
    load_planner_state,
    mark_today_complete,
    mark_today_missed,
    save_mock_scores,
)
from tools.profile_tools import create_profile, load_profile, save_profile
from tools.question_bank_tools import build_grounded_quiz_prompt
from tools.voice_tools import (
    get_default_voice_name,
    listen_once,
    list_available_voices,
    speak_text_async,
    stop_speaking,
    voice_features_supported,
)

load_dotenv()
if os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
if os.getenv("GOOGLE_API_KEY") and os.getenv("GEMINI_API_KEY"):
    os.environ.pop("GEMINI_API_KEY", None)

logging.getLogger("google_genai.types").setLevel(logging.ERROR)
logging.getLogger("google.adk.sessions.in_memory_session_service").setLevel(logging.ERROR)

APP_NAME = "adaptive_learning_tutor"
USER_ID = "student"
SESSION_ID = "session1"

RESET = "\033[0m"
BOLD = "\033[1m"
STUDENT_COLOR = "\033[96m"
TUTOR_COLOR = "\033[92m"
HEADER_COLOR = "\033[95m"


def enable_ansi_colors():
    if os.name != "nt":
        return True

    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)) == 0:
            return False
        return kernel32.SetConsoleMode(handle, mode.value | 0x0004) != 0
    except Exception:
        return False


ANSI_ENABLED = enable_ansi_colors()


def colorize(text, color):
    if not ANSI_ENABLED:
        return text
    return f"{color}{text}{RESET}"


def prompt_for_exam_goals(existing_profile=None):
    print("\nLet's set up your exam goals.\n")

    raw_exams = input(
        "Which exams are you preparing for? (comma separated, e.g. GRE, GMAT, CAT, JEE, IELTS): "
    ).strip()
    exam_names = [exam.strip().upper() for exam in raw_exams.split(",") if exam.strip()]

    exams = []
    all_subjects = []

    for exam_name in exam_names:
        if exam_name == "JEE":
            main_date = input("Enter exam date for JEE Main (YYYY-MM-DD): ").strip()
            advanced_date = input("Enter exam date for JEE Advanced (YYYY-MM-DD): ").strip()
            for staged_name, staged_date in (
                ("JEE MAIN", main_date),
                ("JEE ADVANCED", advanced_date),
            ):
                subjects = DEFAULT_EXAM_SUBJECTS.get(staged_name, ["Physics", "Chemistry", "Mathematics"])
                print(f"Using default sections for {staged_name}: {', '.join(subjects)}")
                exams.append(
                    {
                        "name": staged_name,
                        "exam_date": staged_date,
                        "subjects": subjects,
                    }
                )
                all_subjects.extend(subjects)
            continue

        if exam_name == "CAT":
            written_date = input("Enter exam date for CAT written exam (YYYY-MM-DD): ").strip()
            gdpi_date = input(
                "Enter expected GDPI/Interview prep start or target date for CAT GDPI (YYYY-MM-DD): "
            ).strip()
            for staged_name, staged_date in (
                ("CAT", written_date),
                ("CAT GDPI", gdpi_date),
            ):
                subjects = DEFAULT_EXAM_SUBJECTS.get(staged_name, [])
                print(f"Using default sections for {staged_name}: {', '.join(subjects)}")
                exams.append(
                    {
                        "name": staged_name,
                        "exam_date": staged_date,
                        "subjects": subjects,
                    }
                )
                all_subjects.extend(subjects)
            continue

        exam_date = input(f"Enter exam date for {exam_name} (YYYY-MM-DD): ").strip()
        default_subjects = DEFAULT_EXAM_SUBJECTS.get(exam_name, [])
        if default_subjects:
            subjects = default_subjects
            print(f"Using default sections for {exam_name}: {', '.join(subjects)}")
        else:
            raw_subjects = input(
                f"Enter the sections/subjects for {exam_name} (comma separated): "
            ).strip()
            subjects = [subject.strip() for subject in raw_subjects.split(",") if subject.strip()]

        exams.append(
            {
                "name": exam_name,
                "exam_date": exam_date,
                "subjects": subjects,
            }
        )
        all_subjects.extend(subjects)

    if existing_profile:
        profile = dict(existing_profile)
        profile["exams"] = exams
        profile["exam"] = ", ".join(exam["name"] for exam in exams)
        profile["exam_date"] = min(exam["exam_date"] for exam in exams)
        profile["subjects"] = all_subjects
    else:
        max_hours = float(
            input(
                "What is the maximum number of hours you can realistically study in a day?: "
            ).strip()
        )
        preferred_persona = input(
            "Which person or celebrity vibe should your AI tutor be inspired by? "
            "(press Enter to skip): "
        ).strip()

        profile = {
            "exam": ", ".join(exam["name"] for exam in exams),
            "exam_date": min(exam["exam_date"] for exam in exams),
            "study_hours_per_day": max_hours,
            "max_study_hours_per_day": max_hours,
            "subjects": all_subjects,
            "preferred_persona": preferred_persona or "friendly study coach",
            "preferred_voice": get_default_voice_name() or "",
            "voice_rate": -2,
            "exams": exams,
        }

    return profile


def ensure_persona_preference(current_profile):
    if current_profile.get("preferred_persona"):
        return current_profile

    persona = input(
        "\nWho should your AI tutor's vibe be inspired by? "
        "(press Enter to keep it as a friendly study coach): "
    ).strip()

    current_profile["preferred_persona"] = persona or "friendly study coach"
    save_profile(current_profile)
    return current_profile


def prompt_for_mock_scores(current_profile):
    print("\nBefore planning, please enter your latest trial mock scores out of 100.")
    scores = {}

    for exam in get_exam_entries(current_profile):
        scores[exam["name"]] = {}
        print(f"\n{exam['name']} mock scores:")

        for subject in exam["subjects"]:
            while True:
                raw_score = input(f"{subject} mock score: ").strip()
                try:
                    score = float(raw_score)
                except ValueError:
                    print("Please enter a numeric score between 0 and 100.")
                    continue

                if 0 <= score <= 100:
                    scores[exam["name"]][subject] = score
                    break

                print("Please enter a numeric score between 0 and 100.")

    save_mock_scores(current_profile, scores)
    award_points(current_profile["name"], 25, "updating trial mock scores")
    print("\nMock scores saved. Future plans will now adapt across all your exams.\n")
    record_behavior_event(
        current_profile["name"],
        event_type="mock_update",
        user_input="update mock scores",
        tutor_response="Mock scores saved and planning updated.",
        metadata={"exams": [exam["name"] for exam in get_exam_entries(current_profile)]},
    )


def refresh_session_profile(session_service, current_profile):
    session = asyncio.run(
        session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
        )
    )
    if session is not None:
        session.state["profile"] = current_profile


def build_quiz_request(user_input):
    question_match = re.search(r"(\d+)\s+questions?", user_input, re.IGNORECASE)
    return int(question_match.group(1)) if question_match else 3


def print_tutor_message(message):
    prefix = colorize(f"{BOLD}Tutor:{RESET}" if ANSI_ENABLED else "Tutor:", TUTOR_COLOR)
    output = f"\n{prefix} {message}"
    try:
        print(output)
    except UnicodeEncodeError:
        encoding = sys.stdout.encoding or "utf-8"
        safe_output = output.encode(encoding, errors="replace").decode(
            encoding, errors="replace"
        )
        print(safe_output)


def _message_display_chunks(message):
    lines = message.splitlines()
    chunks = []

    for index, line in enumerate(lines):
        if not line.strip():
            chunks.append("\n")
            continue

        sentence_chunks = re.split(r"(?<=[.!?])\s+", line)
        for sentence in sentence_chunks:
            if sentence:
                chunks.append(sentence + " ")

        if index < len(lines) - 1:
            chunks.append("\n")

    return chunks or [message]


def print_tutor_message_with_voice_sync(message, voice_mode=False):
    if not voice_mode:
        print_tutor_message(message)
        return

    prefix = colorize(f"{BOLD}Tutor:{RESET}" if ANSI_ENABLED else "Tutor:", TUTOR_COLOR)
    try:
        print(f"\n{prefix} ", end="", flush=True)
        for chunk in _message_display_chunks(message):
            print(chunk, end="", flush=True)
            if chunk == "\n":
                time.sleep(0.06)
            else:
                time.sleep(0.08)
        print()
    except UnicodeEncodeError:
        print_tutor_message(message)


def respond_with_tracking(profile, user_input, message, event_type, metadata=None, voice_mode=False):
    if voice_mode:
        speak_text_async(
            message,
            voice_name=profile.get("preferred_voice") or get_default_voice_name(),
            rate=profile.get("voice_rate", -2),
            chunked=True,
        )
    print_tutor_message_with_voice_sync(message, voice_mode=voice_mode)
    record_behavior_event(
        profile["name"],
        event_type=event_type,
        user_input=user_input,
        tutor_response=message,
        metadata=metadata,
    )


def contains_any_phrase(text, phrases):
    lowered = text.lower()
    return any(phrase in lowered for phrase in phrases)


print(f"\n{colorize('Adaptive Learning Tutor', HEADER_COLOR)}")
print("Type 'exit' to quit\n")

name = input("Enter your name: ").strip()
if name.lower() == "exit":
    raise SystemExit

while not name:
    print("Please enter your name or type 'exit' to quit.")
    name = input("Enter your name: ").strip()
    if name.lower() == "exit":
        raise SystemExit

profile = load_profile(name)

if profile is None:
    print("\nLet's create your learning profile.\n")
    profile_payload = prompt_for_exam_goals()
    profile = create_profile(
        name,
        profile_payload["exam"],
        profile_payload["exam_date"],
        profile_payload["study_hours_per_day"],
        profile_payload["subjects"],
        profile_payload["preferred_persona"],
        exams=profile_payload["exams"],
        max_study_hours_per_day=profile_payload["max_study_hours_per_day"],
    )
    print("\nProfile created successfully!\n")
else:
    print(f"\nWelcome back {name}\n")

profile = ensure_persona_preference(profile)
if not profile.get("preferred_voice"):
    profile["preferred_voice"] = get_default_voice_name() or ""
    profile = save_profile(profile)

print("Your Profile:")
print(profile)

print("\n====================================")
print("How to interact with the tutor")
print("====================================")
print("Explain <topic>")
print("Generate quiz <topic>")
print("Generate quiz 10 questions on ratios")
print("Create study plan")
print("What should I study today?")
print("Show weekly plan")
print("How am I doing behaviorally?")
print("Turn on voice mode")
print("Turn off voice mode")
print("Turn on voice chat mode")
print("Turn off voice chat mode")
print("Listen once")
print("Show voice options")
print("Change tutor voice")
print("Test tutor voice")
print("Stop voice")
print("Speak faster")
print("Speak slower")
print("Show voice speed")
print("Update mock scores")
print("Update exam goals")
print("Mark today's work complete")
print("I missed today's work")
print("Show my points")
print("Change tutor persona")
print("\nExample:")
print("Explain probability")
print("Generate quiz 5 questions on percentages")
print("====================================")

if get_missing_mock_subjects(profile, load_planner_state(profile["name"])):
    prompt_for_mock_scores(profile)

session_service = InMemorySessionService()

asyncio.run(
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state={"profile": profile},
    )
)

runner = Runner(
    app_name=APP_NAME,
    agent=supervisor_agent,
    session_service=session_service,
    auto_create_session=False,
)

voice_mode = False
voice_chat_mode = False
voice_supported = voice_features_supported()
last_tutor_message = ""
if not voice_supported:
    print("Voice mode is unavailable right now. Text mode will still work normally.")

while True:
    student_prompt = colorize(f"{BOLD}Student:{RESET}" if ANSI_ENABLED else "Student:", STUDENT_COLOR)
    user_input = input(f"\n{student_prompt} ").strip()

    if user_input.lower() == "exit":
        break

    normalized_input = user_input.lower()

    if contains_any_phrase(
        normalized_input,
        ["turn voice mode on", "voice mode on", "enable voice mode", "turn on voice mode"],
    ):
        if not voice_supported:
            print_tutor_message("Voice mode is not available on this system right now.")
        else:
            voice_mode = True
            print_tutor_message("Voice mode is now on. I will speak my replies.")
        continue

    if contains_any_phrase(
        normalized_input,
        ["turn on voice chat mode", "enable voice chat mode", "voice chat mode on"],
    ):
        if not voice_supported:
            print_tutor_message("Voice chat mode is not available on this system right now.")
        else:
            voice_mode = True
            voice_chat_mode = True
            print_tutor_message(
                "Voice chat mode is now on. I will keep replies shorter, more conversational, and speak them aloud."
            )
        continue

    if contains_any_phrase(
        normalized_input,
        ["turn voice mode off", "voice mode off", "disable voice mode", "turn off voice mode"],
    ):
        if voice_supported:
            stop_speaking()
        voice_mode = False
        voice_chat_mode = False
        print_tutor_message("Voice mode is now off.")
        continue

    if contains_any_phrase(
        normalized_input,
        ["turn off voice chat mode", "disable voice chat mode", "voice chat mode off"],
    ):
        if voice_supported:
            stop_speaking()
        voice_chat_mode = False
        print_tutor_message("Voice chat mode is now off. I will go back to normal reply style.")
        continue

    if normalized_input in {
        "stop voice",
        "stop reciting",
        "stop speaking",
        "stop voice recitation",
    }:
        if not voice_supported:
            print_tutor_message("Voice mode is not available on this system right now.")
            continue
        stop_speaking()
        print_tutor_message("I have stopped the voice recitation.")
        continue

    if normalized_input in {"speak faster", "increase voice speed", "increase speaking speed"}:
        current_rate = int(profile.get("voice_rate", -2))
        new_rate = min(5, current_rate + 1)
        profile["voice_rate"] = new_rate
        profile = save_profile(profile)
        refresh_session_profile(session_service, profile)
        last_tutor_message = f"Voice speed increased. Current speaking rate is {new_rate}."
        print_tutor_message(last_tutor_message)
        continue

    if normalized_input in {"speak slower", "decrease voice speed", "decrease speaking speed"}:
        current_rate = int(profile.get("voice_rate", -2))
        new_rate = max(-8, current_rate - 1)
        profile["voice_rate"] = new_rate
        profile = save_profile(profile)
        refresh_session_profile(session_service, profile)
        last_tutor_message = f"Voice speed decreased. Current speaking rate is {new_rate}."
        print_tutor_message(last_tutor_message)
        continue

    if normalized_input in {"show voice speed", "what is the voice speed", "current voice speed"}:
        current_rate = int(profile.get("voice_rate", -2))
        speed_hint = "calm and slow" if current_rate <= -3 else "balanced" if current_rate <= 1 else "fast"
        last_tutor_message = (
            f"Your current tutor voice speed is {current_rate}. "
            f"That should sound {speed_hint}."
        )
        print_tutor_message(last_tutor_message)
        continue

    if contains_any_phrase(
        normalized_input,
        ["recite last answer", "recite the above answer", "speak the above answer", "speak that", "read that out", "recite that"],
    ):
        if not last_tutor_message:
            print_tutor_message("I do not have a recent tutor reply to recite yet.")
            continue
        if not voice_supported:
            print_tutor_message("Voice mode is not available on this system right now.")
            continue
        speak_text_async(
            last_tutor_message,
            voice_name=profile.get("preferred_voice") or get_default_voice_name(),
            rate=profile.get("voice_rate", -2),
            chunked=True,
        )
        print_tutor_message("I am reciting the last answer now.")
        continue

    if normalized_input in {"generate study plan", "create study plan"}:
        last_tutor_message = format_study_plan(profile)
        respond_with_tracking(
            profile,
            user_input,
            last_tutor_message,
            event_type="study_plan_request",
            voice_mode=voice_mode,
        )
        continue

    if normalized_input == "what should i study today?":
        last_tutor_message = format_today_schedule(profile)
        respond_with_tracking(
            profile,
            user_input,
            last_tutor_message,
            event_type="today_plan_request",
            voice_mode=voice_mode,
        )
        continue

    if normalized_input == "show weekly plan":
        last_tutor_message = format_weekly_schedule(profile)
        respond_with_tracking(
            profile,
            user_input,
            last_tutor_message,
            event_type="weekly_plan_request",
            voice_mode=voice_mode,
        )
        continue

    if normalized_input in {
        "how am i doing behaviorally?",
        "how am i doing behaviorally",
        "show behavior report",
    }:
        last_tutor_message = format_behavior_report(profile)
        respond_with_tracking(
            profile,
            user_input,
            last_tutor_message,
            event_type="behavior_report_request",
            voice_mode=voice_mode,
        )
        continue

    if normalized_input == "listen once":
        if not voice_supported:
            print_tutor_message("Voice input is not available on this system right now.")
            continue
        print_tutor_message("Listening for one voice message now.")
        ok, transcript = listen_once()
        if not ok:
            print_tutor_message(f"Voice input failed: {transcript}")
            continue
        print(colorize("Heard:", HEADER_COLOR), transcript)
        user_input = transcript.strip()
        normalized_input = user_input.lower()

    if normalized_input == "show voice options":
        voices = list_available_voices()
        if not voices:
            print_tutor_message("I could not find any installed system voices.")
        else:
            current_voice = profile.get("preferred_voice") or get_default_voice_name() or "Default"
            last_tutor_message = (
                "Available tutor voices:\n"
                f"Current voice: {current_voice}\n\n"
                + "\n".join(f"- {voice}" for voice in voices)
            )
            voice_lines = [
                "Available tutor voices:",
                f"Current voice: {current_voice}",
                "",
            ]
            for voice in voices:
                voice_lines.append(f"- {voice}")
            print_tutor_message("\n".join(voice_lines))
        continue

    if normalized_input == "change tutor voice":
        voices = list_available_voices()
        if not voices:
            print_tutor_message("I could not find any installed system voices.")
            continue
        last_tutor_message = "Available voices:\n" + "\n".join(f"- {voice}" for voice in voices)
        print_tutor_message(last_tutor_message)
        chosen_voice = input("Enter the voice name you want to use: ").strip()
        matched_voice = next(
            (voice for voice in voices if chosen_voice.lower() in voice.lower()),
            None,
        )
        if not matched_voice:
            print_tutor_message("I could not match that voice name. Please try again using one of the listed voices.")
            continue
        profile["preferred_voice"] = matched_voice
        profile = save_profile(profile)
        refresh_session_profile(session_service, profile)
        last_tutor_message = f"Tutor voice changed to {matched_voice}."
        print_tutor_message(last_tutor_message)
        continue

    if normalized_input == "test tutor voice":
        if not voice_supported:
            print_tutor_message("Voice mode is not available on this system right now.")
            continue
        test_message = (
            "Hello. This is your adaptive learning tutor voice test. "
            "I will try to sound calm, clear, and easy to listen to."
        )
        last_tutor_message = test_message
        print_tutor_message(test_message)
        speak_text_async(
            test_message,
            voice_name=profile.get("preferred_voice") or get_default_voice_name(),
            rate=profile.get("voice_rate", -2),
            chunked=True,
        )
        continue

    if normalized_input == "update mock scores":
        prompt_for_mock_scores(profile)
        refresh_session_profile(session_service, profile)
        continue

    if normalized_input == "update exam goals":
        updated_profile = prompt_for_exam_goals(profile)
        updated_profile["name"] = profile["name"]
        updated_profile["preferred_persona"] = profile.get(
            "preferred_persona", "friendly study coach"
        )
        updated_profile["study_hours_per_day"] = profile.get(
            "study_hours_per_day", profile.get("max_study_hours_per_day", 6)
        )
        updated_profile["max_study_hours_per_day"] = profile.get(
            "max_study_hours_per_day", profile.get("study_hours_per_day", 6)
        )
        profile = save_profile(updated_profile)
        refresh_session_profile(session_service, profile)
        last_tutor_message = "Your exam goals have been updated. Please refresh mock scores next."
        respond_with_tracking(
            profile,
            user_input,
            last_tutor_message,
            event_type="exam_goal_update",
            voice_mode=voice_mode,
        )
        continue

    if normalized_input == "show my points":
        last_tutor_message = format_points_summary(profile)
        respond_with_tracking(
            profile,
            user_input,
            last_tutor_message,
            event_type="motivation_dashboard_request",
            voice_mode=voice_mode,
        )
        continue

    if normalized_input == "change tutor persona":
        persona = input(
            "Enter the person or celebrity vibe you want your AI tutor to be inspired by: "
        ).strip()
        profile["preferred_persona"] = persona or "friendly study coach"
        profile = save_profile(profile)
        refresh_session_profile(session_service, profile)
        last_tutor_message = f"Done. I will keep the tutoring vibe inspired by {profile['preferred_persona']}."
        respond_with_tracking(
            profile,
            user_input,
            last_tutor_message,
            event_type="persona_update",
            voice_mode=voice_mode,
        )
        continue

    if normalized_input in {
        "mark today's work complete",
        "mark todays work complete",
    }:
        completion_message = mark_today_complete(profile)
        if "marked as completed" in completion_message:
            streak_state = record_daily_completion(profile["name"])
            bonus = 50 + min(50, streak_state["current_streak"] * 10)
            points_state = award_points(
                profile["name"],
                bonus,
                f"completing today's work with a {streak_state['current_streak']}-day streak",
            )
            completion_message += (
                f" You earned {bonus} points and now have {points_state['points']} total points."
            )
        last_tutor_message = completion_message
        respond_with_tracking(
            profile,
            user_input,
            last_tutor_message,
            event_type="study_completion",
            voice_mode=voice_mode,
        )
        continue

    if normalized_input in {
        "i missed today's work",
        "i missed todays work",
        "mark today's work missed",
        "mark todays work missed",
    }:
        missed_message = mark_today_missed(profile)
        if "moved into your backlog" in missed_message:
            break_streak(profile["name"])
        last_tutor_message = missed_message
        respond_with_tracking(
            profile,
            user_input,
            last_tutor_message,
            event_type="missed_work",
            voice_mode=voice_mode,
        )
        continue

    record_bond_interaction(profile["name"])
    if normalized_input.startswith("generate quiz"):
        question_count = build_quiz_request(user_input)
        outgoing_message = build_grounded_quiz_prompt(profile, user_input, question_count)
    else:
        outgoing_message = user_input
        if voice_chat_mode:
            outgoing_message += (
                "\n\nVoice chat mode is on. Reply in a short, natural, conversational way. "
                "Keep the response easy to speak aloud, ideally within 3 to 5 short sentences "
                "unless the user explicitly asks for more detail."
            )
    content = Content(role="user", parts=[{"text": outgoing_message}])

    events = runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content,
    )

    for event in events:
        if event.is_final_response():
            response_text = event.content.parts[0].text
            last_tutor_message = response_text
            if voice_mode:
                speak_text_async(
                    response_text,
                    voice_name=profile.get("preferred_voice") or get_default_voice_name(),
                    rate=profile.get("voice_rate", -2),
                    chunked=True,
                )
            print_tutor_message_with_voice_sync(response_text, voice_mode=voice_mode)
            record_behavior_event(
                profile["name"],
                event_type="chat",
                user_input=user_input,
                tutor_response=response_text,
            )
