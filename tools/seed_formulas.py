import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMULA_DIR = ROOT / "app_data" / "formulas"
FORMULA_PATH = FORMULA_DIR / "jee_formulas.json"


SUBJECT_CHAPTERS = {
    "physics": [
        ("units_dimensions", "Units And Measurements", 1, 2),
        ("kinematics", "Kinematics", 2, 4),
        ("laws_of_motion", "Laws Of Motion", 3, 5),
        ("work_energy_power", "Work Energy And Power", 4, 4),
        ("rotational_motion", "Rotational Motion", 5, 6),
        ("gravitation", "Gravitation", 6, 4),
        ("properties_of_solids", "Properties Of Solids", 7, 2),
        ("properties_of_fluids", "Properties Of Fluids", 8, 3),
        ("thermal_properties", "Thermal Properties Of Matter", 9, 3),
        ("thermodynamics", "Thermodynamics", 10, 4),
        ("kinetic_theory", "Kinetic Theory Of Gases", 11, 2),
        ("shm", "Oscillations", 12, 4),
        ("waves", "Waves", 13, 4),
        ("electrostatics", "Electrostatics", 14, 6),
        ("current_electricity", "Current Electricity", 15, 6),
        ("magnetic_effects", "Magnetic Effects Of Current", 16, 5),
        ("magnetism_matter", "Magnetism And Matter", 17, 2),
        ("emi", "Electromagnetic Induction", 18, 4),
        ("ac_circuits", "Alternating Current", 19, 4),
        ("em_waves", "Electromagnetic Waves", 20, 1),
        ("ray_optics", "Ray Optics", 21, 5),
        ("wave_optics", "Wave Optics", 22, 4),
        ("modern_physics", "Modern Physics", 23, 7),
    ],
    "chemistry": [
        ("some_basic_concepts", "Some Basic Concepts Of Chemistry", 1, 4),
        ("atomic_structure", "Atomic Structure", 2, 4),
        ("periodic_table", "Classification And Periodicity", 3, 3),
        ("chemical_bonding", "Chemical Bonding", 4, 6),
        ("states_of_matter", "States Of Matter", 5, 2),
        ("thermodynamics", "Chemical Thermodynamics", 6, 5),
        ("equilibrium", "Equilibrium", 7, 6),
        ("redox", "Redox Reactions", 8, 3),
        ("hydrogen", "Hydrogen", 9, 1),
        ("s_block", "s-Block Elements", 10, 2),
        ("p_block", "p-Block Elements", 11, 5),
        ("organic_basics", "Organic Chemistry Basics", 12, 5),
        ("hydrocarbons", "Hydrocarbons", 13, 4),
        ("solid_state", "Solid State", 14, 2),
        ("solutions", "Solutions", 15, 5),
        ("electrochemistry", "Electrochemistry", 16, 5),
        ("chemical_kinetics", "Chemical Kinetics", 17, 4),
        ("surface_chemistry", "Surface Chemistry", 18, 2),
        ("d_f_block", "d And f Block Elements", 19, 4),
        ("coordination", "Coordination Compounds", 20, 5),
        ("haloalkanes", "Haloalkanes And Haloarenes", 21, 3),
        ("alcohols_phenols_ethers", "Alcohols Phenols And Ethers", 22, 3),
        ("biomolecules", "Biomolecules And Polymers", 23, 3),
    ],
    "mathematics": [
        ("sets_relations_functions", "Sets Relations And Functions", 1, 3),
        ("trigonometry", "Trigonometry", 2, 5),
        ("complex_numbers", "Complex Numbers", 3, 4),
        ("quadratic_equations", "Quadratic Equations", 4, 3),
        ("sequences_series", "Sequences And Series", 5, 5),
        ("permutations_combinations", "Permutations And Combinations", 6, 4),
        ("binomial_theorem", "Binomial Theorem", 7, 3),
        ("straight_lines", "Straight Lines", 8, 4),
        ("circles", "Circles", 9, 4),
        ("conic_sections", "Conic Sections", 10, 6),
        ("limits_continuity", "Limits Continuity And Differentiability", 11, 7),
        ("differentiation", "Differentiation", 12, 6),
        ("applications_derivatives", "Applications Of Derivatives", 13, 5),
        ("indefinite_integration", "Indefinite Integration", 14, 6),
        ("definite_integration", "Definite Integration", 15, 6),
        ("differential_equations", "Differential Equations", 16, 4),
        ("matrices", "Matrices", 17, 4),
        ("determinants", "Determinants", 18, 4),
        ("vectors", "Vectors", 19, 5),
        ("three_d_geometry", "Three Dimensional Geometry", 20, 5),
        ("probability", "Probability", 21, 5),
        ("statistics", "Statistics", 22, 2),
        ("mathematical_reasoning", "Mathematical Reasoning", 23, 1),
    ],
}


