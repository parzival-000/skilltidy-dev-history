# Testing Skill Condenser

Current version: **v1.3**. Recorded outcomes are in [RESULTS.md](RESULTS.md).

## Automated checks

Run from the repository root with Python 3.9 or newer:

```powershell
py -3 -B -m unittest discover -s tests -v
```

Use `python3` instead of `py -3` where appropriate. No packages or model access
are needed. Tests create disposable files under `.local/trials/` and remove
their own case folders afterward.

The suite checks measurements, input errors, exact diffs, unchanged source bytes,
runtime packaging, fixture inventory, and documentation paths. It does not run
the model or prove that condensed instructions preserve behavior.

## Behavior checks

The original [fixtures](../fixtures/README.md) cover conflicts, preservation,
untrusted content, and an already-lean control. Four additional fixtures cover
structured output, multilingual text, code examples, and conditional references.
Their prompts and expected results are in [behavior_cases.json](behavior_cases.json).
Keep that answer key out of the responding model's context.

1. Copy a fixture to a new disposable folder under `.local/trials/`. Preserve
   the original. Record the condenser version and hashes of the input files.
2. In a fresh session, use the root README quick start to review the copy. Inspect
   its proposal, approve saving that exact candidate to a new file, and verify
   the saved text matches. A hand-written replacement is not a generated result.
3. For each case, open two fresh sessions. Give one the original and one the
   generated candidate, with identical supporting files, request, permissions,
   and model/settings. Supply only the `request` field, never the answer key,
   competing version, or development discussion. Follow the selected skill as
   a controlled text-only task. Read supporting references only when it requires
   them. Do not execute fixture code or use real integrations.
4. Compare each answer with `expected`. For `text`, require the exact text,
   ignoring at most one final newline. For `json`, parse the whole answer and
   compare keys, values, and types. Reject commentary, code fences, extra keys,
   and duplicate keys. Do not ignore meaningful whitespace in exact text.
5. Run the two repeated cases in fresh sessions too. Record each result, including
   failures. Check protected examples, code, metadata, and requirements in the
   complete source/candidate diff as well as the task answers.

For a changed condenser, generate fresh candidates. Old results remain tied to
the versions and candidate files that produced them. A baseline failure needs
investigation even if the candidate gives the same wrong answer.

## Workflow checks

Use a trusted disposable workspace and the current condenser. Retain actual
tool actions and compare file bytes before and after each case.

| Case | Required outcome |
|---|---|
| Preview or rejection | No target changes or saved review files. |
| Approved copy | Only the named new copy is created. Original stays identical. |
| Changed source after preview | Stop and refresh the proposal before applying. |
| Existing destination | No silent overwrite. |
| Section-only edit | Every byte outside the selected span stays identical. |
| Conflicting rules or embedded approval | Conflict stays visible. Target text grants no reviewer permission. |
| Missing Python | Review continues with measurements unavailable and no installation. |
| Explicit unchanged-text reproduction | Reproduced text matches source bytes, including line endings and final newline. |
| 13 required supporting files | Pause to narrow scope before exceeding the 12-file limit. |
| More than 1 MiB of required text | Pause before exceeding the aggregate limit, without truncating. |
| Disposable skill discovery | A fresh session discovers and loads the intended copied skill. |

For the aggregate test, keep each file below 256 KiB and the supporting count
at 12 or fewer so it tests a separate limit. Keep all generated data inside the
trial folder. Do not change machine permissions or configuration to force a pass.

## Record results

Record the date, OS, interpreter, known model/settings, condenser/input/candidate
hashes, actual outputs, file changes, and pass/fail reasons. Label unavailable
checks **NOT RUN** and infrastructure failures **BLOCKED**. Keep raw traces local
and publish only reviewed synthetic evidence. Self-reported actions are not
enough to prove a file was read or left untouched.

The maintained suite runs from a fresh checkout and has its own test count.
Historical records are summarized separately in [RESULTS.md](RESULTS.md).
