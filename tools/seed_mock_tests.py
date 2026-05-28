import json
import os
from pathlib import Path

from dotenv import load_dotenv

try:
    from google import genai
except Exception:
    genai = None


ROOT = Path(__file__).resolve().parents[1]
MOCK_DIR = ROOT / "app_data" / "mock_tests"
CATALOGUE_PATH = MOCK_DIR / "mock_test_catalogue.json"
BANK_PATH = MOCK_DIR / "physics_mock_bank.json"
MODEL_NAME = "gemini-2.5-flash"


UNIT_POOLS = {
    "physics_mock_1": [
        ("Kinematics", "Projectile Motion"),
        ("Laws of Motion", "Friction on Inclined Plane"),
        ("Work Energy Power", "Work-Energy Theorem"),
        ("Rotational Motion", "Rolling Motion"),
        ("Gravitation", "Orbital Speed"),
    ],
    "physics_mock_2": [
        ("Simple Harmonic Motion", "Spring-Mass Oscillation"),
        ("Waves", "Standing Waves"),
        ("Ray Optics", "Lens Formula"),
        ("Wave Optics", "Young's Double Slit Experiment"),
        ("Dual Nature of Matter", "Photoelectric Effect"),
    ],
    "physics_mock_3": [
        ("Electrostatics", "Electric Field and Potential"),
        ("Current Electricity", "Kirchhoff Laws"),
        ("Magnetic Effects of Current", "Force on Moving Charge"),
        ("Electromagnetic Induction", "Motional EMF"),
        ("Alternating Current", "LCR Circuit"),
    ],
    "physics_mock_4": [
        ("Units and Measurements", "Dimensional Analysis"),
        ("Thermodynamics", "First Law of Thermodynamics"),
        ("Kinetic Theory of Gases", "RMS Speed"),
        ("Magnetism and Matter", "Magnetic Dipole"),
        ("Atoms and Nuclei", "Radioactive Decay"),
        ("Semiconductor Devices", "Diode Circuits"),
    ],
    "physics_mock_5": [
        ("Properties of Matter", "Surface Tension"),
        ("Electromagnetic Waves", "EM Wave Spectrum"),
        ("Current Electricity", "Meter Bridge"),
        ("Rotational Motion", "Angular Momentum"),
        ("Wave Optics", "Diffraction"),
        ("Atoms and Nuclei", "Bohr Model"),
    ],
}


def load_catalogue():
    with CATALOGUE_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle).get("mock_tests", [])


def extract_json(text):
    raw = str(text or "").strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json", "", 1).strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start >= 0 and end > start:
        raw = raw[start : end + 1]
    return json.loads(raw)


def make_fallback_question(test, number, q_type):
    test_index = int(test["id"].rsplit("_", 1)[-1])
    qid = f"MT{test_index}_Q{number}"
    unit, topic = UNIT_POOLS.get(test["id"], UNIT_POOLS["physics_mock_1"])[(number - 1) % len(UNIT_POOLS.get(test["id"], UNIT_POOLS["physics_mock_1"]))]
    difficulty = "hard" if test.get("difficulty") == "hard" or q_type == "mcq_multi" else "medium"
    base = 2 + ((number + test_index) % 5)
    velocity = 5 * base
    time_value = base + 1
    distance = velocity * time_value
    acceleration = 2 * base
    answer_int = str(acceleration * base)

    if q_type == "integer":
        return {
            "id": qid,
            "mock_test_id": test["id"],
            "question_number": number,
            "type": "integer",
            "question": (
                f"In a JEE Physics problem from {topic}, a body starts from rest and moves with uniform acceleration "
                f"{acceleration} m s^-2. Find its speed in m s^-1 after {base} s."
            ),
            "options": [],
            "correct_answer": answer_int,
            "correct_options": [],
            "solution": (
                f"Use v = u + at. Here u = 0, a = {acceleration} m s^-2 and t = {base} s. "
                f"So v = 0 + {acceleration} x {base} = {int(acceleration * base)} m s^-1. "
                "Check: acceleration times time has unit m s^-1."
            ),
            "topic": topic,
            "unit": unit,
            "difficulty": difficulty,
            "marks_correct": 4,
            "marks_wrong": 0,
            "time_suggested_seconds": 120,
        }

    if q_type == "mcq_multi":
        return {
            "id": qid,
            "mock_test_id": test["id"],
            "question_number": number,
            "type": "mcq_multi",
            "question": (
                f"For a particle moving with constant acceleration in the {topic} context, which statements are correct? "
                f"Take initial speed {velocity} m s^-1 and acceleration {acceleration} m s^-2."
            ),
            "options": [
                "A. The velocity-time graph is a straight line",
                "B. The displacement-time graph is always a straight line",
                "C. The slope of the velocity-time graph equals acceleration",
                "D. Acceleration must be zero if speed is increasing uniformly",
            ],
            "correct_answer": "",
            "correct_options": ["A", "C"],
            "solution": (
                "For constant acceleration, v = u + at, so the velocity-time graph is linear and its slope is acceleration. "
                "Displacement varies as s = ut + (1/2)at^2, so it is generally parabolic, not straight. Increasing speed uniformly means non-zero acceleration."
            ),
            "topic": topic,
            "unit": unit,
            "difficulty": difficulty,
            "marks_correct": 4,
            "marks_wrong": -2,
            "time_suggested_seconds": 150,
        }

    options = [
        f"A. {distance - velocity} m",
        f"B. {distance} m",
        f"C. {distance + velocity} m",
        f"D. {distance * 2} m",
    ]
    return {
        "id": qid,
        "mock_test_id": test["id"],
        "question_number": number,
        "type": "mcq_single",
        "question": (
            f"In a {topic} question, a particle moves with constant speed {velocity} m s^-1 for {time_value} s. "
            "What is the displacement magnitude?"
        ),
        "options": options,
        "correct_answer": "B",
        "correct_options": ["B"],
        "solution": (
            f"For uniform motion, displacement magnitude s = vt. Substitute v = {velocity} m s^-1 and t = {time_value} s. "
            f"Therefore s = {velocity} x {time_value} = {distance} m. The common trap is using acceleration equations when speed is already constant."
        ),
        "topic": topic,
        "unit": unit,
        "difficulty": difficulty,
        "marks_correct": 4,
        "marks_wrong": -1,
        "time_suggested_seconds": 120,
    }


