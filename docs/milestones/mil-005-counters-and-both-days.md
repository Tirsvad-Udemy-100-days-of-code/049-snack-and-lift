# MIL-005 Lecture steps 5 and 6: counters and every Tuesday and Thursday class

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-005 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version | pending |

---

## Purpose

Decide whether the bot counts what it does, prints the summary and the detailed list, and handles every Tuesday and Thursday 6pm class, which completes lecture steps 5 and 6.

## Deliverable

Counters and a summary, a detailed class list, booking of all Tuesday and Thursday 6pm classes, unit tests, and screenshots for lecture steps 5 and 6.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | Unit tests for the counters, summary text and detailed list pass | 0 failures | A test fails |
| 2 | A container run processes every Tuesday and Thursday 6pm card in the window once | Total equals the cards found | A card is skipped or repeated |
| 3 | `docs/images/step-5.png` and `docs/images/step-6.png` exist | Both files exist and show the console summary or schedule | A file is missing |
| 4 | The code review against `qc-programming-python.md` is `Go` | `RC-*` is `Go` | `No-Go` |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-004 | Needs the booking decision |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O4, success criteria 1, 2 | [BC-001] |
| CN-001 | [SA-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S02 (AI as stand-in, autonomous mode, not independent) |

## Target Date

2026-11-01 — inside the planned window 2026-10-28 to 2026-11-06 of [PP-001]; the Business Case sets no deadline.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Add counters and the summary | Count new bookings, waitlists joined and classes already booked or waitlisted; print `--- BOOKING SUMMARY ---` with the total of Tuesday 6pm classes. Save the screenshot `step-5.png`. | No | O4 |
| 2 | Handle Tuesday and Thursday | Process every Tuesday and Thursday 6pm card, not only the first; keep a list of what happened for each card, with `Tomorrow` and date labels as the site shows them. | No | O4 |
| 3 | Print the detailed class list | Print `--- DETAILED CLASS LIST ---` with one line per class: `[New Booking]`, `[New Waitlist]`, `[Already Booked]` or `[Already Waitlisted]`. Save the screenshot `step-6.png`. | No | O4 |
| 4 | Test counting and reporting | Unit tests for the counters, the summary and the detail lines, including the case of no matching class. | No | O4 |

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
[SA-001]: ../stakeholder-analysis.md
