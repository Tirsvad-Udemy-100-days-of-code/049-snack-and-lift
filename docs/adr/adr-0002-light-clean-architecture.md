# ADR-0002 Light Clean Architecture without a presentation layer

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0002 |
| CrossReference | [BC-001], [SA-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version | [50e8331] |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

S02 wants simple code with the assignment's function names, while the framework's `clean-architecture` skill wants business rules that do not depend on Selenium. The booking rules (which class is a Tuesday 6pm class, what to do for each button state, how to count and compare) can be tested without a browser. Options:

1. One script file with all steps, as in the lecture.
2. Layers `domain` (rules and plain data), `application` (use of the rules through a browser port, `retry`), `infrastructure` (Selenium adapter) and a thin command-line entry point.
3. Full four layers with MVC.

## Decision

Option 2. `domain` and `application` import no Selenium; `infrastructure` holds the Selenium adapter; `cli.py` and `__main__.py` compose them. The assignment's functions `retry`, `login`, `book_class` and `get_my_bookings` are the public names in `application`. There is no MVVM or MVC layer because the program is a command-line bot.

## Consequences

**Positive:**

- The rules and the retry logic are unit tested with fakes, without a browser.
- Selenium is the only runtime dependency and is confined to one package.

**Negative:**

- More files than the lecture's single script, which S02 has to navigate; the README and wiki explain the map.

## Affected Artifacts

- [BC-001] — objective O7 and success criterion 5
- [SA-001] — concerns CN-004 and CN-008

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[50e8331]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/commit/50e8331bd21910a72ae56b74c9ff6a3677a709b3
