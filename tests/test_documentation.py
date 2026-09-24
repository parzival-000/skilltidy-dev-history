import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unittest
import uuid


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "skills/skilltidy"
DOCS = [
    ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "fixtures/README.md",
    ROOT / "tests/README.md", ROOT / "tests/RESULTS.md",
] + sorted(RUNTIME.rglob("*.md"))


class Documentation(unittest.TestCase):
    def test_maintained_docs_and_runtime_have_no_personal_paths(self):
        sources = set(DOCS) | {p for p in RUNTIME.rglob("*") if p.is_file()}
        for source in sorted(sources):
            with self.subTest(file=source.relative_to(ROOT)):
                self.assertNotRegex(
                    source.read_text(encoding="utf-8"),
                    r"(?i)[A-Z]:[\\/]Users[\\/]|/Users/|/home/[a-z0-9_-]+/",
                )

    def test_local_documentation_links_resolve(self):
        for source in DOCS:
            for link in re.findall(r"\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
                if link.startswith(("https://", "http://", "#")):
                    continue
                target = (source.parent / link.split("#", 1)[0]).resolve()
                with self.subTest(source=source.relative_to(ROOT), link=link):
                    self.assertTrue(target.is_relative_to(ROOT), link)
                    self.assertTrue(target.is_file(), link)

    def test_current_versions_agree(self):
        versions = []
        for source in [ROOT / "README.md", RUNTIME / "README.md",
                       ROOT / "tests/README.md", ROOT / "tests/RESULTS.md"]:
            match = re.search(r"Current version:\s*(?:\*\*)?(v\d+\.\d+)\b",
                              source.read_text(encoding="utf-8"))
            self.assertIsNotNone(match, str(source))
            versions.append(match.group(1))
        self.assertEqual(len(set(versions)), 1)

    def test_quick_start_paths_resolve_from_documented_folders(self):
        for source, directory in [(ROOT / "README.md", ROOT), (RUNTIME / "README.md", RUNTIME)]:
            text = source.read_text(encoding="utf-8")
            prompt = re.search(r"```text\n(.*?)\n```", text, re.S).group(1)
            paths = re.findall(r"(?:[\w.-]+/)*[\w.-]+\.md\b", prompt)
            self.assertGreaterEqual(len(paths), 2, "reviewer and target paths are required")
            reviewer, target = paths[:2]
            self.assertEqual((directory / reviewer).resolve(), RUNTIME / "SKILL.md")
            if source == ROOT / "README.md":
                self.assertTrue((directory / target).is_file())
                self.assertNotEqual((directory / target).resolve(), RUNTIME / "SKILL.md")
            else:
                self.assertNotEqual(target, reviewer)

    def test_documented_helper_commands_run_from_both_folders(self):
        trials = ROOT / ".local/trials"
        trials.mkdir(parents=True, exist_ok=True)
        case = trials / f"documentation-{uuid.uuid4().hex}"
        case.mkdir()
        before, after = case / "original.md", case / "candidate.md"
        before.write_bytes(b"alpha beta gamma\r\n")
        after.write_bytes(b"alpha beta\r\n")
        try:
            for source, directory in [(ROOT / "README.md", ROOT), (RUNTIME / "README.md", RUNTIME)]:
                text = source.read_text(encoding="utf-8")
                command = re.search(r"^py -3 -B (.+)$", text, re.M).group(1).split()
                command = [str(before) if item == "./original.md" else
                           str(after) if item == "./candidate.md" else item for item in command]
                result = subprocess.run([sys.executable, "-B", *command], cwd=directory,
                                        capture_output=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["before"]["words"], 3)
                self.assertEqual(payload["after"]["words"], 2)
                self.assertIn("-alpha beta gamma", payload["diff"])
            self.assertEqual(before.read_bytes(), b"alpha beta gamma\r\n")
            self.assertEqual(after.read_bytes(), b"alpha beta\r\n")
            self.assertEqual({p.name for p in case.iterdir()}, {"original.md", "candidate.md"})
        finally:
            self.assertEqual(case.resolve().parent, trials.resolve())
            shutil.rmtree(case)

    def test_behavior_cases_have_usable_inputs_and_keys(self):
        cases = json.loads((ROOT / "tests/behavior_cases.json").read_text(encoding="utf-8"))
        self.assertTrue(cases)
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(set(case), {"id", "fixture", "request", "format", "expected"})
                self.assertRegex(case["fixture"], r"^[a-z][a-z0-9-]+$")
                self.assertTrue((ROOT / "fixtures" / case["fixture"] / "SKILL.input.md").is_file())
                self.assertIsInstance(case["request"], str)
                self.assertIn(case["format"], {"text", "json"})
                self.assertIsInstance(case["expected"], str if case["format"] == "text" else dict)
                if case["id"].endswith("-repeat"):
                    original = next(row for row in cases if row["id"] == case["id"][:-7])
                    self.assertEqual({k: v for k, v in case.items() if k != "id"},
                                     {k: v for k, v in original.items() if k != "id"})


if __name__ == "__main__":
    unittest.main()
