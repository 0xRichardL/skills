# Learning Guide: Event logs

> Created: 2026-10-15
> Guide version: 1
> Target slug: event-logs

## Learning contract

| Field | Value |
| --- | --- |
| Desired outcome | Inspect a JSON-lines event log and identify malformed records. |
| Current level | Can read JSON, new to event logs. |
| Success criteria | Explain line-by-line parsing and identify an invalid record. |
| Total active-learning budget | 30 minutes |
| Constraints | Use only local notes. |

## Priority and scope

### Must learn

- Parse each line independently and inspect event fields.

### Supporting knowledge

- Report line numbers for malformed records.

### Deliberately deferred

- Streaming large files; outside this budget.

## Roadmap

| ID | Unit | Observable outcome | Key ideas | Practice and mastery evidence | Estimate |
| --- | --- | --- | --- | --- | ---: |
| LG-01 | Inspect records | Identify valid and malformed records | One JSON object per line; required fields | Classify sample records and explain the malformed line | 20 minutes |

**Planned total:** 20 minutes

## Milestones

| Milestone | Units | Cumulative time | Evidence |
| --- | --- | ---: | --- |
| Basic inspection | LG-01 | 20 minutes | Correctly classify records. |

## Compact reference

### Parsing rule

- Parse each line separately; report malformed line numbers.

## Sources

1. [Event log notes](../../event-log-notes.md) — Defines the record format.

## Research limits

- Local notes only, as requested.
