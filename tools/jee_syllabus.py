from collections import OrderedDict
from copy import deepcopy


TOPIC_CONFIDENCE_THRESHOLDS = {
    "new": 0,
    "low": 40,
    "medium": 60,
    "good": 75,
    "strong": 85,
}

SPACED_REPETITION_INTERVALS = {
    "low": [1, 2, 4, 7],
    "medium": [3, 7, 14],
    "good": [7, 21],
    "strong": [30],
}


def _unit(
    unit_number,
    name,
    topics,
    jee_main_weightage_percent,
    jee_advanced_weightage_percent,
    prerequisite_unit_numbers=None,
    estimated_learn_days=3,
    estimated_revise_days=2,
    difficulty=3,
):
    return {
        "unit_number": unit_number,
        "name": name,
        "topics": list(topics or []),
        "jee_main_weightage_percent": jee_main_weightage_percent,
        "jee_advanced_weightage_percent": jee_advanced_weightage_percent,
        "prerequisite_unit_numbers": list(prerequisite_unit_numbers or []),
        "estimated_learn_days": estimated_learn_days,
        "estimated_revise_days": estimated_revise_days,
        "difficulty": difficulty,
    }


JEE_SYLLABUS = OrderedDict(
    [
        (
            "physics",
            [
                _unit(1, "Units and Measurements", ["dimensions", "errors", "significant figures"], 2, 1, [], 2, 1, 1),
                _unit(2, "Kinematics", ["1D motion", "2D motion", "projectile motion", "relative motion"], 4, 3, [1], 4, 2, 2),
                _unit(3, "Laws of Motion", ["free body diagram", "friction", "connected bodies", "pulleys"], 5, 4, [2], 4, 2, 3),
                _unit(4, "Work Energy Power", ["work theorem", "power", "potential energy", "conservation"], 5, 4, [3], 3, 2, 3),
                _unit(5, "Rotational Motion", ["torque", "moment of inertia", "angular momentum", "rolling"], 5, 6, [4], 5, 3, 5),
                _unit(6, "Gravitation", ["Kepler laws", "satellites", "escape velocity"], 3, 3, [2], 3, 2, 3),
                _unit(7, "Properties of Matter", ["elasticity", "surface tension", "viscosity"], 3, 3, [3], 3, 2, 3),
                _unit(8, "Thermodynamics", ["first law", "processes", "heat engines", "entropy"], 5, 5, [7], 4, 2, 4),
                _unit(9, "Kinetic Theory of Gases", ["ideal gas", "rms speed", "degrees of freedom"], 3, 2, [8], 2, 1, 2),
                _unit(10, "Simple Harmonic Motion", ["displacement", "energy in SHM", "time period"], 4, 4, [3], 3, 2, 3),
                _unit(11, "Waves", ["wave equation", "superposition", "beats", "Doppler effect"], 4, 4, [10], 4, 2, 3),
                _unit(12, "Electrostatics", ["Coulomb law", "electric field", "potential", "capacitors"], 7, 7, [1], 5, 3, 4),
                _unit(13, "Current Electricity", ["Ohm law", "circuits", "Kirchhoff", "Wheatstone bridge"], 6, 6, [12], 5, 3, 4),
                _unit(14, "Magnetic Effects of Current", ["Biot Savart", "Ampere law", "force on charge", "moving coil"], 5, 5, [13], 4, 2, 4),
                _unit(15, "Magnetism and Matter", ["bar magnet", "magnetic properties", "Earth magnetism"], 3, 3, [14], 2, 1, 2),
                _unit(16, "Electromagnetic Induction", ["Faraday law", "Lenz law", "inductance", "eddy currents"], 5, 5, [14], 4, 2, 4),
                _unit(17, "Alternating Current", ["AC circuits", "reactance", "resonance", "power factor"], 4, 4, [16], 3, 2, 4),
                _unit(18, "Electromagnetic Waves", ["spectrum", "propagation", "applications"], 2, 2, [17], 2, 1, 2),
                _unit(19, "Ray Optics", ["mirror formula", "lens formula", "instruments", "refraction"], 4, 4, [1], 4, 2, 3),
                _unit(20, "Wave Optics", ["YDSE", "diffraction", "polarization"], 4, 4, [11], 3, 2, 4),
                _unit(21, "Dual Nature of Matter", ["photoelectric effect", "de Broglie"], 3, 3, [12], 2, 1, 3),
                _unit(22, "Atoms and Nuclei", ["Bohr model", "radioactivity", "nuclear reactions"], 4, 4, [21], 3, 2, 3),
                _unit(23, "Semiconductor Devices", ["diodes", "transistors", "logic gates"], 3, 3, [13], 3, 2, 3),
            ],
        ),
        (
            "chemistry",
            [
                _unit(1, "Basic Concepts of Chemistry", ["mole concept", "stoichiometry", "limiting reagent"], 2, 2, [], 2, 1, 1),
                _unit(2, "Atomic Structure", ["Bohr model", "quantum numbers", "electronic configuration"], 3, 3, [1], 3, 2, 2),
                _unit(3, "Chemical Bonding", ["VSEPR", "hybridization", "MOT", "H-bonding"], 4, 5, [2], 4, 2, 4),
                _unit(4, "States of Matter", ["gas laws", "real gases", "liquids"], 3, 3, [1], 3, 2, 2),
                _unit(5, "Thermodynamics", ["enthalpy", "entropy", "Gibbs energy"], 5, 5, [4], 4, 2, 4),
                _unit(6, "Equilibrium", ["chemical equilibrium", "ionic equilibrium", "pH", "buffers"], 5, 5, [5], 4, 2, 4),
                _unit(7, "Redox Reactions", ["oxidation number", "balancing", "disproportionation"], 3, 3, [1], 2, 1, 2),
                _unit(8, "Hydrogen and s-Block", ["hydrides", "alkali metals", "alkaline earth metals"], 3, 2, [3], 3, 2, 2),
                _unit(9, "p-Block Elements Group 13-14", ["boron family", "carbon family", "anomalous behavior"], 3, 3, [], 3, 2, 3),
                _unit(10, "Organic Chemistry Basics", ["IUPAC", "isomerism", "reaction intermediates"], 4, 4, [3], 4, 2, 3),
                _unit(11, "Hydrocarbons", ["alkanes", "alkenes", "alkynes", "aromaticity"], 4, 5, [10], 4, 2, 3),
                _unit(12, "Solutions", ["concentration", "Raoult law", "colligative properties"], 4, 4, [4], 3, 2, 3),
                _unit(13, "Electrochemistry", ["cell potential", "Nernst equation", "electrolysis"], 5, 5, [7], 4, 2, 4),
                _unit(14, "Chemical Kinetics", ["rate law", "order", "Arrhenius equation"], 4, 4, [6], 3, 2, 3),
                _unit(15, "Surface Chemistry", ["adsorption", "colloids", "catalysis"], 2, 2, [], 2, 1, 2),
                _unit(16, "p-Block Group 15-18", ["nitrogen family", "oxygen family", "halogens", "noble gases"], 4, 4, [], 4, 2, 3),
                _unit(17, "d and f Block Elements", ["transition trends", "lanthanoids", "actinoids"], 4, 4, [], 3, 2, 3),
                _unit(18, "Coordination Compounds", ["naming", "bonding", "isomerism", "CFT"], 5, 6, [17], 4, 2, 5),
                _unit(19, "Haloalkanes and Haloarenes", ["SN1", "SN2", "elimination"], 4, 5, [11], 3, 2, 3),
                _unit(20, "Alcohols Phenols Ethers", ["preparation", "reactions", "acidity order"], 4, 4, [19], 3, 2, 3),
                _unit(21, "Aldehydes Ketones Acids", ["carbonyl reactions", "nucleophilic addition", "acidity"], 5, 5, [20], 4, 2, 4),
                _unit(22, "Amines", ["basicity", "diazotization", "named reactions"], 3, 4, [21], 3, 2, 3),
                _unit(23, "Biomolecules and Polymers", ["carbohydrates", "proteins", "polymers"], 3, 2, [], 3, 1, 2),
            ],
        ),
        (
            "mathematics",
            [
                _unit(1, "Sets Relations Functions", ["sets", "relations", "functions"], 3, 3, [], 3, 2, 2),
                _unit(2, "Complex Numbers", ["algebra of complex numbers", "Argand plane", "polar form"], 4, 5, [1], 4, 2, 4),
                _unit(3, "Quadratic Equations", ["roots", "discriminant", "nature of roots"], 3, 3, [2], 3, 2, 2),
                _unit(4, "Sequences and Series", ["AP", "GP", "special sums"], 4, 4, [3], 3, 2, 3),
                _unit(5, "Permutations Combinations", ["arrangements", "combinations", "counting"], 4, 5, [], 3, 2, 4),
                _unit(6, "Binomial Theorem", ["expansion", "general term", "middle term"], 3, 3, [5], 2, 1, 3),
                _unit(7, "Matrices and Determinants", ["matrix operations", "inverse", "determinants"], 5, 5, [], 4, 2, 4),
                _unit(8, "Straight Lines", ["slope", "distance", "family of lines"], 4, 4, [1], 3, 2, 3),
                _unit(9, "Circles", ["equation", "tangents", "chords"], 4, 4, [8], 3, 2, 3),
                _unit(10, "Conic Sections", ["parabola", "ellipse", "hyperbola"], 5, 6, [9], 5, 3, 5),
                _unit(11, "3D Geometry", ["direction cosines", "line", "plane"], 5, 5, [8], 4, 2, 4),
                _unit(12, "Vectors", ["vector algebra", "dot product", "cross product"], 4, 5, [11], 3, 2, 4),
                _unit(13, "Limits and Continuity", ["limits", "continuity", "standard limits"], 4, 5, [1], 4, 2, 4),
                _unit(14, "Differentiation", ["derivative rules", "chain rule", "implicit differentiation"], 5, 5, [13], 4, 2, 4),
                _unit(15, "Applications of Derivatives", ["maxima minima", "monotonicity", "tangent normal"], 5, 6, [14], 4, 2, 5),
                _unit(16, "Indefinite Integration", ["basic integrals", "substitution", "partial fractions"], 5, 6, [14], 5, 3, 5),
                _unit(17, "Definite Integration", ["properties", "area", "evaluation"], 5, 6, [16], 4, 2, 5),
                _unit(18, "Differential Equations", ["formation", "order degree", "solution methods"], 4, 4, [17], 3, 2, 4),
                _unit(19, "Probability", ["conditional probability", "independent events", "Bayes theorem"], 5, 5, [5], 4, 2, 4),
                _unit(20, "Trigonometry", ["identities", "equations", "heights and distances"], 4, 4, [1], 4, 2, 3),
                _unit(21, "Inverse Trigonometry", ["principal values", "identities", "transformations"], 3, 3, [20], 2, 1, 3),
                _unit(22, "Mathematical Reasoning", ["statements", "logic", "quantifiers"], 2, 2, [], 2, 1, 1),
                _unit(23, "Statistics", ["mean", "variance", "standard deviation"], 2, 2, [], 2, 1, 1),
            ],
        ),
    ]
)


