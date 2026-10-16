#!/usr/bin/env python3
"""Evaluate the run-learning-guide skill."""

from pathlib import Path

from common import GUIDE_PATH, PROGRESS_PATH, FIXTURES, copy_fixture, run_cases


CASES = {
    "run-start": (
        "Use $run-learning-guide with "
        "learning/event-logs/EVENT_LOGS_GUIDE.md. Start the guide."
    ),
    "run-teach": (
        "Use $run-learning-guide with "
        "learning/event-logs/EVENT_LOGS_GUIDE.md. Start the guide. "
        "I have 15 minutes of active learning time for this session."
    ),
    "run-invalid": (
        "Use $run-learning-guide with "
        "learning/event-logs/EVENT_LOGS_GUIDE.md. Start the guide. "
        "I have 15 minutes."
    ),
}


def setup(workspace: Path, name: str) -> None:
    copy_fixture(workspace, "event-log-notes.md", Path("event-log-notes.md"))
    if name == "run-invalid":
        guide = workspace / GUIDE_PATH
        guide.parent.mkdir(parents=True, exist_ok=True)
        guide.write_text("# Incomplete guide\n")
    else:
        copy_fixture(workspace, "EVENT_LOGS_GUIDE.md", GUIDE_PATH)


def checks_for(name: str, workspace: Path, final: str) -> list[tuple[str, bool]]:
    guide = workspace / GUIDE_PATH
    progress = workspace / PROGRESS_PATH
    guide_content = guide.read_text() if guide.exists() else ""
    content = progress.read_text() if progress.exists() else ""
    if name == "run-start":
        return [
            ("guide remains read-only", guide_content == (FIXTURES / "EVENT_LOGS_GUIDE.md").read_text()),
            ("adjacent progress file created", progress.exists()),
            ("progress references guide and unit", "EVENT_LOGS_GUIDE.md" in content and "LG-01" in content),
            ("does not start teaching without session time", "?" in final and "minute" in final.lower()),
        ]
    if name == "run-teach":
        reply = final.lower()
        return [
            ("guide remains read-only", guide_content == (FIXTURES / "EVENT_LOGS_GUIDE.md").read_text()),
            ("adjacent progress file created", progress.exists()),
            ("does not mark item complete without learner evidence", "- [x] LG-01" not in content),
            ("teaches the current item and asks for application", (
                "lg-01" in reply and "line" in reply
                and any(phrase in reply for phrase in ("your turn", "classify", "which line"))
            )),
        ]
    if name == "run-invalid":
        return [
            ("invalid guide preserved", guide_content == "# Incomplete guide\n"),
            ("no progress file created", not progress.exists()),
            ("recommends rebuilding", "build-learning-guide" in final),
        ]
    raise ValueError(name)


if __name__ == "__main__":
    raise SystemExit(run_cases("run-learning-guide", CASES, setup, checks_for))