BASE_FORMULAS = {
    "physics": [
        ("Newton Second Law", "F = ma", {"F": "net force", "m": "mass", "a": "acceleration"}, "Use net force along one axis", "Resolve forces before substituting"),
        ("Work Energy Theorem", "W_net = Delta K", {"W_net": "net work", "Delta K": "change in kinetic energy"}, "Particle or rigid body energy accounting", "Energy often avoids lengthy force algebra"),
        ("Average Rate", "average rate = change in quantity / time taken", {"change": "final value - initial value"}, "Average value over a finite interval", "Write what quantity is changing first"),
        ("Power", "P = work / time = dW/dt", {"P": "power", "W": "work", "t": "time"}, "Average or instantaneous depending on context", "Power is the speed of energy transfer"),
    ],
    "chemistry": [
        ("Mole Relation", "n = given mass / molar mass", {"n": "moles", "molar mass": "mass of 1 mole"}, "Use consistent units", "Moles connect mass to particles"),
        ("Concentration", "M = moles of solute / volume of solution in L", {"M": "molarity"}, "Volume must be in litres", "Most mistakes are unit mistakes"),
        ("Equilibrium Form", "K = products / reactants", {"K": "equilibrium constant"}, "Use stoichiometric powers", "Pure solids and liquids do not enter K"),
        ("Ideal Gas Equation", "PV = nRT", {"P": "pressure", "V": "volume", "n": "moles", "T": "temperature in kelvin"}, "Ideal gas approximation", "Always convert temperature to kelvin"),
    ],
    "mathematics": [
        ("Algebraic Identity", "(a + b)^2 = a^2 + 2ab + b^2", {"a,b": "real or complex terms"}, "Expansion identity", "Watch signs"),
        ("Function Idea", "slope = change in y / change in x", {"slope": "rate of change"}, "For straight-line rate", "Graph meaning often solves faster"),
        ("Counting Rule", "total ways = choices_1 x choices_2 x ...", {"choices": "independent selections"}, "Use when choices are independent", "Separate cases first"),
        ("Quadratic Roots", "x = (-b +/- sqrt(b^2 - 4ac)) / 2a", {"a,b,c": "coefficients of ax^2 + bx + c"}, "a is not zero", "Discriminant tells the nature of roots"),
    ],
}


