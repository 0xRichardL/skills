# Learning Guide Skills

Two skills for building and running time-boxed learning guides:

- `build-learning-guide` creates a guide and roadmap.
- `run-learning-guide` teaches from an existing guide and tracks progress.

## Install

List the skills available in this repository:

```sh
npx skills add 0xRichardL/skills --list
```

Install both globally for Codex:

```sh
npx skills add 0xRichardL/skills --skill build-learning-guide --skill run-learning-guide -a codex -g -y
```

Omit `-g` to install them in the current project instead.

## Evaluate

Run each skill's isolated behavioral cases with the Codex CLI:

```sh
python3 evals/build_learning_guide.py
python3 evals/run_learning_guide.py
```

Use `--list` with either script to see its cases, or `--case build-create` / `--case run-teach` to run one. Each case copies its skill into a temporary workspace, invokes it through `codex exec`, and checks file behavior. The scripts save final responses, event logs, generated files, and pass/fail summaries under `evals/results/<skill>/` (ignored by Git). Review the saved responses and artifacts for teaching and research quality; the automated checks cover core file and workflow invariants.

For a manual review, check that the guide's scope, source claims, and time estimates are credible. For a teaching case, check that the explanation is accurate, the exercise matches the unit's mastery evidence, and the saved progress describes the same exercise and next action shown to the learner. These judgment calls are not covered by the automatic pass/fail result.

## Publish

Commit and push `skills/`, `evals/`, and this README to the GitHub repository. Make the repository public for anyone to install with the commands above. The `skills` CLI reads the `SKILL.md` files directly from GitHub; no npm package or registry publish step is needed.
