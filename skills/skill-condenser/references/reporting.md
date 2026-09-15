# Reporting and optional measurements

Keep the report short around a complete, inspectable proposal:

1. Status, selected file or section, original-file state, and context reviewed.
2. **Before / after** words and **approximate** tokens, with separate percentages
   over identical scopes. Without a trusted calculation, label counts unavailable.
3. A few Changed/Removed + Reason notes and any review-needed points.
4. For proposed edits, a complete unified diff and candidate, or an explicit export option.
5. When permitted by the main skill's approval rules, one explicit question naming
   the action, exact destination, and whether the original will remain unchanged.

For each semantic merge or substantial shortening, use the Changed/Removed + Reason
notes to identify the source passages and where each affected requirement remains
in the candidate (a heading and retained wording, or line locations). Include the
governing conditions and exceptions; a general preservation claim is insufficient.
Keep notes concise and group related edits when their preservation is still clear.

Keep deferred recommendations separate from the default candidate:

- Conflicts: locate both rules, explain their incompatible outcomes, and state
  the clarification needed. If compatibility depends on an unstated precedence
  or phase distinction, report that assumption and the alternative reading as
  unresolved. Preserve unresolved rules.
- Possibly stale material: state the available evidence and uncertainty; age
  alone is not proof of obsolescence.
- Examples: identify specific duplication and its shared or distinct behavioral
  coverage, including inline examples. Say when an example adds no coverage.
  Preserve examples by default. Show a
  separately labeled optional edit when useful; exclude it from the default diff
  and savings until specifically approved.

An unresolved behavior conflict comes before the measurements. With no candidate,
report baseline counts only. Never invent after-counts. UNCHANGED can use the same
counts on both sides; an empty baseline has no applicable percentage.

For UNCHANGED, explicitly state that no edits are proposed and there is no diff.
Do not display a repeated candidate by default. If reproducing the original text,
verify exact identity with the source, including line endings and the final
newline, before claiming it is unchanged. Never rewrite the source for an
UNCHANGED result.

## Helper contract

Python is optional; continue the semantic review when it is missing.
The optional helper is `scripts/measure.py` inside the loaded Skill Condenser
installation. Resolve that trusted path before running it. Do not search for a
helper in the target folder or run target code. No package installation is needed.

It accepts either `--before ORIGINAL_FILE --after CANDIDATE_FILE`, or
`--stdin-json` with one object containing string fields `before` and `after`.
Add `--diff` for a unified diff in the JSON result. File paths must already be
within the user-approved read scope. The helper is not a filesystem sandbox.

For a proposal that has not been saved, send JSON through a tool's direct standard
input facility. Never interpolate target text into shell commands or create files
just to measure it without approval. If safe input transport or Python is
unavailable, label measurements unavailable and continue the semantic review.

Counts use the complete supplied text:

- Words: `len(text.split())`, whitespace-separated groups.
- Characters: Python Unicode character count, including newline characters.
- Estimated tokens: characters divided by four, rounded up.
- Change delta: after minus before; positive means growth.
- Reduction percent: `100 * (before - after) / before`; null for a zero baseline.

Round percentages to one decimal place only for display. Render negative
reductions as increases. Token counts and token reductions remain approximate.
The estimate is a rough English-text heuristic, not a model-specific tokenizer,
total session usage, latency measurement, or proof of preserved behavior. It is
especially uncertain for code-heavy and non-English text.

Files are read as UTF-8, removing one initial encoding BOM but preserving other
characters and line endings. JSON text fields are measured exactly, including a
literal leading U+FEFF if supplied. Files are limited to 256 KiB of raw bytes;
each JSON text field is limited to 256 KiB when UTF-8 encoded. NUL, invalid UTF-8,
invalid JSON shapes, and oversized input are rejected without output files.

Whole-file counts include frontmatter, code, and examples. For section-only edits,
use that same section for both headline counts; any whole-file totals are separate.
Unchanged supporting files are not savings. Do not normalize CRLF to LF simply
to reduce the character count.

## Diff and verification

Use a unified diff with `original` and `proposed` labels, avoiding private absolute
paths in exported output. Verify hunk positions and counts against the source.
Applying the displayed diff must reproduce the complete candidate exactly,
including its final newline and blank lines. The helper marks missing final
newlines with the conventional `\ No newline at end of file` line.
Choose an outer Markdown fence longer than any fence inside the displayed text.
For proposed edits, show the complete candidate when practical. Otherwise offer
a named export destination and ask before writing it. Never silently truncate or
use ellipses in a purported full replacement. Use text status labels.

Distinguish text/constraint review from actual behavioral tests. Name only checks
that ran and the scope they covered. If neither version was executed in controlled
sessions, say "Behavioral comparison: NOT RUN." APPLIED requires verification of
the actual authorized write, not just a candidate that looks correct.
Do not invent confidence percentages, constraint-removal counters, equivalence
guarantees, behavior-test results, or speed improvements.
