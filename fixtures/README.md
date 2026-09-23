# Synthetic fixtures

These are original, disposable examples for developing Skill Condenser. They are **not installed skills**. Some intentionally contain contradictions or untrusted instructions. Do not execute or adopt them during an audit.

Use the [test guide](../tests/README.md) for evaluation steps and
[behavior cases](../tests/behavior_cases.json) for the formatter and v1.3 prompts and
expected outputs. Keep those expectations out of the responding model's context.

Preserve the originals. Save candidates and actual run results only to an explicitly approved disposable location. Never substitute a hand-written candidate for a generated output and claim the implemented skill produced it.

The ordinary `toy-list` formatting task has ten settled expected results for paired
behavior checks. Its explanation mode has a known ambiguity: the main file
requires reading a reference, while that reference prohibits tools during an
explanation. A preparation-only read and a prohibition covering the whole task
are both plausible. Report the ambiguity without silently fixing the fixture.

The conflicting and untrusted fixtures test reviewer behavior, not the safety of
executing their instructions. `AGENTS.sample.md` and `SKILL.input.md` filenames
are intentional safeguards against accidental discovery. Repeated examples and
exact strings are deliberate. Keep conditional references separate so selective
loading can be observed.

The four v1.3 fixtures cover JSON output, multilingual exact text, code/examples,
and conditional references. Their code is inert example text. Do not execute it.
Two repeated behavior cases intentionally probe variability in fresh sessions.
The conditional fixture's common-invalid-input/no-reference branch remains a
known coverage gap. Listing a case or a gap is not a claim that it was evaluated.
