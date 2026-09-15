# Validation results

Current version: **v1.3**

## v1.3 checks

Run date: 2026-09-14, Windows, Python 3.11.9, Codex CLI 0.154.0-alpha.6.2.
The existing CLI used fresh ephemeral sessions with no model or reasoning
override. Backend model revision, temperature, and seed were not exposed.

| Check | Observed result |
|---|---|
| Automated suite | 37/37 passed in the working copy and a clean export of the staged repository. |
| Authoring validator | Passed with the already installed validator. |
| Final condensation reviews | 4/4 passed independent text, diff, and trace review. |
| Final-candidate behavior matrix | 14 matched pairs / 28 passing responses, including two repeated cases. |
| Workflow checks | Eight cases passed, plus three focused regression runs. |

The behavior matrix covers the 12 distinct cases and two repeats in
[behavior_cases.json](behavior_cases.json). The final code and multilingual
candidates changed, so all six of their original/candidate pairs were rerun:
12/12 responses passed. The other 16 results were retained only after verifying
that the final candidates, originals, and supporting files exactly matched their
previously tested hashes. In total, 40 behavior responses ran and passed.

JSON outputs were parsed with duplicate-key rejection and exact key/value/type
comparison. Text outputs required exact text, allowing at most one final newline.
Actual command traces confirmed that conditional tasks read only their selected
reference. All behavior input hashes and case inventories remained unchanged.

### Final generated candidates

These are whole-file word counts, including metadata and examples, measured
with the shipped helper. Unchanged references are excluded equally.

| Fixture | Original | Candidate | Fewer words |
|---|---:|---:|---:|
| Structured output | 401 | 365 | 9.0% |
| Multilingual | 397 | 371 | 6.5% |
| Code examples | 337 | 320 | 5.0% |
| Conditional reference | 693 | 670 | 3.3% |

Each candidate came from an actual final-runtime review. The test supervisor
checked the conversation proposal, replayed its displayed diff without fuzzy
matching, and saved the reconstructed candidate. Markdown fence separators are
transport, not file content; the source and displayed diff establish the final
newline. Complete candidates, metadata, code, examples, and requirements were
also independently inspected. No hand-written candidate replaced a model output.

Candidate SHA-256 fingerprints:

```text
structured-output      b2fd38192ce49c0bb46e304e20458f3b1e931a397f741f88678947fa7595fed8
multilingual           2962ef2dfc7fd45ef09ddc12eb0d2d89f883085415e1f3fa2e00f1208de155ab
code-examples          3312567a3bc724a84f2dc31e1c20c7879c5d7f17a232cc505b81d0aa88819c4c
conditional-reference  26fd76595dd8c928697ed936eea0c26948a1087b86d0f609283edd65da7d33d0
```

### Failures found and corrected

Four rounds of four audits were retained. An initial multilingual diff had an
incorrect hunk position. Two later code-example reviews mistook JSON-escaped
tool output for literal file content, falsely reported a conflict, and doubled
backslashes in the candidate without including those edits in the diff.
Those reports failed review and their candidates were rejected.

The final instructions require exact diff reconstruction and source character
verification when escaped output is ambiguous. A general reminder to use decoded
text was insufficient and was replaced. The final code review checked actual
character values, preserved the literals, and reported no false conflict.
All four final audits passed. This does not erase the earlier failures or
establish that the model will never repeat them.

### Workflow coverage and limits

The eight cases covered a preview with Python unavailable, 13 required support
files, more than 1 MiB of support text, exact UNCHANGED reproduction, conflict
reporting, an approved section copy, changed-source approval invalidation, and
explicit discovery in a disposable CLI project. Source hashes stayed unchanged.
Only the specifically approved copy was created; its CRLF endings and unchanged
prefix/suffix matched byte-for-byte.

Three further runs checked missing-Python diff reconstruction, UNCHANGED
reproduction, and discovery. The missing-Python retry used the final runtime.
The other two used the preceding literal-preservation wording. The unchanged
workflow rules were not retested in every wording revision.

Missing Python was simulated through a controlled unavailable-runtime request.
Discovery verified an actual read of the copied skill through explicit CLI
invocation, not desktop picker behavior or automatic selection. UNCHANGED
reproduction used LF; CRLF was checked separately in the approved copy.
The cases share a host filesystem and are not OS-isolated.

Initial sandbox/bootstrap and approval-policy failures were kept as blocked
attempts, then retried with permitted case-local paths and automatic approval
review. Console encoding and read-command syntax errors were recovered without
changing targets. These attempts are not counted as additional passing cases.

Cross-host compatibility, actual Python absence, actual unreadable-file handling,
and every conditional branch remain outside this evidence. In particular, the
new conditional fixture's common-invalid/no-reference branch is not in this
matrix. Raw traces and rejected proposals remain local.

## Historical results

v1.2 was approved on 2026-09-13. The maintained repository suite passed 32/32
checks on Windows with Python 3.11.9 that day. Earlier local development checks
passed 33/33 with additional development-only coverage.

The saved v1.2 evaluation recorded 20 matched audits, 24 paired behavior runs
(22 distinct scenarios and two repeats, producing 48 passing responses), six
passing application checks, and six focused regression reviews. Audit failures
and subsequent corrections remain recorded in local development evidence.
The 48 responses were tied to candidates generated before the final reviewer
refinements. They do not validate every candidate generated by later instructions.

Earlier formatter comparisons and optional authoring-validator results remain
historical. No external security certification is claimed. Raw evaluation traces
and third-party samples stay local.