SPECIAL_FORMULAS = {
    "kinematics": [
        ("Equations Of Motion", "v = u + at", {"v": "final velocity (m/s)", "u": "initial velocity (m/s)", "a": "acceleration (m/s^2)", "t": "time (s)"}, "Uniform acceleration only", "Always check if acceleration is constant"),
        ("Displacement", "s = ut + (1/2)at^2", {"s": "displacement"}, "Uniform acceleration only", "Use signs carefully"),
        ("Velocity Displacement", "v^2 = u^2 + 2as", {"s": "displacement"}, "No time needed", "Best when time is not given"),
        ("Projectile Range", "R = u^2 sin(2theta) / g", {"R": "range", "theta": "projection angle"}, "Same launch and landing height", "At 45 degrees range is maximum"),
    ],
    "rotational_motion": [
        ("Torque", "tau = rF sin(theta)", {"tau": "torque", "r": "lever arm"}, "Force at angle theta", "Perpendicular component causes rotation"),
        ("Angular Momentum", "L = I omega", {"I": "moment of inertia", "omega": "angular speed"}, "Rigid body rotation", "Conserve L when external torque is zero"),
        ("Solid Sphere MI", "I = (2/5)MR^2", {"M": "mass", "R": "radius"}, "About diameter", "Shape and axis both matter"),
        ("Ring MI", "I = MR^2", {"M": "mass", "R": "radius"}, "About central axis", "Ring stores mass farthest"),
        ("Disc MI", "I = (1/2)MR^2", {"M": "mass", "R": "radius"}, "About central axis", "Disc is between ring and sphere"),
    ],
    "gravitation": [
        ("Gravitational Force", "F = Gm1m2 / r^2", {"G": "universal gravitational constant"}, "Point masses or spherical bodies", "Inverse-square relation"),
        ("Orbital Velocity", "v = sqrt(GM / r)", {"M": "planet mass", "r": "orbital radius"}, "Circular orbit", "Closer orbit means faster speed"),
        ("Escape Velocity", "ve = sqrt(2GM / R)", {"R": "planet radius"}, "From planet surface", "Escape speed is sqrt(2) times orbital speed near surface"),
        ("Kepler Third Law", "T^2 proportional to r^3", {"T": "time period", "r": "orbit radius"}, "Planetary orbit", "Use ratios to avoid constants"),
    ],
    "shm": [
        ("SHM Acceleration", "a = -omega^2 x", {"x": "displacement"}, "Linear SHM", "Minus sign means restoring"),
        ("Time Period", "T = 2pi / omega", {"omega": "angular frequency"}, "Any SHM", "Find omega first"),
        ("Spring Time Period", "T = 2pi sqrt(m/k)", {"m": "mass", "k": "spring constant"}, "Ideal spring", "More mass means slower"),
        ("Simple Pendulum", "T = 2pi sqrt(l/g)", {"l": "length"}, "Small oscillations", "Mass does not matter"),
    ],
    "waves": [
        ("Wave Speed", "v = f lambda", {"f": "frequency", "lambda": "wavelength"}, "Progressive wave", "Frequency comes from source"),
        ("String Speed", "v = sqrt(T/mu)", {"T": "tension", "mu": "mass per unit length"}, "Stretched string", "Tighter string is faster"),
        ("Doppler Effect", "f' = f(v +/- observer)/(v -/+ source)", {"f'": "apparent frequency"}, "Along line of motion", "Signs decide marks"),
    ],
    "electrostatics": [
        ("Coulomb Law", "F = kq1q2 / r^2", {"k": "1/(4pi epsilon0)"}, "Point charges", "Direction is along joining line"),
        ("Electric Field", "E = F/q", {"E": "electric field"}, "Test charge idea", "Field is force per unit charge"),
        ("Potential", "V = kq / r", {"V": "electric potential"}, "Point charge", "Potential is scalar"),
        ("Capacitance", "C = Q/V", {"C": "capacitance"}, "Any capacitor", "Parallel plate C = epsilon A/d"),
    ],
    "current_electricity": [
        ("Ohm Law", "V = IR", {"V": "potential difference", "I": "current", "R": "resistance"}, "Ohmic conductor", "Slope of V-I graph is R"),
        ("Power", "P = VI = I^2R = V^2/R", {"P": "power"}, "Resistor power", "Choose form with given data"),
        ("Series Resistance", "R_eq = R1 + R2 + ...", {"R_eq": "equivalent resistance"}, "Series circuit", "Current same in series"),
        ("Parallel Resistance", "1/R_eq = 1/R1 + 1/R2 + ...", {"R_eq": "equivalent resistance"}, "Parallel circuit", "Voltage same in parallel"),
    ],
    "magnetic_effects": [
        ("Lorentz Force", "F = qvB sin(theta)", {"B": "magnetic field"}, "Moving charge in magnetic field", "No work by magnetic force"),
        ("Biot Savart", "dB = mu0 I dl sin(theta) / (4pi r^2)", {"dB": "small magnetic field"}, "Current element", "Use symmetry"),
        ("Ampere Law", "integral B dl = mu0 I_enclosed", {"I_enclosed": "current through loop"}, "High symmetry", "Choose Amperian loop wisely"),
    ],
    "emi": [
        ("Faraday Law", "emf = -d(phi)/dt", {"phi": "magnetic flux"}, "Changing flux", "Minus sign is Lenz law"),
        ("Motional EMF", "emf = Blv", {"B": "field", "l": "length", "v": "speed"}, "Rod moving perpendicular to B", "Area change causes emf"),
    ],
    "ac_circuits": [
        ("Capacitive Reactance", "Xc = 1/(omega C)", {"C": "capacitance"}, "AC capacitor", "Higher frequency lowers Xc"),
        ("Inductive Reactance", "XL = omega L", {"L": "inductance"}, "AC inductor", "Higher frequency raises XL"),
        ("Impedance", "Z = sqrt(R^2 + (XL - Xc)^2)", {"Z": "impedance"}, "Series RLC", "At resonance XL = Xc"),
        ("Resonance", "omega0 = 1/sqrt(LC)", {"omega0": "resonant angular frequency"}, "RLC resonance", "Current is maximum"),
    ],
    "ray_optics": [
        ("Mirror Formula", "1/f = 1/v + 1/u", {"f": "focal length", "v": "image distance", "u": "object distance"}, "Spherical mirror", "Use sign convention"),
        ("Lens Formula", "1/f = 1/v - 1/u", {"f": "focal length"}, "Thin lens", "Do not mix mirror signs"),
        ("Power Of Lens", "P = 1/f in metre", {"P": "power in dioptre"}, "Lens in air", "Use f in metre"),
        ("Prism Deviation", "delta = i + e - A", {"A": "prism angle"}, "Prism geometry", "At minimum deviation i = e"),
    ],
    "wave_optics": [
        ("YDSE Fringe Width", "beta = lambda D / d", {"D": "screen distance", "d": "slit separation"}, "Young double slit", "Path difference drives brightness"),
        ("Constructive Interference", "path difference = n lambda", {"n": "integer"}, "Bright fringe", "Central bright has n = 0"),
        ("Destructive Interference", "path difference = (2n+1)lambda/2", {"n": "integer"}, "Dark fringe", "Half wavelength gives dark"),
    ],
    "modern_physics": [
        ("Photoelectric Equation", "Kmax = hf - phi", {"h": "Planck constant", "f": "frequency", "phi": "work function"}, "Photoelectric effect", "Intensity changes current, not stopping potential"),
        ("de Broglie Wavelength", "lambda = h/p", {"p": "momentum"}, "Matter waves", "Small particles show wave nature"),
        ("Bohr Radius", "rn = n^2 a0 / Z", {"n": "orbit number", "Z": "atomic number"}, "Hydrogen-like atom", "Only for single-electron species"),
        ("Bohr Energy", "En = -13.6 Z^2 / n^2 eV", {"En": "energy level"}, "Hydrogen-like atom", "Energy is negative for bound electron"),
    ],
    "some_basic_concepts": [
        ("Moles", "n = mass / molar mass", {"n": "moles"}, "Mass in grams", "Mole is a counting unit"),
        ("Particles", "number of particles = n x NA", {"NA": "Avogadro number"}, "Moles to particles", "One mole means 6.022 x 10^23"),
        ("Molarity", "M = n / V", {"V": "volume in litre"}, "Solutions", "Volume must be litre"),
        ("Percentage Yield", "yield % = actual / theoretical x 100", {"actual": "obtained amount"}, "Reaction yield", "Compare same units"),
    ],
    "thermodynamics": [
        ("First Law", "Delta U = q + w", {"Delta U": "internal energy change", "q": "heat", "w": "work"}, "Chemistry sign convention", "Work on system is positive"),
        ("Enthalpy", "Delta H = Delta U + Delta n_g RT", {"Delta n_g": "gas mole change"}, "Gaseous reactions", "Use only gas mole change"),
        ("Gibbs Energy", "Delta G = Delta H - T Delta S", {"Delta G": "free energy"}, "Constant T,P", "Spontaneous if Delta G < 0"),
    ],
    "electrochemistry": [
        ("Nernst Equation", "E = E0 - (0.0591/n) log Q", {"n": "electrons transferred"}, "At 298 K", "Reaction quotient decides voltage"),
        ("Faraday First Law", "m = ZIt", {"m": "mass deposited", "I": "current", "t": "time"}, "Electrolysis", "Charge = It"),
        ("Conductance", "G = 1/R", {"G": "conductance"}, "Conducting solution", "Conductivity depends on ions"),
    ],
    "chemical_kinetics": [
        ("Rate Law", "rate = k[A]^m[B]^n", {"k": "rate constant"}, "Experiment decides order", "Do not use coefficients blindly"),
        ("First Order", "k = 2.303/t log(a/(a-x))", {"a": "initial concentration"}, "First-order reaction", "Half-life is constant"),
        ("Arrhenius", "k = A e^(-Ea/RT)", {"Ea": "activation energy"}, "Temperature effect", "Higher temperature increases k"),
    ],
    "solutions": [
        ("Raoult Law", "p = x p0", {"x": "mole fraction"}, "Ideal solution", "Vapour pressure follows mole fraction"),
        ("Boiling Point Elevation", "Delta Tb = i Kb m", {"i": "van't Hoff factor", "m": "molality"}, "Dilute solution", "Use molality"),
        ("Osmotic Pressure", "pi = iMRT", {"M": "molarity"}, "Dilute solution", "Best for molar mass"),
    ],
    "equilibrium": [
        ("Kp Kc Relation", "Kp = Kc(RT)^Delta n", {"Delta n": "gas product moles - gas reactant moles"}, "Gas equilibrium", "Only gaseous moles count"),
        ("Ionic Product", "Kw = [H+][OH-]", {"Kw": "water ionic product"}, "Aqueous solutions", "At 25 C, Kw = 10^-14"),
        ("pH", "pH = -log[H+]", {"[H+]": "hydrogen ion concentration"}, "Acid-base", "Lower pH means stronger acidity"),
    ],
    "limits_continuity": [
        ("Standard Limit 1", "limit sin x / x = 1 as x -> 0", {"x": "angle in radians"}, "x in radians", "Radians are mandatory"),
        ("Standard Limit 2", "limit (1 - cos x)/x^2 = 1/2 as x -> 0", {"x": "angle"}, "x in radians", "Use for trig limits"),
        ("Continuity", "left limit = right limit = function value", {"limit": "approaching value"}, "Continuity at a point", "Check all three"),
    ],
    "differentiation": [
        ("Power Rule", "d/dx x^n = n x^(n-1)", {"n": "constant power"}, "Power functions", "Reduce power by 1"),
        ("Product Rule", "d/dx(uv) = u v' + v u'", {"u,v": "functions"}, "Product of functions", "Both terms are needed"),
        ("Chain Rule", "d/dx f(g(x)) = f'(g(x)) g'(x)", {"g(x)": "inner function"}, "Composite functions", "Differentiate outside then inside"),
        ("Trig Derivative", "d/dx sin x = cos x", {"x": "radian angle"}, "Radians", "Cos comes from sin"),
    ],
    "indefinite_integration": [
        ("Power Integral", "integral x^n dx = x^(n+1)/(n+1) + C", {"n": "not equal to -1"}, "Power functions", "Do not forget C"),
        ("Log Integral", "integral 1/x dx = ln|x| + C", {"x": "non-zero"}, "Reciprocal function", "Absolute value matters"),
        ("Trig Integral", "integral cos x dx = sin x + C", {"x": "radian angle"}, "Standard trig", "Differentiate to check"),
    ],
    "probability": [
        ("Conditional Probability", "P(A|B) = P(A intersection B)/P(B)", {"P(B)": "non-zero probability"}, "Given B happened", "Condition changes sample space"),
        ("Bayes Theorem", "P(Ai|B) = P(Ai)P(B|Ai) / sum P(Aj)P(B|Aj)", {"Ai": "partition event"}, "Reverse probability", "Denominator is total probability"),
        ("Binomial", "P(X=r) = nCr p^r q^(n-r)", {"p": "success probability", "q": "1-p"}, "Independent trials", "Fixed number of trials"),
    ],
    "vectors": [
        ("Dot Product", "a dot b = |a||b| cos theta", {"theta": "angle between vectors"}, "Scalar product", "Zero for perpendicular"),
        ("Cross Product", "|a x b| = |a||b| sin theta", {"theta": "angle between vectors"}, "Vector product", "Direction by right-hand rule"),
        ("Projection", "projection of a on b = (a dot b)/|b|", {"a,b": "vectors"}, "Scalar projection", "Projection needs direction"),
    ],
    "three_d_geometry": [
        ("Distance Formula", "distance = sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)", {"x,y,z": "coordinates"}, "3D points", "Same as 2D with z added"),
        ("Plane", "ax + by + cz + d = 0", {"a,b,c": "normal vector components"}, "Plane equation", "Normal vector is key"),
        ("Line Vector Form", "r = a + lambda b", {"a": "point vector", "b": "direction vector"}, "3D line", "Direction vector drives line"),
    ],
    "matrices": [
        ("Matrix Multiplication", "(AB)ij = sum aik bkj", {"i,j,k": "indices"}, "Compatible order", "AB may not equal BA"),
        ("Inverse", "A inverse = adj(A)/det(A)", {"det(A)": "determinant"}, "det(A) not zero", "Singular matrix has no inverse"),
    ],
    "determinants": [
        ("Area Of Triangle", "area = 1/2 |x1(y2-y3)+x2(y3-y1)+x3(y1-y2)|", {"x,y": "coordinates"}, "Coordinate triangle", "Zero area means collinear"),
        ("Cramer's Rule", "x = Dx/D, y = Dy/D", {"D": "main determinant"}, "Linear equations", "D must not be zero"),
    ],
    "straight_lines": [
        ("Slope", "m = (y2-y1)/(x2-x1)", {"m": "slope"}, "Two points", "Vertical line has undefined slope"),
        ("Point Slope", "y - y1 = m(x - x1)", {"m": "slope"}, "Line through point", "Fastest line form"),
        ("Distance From Line", "distance = |ax1+by1+c|/sqrt(a^2+b^2)", {"a,b,c": "line constants"}, "Point to line", "Use absolute value"),
    ],
    "circles": [
        ("Circle Standard", "(x-h)^2 + (y-k)^2 = r^2", {"h,k": "centre", "r": "radius"}, "Circle with centre", "Read centre directly"),
        ("General Circle", "x^2 + y^2 + 2gx + 2fy + c = 0", {"centre": "(-g,-f)"}, "General form", "Radius = sqrt(g^2+f^2-c)"),
    ],
    "conic_sections": [
        ("Parabola", "y^2 = 4ax", {"a": "focal distance"}, "Standard right parabola", "Focus is (a,0)"),
        ("Ellipse", "x^2/a^2 + y^2/b^2 = 1", {"a,b": "semi axes"}, "Standard ellipse", "a bigger axis is major"),
        ("Hyperbola", "x^2/a^2 - y^2/b^2 = 1", {"a,b": "semi axes"}, "Standard hyperbola", "Transverse axis decides sign"),
    ],
}


