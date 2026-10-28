# ADR-0001 Skip user stories and use cases

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0001 |
| CrossReference | [BC-001], [PP-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version | pending |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

The journey of the `create-project` skill offers user stories, use cases and their design artifacts (domain model, system sequence diagrams, operation contracts, design class diagrams, ERD). The bot has one actor (S01 running the script), one linear flow (log in, book, verify) and no persistent data of its own. Options:

1. Write user stories and use cases for the nine lecture steps.
2. Skip them and plan the work as technical tasks that cite the Business Case objectives.

## Decision

Option 2. The milestones list technical tasks with the Business Case objective as reference ("Needs its own Use Case/User Story?" is `No`). The lecture steps are the unit of planning.

## Consequences

**Positive:**

- Less documentation than code for a very small program.
- Each task still traces to an objective (O1 to O8).

**Negative:**

- No use case documents or design diagrams exist; the code reviews cannot trace classes to a Design Class Diagram and record that criterion as not applicable with this ADR as reason.

## Affected Artifacts

- [BC-001] — objectives the tasks trace to
- [PP-001] — gateways list no stories

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
