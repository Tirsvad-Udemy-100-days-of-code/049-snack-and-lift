# MIL-010 Gym accounts from a credentials file

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-010 |
| CrossReference | [BC-001], [MIL-003] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version, requested by S01 in chat | pending |

---

## Purpose

Decide whether the bot can read the student and the admin account of the practice site from the personal file `.env.gym`, so that S01 does not set environment variables by hand before each run, while the file stays out of the repository and the tests.

## Deliverable

`credentials.py` that loads the student account and, load-only, the admin account from the environment, plus a small reader of the `.env.gym` file in the infrastructure layer that the command line merges under the real environment, unit tests with dummy values only, and README and wiki instructions.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | Unit tests show that the student and the admin account load from file values, and that a real environment variable wins over the file | 0 failures | A test fails or is missing |
| 2 | Unit tests show that a missing or empty variable raises an error that names the variable and never prints a value, and that the admin account is optional | 0 failures | A test fails or is missing |
| 3 | No test reads `.env` or `.env.gym`; `.env.gym` is in `.gitignore`; no password appears in the repository | `git grep` finds no real credential; tests use `tmp_path` | A real file is read or a credential is committed |
| 4 | All earlier tests pass with at least 80% coverage of the logic modules | Both true | Either false |
| 5 | The code review against `qc-programming-python.md` is `Go` | `RC-*` is `Go` | `No-Go` |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-003 | Changes the credentials handling that MIL-003 built |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O2, O7 | [BC-001] |
| CN-004, CN-005, CN-009 | [SA-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S02 (AI as stand-in, autonomous mode, not independent) |

## Target Date

2026-11-06 — inside the planned window 2026-10-28 to 2026-11-06 of [PP-001]; the Business Case sets no deadline.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Load the student and the admin account | In `credentials.py` read `SNACK_AND_LIFT_EMAIL` and `SNACK_AND_LIFT_PASSWORD` (required) and `SNACK_AND_LIFT_ADMIN_EMAIL` and `SNACK_AND_LIFT_ADMIN_PASSWORD` (optional, load-only; nothing uses the admin yet). Errors name the variables, never a value. | No | O2 |
| 2 | Read the `.env.gym` file | Add a small reader (no new dependency) in `infrastructure/` for `KEY=VALUE` lines; the command line merges the file under the real environment, and a missing file is not an error. | No | O2, O7 |
| 3 | Test and document | Unit tests with dummy values in `tmp_path`; update the README and the Getting Started wiki pages (three languages) and keep `.env.gym` in `.gitignore`. | No | O7, O8 |

---

[BC-001]: ../business-case.md
[MIL-003]: ./mil-003-login.md
[PP-001]: ../project-plan.md
[SA-001]: ../stakeholder-analysis.md
