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

## Publish

Commit and push the `skills/` directory to this GitHub repository. Make the repository public for anyone to install with the commands above. The `skills` CLI reads the `SKILL.md` files directly from GitHub; no npm package or registry publish step is needed.
