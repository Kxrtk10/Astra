import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.knowledge_base_tools import KB_SOURCES_ROOT, add_document_to_kb, get_kb_stats, init_knowledge_base


PHYSICS_MECHANICS = """
Projectile motion:
- Resolve motion into horizontal and vertical components.
- Horizontal acceleration is zero if air resistance is ignored.
- Vertical motion has acceleration due to gravity, g.
Key formulas:
- x = u cos(theta) * t
- y = u sin(theta) * t - 1/2 g t^2
- Time of flight T = 2u sin(theta) / g
- Maximum height H = u^2 sin^2(theta) / 2g
- Range R = u^2 sin(2theta) / g
Common JEE traps:
- Mixing horizontal and vertical equations.
- Forgetting sign convention for g.
- Using range formula when launch and landing heights are different.

Laws of motion:
- Use free-body diagrams before writing equations.
- Newton's second law: F_net = ma.
- Friction can be static or kinetic; do not assume the wrong one.
- Tension, normal force, pseudo force, and friction often decide the answer.
Common JEE traps:
- Writing equations without checking the diagram.
- Using mg directly along an inclined plane without resolving components.

Work, energy, and power:
- Work = force times displacement along the force direction.
- Kinetic energy K = 1/2 mv^2.
- Potential energy changes depend on height and conservative forces.
- Work-energy theorem: net work equals change in kinetic energy.
Common JEE traps:
- Treating work as a vector.
- Forgetting that normal force often does zero work if perpendicular to motion.

Rotational motion:
- Angular displacement, angular velocity, and angular acceleration mirror linear quantities.
- Torque = r x F.
- Angular momentum L = I omega.
- Rotational kinetic energy = 1/2 I omega^2.
Common JEE traps:
- Using linear formulas directly without checking whether motion is translational or rotational.
- Forgetting axis dependence of moment of inertia.
""".strip()


CHEMISTRY_ORGANIC = """
Organic reaction mechanisms:
- Always identify the functional group first.
- Decide whether the reaction is substitution, addition, elimination, oxidation, reduction, or rearrangement.
- Track electron movement and intermediate stability.
- Carbocations, carbanions, radicals, and resonance all affect the final product.
Common JEE traps:
- Memorizing products without checking the mechanism.
- Confusing SN1 with SN2 or E1 with E2.

Named reactions:
- Aldol reaction joins carbonyl compounds with alpha hydrogen.
- Cannizzaro reaction happens for non-enolizable aldehydes.
- Reimer-Tiemann introduces a formyl group on phenols under specific conditions.
- Wurtz reaction couples alkyl halides in dry ether.
Common JEE traps:
- Using a named reaction outside its valid substrate scope.
- Forgetting the reagent order.

Functional groups and trends:
- Alcohols, phenols, ethers, aldehydes, ketones, carboxylic acids, amines, and haloalkanes behave differently.
- Inductive effect, resonance, and hyperconjugation influence reactivity.
- Electron-withdrawing groups often increase acidity.
- Electron-donating groups often stabilize positive charge.
Common JEE traps:
- Treating all oxygen-containing compounds as similar.
- Ignoring resonance when comparing acidity or basicity.

High-yield JEE organic reactions:
- Oxidation of primary alcohols can stop at aldehydes or proceed to acids depending on reagent.
- Addition to alkenes follows regioselectivity and, in some cases, Markovnikov or anti-Markovnikov rules.
- Amines show basic behavior and form salts with acids.
Common JEE traps:
- Not checking the reagent strength.
- Forgetting rearrangement possibility in carbocation pathways.
""".strip()


MATHS_CALCULUS = """
Limits:
- A limit describes the value a function approaches near a point.
- Check direct substitution first.
- If substitution fails, simplify algebraically or use standard limits.
- Common standard limit: lim(x->0) sin x / x = 1.
Common JEE traps:
- Cancelling terms after substituting the limiting value.
- Mixing up approaching with actually reaching.

Derivatives:
- Derivative is the rate of change of a function.
- Use rules carefully: sum, product, quotient, and chain rule.
- Standard derivatives must be memorized well.
- Tangent slope at a point equals the derivative at that point.
Common JEE traps:
- Forgetting chain rule.
- Missing the sign when differentiating trigonometric functions.

Integrals:
- Indefinite integral is the reverse process of differentiation.
- Definite integrals represent signed area.
- Use substitution, parts, and standard forms when needed.
- Keep limits and constants of integration straight.
Common JEE traps:
- Losing the constant of integration.
- Swapping upper and lower limits.

Differential equations:
- Separate variables when possible.
- Use linear differential equation methods when the equation has the standard form.
- Always check whether the solution satisfies the original equation.
Common JEE traps:
- Skipping the integrating factor step.
- Writing the final answer without using the initial condition.

Standard JEE formulas:
- d/dx (x^n) = n x^(n-1)
- d/dx (sin x) = cos x
- d/dx (cos x) = -sin x
- Integral of 1/(1+x^2) is tan^-1 x
Common JEE traps:
- Mixing derivative and integral forms.
- Forgetting domain restrictions in inverse trigonometric forms.
""".strip()


def _write_source_file(filename, content):
    KB_SOURCES_ROOT.mkdir(parents=True, exist_ok=True)
    path = KB_SOURCES_ROOT / filename
    path.write_text(content + "\n", encoding="utf-8")
    return path


def main():
    init_knowledge_base()
    files = [
        ("physics_mechanics.txt", "physics", PHYSICS_MECHANICS),
        ("chemistry_organic.txt", "chemistry", CHEMISTRY_ORGANIC),
        ("maths_calculus.txt", "mathematics", MATHS_CALCULUS),
    ]

    for filename, subject, content in files:
        path = _write_source_file(filename, content)
        result = add_document_to_kb(str(path), subject, Path(filename).stem)
        print(f"Added {filename}: {result}")

    print(f"Final knowledge base stats: {get_kb_stats()}")


if __name__ == "__main__":
    main()
