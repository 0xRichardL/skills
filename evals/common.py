"""Shared process runner for the two learning guide evaluations."""

import argparse
import json
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
GUIDE_PATH = Path("learning/event-logs/EVENT_LOGS_GUIDE.md")
PROGRESS_PATH = Path("learning/event-logs/EVENT_LOGS_PROGRESS.md")


def copy_fixture(workspace: Path, fixture: str, destination: Path) -> None:
    target = workspace / destination
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(FIXTURES / fixture, target)


def run_cases(
    skill: str,
    cases: dict[str, str],
    setup: Callable[[Path, str], None],
    checks_for: Callable[[str, Path, str], list[tuple[str, bool]]],
) -> int:
    parser = argparse.ArgumentParser(description=f"Evaluate {skill} in isolated Codex sessions")
    parser.add_argument("--case", choices=cases, action="append", help="Run selected case; repeatable")
    parser.add_argument("--model", help="Pass a model name to codex exec")
    parser.add_argument("--list", action="store_true", help="List cases without running Codex")
    args = parser.parse_args()
    if args.list:
        print("\n".join(cases))
        return 0
    if not shutil.which("codex"):
        parser.error("codex CLI is required; install or add it to PATH")
    source = ROOT / "skills" / skill
    if not (source / "SKILL.md").exists():
        parser.error(f"missing skills/{skill}/SKILL.md")

    run_dir = ROOT / "evals/results" / skill / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    run_dir.mkdir(parents=True)
    summaries = []
    for name in args.case or list(cases):
        output = run_dir / name
        output.mkdir()
        with tempfile.TemporaryDirectory(prefix=f"skill-eval-{name}-") as temp:
            workspace = Path(temp)
            skill_dir = workspace / ".agents/skills"
            skill_dir.mkdir(parents=True)
            shutil.copytree(source, skill_dir / skill)
            setup(workspace, name)
            command = ["codex", "exec", "--ephemeral", "--skip-git-repo-check", "--sandbox", "workspace-write", "--json", "-C", str(workspace), "-o", str(output / "final.txt")]
            if args.model:
                command += ["--model", args.model]
            command += ["-"]
            print(f"Running {name}...", flush=True)
            try:
                result = subprocess.run(command, input=cases[name], text=True, capture_output=True, timeout=240)
                (output / "events.jsonl").write_text(result.stdout)
                (output / "stderr.txt").write_text(result.stderr)
                final = (output / "final.txt").read_text() if (output / "final.txt").exists() else ""
                checks = checks_for(name, workspace, final) if result.returncode == 0 else []
                error = None if result.returncode == 0 else f"codex exited {result.returncode}"
            except subprocess.TimeoutExpired as exc:
                (output / "events.jsonl").write_text(exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else exc.stdout or "")
                (output / "stderr.txt").write_text(exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else exc.stderr or "")
                checks, error = [], "codex timed out after 240 seconds"
            for path in workspace.rglob("*"):
                if path.is_file() and ".agents" not in path.parts:
                    target = output / "workspace" / path.relative_to(workspace)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(path, target)
            passed = error is None and all(ok for _, ok in checks)
            summaries.append({"case": name, "passed": passed, "error": error, "checks": [{"name": label, "passed": ok} for label, ok in checks]})
            print(f"  {'PASS' if passed else 'FAIL'}" + (f": {error}" if error else ""))
            for label, ok in checks:
                print(f"    {'✓' if ok else '✗'} {label}")
    (run_dir / "summary.json").write_text(json.dumps(summaries, indent=2) + "\n")
    print(f"Results: {run_dir}")
    return 0 if all(item["passed"] for item in summaries) else 1
