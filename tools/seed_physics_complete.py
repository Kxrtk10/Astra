import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.knowledge_base_tools import KB_SOURCES_ROOT, add_document_to_kb, get_kb_stats, init_knowledge_base


PHYSICS_UNITS = [
    {
        "unit": "Units and Measurements",
        "slug": "units_and_measurements",
        "weightage": 2,
        "prerequisites": ["Basic algebra", "Scientific notation"],
        "concepts": [
            "Physical quantities need a number and a unit; without the unit, the number has no physical meaning.",
            "Fundamental and derived units separate base measurements from quantities built using them.",
            "Dimensions track the powers of M, L, T, I, K, mol, and cd in a formula.",
            "Dimensional analysis checks consistency, derives proportional dependence, and converts units.",
            "Significant figures preserve realistic precision after measurement and calculation.",
            "Errors may be absolute, relative, percentage, random, systematic, or instrumental.",
        ],
        "formulas": [
            "[v] = LT^-1; velocity is displacement per unit time.",
            "[a] = LT^-2; acceleration is rate of change of velocity.",
            "[F] = MLT^-2; use F = ma as the dimensional anchor.",
            "[E] = ML^2T^-2; work and energy share the same dimensions.",
            "Percentage error = (absolute error / measured value) x 100.",
            "For products and quotients, fractional errors add.",
            "For powers, fractional error is multiplied by the power.",
        ],
    },
    {
        "unit": "Kinematics",
        "slug": "kinematics",
        "weightage": 6,
        "prerequisites": ["Units and Measurements", "Vectors", "Graphs"],
        "concepts": [
            "Position, displacement, velocity, and acceleration describe motion without asking why it happens.",
            "Average and instantaneous quantities differ; instantaneous values come from slopes or derivatives.",
            "Uniform acceleration allows SUVAT equations, but only when acceleration is constant.",
            "Graphs encode motion: slope of x-t is velocity, slope of v-t is acceleration, area under v-t is displacement.",
            "Projectile motion is two independent one-dimensional motions connected by time.",
            "Relative velocity describes motion as seen from another moving observer.",
        ],
        "formulas": [
            "v = u + at; valid only for constant acceleration.",
            "s = ut + (1/2)at^2; displacement after time t.",
            "v^2 = u^2 + 2as; eliminates time.",
            "x = u cos(theta)t; horizontal projectile motion.",
            "y = u sin(theta)t - (1/2)gt^2; vertical projectile motion.",
            "T = 2u sin(theta)/g, H = u^2 sin^2(theta)/(2g), R = u^2 sin(2theta)/g for same-level projectile.",
            "v_AB = v_A - v_B; relative velocity of A with respect to B.",
        ],
    },
    {
        "unit": "Laws of Motion",
        "slug": "laws_of_motion",
        "weightage": 7,
        "prerequisites": ["Kinematics", "Vectors", "Free body diagrams"],
        "concepts": [
            "Newton's laws connect force with change in motion.",
            "A free body diagram is the real starting point of every mechanics question.",
            "Inertia resists change in velocity, not motion itself.",
            "Friction adjusts up to a limiting value before sliding begins.",
            "Tension and normal reactions are constraint forces determined by the situation.",
            "Pseudo force appears in non-inertial frames and equals -ma_frame.",
        ],
        "formulas": [
            "Sum F = ma; net external force equals mass times acceleration.",
            "f_s <= mu_s N; static friction is self-adjusting.",
            "f_k = mu_k N; kinetic friction has nearly fixed magnitude.",
            "On an incline: mg sin(theta) along the plane, mg cos(theta) normal to plane.",
            "Impulse J = integral F dt = Delta p.",
            "In accelerating frame, F_pseudo = -m a_frame.",
        ],
    },
    {
        "unit": "Work Energy Power",
        "slug": "work_energy_power",
        "weightage": 6,
        "prerequisites": ["Laws of Motion", "Kinematics", "Vectors"],
        "concepts": [
            "Work measures energy transfer by force along displacement.",
            "Kinetic energy is the energy of motion and depends on speed squared.",
            "Potential energy belongs to conservative-force systems.",
            "Work-energy theorem replaces force-time tracking with energy bookkeeping.",
            "Power measures the rate at which work is done or energy is transferred.",
            "Conservative forces make mechanical energy conservation possible.",
        ],
        "formulas": [
            "W = integral F dot dr; only the component along displacement does work.",
            "K = (1/2)mv^2.",
            "W_net = Delta K.",
            "U_g = mgh near Earth's surface.",
            "U_s = (1/2)kx^2 for a spring.",
            "P_avg = W/t and P_inst = F dot v.",
            "For conservative systems, K_i + U_i = K_f + U_f.",
        ],
    },
    {
        "unit": "Rotational Motion",
        "slug": "rotational_motion",
        "weightage": 8,
        "prerequisites": ["Kinematics", "Laws of Motion", "Work Energy Power"],
        "concepts": [
            "Rigid body motion combines translation of centre of mass and rotation about an axis.",
            "Angular variables mirror linear variables but apply to rotation.",
            "Moment of inertia measures resistance to angular acceleration and depends on axis.",
            "Torque is the rotational effect of force.",
            "Angular momentum is conserved when external torque is zero.",
            "Rolling without slipping ties translation and rotation through v = omega R.",
        ],
        "formulas": [
            "s = r theta, v = r omega, a_t = r alpha.",
            "tau = r x F and |tau| = rF sin(theta).",
            "I = sum mr^2 or integral r^2 dm.",
            "tau_net = I alpha for fixed-axis rotation.",
            "K_rot = (1/2)I omega^2.",
            "L = I omega for fixed-axis rotation.",
            "K_rolling = (1/2)Mv_cm^2 + (1/2)I_cm omega^2.",
        ],
    },
    {
        "unit": "Gravitation",
        "slug": "gravitation",
        "weightage": 4,
        "prerequisites": ["Vectors", "Laws of Motion", "Circular motion"],
        "concepts": [
            "Every mass attracts every other mass with a force along their line of centres.",
            "Gravitational field gives force per unit test mass.",
            "Potential is work done per unit mass in bringing a mass from infinity.",
            "Planetary motion follows central-force dynamics and conservation of angular momentum.",
            "Escape speed comes from total mechanical energy becoming zero.",
            "Satellite energy is negative for bound circular orbits.",
        ],
        "formulas": [
            "F = Gm1m2/r^2.",
            "g = GM/r^2 outside a spherical planet.",
            "V = -GM/r; gravitational potential.",
            "U = -GMm/r; potential energy.",
            "v_orb = sqrt(GM/r).",
            "v_esc = sqrt(2GM/R).",
            "T^2 = 4pi^2 r^3/(GM).",
        ],
    },
    {
        "unit": "Properties of Matter",
        "slug": "properties_of_matter",
        "weightage": 5,
        "prerequisites": ["Units and Measurements", "Forces", "Energy"],
        "concepts": [
            "Elasticity describes how solids deform and recover under stress.",
            "Stress is restoring force per area and strain is fractional deformation.",
            "Surface tension makes liquid surfaces behave like stretched membranes.",
            "Viscosity is internal friction in fluid flow.",
            "Bernoulli's theorem connects pressure, speed, and height in ideal flow.",
            "Thermal expansion changes dimensions with temperature.",
        ],
        "formulas": [
            "Young's modulus Y = stress/strain = (F/A)/(Delta L/L).",
            "Bulk modulus K = -Delta P/(Delta V/V).",
            "Surface energy = surface tension x area increase.",
            "Excess pressure in drop = 2T/R; in soap bubble = 4T/R.",
            "Poiseuille flow Q = pi P r^4/(8 eta l).",
            "Stokes force F = 6 pi eta r v.",
            "Bernoulli: P + (1/2)rho v^2 + rho gh = constant.",
        ],
    },
    {
        "unit": "Thermodynamics",
        "slug": "thermodynamics",
        "weightage": 7,
        "prerequisites": ["Kinetic Theory of Gases", "Work Energy Power"],
        "concepts": [
            "Thermodynamics studies heat, work, temperature, and internal energy macroscopically.",
            "Zeroth law gives the meaning of temperature through thermal equilibrium.",
            "First law is energy conservation for thermal systems.",
            "Specific heats describe heat required for temperature change.",
            "Cyclic processes return the gas to its initial state.",
            "Second law limits conversion of heat into work and introduces entropy direction.",
        ],
        "formulas": [
            "Delta Q = Delta U + W by the system.",
            "For ideal gas, Delta U = n C_v Delta T.",
            "Isothermal ideal gas work W = nRT ln(V2/V1).",
            "Adiabatic relation PV^gamma = constant.",
            "C_p - C_v = R.",
            "Efficiency eta = W/Q_in = 1 - Q_out/Q_in.",
            "Carnot efficiency eta = 1 - T_c/T_h.",
        ],
    },
    {
        "unit": "Kinetic Theory of Gases",
        "slug": "kinetic_theory_of_gases",
        "weightage": 3,
        "prerequisites": ["Units and Measurements", "Basic probability", "Thermodynamics"],
        "concepts": [
            "Gas pressure comes from molecular collisions with container walls.",
            "Temperature measures average translational kinetic energy.",
            "RMS speed, average speed, and most probable speed are different averages.",
            "Degrees of freedom determine energy storage modes.",
            "Equipartition assigns (1/2)kT energy per quadratic degree of freedom.",
            "Mean free path estimates average distance between molecular collisions.",
        ],
        "formulas": [
            "PV = nRT = NkT.",
            "P = (1/3)rho v_rms^2.",
            "(1/2)m v_rms^2 = (3/2)kT.",
            "v_rms = sqrt(3RT/M).",
            "Internal energy U = (f/2)nRT.",
            "C_v = fR/2 and C_p = C_v + R.",
            "Mean free path lambda = 1/(sqrt(2) pi d^2 n).",
        ],
    },
    {
        "unit": "Simple Harmonic Motion",
        "slug": "simple_harmonic_motion",
        "weightage": 5,
        "prerequisites": ["Kinematics", "Circular motion", "Differential equations"],
        "concepts": [
            "SHM occurs when restoring force is proportional and opposite to displacement.",
            "The motion can be viewed as projection of uniform circular motion.",
            "Phase tells where the oscillator is in its cycle.",
            "Energy keeps switching between kinetic and potential forms.",
            "Spring-mass and small-angle pendulum are standard JEE models.",
            "Damped and forced oscillations explain real oscillators and resonance.",
        ],
        "formulas": [
            "a = -omega^2 x.",
            "x = A sin(omega t + phi) or A cos(omega t + phi).",
            "v = omega sqrt(A^2 - x^2).",
            "T = 2pi/omega.",
            "Spring: omega = sqrt(k/m), T = 2pi sqrt(m/k).",
            "Simple pendulum: T = 2pi sqrt(l/g) for small angles.",
            "Total energy E = (1/2)kA^2.",
        ],
    },
    {
        "unit": "Waves",
        "slug": "waves",
        "weightage": 5,
        "prerequisites": ["Simple Harmonic Motion", "Superposition", "Graphs"],
        "concepts": [
            "A wave transfers energy and phase without net transport of matter.",
            "Transverse and longitudinal waves differ by direction of particle oscillation.",
            "Superposition explains interference, beats, and standing waves.",
            "Sound waves need a medium and are longitudinal in air.",
            "Standing waves form when two equal opposite waves superpose.",
            "Doppler effect changes observed frequency due to relative motion.",
        ],
        "formulas": [
            "v = f lambda.",
            "y = A sin(kx - omega t + phi).",
            "k = 2pi/lambda and omega = 2pi f.",
            "String wave speed v = sqrt(T/mu).",
            "Sound speed in gas v = sqrt(gamma P/rho).",
            "Beat frequency = |f1 - f2|.",
            "Doppler: f' = f(v +/- v_o)/(v -/+ v_s) with sign from relative motion.",
        ],
    },
    {
        "unit": "Electrostatics",
        "slug": "electrostatics",
        "weightage": 8,
        "prerequisites": ["Vectors", "Integration", "Gravitation analogy"],
        "concepts": [
            "Charge is quantized and conserved.",
            "Coulomb force acts along the line joining point charges.",
            "Electric field is force per unit positive test charge.",
            "Electric potential is work per unit charge and is scalar.",
            "Gauss law uses symmetry to find electric field efficiently.",
            "Capacitors store energy in electric fields.",
        ],
        "formulas": [
            "F = k q1 q2/r^2 where k = 1/(4 pi epsilon0).",
            "E = F/q0.",
            "Point charge field E = kq/r^2.",
            "V = kq/r.",
            "E = -dV/dr in one dimension.",
            "Gauss law: integral E dot dA = q_enclosed/epsilon0.",
            "Capacitance C = Q/V and energy U = (1/2)CV^2 = Q^2/(2C).",
        ],
    },
    {
        "unit": "Current Electricity",
        "slug": "current_electricity",
        "weightage": 7,
        "prerequisites": ["Electrostatics", "Algebra", "Circuit basics"],
        "concepts": [
            "Current is the rate of flow of charge through a cross-section.",
            "Resistance measures opposition to current and depends on material and geometry.",
            "Ohm's law applies to ohmic conductors at constant temperature.",
            "Kirchhoff laws are conservation of charge and energy in circuits.",
            "Cells have internal resistance, so terminal voltage can differ from emf.",
            "Wheatstone and meter bridge problems rely on balanced potential points.",
        ],
        "formulas": [
            "I = dq/dt.",
            "V = IR for ohmic conductors.",
            "R = rho L/A.",
            "J = sigma E and I = n e A v_d.",
            "Power P = VI = I^2R = V^2/R.",
            "Series: R_eq = sum R; parallel: 1/R_eq = sum 1/R.",
            "Terminal voltage V = E - Ir during discharge.",
        ],
    },
    {
        "unit": "Magnetic Effects of Current",
        "slug": "magnetic_effects_of_current",
        "weightage": 6,
        "prerequisites": ["Current Electricity", "Vectors", "Circular motion"],
        "concepts": [
            "Moving charges and currents produce magnetic fields.",
            "Magnetic force acts perpendicular to velocity and magnetic field.",
            "Biot-Savart law builds fields from current elements.",
            "Ampere law finds fields in highly symmetric current distributions.",
            "A current loop behaves like a magnetic dipole.",
            "Charged particles move in circular or helical paths in uniform magnetic fields.",
        ],
        "formulas": [
            "F = q(v x B).",
            "Force on wire F = I(L x B).",
            "Biot-Savart: dB = mu0 I dl sin(theta)/(4 pi r^2).",
            "Long wire B = mu0 I/(2 pi r).",
            "Loop centre B = mu0 I/(2R).",
            "Solenoid B = mu0 nI.",
            "Radius r = mv/(qB) for perpendicular entry.",
        ],
    },
    {
        "unit": "Magnetism and Matter",
        "slug": "magnetism_and_matter",
        "weightage": 3,
        "prerequisites": ["Magnetic Effects of Current", "Dipoles", "Vectors"],
        "concepts": [
            "Magnetic dipoles experience torque in magnetic fields.",
            "Earth's magnetism is resolved into horizontal and vertical components.",
            "Magnetization is magnetic moment per unit volume.",
            "Dia-, para-, and ferromagnetic materials differ by susceptibility and domain behavior.",
            "Hysteresis describes lag of magnetization behind magnetizing field.",
            "Magnetic field intensity H and flux density B separate source current from material response.",
        ],
        "formulas": [
            "Torque tau = M x B.",
            "Potential energy U = -M dot B.",
            "B = mu0(H + M).",
            "M = chi H.",
            "mu_r = 1 + chi.",
            "tan(delta) = B_V/B_H for dip angle.",
            "Time period of magnetic needle T = 2pi sqrt(I/(MB_H)).",
        ],
    },
    {
        "unit": "Electromagnetic Induction",
        "slug": "electromagnetic_induction",
        "weightage": 6,
        "prerequisites": ["Magnetic Effects of Current", "Flux", "Calculus"],
        "concepts": [
            "Changing magnetic flux induces emf.",
            "Lenz law gives the direction that opposes the cause of flux change.",
            "Motional emf comes from magnetic force on moving charges.",
            "Self inductance resists change in current in the same circuit.",
            "Mutual inductance couples changing current in one coil to emf in another.",
            "Eddy currents are circulating induced currents in bulk conductors.",
        ],
        "formulas": [
            "Magnetic flux phi = integral B dot dA.",
            "Faraday law epsilon = -dphi/dt.",
            "For N turns, epsilon = -N dphi/dt.",
            "Motional emf epsilon = B l v for perpendicular rod.",
            "Self induced emf epsilon = -L dI/dt.",
            "Energy in inductor U = (1/2)LI^2.",
            "Mutual emf epsilon2 = -M dI1/dt.",
        ],
    },
    {
        "unit": "Alternating Current",
        "slug": "alternating_current",
        "weightage": 5,
        "prerequisites": ["Electromagnetic Induction", "Phasors", "Trigonometry"],
        "concepts": [
            "AC voltage and current vary sinusoidally with time.",
            "RMS values give equivalent DC heating effect.",
            "Inductors and capacitors introduce phase differences.",
            "Impedance generalizes resistance for AC circuits.",
            "Series LCR circuits can resonate when inductive and capacitive reactances cancel.",
            "Transformers transfer AC power through mutual induction.",
        ],
        "formulas": [
            "V = V0 sin(omega t), I = I0 sin(omega t + phi).",
            "V_rms = V0/sqrt(2), I_rms = I0/sqrt(2).",
            "X_L = omega L.",
            "X_C = 1/(omega C).",
            "Z = sqrt(R^2 + (X_L - X_C)^2).",
            "tan(phi) = (X_L - X_C)/R.",
            "Resonance omega0 = 1/sqrt(LC).",
        ],
    },
    {
        "unit": "Electromagnetic Waves",
        "slug": "electromagnetic_waves",
        "weightage": 2,
        "prerequisites": ["Electromagnetic Induction", "Electric and magnetic fields"],
        "concepts": [
            "Accelerating charges produce electromagnetic waves.",
            "Electric and magnetic fields oscillate perpendicular to each other and to the direction of propagation.",
            "EM waves do not require a material medium.",
            "The speed in vacuum is determined by epsilon0 and mu0.",
            "The electromagnetic spectrum is organized by frequency and wavelength.",
            "Energy flow is described by the Poynting vector.",
        ],
        "formulas": [
            "c = 1/sqrt(mu0 epsilon0).",
            "c = f lambda in vacuum.",
            "E0/B0 = c.",
            "Average energy density u = (1/2)epsilon0 E^2 + B^2/(2mu0).",
            "Poynting vector S = (1/mu0)(E x B).",
            "Radiation pressure p = I/c for absorption and 2I/c for reflection.",
        ],
    },
    {
        "unit": "Ray Optics",
        "slug": "ray_optics",
        "weightage": 7,
        "prerequisites": ["Geometry", "Trigonometry", "Sign convention"],
        "concepts": [
            "Ray optics treats light as straight-line rays when wavelength is small compared with objects.",
            "Reflection follows equal angle of incidence and reflection.",
            "Refraction comes from speed change across media.",
            "Total internal reflection occurs from denser to rarer medium beyond critical angle.",
            "Mirrors and lenses form images using paraxial approximation.",
            "Optical instruments combine lenses to improve angular magnification.",
        ],
        "formulas": [
            "Mirror formula: 1/f = 1/v + 1/u.",
            "Magnification m = -v/u for mirrors.",
            "Snell law n1 sin i = n2 sin r.",
            "Critical angle sin C = n2/n1 for n1 > n2.",
            "Lens formula: 1/f = 1/v - 1/u.",
            "Lens maker: 1/f = (mu - 1)(1/R1 - 1/R2).",
            "Power P = 1/f in metres.",
        ],
    },
    {
        "unit": "Wave Optics",
        "slug": "wave_optics",
        "weightage": 5,
        "prerequisites": ["Waves", "Ray Optics", "Path difference"],
        "concepts": [
            "Wave optics explains phenomena ray optics cannot, such as interference and diffraction.",
            "Coherent sources maintain a constant phase difference.",
            "Young's double slit experiment converts path difference into bright and dark fringes.",
            "Diffraction is bending/spreading around apertures.",
            "Polarization proves the transverse nature of light.",
            "Resolving power depends on aperture and wavelength.",
        ],
        "formulas": [
            "Path difference in YDSE Delta = d x/D.",
            "Fringe width beta = lambda D/d.",
            "Constructive: Delta = n lambda.",
            "Destructive: Delta = (n + 1/2)lambda.",
            "Single slit minima: a sin(theta) = n lambda.",
            "Malus law I = I0 cos^2(theta).",
            "Brewster law tan i_B = n.",
        ],
    },
    {
        "unit": "Dual Nature of Matter",
        "slug": "dual_nature_of_matter",
        "weightage": 4,
        "prerequisites": ["Modern physics basics", "Energy conservation", "Waves"],
        "concepts": [
            "Light behaves as photons in emission and absorption experiments.",
            "Photoelectric effect shows threshold frequency and instantaneous emission.",
            "Stopping potential measures maximum kinetic energy of photoelectrons.",
            "Matter waves assign wavelength to moving particles.",
            "de Broglie hypothesis connects momentum and wavelength.",
            "Davisson-Germer experiment verified electron wave nature.",
        ],
        "formulas": [
            "Photon energy E = hf = hc/lambda.",
            "Photoelectric equation hf = phi + K_max.",
            "K_max = eV_s.",
            "Threshold frequency f0 = phi/h.",
            "de Broglie wavelength lambda = h/p.",
            "For electron accelerated by V, lambda = h/sqrt(2meV).",
        ],
    },
    {
        "unit": "Atoms and Nuclei",
        "slug": "atoms_and_nuclei",
        "weightage": 5,
        "prerequisites": ["Electrostatics", "Dual Nature of Matter", "Energy levels"],
        "concepts": [
            "Bohr model explains hydrogen-like atomic spectra using quantized orbits.",
            "Emission and absorption lines come from transitions between energy levels.",
            "Nucleus contains protons and neutrons bound by nuclear force.",
            "Mass defect appears as binding energy through E = mc^2.",
            "Radioactive decay is statistical and follows exponential law.",
            "Fission and fusion release energy by increasing binding energy per nucleon.",
        ],
        "formulas": [
            "Bohr radius r_n = n^2 a0/Z.",
            "Energy E_n = -13.6 Z^2/n^2 eV.",
            "Rydberg formula 1/lambda = RZ^2(1/n1^2 - 1/n2^2).",
            "Binding energy = Delta m c^2.",
            "N = N0 e^(-lambda t).",
            "Half-life T1/2 = ln2/lambda.",
            "Activity A = lambda N.",
        ],
    },
    {
        "unit": "Semiconductor Devices",
        "slug": "semiconductor_devices",
        "weightage": 5,
        "prerequisites": ["Current Electricity", "Atoms", "Basic circuits"],
        "concepts": [
            "Semiconductors have conductivity between conductors and insulators.",
            "Doping creates n-type and p-type materials by adding donor or acceptor atoms.",
            "A p-n junction forms a depletion region and potential barrier.",
            "Forward bias allows current after threshold; reverse bias allows tiny saturation current until breakdown.",
            "Diodes rectify AC and can be used in clipping and clamping circuits.",
            "Logic gates implement Boolean operations using semiconductor circuits.",
        ],
        "formulas": [
            "Conductivity sigma = ne mu_e + pe mu_h.",
            "Resistivity rho = 1/sigma.",
            "Diode current approximately I = I0(e^(V/eta VT) - 1).",
            "Rectifier ripple frequency is 2f for full-wave rectification.",
            "Zener diode maintains nearly constant voltage in breakdown region.",
            "Boolean: AND gives 1 only when all inputs are 1; OR gives 1 when any input is 1; NOT inverts.",
        ],
    },
]


