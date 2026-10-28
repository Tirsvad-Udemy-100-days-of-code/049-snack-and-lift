# MIL-009 Verification fix: only compare the bookings of the run

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-009 |
| CrossReference | [BC-001], [MIL-006] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version, added after a real run (issue #50) | [3b9e381] |

---

## Purpose

Decide whether the My Bookings check ignores bookings that lie outside the window the bot worked on, so that a real account with bookings from earlier runs ends in SUCCESS, and whether the report never prints a negative count.

## Deliverable

A corrected comparison in `domain/verification.py` and its use in `application/verification.py`, unit tests and an end-to-end fixture with extra future bookings, new screenshots for lecture steps 7 to 9 from a real run, and updated README and wiki notes.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | Unit tests show that entries outside the window of the run are listed as a note and do not cause MISMATCH | 0 failures; a test uses entries after the last handled class | A test fails or is missing |
| 2 | Unit tests show that the missing count is never negative and that a class the bot booked but the page lacks is still a MISMATCH | 0 failures | A test fails or is missing |
| 3 | Unit and container tests of the existing steps still pass with at least 80% coverage of the logic modules | Both true | Either false |
| 4 | The code review against `qc-programming-python.md` is `Go` | `RC-*` is `Go` | `No-Go` |
| 5 | `docs/images/step-8.png` from a real run shows SUCCESS | S01 reran the bot with their own account and the image is committed | The image shows MISMATCH or is not replaced |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-006 | Changes the verification that MIL-006 built |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O5, success criterion 3 | [BC-001] |
| CN-001, CN-003 | [SA-001] |

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
| 1 | Limit the comparison to the window of the run | In `build_verification` count only page entries dated from the first to the last class the bot handled; list the other entries as "also booked, not checked". The missing count never goes below zero. | No | O5 |
| 2 | Test the corrected comparison | Unit tests for entries outside the window, a booked class that is missing on the page, and the count; an end-to-end fixture with extra future bookings. | No | O5 |
| 3 | Refresh the step 7 to 9 screenshots and the notes | S01 reruns the bot with their own account and `--screenshot-dir`; the AI commits the images and removes the MISMATCH note from the README and the step 8 wiki pages in three languages. | No | O5, O8 |

---

[BC-001]: ../business-case.md
[MIL-006]: ./mil-006-verify-and-time-travel.md
[PP-001]: ../project-plan.md
[SA-001]: ../stakeholder-analysis.md
[3b9e381]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/commit/3b9e381cd42c56cc4543869c5b80c8e0014b4948