def get_subject_units(subject):
    return list(JEE_SYLLABUS.get(str(subject or "").strip().lower(), []))


def iter_all_units():
    for subject, units in JEE_SYLLABUS.items():
        for unit in units:
            yield subject, unit


def get_all_unit_topics():
    topics = []
    for subject, units in JEE_SYLLABUS.items():
        for unit in units:
            topics.append(
                {
                    "subject": subject,
                    "unit_number": unit["unit_number"],
                    "unit_name": unit["name"],
                    "topics": list(unit["topics"]),
                }
            )
    return topics


def _subject_prefix(subject):
    return {
        "physics": "PHY",
        "chemistry": "CHE",
        "mathematics": "MTH",
    }.get(str(subject or "").strip().lower(), "JEE")


def _concept_templates(subject, unit_name, topic_name):
    topic = str(topic_name or "").strip().lower()
    unit = str(unit_name or "").strip().lower()
    templates = []

    if any(token in topic for token in ["motion", "kinematics", "velocity", "displacement", "speed", "graph"]):
        templates = [
            "Physical meaning and everyday intuition",
            "Core definition and sign convention",
            "Kinematic equations or graph-based relation",
            "Units, dimensions, and how JEE asks it",
            "Worked JEE-style numerical setup",
        ]
    elif any(token in topic for token in ["projectile", "relative", "circular"]):
        templates = [
            "Why the motion splits into parts or directions",
            "Precise definition of the motion variables",
            "Derivation of the governing formula step by step",
            "Units, dimensions, and hidden assumptions",
            "Worked JEE example with a trap to avoid",
        ]
    elif any(token in topic for token in ["force", "friction", "energy", "power", "work", "moment", "torque"]):
        templates = [
            "Mechanical meaning in a real scene",
            "Definition of the quantity and sign convention",
            "Derivation from Newton's laws or energy balance",
            "Units, dimensions, and common exam patterns",
            "Worked JEE-style numerical example",
        ]
    elif any(token in topic for token in ["thermo", "entropy", "gas", "equilibrium", "electrochem", "kinetics", "pH", "buffer"]):
        templates = [
            "Real-world chemical meaning",
            "Definition and state variables involved",
            "Equation or relation with derivation",
            "Units, dimensions, and limiting cases",
            "Worked numerical / conceptual JEE example",
        ]
    elif any(token in topic for token in ["organic", "reaction", "isomer", "substitution", "elimination", "arene", "amine", "aldehyde", "ketone", "acid", "polymer", "biomolecule"]):
        templates = [
            "Reaction logic and molecular intuition",
            "Rule, reagent, or functional group definition",
            "Mechanism or transformation path step by step",
            "Common JEE pattern and product prediction",
            "Worked JEE-style conversion example",
        ]
    elif any(token in topic for token in ["limit", "derivative", "integral", "probability", "matrix", "determinant", "vector", "coordinate", "circle", "conic", "complex", "series", "sequence"]):
        templates = [
            "Meaning of the mathematical object",
            "Formal definition or theorem statement",
            "Derivation or algebraic manipulation in order",
            "Standard cases, shortcuts, and edge cases",
            "Worked JEE example with full steps",
        ]
    if not templates:
        templates = [
            "Everyday intuition and why the idea matters",
            "Precise definition used in JEE",
            "Key rule or formula and how it is derived",
            "Units, dimensions, or algebraic structure",
            "Worked JEE-style example",
        ]
    return templates


