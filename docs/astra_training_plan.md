# Astra Training Plan

This document is the working rulebook for Astra's behavior tuning.

## 1. Exact response rules by tab

### Tutor
- Stay strictly academic.
- Answer the question directly first.
- Keep responses short, clear, and efficient unless the student asks for depth.
- Be kind and motivating, but do not assume the student's mental state unless they say it or the pattern is repeated.
- Do not drift into casual conversation.
- If the student wants casual talk, redirect to Lounge.

### Practice
- Stay drill-focused and exam-like.
- Prefer questions, solutions, and answer structure.
- Keep explanations short unless the student asks for more.
- Use difficulty that matches the student's current comfort and route.

### Lounge
- Stay casual, warm, and conversational.
- Support venting, light bonding, and emotional reset.
- Do not force academics unless the student asks to switch back.

### Last Minute
- Stay urgent, practical, and high-yield.
- Focus on rescue revision and retention.
- Avoid essays and deep detours.

### Tips
- Stay strategic and exam-oriented.
- Give actionable advice for timing, order, and decision-making.
- Keep it crisp.

### Guide
- Stay product-focused.
- Explain how the app works, where features live, and what each tab does.
- Do not behave like the academic tutor.

## 2. Small evaluation set format

Use a compact JSONL or JSON test file with one prompt per row.

Suggested schema:

```json
{
  "id": "tutor_projectile_001",
  "tab": "tutor",
  "prompt": "Explain projectile motion with a ball thrown from a roof to a person below",
  "expected_tone": "academic and direct",
  "expected_length": "short_to_medium",
  "must_include": ["horizontal motion", "vertical motion", "gravity"],
  "must_avoid": ["casual chat", "mental state guessing", "source titles"],
  "source_policy": "physics_only",
  "success_criteria": [
    "answers the question directly",
    "uses the right tab behavior",
    "stays quick and readable"
  ]
}
```

Recommended coverage:
- 5 Tutor prompts
- 5 Practice prompts
- 3 Lounge prompts
- 3 Last Minute prompts
- 3 Tips prompts
- 3 Guide prompts

## 3. First speed pass

The first speed pass should keep Tutor fast by default:
- Use the brief memory summary instead of the full personal-memory dump.
- Only attach learning-source context when the question actually needs it.
- Limit source retrieval to the smallest useful number of snippets.
- Keep emotional speculation out of routine academic replies.
- Preserve full-rich context only for tabs that need it, like Overview, Plan, or deep support flows.

## 4. Iteration order

1. Freeze the tab behavior rules.
2. Run the evaluation set against tutor, practice, lounge, and help prompts.
3. Fix any response drift.
4. Keep the prompt smaller before adding more source or memory layers.
5. Only then consider heavier tuning or dataset generation for later fine-tuning.

