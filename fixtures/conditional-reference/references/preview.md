# Preview rules

Use these rules only for `preview` mode after common validation succeeds.

If there are more than three entries, return exactly `PREVIEW LIMIT`. Exactly
three entries is allowed. If the array is empty, return exactly `PREVIEW EMPTY`.

Otherwise return exactly two lines:

1. `PREVIEW: N`, where N is the number of array entries.
2. `ITEMS: ` followed by each `id=quantity` pair, joined with exactly ` | `.

Zero quantities are allowed and remain visible in the items line. Preserve
order and duplicates. Never include a total, `CHECK:` line, or final-mode marker
in a preview.

Example input: `{"mode":"preview","items":[{"id":"sample","quantity":0}]}`

Example output:
```text
PREVIEW: 1
ITEMS: sample=0
```

The fences display the example; the actual card is raw text.
