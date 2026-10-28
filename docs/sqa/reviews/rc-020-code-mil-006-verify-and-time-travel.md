# SQA Review Record

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-020 |
| CrossReference | [MIL-006], [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Review record, full review of the source and tests of MIL-006 | [f57040e] |

---

## Artifact Under Review

- Instance reviewed: [MIL-006]
- Checklist used: [QC-PY-001] (`QC-PY-001`)
- Scope: full review of the source and tests of MIL-006
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is `AI as stand-in for S02`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | Modules, functions and variables are `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE`; `ruff check` with the N rules passes. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (for example `retry`, `login`, `book_class`, `get_my_bookings`); no single-letter names outside comprehensions. |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff format` leaves 0 files changed and `ruff check` reports 0 findings; there is no suppression. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every function and method has annotations (ruff ANN rules pass), including `-> None`. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | No bare `except`; specific exceptions are caught, and re-raised with `raise ... from` where the cause matters. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable default arguments; no builtin is shadowed (ruff B and A-style checks pass). |
| 7 | Files, locks and connections are managed with context managers | Pass | Files and the browser are managed with `with`/`try-finally`; no unmanaged file handle exists. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Public modules, classes and functions have Doxygen docstrings (`@brief`, `@param`, `@return`). |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No print calls; messages go through `logging`. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | N-A | No Design Class Diagram exists; ADR-0001 records that design artifacts are skipped. Classes follow ADR-0002. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 174 unit tests (booking entries, verification, date independence for all seven starting weekdays, command line) need no browser or network; 15 container tests run the adapter against local fixtures; coverage of the non-infrastructure modules is 100%. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | N-A | No strict type checker is configured; annotations are complete and checked by ruff. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `pyproject.toml` declares Selenium (runtime) and pytest, pytest-cov, ruff (dev) with lower bounds; none is unused. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | Each rule, constant and message exists once (constants in `constants.py`, rules in `domain/`). |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `domain` and `application` import no Selenium; only `infrastructure` imports it; no import cycle exists. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | One reason to change per module; the adapter hides Selenium behind a port; fakes honour the port contract. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | Layout follows `src/snack_and_lift/{domain,application,infrastructure}` and `tests/{unit,integration,e2e}`; there is no presentation layer for a command-line bot (ADR-0002). |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | All file and folder names are English lowercase with `_`, `-` and `.` only. |

## Overall Verdict

Go-with-conditions - the code of MIL-006 meets every Mandatory criterion of QC-PY-001 and there is no blocking finding, but part of the gate evidence cannot be produced by the stand-in. Gate criterion 1 (unit tests of the comparison and the mismatch message) is met, and the date independence is tested for every starting weekday (no hardcoded date, no list-position rule). Criteria 2 and 3 (container runs on the live site, including after the admin advances 3 days) are not verified, and criterion 4 is not met: `step-7.png` and `step-8.png` come from a run with an account. The framework forbids the stand-in to enter passwords or register on a third-party site; the admin time controls also need a login. The review is not independent: the AI wrote and reviewed it as stand-in for S02, and S01 can challenge it in the end-of-run summary.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Run the bot with your own account (also after advancing the site 3 days as admin) and keep `docs/images/step-7.png` and `step-8.png` | S01 | when S01 has time |

---

[MIL-006]: ../../milestones/mil-006-verify-and-time-travel.md
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[f57040e]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/commit/f57040e136feac01f10d99279038f48992518f43
