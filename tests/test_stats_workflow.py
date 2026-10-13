"""Exercise the workflow's actual Bash scripts with local fixtures and Git remotes."""

import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = yaml.safe_load((ROOT / ".github/workflows/update-stats.yml").read_text(encoding="utf-8"))
STEPS = {step["name"]: step for step in WORKFLOW["jobs"]["update"]["steps"]}
BASH = str(Path("C:/Program Files/Git/bin/bash.exe")) if os.name == "nt" else shutil.which("bash")
TOKEN_ERROR = b'<svg xmlns="http://www.w3.org/2000/svg"><text>Something went wrong!</text><text data-testid="message">Resource not accessible by personal access token</text></svg>'


def bash_path(path):
    path = Path(path).resolve().as_posix()
    return f"/{path[0].lower()}{path[2:]}" if os.name == "nt" else path


def run_bash(script, directory, env):
    return subprocess.run(
        [BASH, "--noprofile", "--norc", "-c", script],
        cwd=directory, env=env, capture_output=True, text=True, timeout=20,
    )


class StatsWorkflowTests(unittest.TestCase):
    def run_download(self, dark=None, light=None, content_type="image/svg+xml; charset=utf-8"):
        with tempfile.TemporaryDirectory(prefix="oouo-stats-test-") as directory:
            workspace = Path(directory)
            for name in ("assets", "fixtures", "bin"):
                (workspace / name).mkdir()
            originals = {}
            for theme, override in (("dark", dark), ("light", light)):
                filename = f"github-stats-{theme}.svg"
                originals[filename] = (ROOT / "assets" / filename).read_bytes()
                (workspace / "assets" / filename).write_bytes(originals[filename])
                (workspace / "fixtures" / f"{theme}.svg").write_bytes(
                    override if override is not None else originals[filename]
                )
            curl = workspace / "bin" / "curl"
            curl.write_text('''#!/usr/bin/env bash
set -euo pipefail
while (( $# )); do
  case "$1" in
    --output) output="$2"; shift 2 ;;
    *theme=tokyonight*) fixture=fixtures/dark.svg; shift ;;
    *theme=default*) fixture=fixtures/light.svg; shift ;;
    *) shift ;;
  esac
done
cp "$fixture" "$output"
printf '%s' "$STATS_CONTENT_TYPE"
''', encoding="utf-8", newline="\n")
            python = workspace / "bin" / "python3"
            python.write_text(
                f"#!/usr/bin/env bash\nexec {shlex.quote(bash_path(sys.executable))} \"$@\"\n",
                encoding="utf-8", newline="\n",
            )
            curl.chmod(0o755)
            python.chmod(0o755)
            summary = workspace / "summary.md"
            env = dict(os.environ, STATS_ENDPOINT="https://stats.invalid/api",
                       STATS_CONTENT_TYPE=content_type, GITHUB_STEP_SUMMARY=str(summary))
            env["PATH"] = str(workspace / "bin") + os.pathsep + env["PATH"]
            # Git Bash prepends its own tools to inherited PATH on Windows.
            script = 'export PATH="$(pwd)/bin:$PATH"\n' + STEPS["Download and validate stats cards"]["run"]
            result = run_bash(script, workspace, env)
            installed = {name: (workspace / "assets" / name).read_bytes() for name in originals}
            return result, originals, installed, summary.read_text(encoding="utf-8") if summary.exists() else ""

    def test_valid_pair_passes(self):
        result, _, _, _ = self.run_download()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_token_error_reports_cause_and_preserves_pair(self):
        result, originals, installed, summary = self.run_download(dark=TOKEN_ERROR)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Resource not accessible by personal access token", result.stderr)
        self.assertIn("PAT_1", result.stderr)
        self.assertIn("Resource not accessible by personal access token", summary)
        self.assertEqual(installed, originals)

    def test_second_card_failure_does_not_install_first_card(self):
        refreshed = (ROOT / "assets/github-stats-dark.svg").read_bytes().replace(
            b"</svg>", b"<!-- refreshed -->\n</svg>"
        )
        result, originals, installed, _ = self.run_download(dark=refreshed, light=TOKEN_ERROR)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(installed, originals)

    def test_existing_validation_guards(self):
        valid = (ROOT / "assets/github-stats-dark.svg").read_bytes()
        cases = {
            "content type": (valid, "text/html", "Unexpected content type"),
            "minimum size": (b'<svg xmlns="http://www.w3.org/2000/svg"/>', "image/svg+xml", "unexpectedly small"),
            "XML syntax": (valid[:-30], "image/svg+xml", "not a complete SVG"),
            "XML root": (valid.replace(b"<svg", b"<other").replace(b"</svg>", b"</other>"), "image/svg+xml", "not a complete SVG"),
            "required fields": (valid.replace(b'data-testid="stars"', b'data-testid="removed"'), "image/svg+xml", "missing stars"),
            "script": (valid.replace(b"</svg>", b"<script/> </svg>"), "image/svg+xml", "unsafe SVG content"),
            "foreign object": (valid.replace(b"</svg>", b"<foreignObject/> </svg>"), "image/svg+xml", "unsafe SVG content"),
            "event handler": (valid.replace(b"<svg", b'<svg onload="alert(1)"', 1), "image/svg+xml", "unsafe SVG content"),
        }
        for name, (card, content_type, error) in cases.items():
            with self.subTest(name=name):
                result, originals, installed, _ = self.run_download(dark=card, content_type=content_type)
                self.assertNotEqual(result.returncode, 0, name)
                self.assertIn(error, result.stderr)
                self.assertEqual(installed, originals)

    def test_keepalive_only_commits_after_thirty_days(self):
        step = STEPS.get("Keep scheduled workflow active")
        self.assertIsNotNone(step, "No repository activity is produced when card refresh fails for 60 days")
        for age in (29, 31):
            with self.subTest(age_days=age), tempfile.TemporaryDirectory(prefix="oouo-keepalive-test-") as directory:
                workspace = Path(directory)
                repository, remote = workspace / "repository", workspace / "remote.git"
                env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")

                def git(*args, cwd=workspace, extra_env=None):
                    return subprocess.run(
                        ["git", *args], cwd=cwd, env={**env, **(extra_env or {})},
                        capture_output=True, text=True, check=True, timeout=10,
                    ).stdout.strip()

                git("init", "--initial-branch=main", str(repository))
                git("init", "--bare", str(remote))
                git("config", "user.name", "Fixture", cwd=repository)
                git("config", "user.email", "fixture@example.invalid", cwd=repository)
                timestamp = f"@{int(time.time()) - age * 86400} +0000"
                git("commit", "--allow-empty", "-m", "fixture", cwd=repository,
                    extra_env={"GIT_AUTHOR_DATE": timestamp, "GIT_COMMITTER_DATE": timestamp})
                git("remote", "add", "origin", str(remote), cwd=repository)
                git("push", "--set-upstream", "origin", "main", cwd=repository)
                result = run_bash(step["run"], repository, env)
                self.assertEqual(result.returncode, 0, result.stderr)
                expected = "2" if age >= 30 else "1"
                self.assertEqual(git("rev-list", "--count", "HEAD", cwd=repository), expected)
                self.assertEqual(git("rev-parse", "HEAD", cwd=repository), git("rev-parse", "main", cwd=remote))
                self.assertEqual(git("diff", "HEAD~1", "HEAD", cwd=repository) if age >= 30 else "", "")
                repeated = run_bash(step["run"], repository, env)
                self.assertEqual(repeated.returncode, 0, repeated.stderr)
                self.assertEqual(git("rev-list", "--count", "HEAD", cwd=repository), expected)


if __name__ == "__main__":
    unittest.main()
