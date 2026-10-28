# MIL-004 Lecture steps 3 and 4: book a class and check its state

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-004 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version | [50e8331] |

---

## Purpose

Decide whether the bot finds the next Tuesday 6pm class by reading the day and time from the page, and acts on the state of its button, which completes lecture steps 3 and 4.

## Deliverable

Class card parsing (day through the parent group, time from the card), the booking decision for the states "Book Class", "Booked", "Waitlisted" and "Join Waitlist", the console messages, unit tests with a fake driver, and screenshots for lecture steps 3 and 4.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | Unit tests cover the four button states and the day and time parsing | 0 failures; each state has a test | A test fails or a state is untested |
| 2 | A container run books or recognises the Tuesday 6pm class and prints the matching message | The message names the class and the date | No message or the wrong class |
| 3 | `docs/images/step-3.png` and `docs/images/step-4.png` exist | Both files exist and show the schedule | A file is missing |
| 4 | The code review against `qc-programming-python.md` is `Go` | `RC-*` is `Go` | `No-Go` |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-003 | Needs the login |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O3, success criterion 1 | [BC-001] |
| CN-001, CN-004 | [SA-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S02 (AI as stand-in, autonomous mode, not independent) |

## Target Date

2026-10-31 — inside the planned window 2026-10-28 to 2026-11-06 of [PP-001]; the Business Case sets no deadline.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Parse class cards | Select the cards with an id-prefix CSS selector and walk to the day group with `ancestor::div`; return plain values (day, time, name, state) so the rules can be tested without a browser. | No | O3 |
| 2 | Book the next Tuesday 6pm class | Find the first Tuesday 6pm card and click "Book Class" or "Join Waitlist"; print `✓ Booked: Spin Class on Tue, Aug 12`. Save the screenshot `step-3.png`. | No | O3 |
| 3 | Check the state before clicking | Decide from the button text: "Booked" and "Waitlisted" only report, "Join Waitlist" joins the waitlist, "Book Class" books. Print the three assignment messages. Save the screenshot `step-4.png`. | No | O3 |
| 4 | Test the decision logic | Write unit tests for parsing and the decision with fake cards, including a day that is not first in the list. | No | O3 |

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
[SA-001]: ../stakeholder-analysis.md
[50e8331]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/commit/50e8331bd21910a72ae56b74c9ff6a3677a709b3
