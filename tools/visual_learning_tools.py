import re


def _extract_number(text, pattern, fallback):
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return fallback
    try:
        return float(match.group(1))
    except (TypeError, ValueError):
        return fallback


def _extract_projectile_params(text):
    velocity = _extract_number(text, r"(?:velocity|speed)[^\d]*(\d+(?:\.\d+)?)", 18.0)
    angle = _extract_number(text, r"(\d+(?:\.\d+)?)\s*(?:degrees|degree|deg|°)", 42.0)

    height = 18.0
    height_patterns = [
        r"(?:from|off|on)\s+(?:a\s+)?(\d+(?:\.\d+)?)\s*(?:meter|metre|m)\s*(?:rooftop|platform|building|tower)",
        r"(\d+(?:\.\d+)?)\s*(?:meter|metre|m)\s*(?:rooftop|platform|building|tower|height)",
    ]
    for pattern in height_patterns:
        extracted = _extract_number(text, pattern, None)
        if extracted is not None:
            height = extracted
            break

    environment = "rooftop"
    if re.search(r"stadium|arena|track", text, re.IGNORECASE):
        environment = "stadium"
    elif re.search(r"lab|classroom|science", text, re.IGNORECASE):
        environment = "lab"

    return {
        "velocity": max(5.0, min(45.0, velocity)),
        "angle": max(10.0, min(80.0, angle)),
        "launcher_height": max(2.0, min(28.0, height)),
        "environment": environment,
    }


def _mastery_profile(scene_type):
    profiles = {
        "projectile": {
            "mastery_tier": "Foundation Scene",
            "chapter_unlock": "Kinematics and projectile motion",
            "reward_points": 28,
            "unlock_note": "A strong visual start for JEE Physics motion questions.",
        },
        "probability_bag": {
            "mastery_tier": "Pattern Recognition",
            "chapter_unlock": "Probability and sample space",
            "reward_points": 24,
            "unlock_note": "Use this scene to lock down outcome counting and event intuition.",
        },
        "shop_percentages": {
            "mastery_tier": "Application Scene",
            "chapter_unlock": "Percentages, profit, loss, and discounts",
            "reward_points": 22,
            "unlock_note": "A real-life arithmetic scene that helps calculations feel concrete.",
        },
        "field_lines": {
            "mastery_tier": "Depth Scene",
            "chapter_unlock": "Electrostatics and field lines",
            "reward_points": 30,
            "unlock_note": "This unlock nudges the student toward deeper spatial reasoning.",
        },
        "concept_flow": {
            "mastery_tier": "Concept Bridge",
            "chapter_unlock": "General concept mapping",
            "reward_points": 18,
            "unlock_note": "A flexible primer for any concept that needs cause-effect clarity.",
        },
    }
    return profiles.get(
        scene_type,
        {
            "mastery_tier": "Concept Bridge",
            "chapter_unlock": "General concept mapping",
            "reward_points": 16,
            "unlock_note": "A flexible primer for any concept that needs cause-effect clarity.",
        },
    )


