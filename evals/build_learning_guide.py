#!/usr/bin/env python3
"""Evaluate the build-learning-guide skill."""

from pathlib import Path

from common import GUIDE_PATH, PROGRESS_PATH, FIXTURES, copy_fixture, run_cases


CREATE_PROMPT = (
    "Use $build-learning-guide to create a guide for event logs. My desired "
    "outcome is to inspect a JSON-lines event log and identify malformed "
    "records. I can read JSON but am new to event logs. My total active "
    "learning budget is 30 minutes. Use only event-log-notes.md as a source."
)
DRAFT_PROMPT = (
    CREATE_PROMPT
    + " We already agreed on the scope: one JSON object per line, checking the "
    "type and timestamp fields, reporting malformed line numbers, and "
    "continuing after a malformed line. Defer streaming large files. "
    "Please prepare the complete guide for my review. I have not approved "
    "the guide draft yet."
)
CASES = {
    "build-scope-review": CREATE_PROMPT,
    "build-draft-review": DRAFT_PROMPT,
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
    if name == "build-scope-review":
        reply = final.lower()
        return [
            ("no guide before scope confirmation", not generated),
            ("no progress file created", not progress.exists()),
            ("proposes scope and asks for human input", (
                any(word in reply for word in ("scope", "cover", "must learn"))
                and any(word in reply for word in ("defer", "exclude", "out of scope"))
                and any(word in reply for word in ("confirm", "correct", "edit"))
            )),
        ]
    if name == "build-draft-review":
        reply = final.lower()
        return [
            ("no guide before draft approval", not generated),
            ("no progress file created", not progress.exists()),
            ("shows complete draft", all(part in final for part in (
                "Learning contract", "Priority and scope", "Roadmap", "Sources", "LG-01"
            ))),
            ("presents a limitation", any(word in reply for word in (
                "limit", "trade-off", "tradeoff"
            ))),
            ("requests edits or explicit approval", "edit" in reply and "approv" in reply),
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
            ("asks for confirmation of another destination", (
                any(word in final.lower() for word in ("confirm", "approve"))
                and any(word in final.lower() for word in ("new destination", "another path", "v2"))
            )),
        ]
    raise ValueError(name)


if __name__ == "__main__":
    raise SystemExit(run_cases("build-learning-guide", CASES, setup, checks_for))