def fallback_test_questions(test):
    if test["type"] == "jee_main":
        types = ["mcq_single"] * 20 + ["integer"] * 5
    else:
        types = ["mcq_single"] * 6 + ["mcq_multi"] * 6 + ["integer"] * 6
    return [make_fallback_question(test, index, q_type) for index, q_type in enumerate(types, start=1)]


def build_prompt(test):
    if test["type"] == "jee_main":
        composition = "20 mcq_single questions and 5 integer questions"
    else:
        composition = "6 mcq_single questions, 6 mcq_multi questions, and 6 integer questions"
    return (
        "Generate one complete JEE Physics mock test. Return JSON only, no markdown.\n"
        f"Test id: {test['id']}\n"
        f"Title: {test['title']}\n"
        f"Topics: {', '.join(test.get('topics_covered', []))}\n"
        f"Difficulty: {test.get('difficulty', 'medium')}\n"
        f"Composition: {composition}.\n"
        "Every question must have complete numerical values, plausible wrong options, and a step-by-step solution.\n"
        "Use this exact shape: {\"questions\": [{\"id\":\"MT1_Q1\",\"mock_test_id\":\"physics_mock_1\",\"question_number\":1,\"type\":\"mcq_single\",\"question\":\"...\",\"options\":[\"A. ...\",\"B. ...\",\"C. ...\",\"D. ...\"],\"correct_answer\":\"B\",\"correct_options\":[\"B\"],\"solution\":\"...\",\"topic\":\"...\",\"unit\":\"...\",\"difficulty\":\"medium\",\"marks_correct\":4,\"marks_wrong\":-1,\"time_suggested_seconds\":120}]}.\n"
        "For integer questions, options must be [] and correct_answer must be the integer string. "
        "For multi-correct, correct_answer can be empty and correct_options must list letters."
    )


def generate_with_gemini(test, client):
    response = client.models.generate_content(model=MODEL_NAME, contents=build_prompt(test))
    payload = extract_json(response.text)
    questions = payload.get("questions", [])
    if not isinstance(questions, list):
        return []
    return questions


def normalize_question(question, fallback):
    merged = dict(fallback)
    if isinstance(question, dict):
        merged.update({key: value for key, value in question.items() if value is not None})
    merged["id"] = str(merged["id"])
    merged["mock_test_id"] = str(merged["mock_test_id"])
    merged["question_number"] = int(merged["question_number"])
    merged["type"] = str(merged.get("type") or fallback["type"]).strip()
    merged["options"] = list(merged.get("options") or [])
    merged["correct_options"] = list(merged.get("correct_options") or [])
    merged["marks_correct"] = int(merged.get("marks_correct") or 4)
    merged["marks_wrong"] = int(merged.get("marks_wrong") or (0 if merged["type"] == "integer" else -1))
    merged["time_suggested_seconds"] = int(merged.get("time_suggested_seconds") or 120)
    return merged


def main():
    load_dotenv(ROOT / ".env")
    MOCK_DIR.mkdir(parents=True, exist_ok=True)
    catalogue = load_catalogue()
    client = None
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if genai and api_key:
        try:
            client = genai.Client(api_key=api_key)
        except Exception as exc:
            print(f"Gemini unavailable, using local fallback: {exc}")

    all_questions = []
    for test in catalogue:
        fallback_questions = fallback_test_questions(test)
        generated = []
        if client:
            try:
                generated = generate_with_gemini(test, client)
            except Exception as exc:
                print(f"{test['id']}: Gemini generation failed, using fallback. {exc}")
        for index, fallback in enumerate(fallback_questions):
            question = normalize_question(generated[index] if index < len(generated) else {}, fallback)
            all_questions.append(question)
            print(f"Indexed {question['mock_test_id']} question {question['question_number']}: {question['type']}")

    BANK_PATH.write_text(
        json.dumps({"mock_tests": catalogue, "questions": all_questions}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Saved {len(all_questions)} questions to {BANK_PATH}")


if __name__ == "__main__":
    main()
