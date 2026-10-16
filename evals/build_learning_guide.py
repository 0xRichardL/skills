#!/usr/bin/env python3
"""Evaluate the build-learning-guide skill."""

import re
from pathlib import Path

from common import GUIDE_PATH, PROGRESS_PATH, FIXTURES, copy_fixture, run_cases


CREATE_PROMPT = (
    "Use $build-learning-guide to create a guide for event logs. My desired "
    "outcome is to inspect a JSON-lines event log and identify malformed "
    "records. I can read JSON but am new to event logs. My total active "
    "learning budget is 30 minutes. Use only event-log-notes.md as a source."
)
CASES = {
    "build-create": CREATE_PROMPT,
    "build-missing-input": (
        "Use $build-learning-guide to make a guide about event logs. "
        "Use only event-log-notes.md as a source."
    ),
    "build-existing": CREATE_PROMPT,
}


def setup(workspace: Path, name: str) -> None:
    copy_fixture(workspace, "event-log-notes.md", Path("event-log-notes.md"))
    if name == "build-existing":
        copy_fixture(workspace, "EVENT_LOGS_GUIDE.md", GUIDE_PATH)


def checks_for(name: str, workspace: Path, final: str) -> list[tuple[str, bool]]:
    guide = workspace / GUIDE_PATH
    progress = workspace / PROGRESS_PATH
    content = guide.read_text() if guide.exists() else ""
    generated = list(workspace.rglob("*_GUIDE.md"))
    if name == "build-create":
        rows = re.findall(r"^\|\s*(LG-\d+)\s*\|.*\|\s*(\d+)\s+(?:min|minutes?)\s*\|$", content, re.M)
        return [
            ("guide created at target path", guide.exists()),
            ("no progress file created", not progress.exists()),
            ("outcome and success criteria present", "Desired outcome" in content and "Success criteria" in content),
            ("roadmap has unique unit IDs and fits budget", bool(rows) and len(rows) == len(set(x[0] for x in rows)) and sum(int(x[1]) for x in rows) <= 30),
            ("source cited and no placeholders", "event-log-notes.md" in content and "<" not in content),
        ]
    if name == "build-missing-input":
        reply = final.lower()
        return [
            ("no guide created", not generated),
            ("asks for missing information", (
                any(word in reply for word in ("outcome", "want to be able", "goal"))
                and any(word in reply for word in ("level", "experience"))
                and any(word in reply for word in ("time", "budget", "minutes"))
                and any(word in reply for word in ("reply", "provide", "tell", "?"))
            )),
        ]
    if name == "build-existing":
        return [
            ("existing guide preserved", content == (FIXTURES / "EVENT_LOGS_GUIDE.md").read_text()),
            ("no second guide created without confirmation", len(generated) == 1),
            ("asks for confirmation of another destination", "?" in final),
        ]
    raise ValueError(name)


if __name__ == "__main__":
    raise SystemExit(run_cases("build-learning-guide", CASES, setup, checks_for))
