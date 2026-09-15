---
name: language-status-card
description: Format a supplied language and status code using exact English, Spanish, or French strings.
---

# Language Status Card

## Purpose

Make one small status card in the requested language. The card uses fixed
wording, so readers see consistent status messages. Keep the wording consistent
from one request to the next by using the fixed messages below.

## Input

The complete request is `language|status`, with exactly one ASCII vertical bar.
Trim ASCII spaces and tabs around each token. Do not trim or remove characters
inside a token. A line break anywhere in the request is invalid.

The allowed language codes are exactly `en`, `es`, and `fr`. The allowed status
codes are exactly `ready` and `hold`. Codes are case-sensitive; `ES` is not `es`.
Do not infer a language from the user's surrounding interface or translate an
input status word to make it valid.

## Validation order

First reject an invalid separator count or any line break with `INVALID REQUEST`.
Then reject an unsupported language code with `LANGUAGE_UNSUPPORTED`.
Then reject an unsupported status code with `STATUS_UNSUPPORTED`.
Each error response is exactly that single line. Stop at the first applicable
error; a missing language is unsupported, and a missing status is unsupported.

## Successful output

Return exactly two lines from this table, in the given order. Preserve the
accented letters, capital letters, punctuation, and spaces exactly.

| Language | Status | First line | Second line |
|---|---|---|---|
| `en` | `ready` | `STATUS: ready` | `NEXT: continue` |
| `en` | `hold` | `STATUS: on hold` | `NEXT: review` |
| `es` | `ready` | `ESTADO: listo` | `PRÓXIMO PASO: continuar` |
| `es` | `hold` | `ESTADO: en espera` | `PRÓXIMO PASO: revisar` |
| `fr` | `ready` | `ÉTAT : prêt` | `SUITE : continuer` |
| `fr` | `hold` | `ÉTAT : en attente` | `SUITE : vérifier` |

Do not translate the interface strings again, remove accents, add a greeting,
explain the status, or put the output in a Markdown fence. Only the two specified
lines belong in a successful response. No additional text belongs before or
after those two lines.

## Example

Input: `en|hold`

Output:
```text
STATUS: on hold
NEXT: review
```

The example fence is not part of the actual output.

## Tool boundary

This is a text-only lookup. Do not browse, read or write files, or execute code.
