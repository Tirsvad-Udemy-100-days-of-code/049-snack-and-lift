# MIL-006 Lecture steps 7 and 8: verify bookings and time travel QA

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-006 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version | pending |

---

## Purpose

Decide whether the bot verifies its work on the "My Bookings" page and behaves correctly on other dates of the site, which completes lecture steps 7 and 8.

## Deliverable

Navigation to "My Bookings", verification with `NoSuchElementException`, a comparison of expected and found, handling of any start date, unit tests, and screenshots for lecture steps 7 and 8.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | Unit tests for the comparison and the mismatch message pass | 0 failures | A test fails |
| 2 | A container run prints the verification result and "SUCCESS" when all bookings are found | Expected equals found | A mismatch without cause |
| 3 | A container run after the admin advances 3 days books new classes in the window | New Tuesday and Thursday classes are processed | The bot assumes the first day is Monday or hardcodes a date |
| 4 | `docs/images/step-7.png` and `docs/images/step-8.png` exist | Both files exist | A file is missing |
| 5 | The code review against `qc-programming-python.md` is `Go` | `RC-*` is `Go` | `No-Go` |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-005 | Needs the counters and the full class list |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O5, success criteria 1, 3 | [BC-001] |
| CN-001, CN-003 | [SA-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S02 (AI as stand-in, autonomous mode, not independent) |

## Target Date

2026-11-02 — inside the planned window 2026-10-28 to 2026-11-06 of [PP-001]; the Business Case sets no deadline.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Read the My Bookings page | Navigate to "My Bookings", collect the booked and waitlisted entries, and raise `NoSuchElementException` when the page has none where bookings are expected. Save the screenshot `step-7.png`. | No | O5 |
| 2 | Compare expected with found | Print `--- VERIFYING ON MY BOOKINGS PAGE ---`, the expected and found counts and `SUCCESS` or the `MISMATCH` with the difference, in singular or plural. | No | O5 |
| 3 | Make the bot date independent | Remove any assumption about the first visible day, a hardcoded date or the list position; test with fake cards for several start weekdays. | No | O5 |
| 4 | Rehearse time travel in a container run | Reset the data through the admin account, advance 3 days, run the bot and save the screenshot `step-8.png`. The admin credentials are the practice site's published ones. | No | O5 |

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
[SA-001]: ../stakeholder-analysis.md
