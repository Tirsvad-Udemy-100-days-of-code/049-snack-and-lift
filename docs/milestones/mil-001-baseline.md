# MIL-001 Baseline and repository set-up

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-001 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version | pending |

---

## Purpose

Decide whether the planning baseline is complete and accepted, so that code may be planned and written. The gate checks the documents, the recorded decisions and the repository metadata.

## Deliverable

Accepted Business Case, Stakeholder Analysis, Project Plan and milestones with `Go` review records; ADRs for the decisions; the dictionary; the Traceability Matrix; repository description and topics on the git host.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | Business Case, Stakeholder Analysis, Project Plan and all milestones have an `RC-*` with `Go` and an `Accepted` row (the Project Plan is accepted by S01 through the plan acceptance) | All rows `Accepted` | Any row `Proposed` or `No-Go` |
| 2 | `bash framework/scripts/check-plan.sh` reports no finding | Exit code 0 | Exit code 1 |
| 3 | The repository shows a description and at least 5 topics | API response contains both | Either is missing |
| 4 | ADR-0001 to ADR-0003 are `Accepted` | Three accepted ADRs | A decision is unrecorded |

## Dependencies

| Depends on | Reason |
| --- | --- |
| none | First gateway |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O7, success criterion 8 | [BC-001] |
| CN-002, CN-009 | [SA-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S02 (AI as stand-in, autonomous mode, not independent) |

## Target Date

2026-10-28 — inside the planned window 2026-10-28 to 2026-11-06 of [PP-001]; the Business Case sets no deadline.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Review and accept the baseline documents | Review BC-001, SA-001, PP-001 and MIL-001 to MIL-008 against their QC checklists, write the `RC-*` records and set the rows to `Accepted`. In autonomous mode the AI is stand-in reviewer and says so in each record. | No |  |
| 2 | Record the planning decisions as ADRs | Write ADR-0001 (skip user stories and use cases: one actor, one linear flow), ADR-0002 (light Clean Architecture: booking rules separate from the Selenium adapter, no presentation layer) and ADR-0003 (browser runs and screenshots in a Docker container with headless Chrome, never on the host desktop). | No | ADR-0001, ADR-0002, ADR-0003 |
| 3 | Create the domain dictionary | Create `docs/dictionary.md` with the PO and IT terms of the gym site and course (class card, booking, waitlist, retry, profile, lecture step), because the language review of the PO-language documents checks their terms against it. | No | DICT-001 |
| 4 | Create the Traceability Matrix | Create `docs/sqa/traceability-matrix.md` and add a row for each artifact and its review, so coverage of the stakeholder concerns can be read in one place. | No | TM-001 |
| 5 | Set repository description and topics | Set the description and topics (python, selenium, udemy, 100-days-of-code, automation, gym-booking) on the git host with the API. The token comes from the personal `.env`; it is never printed, imported, tested or committed. Confirm the target repository with S01 first if it differs from `origin`. | No | O7 |
| 6 | Check repository visibility and the AI prompt log | Ask the host API whether the repository is private. If it is public, put `/docs/ai-prompts/` in `.gitignore`; record each session's prompts in `docs/ai-prompts/session-NNN/prompts.md` as the framework requires. | No |  |
| 7 | Enable the plan gate commit hook | Run `bash framework/scripts/install-git-hooks.sh --enable-plan-gate` so a commit under `src/` or `tests/` needs a `Task: MIL-NNN#N` trailer. | No |  |

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
[SA-001]: ../stakeholder-analysis.md
