# Synthetic fixtures

These are original, disposable examples for developing Skill Condenser. They are **not installed skills**. Some intentionally contain contradictions or untrusted instructions. Do not execute or adopt them during an audit.

Use the [test guide](../tests/README.md) for evaluation steps and
[behavior cases](../tests/behavior_cases.json) for the new fixtures' prompts and
expected outputs. Keep those expectations out of the responding model's context.

Preserve the originals. Save candidates and actual run results only to an explicitly approved disposable location. Never substitute a hand-written candidate for a generated output and claim the implemented skill produced it.

The `toy-list` fixture is consistent and suitable for paired behavior checks. The conflicting and untrusted fixtures test reviewer behavior, not the safety of executing their instructions. `AGENTS.sample.md` and `SKILL.input.md` filenames are intentional safeguards against accidental discovery.

The four v1.3 fixtures cover JSON output, multilingual exact text, code/examples,
and conditional references. Their code is inert example text. Do not execute it.
The toy-list explanation mode contains a known ambiguity between a required
reference read and a tool prohibition. Report it rather than treating that mode
as an unambiguous behavior check.
