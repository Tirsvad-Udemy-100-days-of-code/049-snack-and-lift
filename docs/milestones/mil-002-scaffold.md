# MIL-002 Project scaffold and tooling

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-002 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version | [50e8331] |

---

## Purpose

Decide whether the Python project skeleton, the tooling and the container image are ready, so that the lecture steps can be built on them.

## Deliverable

`pyproject.toml`, `src/` and `tests/` layout, `constants.py`, `.gitignore`, Doxyfile, README from the framework template with `.venv` instructions, and a Docker image with headless Chrome for browser runs.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `pip install -e .[dev]` in a fresh `.venv` and `pytest` pass | 0 failures | An install or test failure |
| 2 | `pyproject.toml` requires Python 3.13 or newer and lists Selenium as the only runtime dependency | Both true | Either false |
| 3 | `doxygen Doxyfile` runs without warnings on the skeleton | 0 warnings | Any warning |
| 4 | `bash framework/scripts/check-readme.sh` reports no finding | Exit code 0 | Exit code 1 |
| 5 | The container image builds and starts headless Chrome | A Selenium smoke run reads a page title | Build or run fails |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-001 | Needs the accepted baseline |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O7, success criteria 5, 6, 9 | [BC-001] |
| CN-004, CN-005, CN-008 | [SA-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S02 (AI as stand-in, autonomous mode, not independent) |

## Target Date

2026-10-29 — inside the planned window 2026-10-28 to 2026-11-06 of [PP-001]; the Business Case sets no deadline.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Create pyproject.toml and the package layout | Create `pyproject.toml` (Python 3.13 or newer, Selenium runtime, pytest and pytest-cov in a `dev` extra, a console script) and the `src/snack_and_lift` and `tests/` folders with a first passing test. | No | O7 |
| 2 | Add constants.py | Create `constants.py` holding the site URL, element IDs and selectors, the Tuesday and Thursday 6pm rule, the retry count and the Chrome profile folder name, so no magic value is in the logic. | No | O7 |
| 3 | Add .gitignore, Doxyfile and .dockerignore | Add a Python `.gitignore` (including `chrome_profile/`, `.venv/` and `.env`), a `Doxyfile` for the Doxygen comments and a `.dockerignore`. | No | O7 |
| 4 | Write the README with .venv instructions | Write `README.md` from the framework template: overview, requirements, creating and using a local `.venv`, `python -m pip install --upgrade pip`, run and test commands, and the container run. | No | O7 |
| 5 | Build the browser container image | Create a `Dockerfile` with headless Chrome and the project, so browser runs and screenshots never use the host desktop (`framework/process/gui-testing.md`). Prove it with a smoke run that reads the site's page title. | No | O7 |

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
[SA-001]: ../stakeholder-analysis.md
[50e8331]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/commit/50e8331bd21910a72ae56b74c9ff6a3677a709b3
