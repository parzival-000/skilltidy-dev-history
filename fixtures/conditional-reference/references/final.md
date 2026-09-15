# Final rules

Use these rules only for `final` mode after common validation succeeds.

Validate in this order:

1. If any quantity is zero, return exactly `FINAL QUANTITY REQUIRED`.
2. If there are more than five entries, return exactly `FINAL LIMIT`.
   Exactly five entries is allowed.
3. If the array is empty, return exactly `FINAL EMPTY`.

Otherwise return these three lines in order:

1. `FINAL: N`, where N is the number of array entries.
2. `ITEMS: ` followed by each `id=quantity` pair, joined with exactly ` | `.
3. `TOTAL: T`, where T is the sum of all quantities, including repeated IDs.

If T is 10 or more, append exactly `CHECK: REQUIRED` as a fourth line. Exactly
10 requires this line. If T is less than 10, omit the line entirely.

Never include a preview-mode marker. Preserve input order and duplicate IDs.

Example input: `{"mode":"final","items":[{"id":"sample","quantity":2}]}`

Example output:
```text
FINAL: 1
ITEMS: sample=2
TOTAL: 2
```

The fences display the example; the actual card is raw text.