def _subtopic_name(topic):
    text = str(topic or "").strip().replace("_", " ").replace("-", " ")
    return " ".join(word.capitalize() for word in text.split())


def _build_subtopics(subject, unit):
    topics = list(unit.get("topics") or [])
    unit_number = int(unit.get("unit_number") or 0)
    subject_prefix = _subject_prefix(subject)
    subtopics = []
    learn_days = max(1, int(unit.get("estimated_learn_days") or 1))
    estimated_minutes = max(20, round((learn_days * 60) / max(len(topics) or 1, 1)))
    for index, topic in enumerate(topics, start=1):
        subtopics.append(
            {
                "id": f"{subject_prefix}-{unit_number:02d}-{index:02d}",
                "name": _subtopic_name(topic),
                "concepts": _concept_templates(subject, unit.get("name", ""), topic),
                "checkpoint_after": True,
                "estimated_minutes": estimated_minutes,
            }
        )
    if not subtopics:
        subtopics.append(
            {
                "id": f"{subject_prefix}-{unit_number:02d}-01",
                "name": _subtopic_name(unit.get("name", "Chapter")),
                "concepts": _concept_templates(subject, unit.get("name", ""), unit.get("name", "")),
                "checkpoint_after": True,
                "estimated_minutes": estimated_minutes,
            }
        )
    return subtopics


def build_chapter_ready_syllabus():
    syllabus = deepcopy(JEE_SYLLABUS)
    for subject, units in syllabus.items():
        for unit in units:
            unit.setdefault("jee_weightage_percent", unit.get("jee_main_weightage_percent", 0))
            unit.setdefault("prerequisite_units", list(unit.get("prerequisite_unit_numbers", [])))
            unit.setdefault("estimated_days", int(unit.get("estimated_learn_days", 1) or 1))
            unit.setdefault("chapter_test_questions", 15)
            unit.setdefault("chapter_test_duration_minutes", 30)
            unit["subtopics"] = _build_subtopics(subject, unit)
    return syllabus
