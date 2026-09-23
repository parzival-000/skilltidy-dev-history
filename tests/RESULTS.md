# Validation results

Current version: **v1.3**

## Local maintenance, 2026-09-22

Windows 10 build 19045, Python 3.11.9. Command from the repository root:

```powershell
py -3 -B -m unittest discover -s tests -v
```

Baseline: **37/37 passed**, no failures or skips. After documentation and test
maintenance: **36/36 passed** in both the working copy and a clean disposable
30-file export, with no failures or skips. The removed test constructed
its own ZIP from a constant list and checked that same list without exercising
production packaging. Six-file runtime inventory, metadata, inactive fixtures,
helper behavior, runnable examples, and local links remain checked. Privacy
checks now cover all maintained guides and runtime files.

Model audits, paired behavior checks, installation/discovery, authoring validator,
and external scanner: **NOT RUN in this cleanup**. The six runtime files and 14
fixture input/context files are frozen byte-for-byte. Byte identity supports
unchanged inputs, not a universal claim about model behavior.

## Historical v1.3 evidence, 2026-09-14

Windows, Python 3.11.9, Codex CLI 0.154.0-alpha.6.2. Fresh ephemeral sessions used
no model/reasoning override. Backend revision, temperature, and seed were unknown.

| Check | Recorded result |
|---|---|
| Automated suite | 37/37 passed in the working copy and a clean staged export. |
| Authoring validator | Passed using the already installed validator. |
| Final condensation reviews | 4/4 passed independent text, diff, and trace review. |
| Final-candidate behavior | 14 matched pairs / 28 passing responses, including two repeats. |
| Workflow checks | Eight passed cases and three focused regression runs, with revision limits below. |

That matrix covers the 14 non-toy-list rows in
[behavior_cases.json](behavior_cases.json). Six code/multilingual pairs were rerun
after their candidates changed, yielding 12/12 passing responses. The other 16
responses were reused only after final original/candidate/context hashes matched.
Across these runs, 40 behavior responses passed. JSON scoring rejected duplicate
keys and compared exact keys, values, and types. Text allowed at most one final
newline. Command traces showed conditional tasks reading only their selected
reference, and behavior input hashes/inventories stayed unchanged.

### Generated candidates

Whole-file words include metadata and examples; unchanged references are excluded
equally. These are measured historical examples, not reduction targets.

| Fixture | Original | Candidate | Fewer words |
|---|---:|---:|---:|
| Structured output | 401 | 365 | 9.0% |
| Multilingual | 397 | 371 | 6.5% |
| Code examples | 337 | 320 | 5.0% |
| Conditional reference | 693 | 670 | 3.3% |

Each candidate came from a final-runtime review. The supervisor reconstructed its
displayed diff without fuzzy matching, using source/diff evidence for final
newlines rather than Markdown transport fences. Complete text, requirements,
metadata, code, and examples were inspected. No handwritten replacement was used.

Candidate SHA-256 fingerprints:

```text
structured-output      b2fd38192ce49c0bb46e304e20458f3b1e931a397f741f88678947fa7595fed8
multilingual           2962ef2dfc7fd45ef09ddc12eb0d2d89f883085415e1f3fa2e00f1208de155ab
code-examples          3312567a3bc724a84f2dc31e1c20c7879c5d7f17a232cc505b81d0aa88819c4c
conditional-reference  26fd76595dd8c928697ed936eea0c26948a1087b86d0f609283edd65da7d33d0
```

### Failures, corrections, and limits

Four rounds of four audits were retained. An initial multilingual diff had the
wrong hunk position. Two later code reviews misread JSON-escaped tool output,
reported a false conflict, and doubled backslashes without showing those changes
in the diff. Those reports/candidates failed review. A general decoded-text
reminder was insufficient. Final instructions require exact diff reconstruction
and source-character checks when escapes are ambiguous; all four final audits
passed. Earlier failures remain evidence of limitations.

