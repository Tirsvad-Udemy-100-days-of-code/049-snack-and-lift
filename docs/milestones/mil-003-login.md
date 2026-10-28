# MIL-003 Lecture steps 1 and 2: profile, navigation and automated login

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-003 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version | [50e8331] |

---

## Purpose

Decide whether the bot can start Chrome with its own persistent profile, open the gym site and log in by itself, which completes lecture steps 1 and 2.

## Deliverable

Browser set-up with the `detach` option and the `chrome_profile` directory, navigation to the site, a `login()` function with explicit waits, unit tests, and screenshots for lecture steps 1 and 2.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | A container run opens the site with a profile directory and, after the test account exists, logs in and finds the class schedule | The schedule element is present | Login fails or times out |
| 2 | Unit tests for the option building and the credentials handling pass without a browser | 0 failures | A test fails |
| 3 | `docs/images/step-1.png` and `docs/images/step-2.png` exist | Both files exist and show the site | A file is missing |
| 4 | The code review against `qc-programming-python.md` is `Go` | `RC-*` is `Go` | `No-Go` |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-002 | Needs the scaffold and the container image |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O1, O2 | [BC-001] |
| CN-001, CN-004 | [SA-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S02 (AI as stand-in, autonomous mode, not independent) |

## Target Date

2026-10-30 — inside the planned window 2026-10-28 to 2026-11-06 of [PP-001]; the Business Case sets no deadline.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Start Chrome with a persistent profile | Build the Chrome options with `detach` and `--user-data-dir` pointing at a `chrome_profile` folder in the project, so the site's data survives between runs, and open the site URL. Save the screenshot `step-1.png`. | No | O1 |
| 2 | Register the test account in the profile | Document and script the one-time registration of the student account in the opened browser (the assignment does it by hand once). The container run registers it with a documented test e-mail and a strong password and keeps it in a profile volume. | No | O1 |
| 3 | Implement the login | Implement `login()` which clicks the login button, fills e-mail and password, submits and waits with `WebDriverWait` and `presence_of_element_located` for the class schedule. Save the screenshot `step-2.png`. | No | O2 |
| 4 | Read credentials safely | Take `ACCOUNT_EMAIL` and `ACCOUNT_PASSWORD` from environment variables with documented defaults for the practice site only, never from the personal `.env` and never printed. | No | O2 |

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
[SA-001]: ../stakeholder-analysis.md
[50e8331]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/commit/50e8331bd21910a72ae56b74c9ff6a3677a709b3
