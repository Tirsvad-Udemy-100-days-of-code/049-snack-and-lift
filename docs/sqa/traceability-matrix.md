# Traceability Matrix

## Metadata
| Key | Value |
| --- | --- |
| ID | TM-001 |
| CrossReference | [BC-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version: baseline artifacts | pending |

---

## Purpose

Tracks backward and forward links between artifact instances so that the Business Case's traceability can be read in one place. A row is added or updated whenever an artifact is created or reviewed. Rows for code and tests are added by the milestones that create them.

## Traceability Table

| Artifact Instance | Type | Language | Domain | Upstream (Backward Link) | Downstream (Forward Link) | Last Reviewed (RC-ID) |
| --- | --- | --- | --- | --- | --- | --- |
| [BC-001] | Business Case | en | it | - | [SA-001], [PP-001] | RC-001 |
| [SA-001] | Stakeholder Analysis | en | it | [BC-001] | [PP-001] | RC-002 |
| [PP-001] | Project Plan | en | it | [BC-001], [SA-001] | [MIL-001] to [MIL-008] | RC-003 |
| [DICT-001] | Domain Dictionary | en | it | [BC-001], [SA-001] | - | RC-004 |
| [ADR-0001] | ADR | - | - | [BC-001] | [PP-001] | RC-005 |
| [ADR-0002] | ADR | - | - | [BC-001], [SA-001] | code from MIL-002 onward | RC-006 |
| [ADR-0003] | ADR | - | - | [BC-001] | [MIL-002], [MIL-003] | RC-007 |
| [MIL-001] | Milestone | en | it | [BC-001], [PP-001] | [MIL-002] | RC-008 |
| [MIL-002] | Milestone | en | it | [BC-001], [PP-001] | [MIL-003] | RC-009 |
| [MIL-003] | Milestone | en | it | [BC-001], [PP-001] | [MIL-004] | RC-010 |
| [MIL-004] | Milestone | en | it | [BC-001], [PP-001] | [MIL-005] | RC-011 |
| [MIL-005] | Milestone | en | it | [BC-001], [PP-001] | [MIL-006] | RC-012 |
| [MIL-006] | Milestone | en | it | [BC-001], [PP-001] | [MIL-007] | RC-013 |
| [MIL-007] | Milestone | en | it | [BC-001], [PP-001] | [MIL-008] | RC-014 |
| [MIL-008] | Milestone | en | it | [BC-001], [PP-001] | - | RC-015 |

## Concern Coverage

| Concern (CN-ID) | Views that answer it | Decisions (ADR) | Quality check | Status |
| --- | --- | --- | --- | --- |
| CN-001 | [BC-001], [MIL-003] to [MIL-006] | [ADR-0002] | Unit tests per gateway | Planned |
| CN-002 | [PP-001], [MIL-001] | [ADR-0001] | Review records RC-001 onward | Covered |
| CN-003 | [MIL-006], [MIL-007] | [ADR-0002] | Unit tests of `retry`; container chaos run | Planned |
| CN-004 | [MIL-003] to [MIL-007] | [ADR-0002] | Code review against QC-PY-001 | Planned |
| CN-005 | [MIL-002], [MIL-008] | - | `check-readme.sh` | Planned |
| CN-006 | [MIL-008] | - | Page count per language | Planned |
| CN-007 | [MIL-001] | - | Repository API response | Covered |
| CN-008 | [MIL-002] | [ADR-0002] | `pyproject.toml` | Planned |
| CN-009 | [MIL-001] | - | `.gitignore` lists `.env` | Covered |

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[PP-001]: ../project-plan.md
[DICT-001]: ../dictionary.md
[ADR-0001]: ../adr/adr-0001-skip-stories-use-cases.md
[ADR-0002]: ../adr/adr-0002-light-clean-architecture.md
[ADR-0003]: ../adr/adr-0003-docker-headless-browser.md
[MIL-001]: ../milestones/mil-001-baseline.md
[MIL-002]: ../milestones/mil-002-scaffold.md
[MIL-003]: ../milestones/mil-003-login.md
[MIL-004]: ../milestones/mil-004-book-class.md
[MIL-005]: ../milestones/mil-005-counters-and-both-days.md
[MIL-006]: ../milestones/mil-006-verify-and-time-travel.md
[MIL-007]: ../milestones/mil-007-resilience.md
[MIL-008]: ../milestones/mil-008-documentation.md
