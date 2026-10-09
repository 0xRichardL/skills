---
name: build-learning-guide
description: Research any learning target and create a concise, time-boxed guide named with an uppercase target prefix and _GUIDE.md suffix. Use only when explicitly invoked to build a learning guide; do not use it to teach lessons or track progress.
---

# Build Learning Guide

Create the stable learning compass. Optimize for complete coverage of the high-value backbone, not exhaustive detail.

## Required inputs

Before researching or writing, establish:

- the learning target;
- the learner's desired outcome;
- the learner's current level; and
- the total active-learning time budget.

Ask one concise question for any missing required input. Do not create the guide until all four are known. Treat the budget as learner study time, not agent research time. Capture optional deadlines, source restrictions, accessibility needs, or required tools only when the user supplies them or they materially affect the plan.

Derive a lowercase hyphenated target slug and convert it to an uppercase snake-case filename prefix. Name the guide `<TARGET>_GUIDE.md`; for example, `sample-topic` becomes `SAMPLE_TOPIC_GUIDE.md`. Use the user's destination directory when specified. Otherwise use `learning/<target-slug>/<TARGET>_GUIDE.md` in the active workspace. If the user supplies an explicit filename, require the `_GUIDE.md` suffix and preserve its prefix exactly. Inspect the destination before writing. Never overwrite an existing guide; suggest a sibling destination such as `<target-slug>-v2` and wait for the user's confirmation.

## Research with a stopping rule

Inspect relevant user-provided and local material first, then use available research tools unless the user prohibited external research.

1. **Coverage pass:** identify the outcomes, core concepts, dependencies, and representative practice from primary or authoritative sources.
2. **Validation pass:** compare the proposed backbone with established curricula, syllabi, standards, or respected practitioner guidance and close material gaps.

Prefer current primary sources. Use secondary sources mainly to validate coverage or provide practical perspective. Keep roughly 5–10 high-value sources when the subject supports that range; do not pad the list. Stop after the two passes, or earlier when another pass adds no essential outcome. If network research is unavailable or the target is private/local, use the accessible corpus and state the limitation in the guide.

## Design the time-boxed backbone

- Classify material as must learn, supporting, or deferred. Exclude low-value detail explicitly rather than hiding it.
- Create ordered, independently resumable units with stable IDs `LG-01`, `LG-02`, and so on.
- Give every unit one observable outcome, only the key ideas needed for it, suitable practice, mastery evidence, and an active-learning estimate.
- Include retrieval, application, and review time. The sum of all unit estimates must not exceed the user's total budget.
- If the target cannot fit honestly, narrow the promised outcome and list the rest as deferred. Do not use unrealistically small estimates to force a fit.
- Keep explanations skeletal. The teaching skill researches and expands one unit at a time.

## Write only the guide

Read [assets/GUIDE.template.md](assets/GUIDE.template.md), copy its structure, and replace every placeholder. Keep the compact reference useful after learning is complete. Cite sources with direct links and a short note about what each source established.

Create only `<TARGET>_GUIDE.md`. Do not create the matching `<TARGET>_PROGRESS.md`, lesson transcripts, exercises, or source archives.

Before finishing, verify that required inputs and success criteria are explicit, unit IDs are unique, unit estimates add up within the budget, deferred material is visible, and no placeholder remains. Report the created path, planned total, and first unit concisely.