The eight workflow cases covered simulated Python absence, 13 support files,
more than 1 MiB, exact UNCHANGED reproduction, conflicts, an approved section
copy, changed-source approval invalidation, and explicit disposable CLI discovery.
Source hashes stayed unchanged. Only the approved copy was created, with CRLF
and prefix/suffix bytes preserved.

Three follow-ups covered missing-Python diff reconstruction, UNCHANGED reproduction,
and discovery. Only the missing-Python retry used the final wording; the other
two preceded the last literal-preservation refinement. Rules were not retested
after every wording revision. UNCHANGED reproduction used LF; CRLF was covered
in the approved copy. Discovery verified explicit CLI loading, not automatic
selection or the desktop picker. Cases shared a host filesystem, not OS isolation.
Bootstrap/approval-policy failures were blocked attempts, then retried within
permitted scope. Recovered console/read-command errors are not extra passes.

Cross-host behavior, actual Python absence, actual unreadable-file review, and
every conditional branch were not established. The conditional fixture's
common-invalid-input/no-reference branch is a known coverage gap.

## Earlier historical evidence

| Date / scope | Recorded result and limit |
|---|---|
| 2026-09-10, initial build | 33/33 eventually passed on Windows/Python 3.14.3. An earlier 20-test measurement attempt had 26 setup/cleanup errors from temporary-directory permissions. Inherited workspace permissions fixed the setup without weakening expectations. |
| 2026-09-10, toy formatter | The 918-to-640-word candidate passed B1-B10 for both versions: 20/20 responses. Two explanation responses met content expectations but did not resolve the reference-read/tool-ban ambiguity. The separate 694-word proposal had no paired behavior validation. Exact model/effort identifiers were unavailable. |
| 2026-09-10, workflow/reporting | Nine approval scenarios and later focused section/path/audit checks were recorded. Inventories, hashes, and applied diffs supported write outcomes; several tool actions were self-reported. Missing explicit approval questions and an UNCHANGED extra-blank-line display were found, then addressed with focused checks. |
| 2026-09-10, path order | An earlier reported ordering deviation had unverified chronology. A later supervisor-instrumented read-order check passed, without proving all ordinary sessions follow it. A non-shipped calculation miscounted 251 versus 252 characters; the trusted helper cross-check was correct. |
| 2026-09-11, programmatic suite | 32/33 passed. A local-link test incorrectly treated an HTTPS author URL as a file. This historical test defect is absent from the current passing suite. |
| 2026-09-13, v1.2 | Approved that day. Maintained suite: 32/32 on Windows/Python 3.11.9. Earlier development suite: 33/33 with additional development-only coverage. |

The v1.2 evaluation recorded 20 matched audits, 24 behavior pairs (22 scenarios
and two repeats, 48 passing responses), six passing application checks, and six
additional regression reviews. It used the existing CLI with requested
gpt-6-astra/xhigh settings in fresh sessions, excluding project guidance and keys.
Backend revision, temperature, and seed were not exposed. The validator passed
with already installed tools.

Both initial formatter audits missed explanation-mode ambiguity, and the first
reporting correction also failed. The final targeted candidate review stated both
readings and returned REVIEW NEEDED. A procedural holdout read target content too
early. Both later read-order checks passed, but one export failed with write
errors, proving only the narrow ordering result. Reused holdouts were regression
checks, not fresh holdout successes. A six-versus-seven-column answer-key error
received a source-based erratum before scoring, applied equally to both versions.

The 48 behavior responses validate their exact earlier generated candidates.
Later reviewer refinements did not receive another complete fresh-candidate
matrix. A third-party coauthoring sample retained unresolved tool wording and
lacked redistribution clearance. Its raw content remains private.

A historical screenshot reported SkillSpector 2.11.1, exit 1, MEDIUM/CAUTION and
83.3% coverage. It described an incomplete scan and no confirmed vulnerability
in its manual review. Raw scanner output was unavailable. The v1.2 manual
assessment remained CAUTION with no fresh scan. Neither is security certification.
Raw traces, rejected proposals, and third-party samples remain local.
