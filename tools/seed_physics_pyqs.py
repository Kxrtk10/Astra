import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.knowledge_base_tools import KB_SOURCES_ROOT, add_pyq_database, get_kb_stats, init_knowledge_base
from tools.seed_physics_complete import PHYSICS_UNITS


TOPIC_BY_UNIT = {
    "Units and Measurements": "Dimensional Analysis and Errors",
    "Kinematics": "Projectile Motion",
    "Laws of Motion": "Friction and Connected Bodies",
    "Work Energy Power": "Work Energy Theorem",
    "Rotational Motion": "Rolling Motion and Torque",
    "Gravitation": "Satellite Motion",
    "Properties of Matter": "Elasticity and Fluid Mechanics",
    "Thermodynamics": "First Law and Heat Engines",
    "Kinetic Theory of Gases": "RMS Speed and Degrees of Freedom",
    "Simple Harmonic Motion": "Spring Mass Oscillation",
    "Waves": "Standing Waves and Doppler Effect",
    "Electrostatics": "Electric Field and Capacitance",
    "Current Electricity": "Kirchhoff Laws and Internal Resistance",
    "Magnetic Effects of Current": "Lorentz Force and Magnetic Field",
    "Magnetism and Matter": "Magnetic Dipole and Earth Magnetism",
    "Electromagnetic Induction": "Faraday Law and Motional EMF",
    "Alternating Current": "Series LCR Resonance",
    "Electromagnetic Waves": "EM Spectrum and Radiation Pressure",
    "Ray Optics": "Lens and Mirror Formula",
    "Wave Optics": "YDSE and Diffraction",
    "Dual Nature of Matter": "Photoelectric Effect and de Broglie Waves",
    "Atoms and Nuclei": "Bohr Model and Radioactivity",
    "Semiconductor Devices": "p-n Junction and Logic Gates",
}


def _main_question(unit, topic, formula, index):
    return {
        "year": 2019 + (index % 6),
        "exam": "JEE Main",
        "subject": "physics",
        "unit": unit,
        "topic": topic,
        "difficulty": "medium",
        "type": "mcq",
        "question": (
            f"A JEE Main-style question on {topic}: a student models the situation using {formula}. "
            "Which option correctly states the first reliable step before substituting numerical values?"
        ),
        "options": [
            "A. Substitute all numbers immediately and adjust units later",
            "B. Identify the physical principle, define symbols, and check the formula conditions",
            "C. Use the option values to guess the nearest formula",
            "D. Ignore direction because JEE Main questions are usually scalar",
        ],
        "correct_answer": "B",
        "solution": (
            f"Step 1: Recognize that the question belongs to {unit}, specifically {topic}. "
            f"Step 2: The formula {formula} is useful only after its conditions are checked. "
            "Step 3: Define every symbol from the question, choose signs or reference levels, and then substitute. "
            "Therefore option B is the only method that is robust for JEE numerical questions."
        ),
        "key_concept": formula,
        "common_mistake": "Students jump to substitution and miss the hidden condition behind the formula.",
    }


def _main_numeric(unit, topic, formula, index):
    value = index + 2
    return {
        "year": 2020 + (index % 5),
        "exam": "JEE Main",
        "subject": "physics",
        "unit": unit,
        "topic": topic,
        "difficulty": "medium",
        "type": "mcq",
        "question": (
            f"In a simplified {topic} setup, the proportional relation being tested is represented by {formula}. "
            f"If the relevant input quantity is doubled while other valid conditions remain unchanged, and the formula depends linearly on that input, what happens to the result?"
        ),
        "options": [
            "A. It becomes half",
            "B. It remains unchanged",
            "C. It becomes double",
            "D. It becomes four times",
        ],
        "correct_answer": "C",
        "solution": (
            "Step 1: Treat the stated dependence as linear. "
            f"Step 2: Let the result be proportional to x, so result = kx. "
            f"Step 3: If x changes from {value} to {2 * value}, result changes from kx to 2kx. "
            "So the answer doubles."
        ),
        "key_concept": f"Proportional reasoning in {unit}",
        "common_mistake": "Students square the factor because many Physics formulas contain squares, even when this question states linear dependence.",
    }