def build_visual_learning_aid(user_input):
    text = (user_input or "").strip().lower()
    if not text:
        return None

    if any(term in text for term in ["projectile", "trajectory", "parabola", "ball thrown", "thrown from", "angle of projection", "motion of a ball"]):
        projectile = _extract_projectile_params(text)
        mastery = _mastery_profile("projectile")
        return {
            "title": "Projectile Motion Scene",
            "mastery": mastery,
            "animation": {
                "type": "projectile",
                "duration_ms": 4800,
                "axes": {"x": "horizontal distance", "y": "height"},
            },
            "scene_config": {
                "environment": projectile["environment"],
                "interaction_hint": "Drag the mouse to rotate the rooftop scene and inspect the path from every side.",
                "launch": {
                    "velocity": projectile["velocity"],
                    "angle": projectile["angle"],
                    "height": projectile["launcher_height"],
                },
                "characters": {
                    "thrower": {"name": "Sky Runner", "palette": "sunrise"},
                    "catcher": {"name": "Coach Nova", "palette": "teal"},
                },
            },
            "scenario": (
                "Imagine a ball being thrown from the top of a building while a child waits below to catch it."
            ),
            "frames": [
                "Frame 1: The ball starts with an initial velocity that can be split into horizontal and vertical parts.",
                "Frame 2: The horizontal motion keeps moving steadily forward while gravity pulls the ball downward.",
                "Frame 3: The path becomes a curve because the horizontal and vertical motions are happening together.",
                "Frame 4: By the time the ball reaches the child, its vertical speed has changed because gravity acted the whole time.",
            ],
            "case_study": (
                "Use this when solving JEE-style questions: treat horizontal and vertical motion separately, then combine them to understand the full curved path."
            ),
        }

    if any(term in text for term in ["probability", "chance", "event", "sample space", "bag of balls", "coin toss", "dice"]):
        mastery = _mastery_profile("probability_bag")
        return {
            "title": "Probability As A Real-Life Decision Scene",
            "mastery": mastery,
            "animation": {
                "type": "probability_bag",
                "duration_ms": 4200,
                "axes": {"x": "possible outcomes", "y": "selected event"},
            },
            "scene_config": {
                "interaction_hint": "Rotate the scene to inspect the bag and every possible outcome.",
            },
            "scenario": (
                "Picture a game stall where you pick one ball from a bag containing red, blue, and green balls."
            ),
            "frames": [
                "Frame 1: Count the total number of possible outcomes in the bag.",
                "Frame 2: Count how many outcomes match the event you care about, like picking a red ball.",
                "Frame 3: Probability becomes favorable outcomes divided by total outcomes.",
                "Frame 4: The closer the value is to 1, the more likely the event feels in real life.",
            ],
            "case_study": (
                "This helps when a student feels probability is abstract: every event becomes a concrete choice among visible outcomes."
            ),
        }

    if any(term in text for term in ["percentage", "percentages", "profit", "loss"]):
        mastery = _mastery_profile("shop_percentages")
        return {
            "title": "Percentages In A Shop Scene",
            "mastery": mastery,
            "animation": {
                "type": "shop_percentages",
                "duration_ms": 4200,
                "axes": {"x": "price change", "y": "profit / loss"},
            },
            "scene_config": {
                "interaction_hint": "Drag the mouse to inspect the price bars from every angle.",
            },
            "scenario": (
                "Imagine a student running a small snack stall and comparing cost price, selling price, discount, profit, and loss."
            ),
            "frames": [
                "Frame 1: Start with the original price as the reference value.",
                "Frame 2: A percentage increase or decrease changes that value relative to the original.",
                "Frame 3: Discounts reduce selling price, while profit and loss compare final price against cost price.",
                "Frame 4: The whole topic becomes easier when each percentage is tied to a real money change.",
            ],
            "case_study": (
                "This is useful for JEE-style arithmetic because the student can mentally track price movement instead of memorizing formulas blindly."
            ),
        }

    if any(term in text for term in ["electric field", "magnetic field", "electrostatics", "field lines", "charge distribution", "coulomb"]):
        mastery = _mastery_profile("field_lines")
        return {
            "title": "Field Visualization",
            "mastery": mastery,
            "animation": {
                "type": "field_lines",
                "duration_ms": 4200,
                "axes": {"x": "space", "y": "field strength"},
            },
            "scene_config": {
                "interaction_hint": "Rotate around the charges to see how the field lines spread through space.",
            },
            "scenario": (
                "Picture charges placed on a flat surface while invisible field lines spread through the surrounding space."
            ),
            "frames": [
                "Frame 1: A positive charge pushes field lines outward; a negative charge pulls them inward.",
                "Frame 2: The closer another charge is brought, the stronger the force it experiences.",
                "Frame 3: Field strength changes with distance, so space around the charge is not equally active everywhere.",
                "Frame 4: Superposition means the final field is the combined effect of every nearby charge.",
            ],
            "case_study": (
                "Students understand this better when they imagine space itself carrying influence, not just memorize formulas."
            ),
        }

    if text.startswith("explain ") or "concept" in text:
        mastery = _mastery_profile("concept_flow")
        return {
            "title": "Concept Visualizer",
            "mastery": mastery,
            "animation": {
                "type": "concept_flow",
                "duration_ms": 3600,
                "axes": {"x": "cause", "y": "effect"},
            },
            "scene_config": {
                "interaction_hint": "Rotate the scene to connect the cause, rule, and result visually.",
            },
            "scenario": (
                "Treat the concept like a scene from real life, with objects, motion, and cause-and-effect instead of pure formulas."
            ),
            "frames": [
                "Frame 1: Identify the objects or quantities involved.",
                "Frame 2: Track what changes over time or with interaction.",
                "Frame 3: Connect each formula to a visible action or relationship.",
                "Frame 4: Turn the final understanding into a mini case study the student can retell in their own words.",
            ],
            "case_study": (
                "This gives the tutor a structure to make learning feel visual and memorable rather than mechanical."
            ),
        }

    return None


def build_video_explanation(user_input, response_language="English"):
    visual = build_visual_learning_aid(user_input)
    if not visual:
        return None

    text = (user_input or "").strip().lower()
    calculations = [
        "Start by identifying what is changing and what stays constant.",
        "Map each quantity to a symbol before substituting any formula.",
        "Solve one relationship at a time instead of mixing all steps together.",
    ]
    if "projectile" in text:
        calculations = [
            "Split the initial velocity into horizontal and vertical components.",
            "Use horizontal motion to find displacement with constant velocity.",
            "Use vertical motion with gravity to track height and time.",
        ]
    elif "probability" in text:
        calculations = [
            "Count total possible outcomes.",
            "Count favorable outcomes for the event you care about.",
            "Compute probability as favorable outcomes divided by total outcomes.",
        ]
    elif any(term in text for term in ["percentage", "percentages", "profit", "loss"]):
        calculations = [
            "Choose the base value first.",
            "Convert the percentage into a fractional or decimal change.",
            "Apply the increase or decrease stepwise to avoid sign mistakes.",
        ]

    return {
        "title": f"{visual['title']} Video Walkthrough",
        "subtitle_language": response_language,
        "scenes": [
            {
                "label": f"Scene {index + 1}",
                "subtitle": frame,
            }
            for index, frame in enumerate(visual.get("frames", []))
        ],
        "reasoning": [
            visual.get("scenario", ""),
            visual.get("case_study", ""),
            "Connect each step to what the student can actually picture in the scene.",
        ],
        "calculations": calculations,
    }
