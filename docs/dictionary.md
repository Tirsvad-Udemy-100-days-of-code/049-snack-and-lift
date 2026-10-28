# Domain Dictionary

## Metadata
| Key | Value |
| --- | --- |
| ID | DICT-001 |
| CrossReference | [BC-001], [SA-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version: eight gym and course terms | pending |

---

## Purpose and Scope

Maps each Product Owner (PO) term to its professional IT term. PO language: English (`en`), domain `it`. It covers the gym site and course terms used by the Business Case and the milestones.

## Dictionary

| PO term | Language | IT term | Definition | Used as PO term in | Used as IT term in |
| --- | --- | --- | --- | --- | --- |
| Booking | en | Reservation record | A place in a class held by the student account, shown on the My Bookings page. | BC, SA, MIL | - |
| Bot | en | Automation script | A program that books classes without a human. | BC, SA, MIL | - |
| Class card | en | Schedule entry | One class in the schedule, with its name, time and booking button. | BC, MIL | - |
| Lecture step | en | Assignment step | One of the nine numbered steps of the Udemy challenge. | BC, SA, MIL | - |
| Profile | en | Browser profile | The Chrome user data folder where the practice site keeps its data between runs. | BC, MIL | - |
| Retry | en | Retry wrapper | A function that repeats an action that failed because of a network error. | BC, SA, MIL | - |
| Time travel | en | Simulated clock | The admin control that moves the practice site's date forward. | BC, MIL | - |
| Waitlist | en | Waiting queue | The list a student joins when a class is full. | BC, SA, MIL | - |

## Rules

- The Domain Model, use cases and user stories use the PO term; the Operation
  Contract, Sequence Diagram, Design Class Diagram and ERD use the IT term.
- One IT term per PO term and one PO term per IT term; no synonyms.
- Rows are in ascending order of the PO term (case-insensitive, by the
  alphabet of the PO language), so a term is found without searching.

---

[BC-001]: ./business-case.md
[SA-001]: ./stakeholder-analysis.md
