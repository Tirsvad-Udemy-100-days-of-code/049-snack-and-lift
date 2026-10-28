# MIL-007 Lecture step 9: resilience against network failures

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-007 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version | [50e8331] |

---

## Purpose

Decide whether the bot completes a full run when the site fails half of its requests, which completes lecture step 9.

## Deliverable

A `retry(func, retries=7, description=None)` wrapper, `login()`, `book_class()` and `get_my_bookings()` made resilient with it, unit tests with a failing fake, and the screenshot for lecture step 9.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | Unit tests show that `retry` returns on success, repeats on failure and raises after the last attempt | 0 failures | A test fails |
| 2 | Booking is only counted when the page confirms it (the button changes state) | Confirmed in tests and in a run | A click is counted without confirmation |
| 3 | Container runs with 50% simulated failures reach the verification result in 3 of 3 attempts | 3 of 3 | Fewer than 3 |
| 4 | `docs/images/step-9.png` exists | The file exists | The file is missing |
| 5 | The code review against `qc-programming-python.md` is `Go` | `RC-*` is `Go` | `No-Go` |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-006 | Needs login, booking and verification to wrap |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O6, success criteria 4, 5 | [BC-001] |
| CN-003 | [SA-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S02 (AI as stand-in, autonomous mode, not independent) |

## Target Date

2026-11-04 — inside the planned window 2026-10-28 to 2026-11-06 of [PP-001]; the Business Case sets no deadline.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Write the retry wrapper | Implement `retry(func, retries=7, description=None)` that calls the function, logs each failed attempt with the description and re-raises after the last one. Unit-test it with a fake that fails n times. | No | O6 |
| 2 | Wrap the login in retry | Move all login steps into `login()` and call it through `retry`, so a failed page load is repeated. | No | O6 |
| 3 | Make booking confirm its result | Put the booking steps in `book_class()` and treat the click as done only when the button reads "Booked" or "Waitlisted"; call it through `retry`. | No | O6 |
| 4 | Make the bookings read resilient | Put the My Bookings retrieval in `get_my_bookings()` and call it through `retry`. | No | O6 |
| 5 | Run the chaos test in a container | Clear the bookings in the admin panel, enable the network simulation at 50%, run the bot three times and keep the output. Save the screenshot `step-9.png`. | No | O6 |

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
[SA-001]: ../stakeholder-analysis.md
[50e8331]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/commit/50e8331bd21910a72ae56b74c9ff6a3677a709b3