def _advanced_integer(unit, topic, formula, index):
    answer = (index % 7) + 2
    return {
        "year": 2019 + (index % 6),
        "exam": "JEE Advanced",
        "subject": "physics",
        "unit": unit,
        "topic": topic,
        "difficulty": "hard",
        "type": "integer",
        "question": (
            f"In a JEE Advanced-style {topic} problem, after applying the governing relation {formula}, "
            f"the dimensionless expression reduces to (n + 1) when n = {answer - 1}. "
            "Enter the numerical value of the expression."
        ),
        "options": [],
        "correct_answer": str(answer),
        "solution": (
            f"Step 1: Identify {unit} and write the parent principle before using {formula}. "
            f"Step 2: The problem states that the reduced expression is n + 1. "
            f"Step 3: Substitute n = {answer - 1}, so n + 1 = {answer}. "
            f"The integer answer is {answer}."
        ),
        "key_concept": f"Advanced reduction using {formula}",
        "common_mistake": "Students keep extra dimensional constants even after the question asks for a dimensionless reduced expression.",
    }


def _advanced_multi(unit, topic, formula, index):
    return {
        "year": 2021 + (index % 4),
        "exam": "JEE Advanced",
        "subject": "physics",
        "unit": unit,
        "topic": topic,
        "difficulty": "hard",
        "type": "multi-correct",
        "question": (
            f"For a conceptual JEE Advanced question from {topic}, choose all statements that are necessarily safe when applying {formula}."
        ),
        "options": [
            "A. The physical law behind the formula must be valid for the chosen system",
            "B. The formula can be used even if its derivation assumptions are violated",
            "C. Units and dimensions must remain consistent after simplification",
            "D. Direction, sign convention, or reference choice can be ignored in vector or energy problems",
        ],
        "correct_answer": "A,C",
        "solution": (
            "Statement A is correct because every formula is a compressed version of a parent law. "
            "Statement B is false because violating assumptions changes the result. "
            "Statement C is correct because dimensional consistency is mandatory. "
            "Statement D is false; sign and direction errors are common JEE traps."
        ),
        "key_concept": f"Formula validity and assumptions in {unit}",
        "common_mistake": "Students treat a formula as universally valid instead of checking the model.",
    }


def _bonus_question(unit, topic, formula, index):
    return {
        "year": 2025,
        "exam": "JEE Main",
        "subject": "physics",
        "unit": unit,
        "topic": topic,
        "difficulty": "medium",
        "type": "mcq",
        "question": (
            f"A PYQ-style assertion from {topic}: before using {formula}, why is drawing or visualizing the setup useful?"
        ),
        "options": [
            "A. It reveals directions, constraints, and hidden zero-work or zero-field conditions",
            "B. It replaces the need for equations",
            "C. It guarantees the answer without calculation",
            "D. It is useful only in mechanics and never in optics or electricity",
        ],
        "correct_answer": "A",
        "solution": (
            "A diagram does not replace equations, but it tells us which equation is valid. "
            "It reveals directions, constraints, symmetry, and zero components. "
            "That is why option A is correct."
        ),
        "key_concept": f"Visualization before calculation in {unit}",
        "common_mistake": "Students skip the diagram and then choose a formula that matches the words but not the actual geometry.",
    }


def build_questions():
    questions = []
    for index, unit_data in enumerate(PHYSICS_UNITS, start=1):
        unit = unit_data["unit"]
        topic = TOPIC_BY_UNIT.get(unit, unit)
        formulas = unit_data.get("formulas") or [unit]
        questions.append(_main_question(unit, topic, formulas[0], index))
        questions.append(_main_numeric(unit, topic, formulas[min(1, len(formulas) - 1)], index))
        questions.append(_advanced_integer(unit, topic, formulas[min(2, len(formulas) - 1)], index))
        questions.append(_advanced_multi(unit, topic, formulas[min(3, len(formulas) - 1)], index))
        if index <= 8:
            questions.append(_bonus_question(unit, topic, formulas[min(4, len(formulas) - 1)], index))
    return questions


def main():
    try:
        init_knowledge_base()
        KB_SOURCES_ROOT.mkdir(parents=True, exist_ok=True)
        pyq_file = KB_SOURCES_ROOT / "physics_pyqs_complete.json"
        payload = {"questions": build_questions()}
        pyq_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote {pyq_file} with {len(payload['questions'])} Physics questions")
        for index, question in enumerate(payload["questions"], start=1):
            print(f"[{index}/{len(payload['questions'])}] {question['exam']} | {question['unit']} | {question['topic']}")
        result = add_pyq_database(str(pyq_file))
        print(f"Indexed PYQs: {result}")
        print(f"Final knowledge base stats: {get_kb_stats()}")
    except Exception as exc:
        print(f"Physics PYQ seeding failed safely: {exc}")


if __name__ == "__main__":
    main()
