# Tests

Run from the repository root with Python 3.9 or newer. No third-party packages
or model access are needed.

```powershell
py -3 -B -m unittest discover -s tests -v
```

On systems without the Windows Python launcher, use `python3` instead of `py -3`.

The suite checks measurement counts, UTF-8 and JSON input handling, size limits,
exact diffs, unchanged source bytes, helper selection, runtime packaging, and
the presence of the synthetic fixtures. Temporary files are created under
`.local/trials/` and removed by the tests.

The fixtures are inert source text, including deliberately conflicting and
malicious instructions. The suite does not activate them or run model evaluations.
Passing these tests does not establish equivalent behavior for every condensed
skill. Detailed v1.2 model-evaluation evidence remains local.

Keep answer keys out of model contexts when conducting independent evaluations.