COMMON_MISTAKES = [
    "Using a memorized formula without checking whether its assumptions are valid.",
    "Ignoring sign convention and then interpreting a negative answer as automatically wrong.",
    "Skipping the diagram or graph, which hides the actual constraint in the question.",
    "Mixing scalar and vector quantities in the same equation.",
    "Substituting numbers before simplifying symbols, causing algebra mistakes.",
    "Forgetting units during the calculation and only checking them at the end.",
    "Assuming a special case, such as zero friction or same height, when the problem never says so.",
    "Rounding too early and losing the final option in a close numerical MCQ.",
]


def _lines_for_unit(unit):
    lines = [
        f"UNIT: {unit['unit']}",
        f"JEE WEIGHTAGE: {unit['weightage']}%",
        f"PREREQUISITES: {', '.join(unit['prerequisites'])}",
        "",
        "CORE CONCEPTS:",
    ]
    for index, concept in enumerate(unit["concepts"], start=1):
        lines.extend(
            [
                f"{index}. {concept}",
                "   In JEE questions, first identify where this idea appears in the physical situation.",
                "   Then translate the sentence into variables, direction, constraints, and a valid equation.",
            ]
        )
    lines.extend(["", "KEY FORMULAS:"])
    for index, formula in enumerate(unit["formulas"], start=1):
        lines.extend(
            [
                f"{index}. {formula}",
                "   Variables must be defined from the question before substitution.",
                "   Derivation hint: start from the core law, apply the geometry or constraint, then simplify.",
            ]
        )
    lines.extend(
        [
            "",
            "INTUITIVE EXPLANATION:",
            f"Think of {unit['unit']} as a way to translate a real physical scene into a small set of reliable rules.",
            "A confused student usually tries to jump directly to a formula; a strong student first asks what is changing, what is fixed, and what interaction is responsible.",
            "Use everyday language first: identify the object, the push or field or constraint acting on it, and the quantity that the question wants.",
            "Only after the story is clear should the algebra begin.",
            "For JEE Main, accuracy comes from recognizing the standard model quickly.",
            "For JEE Advanced, marks come from detecting where the standard model breaks and adding the missing constraint.",
            "",
            "MATHEMATICAL FRAMEWORK:",
            "1. Define the system and variables explicitly.",
            "2. Choose axes, sign convention, origin, zero potential, or reference state as needed.",
            "3. Write the governing law before writing a derived formula.",
            "4. Apply constraints such as contact, rolling, circuit junctions, symmetry, phase relation, or conservation law.",
            "5. Reduce the equations symbolically before substituting numerical values.",
            "6. Check limiting cases: zero angle, zero friction, infinite distance, very large resistance, or small amplitude where relevant.",
            "7. Verify dimensions and units before choosing the final option.",
            "",
            "COMMON MISTAKES:",
        ]
    )
    for index, mistake in enumerate(COMMON_MISTAKES, start=1):
        lines.append(f"{index}. {mistake} This happens because the student solves from memory instead of from the physical model.")
    lines.extend(
        [
            "",
            "JEE TRAPS:",
            "1. Hidden constraint: the phrase 'just loses contact', 'minimum value', 'maximum extension', or 'steady state' changes the equation.",
            "2. Direction trap: vectors, fields, torques, and velocities must be resolved before adding.",
            "3. Special-case trap: a common formula may require same level, constant acceleration, small angle, ideal source, or paraxial rays.",
            "4. Energy trap: non-conservative work, internal resistance, damping, or heat loss may quietly enter.",
            "5. Symmetry trap: a direct calculation is possible but symmetry gives the cleaner route.",
            "6. Graph trap: slope and area represent different physical quantities.",
            "7. Unit trap: options often differ by powers of 10 or by missing SI conversion.",
            "",
            "PREREQUISITE GAPS:",
        ]
    )
    for prerequisite in unit["prerequisites"]:
        lines.append(
            f"- Confusion in {unit['unit']} often means {prerequisite} is weak; revisit its definition, standard equations, and one easy example first."
        )
    lines.extend(
        [
            "- If the student cannot choose a formula, the root cause is usually failure to identify the principle.",
            "- If the student gets the equation right but answer wrong, the root cause is usually sign, unit, or algebra control.",
            "- If the student cannot start, the root cause is usually missing diagram, reference direction, or known/unknown listing.",
            "- If the student uses too many formulas, the root cause is usually not seeing the conservation law or symmetry.",
            "",
            "RECOVERY PATHS:",
            f"- Below 50%: start with the first concept in {unit['unit']} and use a familiar daily-life scene before any equation.",
            "- If formulas feel random: build a one-page formula map showing parent law -> condition -> final formula.",
            "- If diagrams are weak: solve three questions using only labelled diagrams and no numbers first.",
            "- If calculations fail: use one easy numerical example with units written at every line.",
            "- If Advanced questions fail: add one constraint at a time and compare with the Main-level version.",
            "",
            "PROBLEM SOLVING STRATEGY:",
            "STEP 1 - READ AND IDENTIFY: classify the model, underline given quantities, and circle what is asked.",
            "STEP 2 - DRAW AND VISUALIZE: draw the object, axes, forces, fields, rays, graphs, or circuit loop.",
            "STEP 3 - IDENTIFY THE PRINCIPLE: name the law, conservation rule, or wave/field relation before using it.",
            "STEP 4 - SET UP THE EQUATION: write symbols first, then substitute values with units.",
            "STEP 5 - SOLVE AND VERIFY: calculate, check dimensions, check physical magnitude, and compare with limiting cases.",
            "",
            "SUBTOPIC DRILL MAP:",
        ]
    )
    for concept in unit["concepts"]:
        lines.extend(
            [
                f"- Drill: {concept}",
                "  Easy: ask for the direct definition or one-step formula.",
                "  Medium: combine it with a graph, circuit, diagram, or constraint.",
                "  Hard: combine it with a second unit and force the student to choose the governing principle.",
                "  Recovery analogy: explain it with a familiar object before deriving the equation.",
                "  Checkpoint: ask the student why the chosen formula is valid here.",
            ]
        )
    lines.extend(["", "JEE ADVANCED EDGE CASES:"])
    for formula in unit["formulas"]:
        lines.extend(
            [
                f"- Edge case for {formula}",
                "  Ask whether the condition behind this formula is still true.",
                "  If the condition changes, return to the parent law and re-derive.",
                "  This is how JEE Advanced turns a familiar formula into a reasoning question.",
            ]
        )
    while len(lines) < 305:
        cycle = len(lines) % max(len(unit["concepts"]), 1)
        concept = unit["concepts"][cycle]
        lines.extend(
            [
                f"REVISION LOOP {len(lines)}:",
                f"- Re-explain: {concept}",
                "- Ask: what is the physical cause, what changes, and what remains constant?",
                "- Formula check: write the parent law and define every symbol.",
                "- Mistake check: identify the sign, unit, and assumption most likely to fail.",
                "- JEE check: solve one Main-level direct question, then one Advanced-style constraint variation.",
            ]
        )
    return "\n".join(lines) + "\n"


def main():
    try:
        init_knowledge_base()
        KB_SOURCES_ROOT.mkdir(parents=True, exist_ok=True)
        added = 0
        failed = 0
        for index, unit in enumerate(PHYSICS_UNITS, start=1):
            filename = f"physics_{unit['slug']}.txt"
            path = KB_SOURCES_ROOT / filename
            path.write_text(_lines_for_unit(unit), encoding="utf-8")
            print(f"[{index}/{len(PHYSICS_UNITS)}] Wrote {filename}")
            result = add_document_to_kb(str(path), subject="physics", source_name=path.stem)
            if result.get("ok"):
                added += 1
                print(f"    Indexed {result.get('chunks_added', 0)} chunks")
            else:
                failed += 1
                print(f"    Failed: {result.get('message', 'unknown error')}")
        print(f"Physics units indexed: {added}")
        print(f"Physics units failed: {failed}")
        print(f"Final knowledge base stats: {get_kb_stats()}")
    except Exception as exc:
        print(f"Physics KB seeding failed safely: {exc}")


if __name__ == "__main__":
    main()
