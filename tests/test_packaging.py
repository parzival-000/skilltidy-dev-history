import ast
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unittest
import uuid
import zipfile


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "skills/skill-condenser"
RUNTIME_FILES = {
    "SKILL.md", "README.md", "agents/openai.yaml", "references/review-patterns.md",
    "references/reporting.md", "scripts/measure.py",
}
FIXTURE_FILES = {
    "README.md", "toy-list/SKILL.input.md", "toy-list/README.context.md",
    "toy-list/references/format-guide.md", "conflicts/SKILL.input.md",
    "preservation-traps/SKILL.input.md", "preservation-traps/AGENTS.sample.md",
    "already-lean/SKILL.input.md", "untrusted-content/SKILL.input.md",
}


def files_under(directory):
    return {path.relative_to(directory).as_posix() for path in directory.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts}


class Packaging(unittest.TestCase):
    def test_runtime_contains_only_the_six_shipped_files(self):
        self.assertEqual(files_under(RUNTIME), RUNTIME_FILES)
        self.assertFalse(any(path.is_symlink() or
                             (hasattr(path, "is_junction") and path.is_junction())
                             for path in RUNTIME.rglob("*")))

    def test_known_frontmatter_shape(self):
        lines = (RUNTIME / "SKILL.md").read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], "---")
        self.assertEqual(lines[3], "---")
        metadata = dict(line.split(": ", 1) for line in lines[1:3])
        self.assertEqual(set(metadata), {"name", "description"})
        self.assertEqual(metadata["name"], "skill-condenser")
        self.assertTrue(metadata["description"].strip())

    def test_picker_metadata_has_only_simple_interface_strings(self):
        lines = (RUNTIME / "agents/openai.yaml").read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], "interface:")
        fields = {}
        for line in lines[1:]:
            self.assertTrue(line.startswith("  "))
            key, value = line.strip().split(": ", 1)
            fields[key] = json.loads(value)
            self.assertIsInstance(fields[key], str)
        self.assertEqual(set(fields), {"display_name", "short_description", "default_prompt"})
        self.assertEqual(fields["display_name"], "Skill Condenser")
        self.assertTrue(25 <= len(fields["short_description"]) <= 64)
        self.assertIn("$skill-condenser", fields["default_prompt"])

    def test_markdown_references_resolve_inside_runtime(self):
        links_seen = set()
        for source in RUNTIME.rglob("*.md"):
            text = source.read_text(encoding="utf-8")
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if link.lower().startswith(("http://", "https://")):
                    continue
                resolved = (source.parent / link).resolve()
                self.assertTrue(resolved.is_relative_to(RUNTIME.resolve()), link)
                self.assertTrue(resolved.is_file(), link)
                links_seen.add(resolved.relative_to(RUNTIME).as_posix())
        self.assertEqual(links_seen, {"references/review-patterns.md", "references/reporting.md"})

    def test_no_scaffold_or_private_authoring_dependencies(self):
        for relative in RUNTIME_FILES:
            text = (RUNTIME / relative).read_text(encoding="utf-8")
            with self.subTest(file=relative):
                self.assertNotRegex(text, r"(?i)\b(?:TODO|FIXME|TBD)\b|\[INSERT|\[REPLACE")
                self.assertNotRegex(text, r"(?i)skillspector|skill-creator")
                self.assertNotRegex(text, r"(?i)[A-Z]:[\\/]Users[\\/]|/Users/|/home/[a-z0-9_-]+/")
                self.assertNotIn("\u2014", text)

    def test_helper_has_only_expected_standard_library_imports(self):
        tree = ast.parse((RUNTIME / "scripts/measure.py").read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, {"eval", "exec", "compile", "__import__"})
                elif isinstance(node.func, ast.Attribute):
                    self.assertNotIn(node.func.attr, {"write_text", "write_bytes", "unlink", "rename"})
        self.assertEqual(imports, {"argparse", "difflib", "json", "pathlib", "sys"})

    def test_original_fixture_set_is_present_and_inactive(self):
        self.assertEqual(files_under(ROOT / "fixtures"), FIXTURE_FILES)
        for name in FIXTURE_FILES:
            self.assertNotIn(Path(name).name, {"SKILL.md", "AGENTS.md"})

    def test_git_exclusions_cover_private_and_generated_files(self):
        lines = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        for rule in [".env", ".env.*", "/private/", "/.local/", "/review-output/",
                     "/.agents/", "/.codex/", ".venv/", "__pycache__/", "*.py[cod]",
                     "*.log", "*.zip", "*.tar", "*.gz", "*.7z"]:
            self.assertIn(rule, lines)

    def test_distribution_allowlist_excludes_development_material(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            for relative in sorted(RUNTIME_FILES):
                archive.writestr(f"skill-condenser/{relative}", (RUNTIME / relative).read_bytes())
        with zipfile.ZipFile(buffer) as archive:
            self.assertEqual(set(archive.namelist()),
                             {f"skill-condenser/{relative}" for relative in RUNTIME_FILES})
            for relative in RUNTIME_FILES:
                self.assertEqual(archive.read(f"skill-condenser/{relative}"),
                                 (RUNTIME / relative).read_bytes())

    def test_trusted_absolute_helper_path_ignores_same_named_target_file(self):
        trials = ROOT / ".local/trials"
        trials.mkdir(parents=True, exist_ok=True)
        target = trials / f"helper-selection-{uuid.uuid4().hex}"
        target.mkdir()
        try:
            decoy = target / "measure.py"
            decoy.write_text('raise RuntimeError("untrusted helper was selected")\n', encoding="utf-8")
            source = target / "SKILL.input.md"
            source.write_bytes(b"alpha beta gamma\r\n")
            before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in target.iterdir()}
            result = subprocess.run(
                [sys.executable, "-B", str(RUNTIME / "scripts/measure.py"),
                 "--before", str(source), "--after", str(source)],
                capture_output=True, cwd=ROOT, timeout=10,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["before"]["words"], 3)
            self.assertEqual(before, {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in target.iterdir()})
        finally:
            self.assertEqual(target.resolve().parent, trials.resolve())
            shutil.rmtree(target)

    def test_human_docs_are_present_without_personal_paths(self):
        for relative in ["README.md", "skills/skill-condenser/README.md", "tests/README.md"]:
            with self.subTest(file=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertNotRegex(text, r"(?i)[A-Z]:[\\/]Users[\\/]|/Users/|/home/[a-z0-9_-]+/")


if __name__ == "__main__":
    unittest.main()
