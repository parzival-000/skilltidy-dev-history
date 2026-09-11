import argparse
import difflib
import json
from pathlib import Path
import sys


MAX_TEXT_BYTES = 256 * 1024
# Two texts can each expand sixfold when JSON escapes every character.
MAX_JSON_BYTES = 12 * MAX_TEXT_BYTES + 1024


def validate_text(text):
    if not isinstance(text, str):
        raise ValueError("before and after must be strings")
    if "\0" in text:
        raise ValueError("NUL-containing text is not supported")
    try:
        size = len(text.encode("utf-8"))
    except UnicodeError:
        raise ValueError("text must contain valid Unicode") from None
    if size > MAX_TEXT_BYTES:
        raise ValueError("text exceeds the 256 KiB limit")
    return text


def read_file(path):
    source = Path(path)
    if not source.is_file():
        raise ValueError("input must be an existing regular file")
    with source.open("rb") as stream:
        raw = stream.read(MAX_TEXT_BYTES + 1)
    if len(raw) > MAX_TEXT_BYTES:
        raise ValueError("file exceeds the 256 KiB limit")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeError:
        raise ValueError("input file must be UTF-8") from None
    return validate_text(text)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("JSON contains a duplicate field")
        result[key] = value
    return result


def read_json(stream):
    raw = stream.read(MAX_JSON_BYTES + 1)
    if len(raw) > MAX_JSON_BYTES:
        raise ValueError("JSON input exceeds the transport limit")
    try:
        payload = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_object)
    except UnicodeError:
        raise ValueError("JSON input must be UTF-8") from None
    except (json.JSONDecodeError, RecursionError):
        raise ValueError("input must be one valid JSON object") from None
    if not isinstance(payload, dict) or set(payload) != {"before", "after"}:
        raise ValueError("JSON must contain only before and after fields")
    return validate_text(payload["before"]), validate_text(payload["after"])


def count_text(text):
    characters = len(text)
    return {
        "words": len(text.split()),
        "characters": characters,
        "estimated_tokens": (characters + 3) // 4,
    }


def split_lf_lines(text):
    parts = text.split("\n")
    return [part + "\n" for part in parts[:-1]] + ([parts[-1]] if parts[-1] else [])


def unified_diff(before, after):
    lines = difflib.unified_diff(
        split_lf_lines(before),
        split_lf_lines(after),
        fromfile="original",
        tofile="proposed",
    )
    output = []
    for line in lines:
        output.append(line)
        if not line.endswith("\n"):
            output.append("\n\\ No newline at end of file\n")
    return "".join(output)


def compare_texts(before, after, include_diff=False):
    validate_text(before)
    validate_text(after)
    original = count_text(before)
    proposed = count_text(after)
    changes = {}
    for metric, baseline in original.items():
        changes[metric] = {
            "delta": proposed[metric] - baseline,
            "reduction_percent": (
                100 * (baseline - proposed[metric]) / baseline if baseline else None
            ),
        }
    result = {
        "before": original,
        "after": proposed,
        "change": changes,
        "identical": before == after,
        "method": {
            "words": "whitespace-separated groups: len(text.split())",
            "characters": "Unicode characters, including line endings",
            "estimated_tokens": "ceil(characters / 4); rough English-text estimate",
            "delta": "after minus before",
            "reduction_percent": "100 * (before - after) / before; null if before is zero",
        },
    }
    if include_diff:
        result["diff"] = unified_diff(before, after)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Measure two inert UTF-8 texts without changing files."
    )
    parser.add_argument("--before", help="original UTF-8 file")
    parser.add_argument("--after", help="candidate UTF-8 file")
    parser.add_argument("--stdin-json", action="store_true", help="read before/after JSON from stdin")
    parser.add_argument("--diff", action="store_true", help="include a unified diff in the JSON result")
    args = parser.parse_args(argv)
    if args.stdin_json:
        if args.before is not None or args.after is not None:
            parser.error("--stdin-json cannot be combined with file arguments")
    elif args.before is None or args.after is None:
        parser.error("provide both --before and --after, or use --stdin-json")
    try:
        if args.stdin_json:
            before, after = read_json(sys.stdin.buffer)
        else:
            before, after = read_file(args.before), read_file(args.after)
        result = compare_texts(before, after, include_diff=args.diff)
    except OSError:
        print("measure: cannot read input file", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"measure: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