def _formula(fid, item):
    name, formula, variables, condition, tip = item
    return {
        "id": fid,
        "name": name,
        "formula": formula,
        "variables": variables,
        "condition": condition,
        "jee_tip": tip,
        "quick_memory": tip,
    }


def _chapter_formulas(subject, chapter_id, chapter_name):
    items = SPECIAL_FORMULAS.get(chapter_id) or BASE_FORMULAS[subject]
    formulas = []
    for index, item in enumerate(items, start=1):
        formulas.append(_formula(f"{subject[:3].upper()}_{chapter_id[:3].upper()}_{index:03d}", item))
    return formulas


def build_database():
    subjects = {}
    for subject, chapters in SUBJECT_CHAPTERS.items():
        subject_chapters = []
        for chapter_id, name, unit_number, weightage in chapters:
            formulas = _chapter_formulas(subject, chapter_id, name)
            subject_chapters.append({
                "id": chapter_id,
                "name": name,
                "unit_number": unit_number,
                "jee_weightage": weightage,
                "formulas": formulas,
                "shortcuts": [
                    {
                        "id": f"{subject[:3].upper()}_{chapter_id[:3].upper()}_S001",
                        "title": f"Fast setup for {name}",
                        "detail": "Write known values, choose the condition, then substitute. Most JEE mistakes happen before calculation.",
                    }
                ],
                "common_mistakes": [
                    "Using a formula without checking its condition",
                    "Mixing units or signs during substitution",
                    "Skipping the final reasonableness check",
                ],
            })
            print(f"Seeded {subject}: {name} ({len(formulas)} formulas)")
        subjects[subject] = {"chapters": subject_chapters}
    return {"subjects": subjects}


def maybe_generate_with_gemini(database):
    if os.getenv("FORMULA_SEED_USE_GEMINI") != "1":
        return database
    try:
        from google import genai

        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Gemini formula expansion skipped: missing GEMINI_API_KEY/GOOGLE_API_KEY")
            return database
        client = genai.Client(api_key=api_key)
        prompt = (
            "Improve this JEE formula database JSON by adding missing high-yield formulas while keeping the exact schema. "
            "Return only valid JSON.\n\n"
            + json.dumps(database)
        )
        response = client.models.generate_content(model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"), contents=prompt)
        text = (response.text or "").strip()
        if text.startswith("```"):
            text = text.strip("`")
            text = text.replace("json", "", 1).strip()
        expanded = json.loads(text)
        print("Gemini formula expansion applied")
        return expanded
    except Exception as exc:
        print(f"Gemini formula expansion skipped: {exc}")
        return database


def main():
    FORMULA_DIR.mkdir(parents=True, exist_ok=True)
    database = maybe_generate_with_gemini(build_database())
    FORMULA_PATH.write_text(json.dumps(database, indent=2, ensure_ascii=False), encoding="utf-8")
    count = sum(
        len(chapter.get("formulas", []))
        for subject in database.get("subjects", {}).values()
        for chapter in subject.get("chapters", [])
    )
    chapter_count = sum(len(subject.get("chapters", [])) for subject in database.get("subjects", {}).values())
    print(f"Saved {chapter_count} chapters and {count} formulas to {FORMULA_PATH}")


if __name__ == "__main__":
    main()
