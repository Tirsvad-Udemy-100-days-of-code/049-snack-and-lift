# Stakeholder Analysis

## Metadata
| Key | Value |
| --- | --- |
| ID | SA-001 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version: S01 to S03 | pending |

---

## Purpose

This analysis names the people the Snack and Lift booking bot project affects, how much power and interest each has, what each needs, and who reviews and accepts the work. It follows the power/interest grid (Manage Closely, Keep Satisfied, Keep Informed, Monitor) and maps each concern to a FURPS+ attribute. The business context is in [BC-001].

## Stakeholder Summary Table

| ID | Name | Role/Title | Organization | Power Level | Interest Level | Quadrant | Primary Concern (Business Language) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | Jens Tirsvad Nielsen | Course participant: Product Owner, developer and reviewer | Tirsvad (personal) | HIGH | HIGH | Manage Closely | Finish the assignment as a reviewed, documented repository |
| S02 | Udemy course participants | Users who share code and compare solutions | Udemy 100 Days of Code community | LOW | HIGH | Keep Informed | Readable, runnable code with the assignment's function names, and README instructions to run it |
| S03 | GitHub viewers | Visitors who browse the repository for ideas | Public | LOW | MEDIUM | Keep Informed | A clear repository description, topics and README, and no runtime dependencies beyond what is needed |

## Power/Interest Classification Rationale

- **Manage Closely (S01):** S01 sets scope, accepts the plan and reviews the result. Every decision outside the accepted plan returns to S01.
- **Keep Informed (S02):** S02 cannot change the project but depends on its clarity. They are informed through the README, the code and the wiki.
- **Keep Informed (S03):** S03 has even less stake: they browse. The description, topics and README are their whole contact with the project.
- No stakeholder is in Keep Satisfied or Monitor.

## Primary Concerns and FURPS+ Mapping

| Concern ID | Stakeholder | Concern | FURPS+ attribute |
| --- | --- | --- | --- |
| CN-001 | S01 | The bot completes the nine lecture steps: login, booking, waitlist, summary, verification | Functionality |
| CN-002 | S01 | Work is planned, reviewed and traceable by branch and pull request | Supportability |
| CN-003 | S01 | The bot survives network failures and any date of the site's time travel | Reliability |
| CN-004 | S02 | Code is readable and uses the assignment's function names | Usability |
| CN-005 | S02 | The README explains how to create a `.venv`, run the bot and run the tests | Usability |
| CN-006 | S02 | The wiki explains what each lecture step teaches, with a screenshot, in English, Danish and Bahasa Malaysia | Usability |
| CN-007 | S03 | The repository has a clear description, topics and README | Usability |
| CN-008 | S03 | No runtime dependency beyond Selenium | Implementation |
| CN-009 | S01 | A token stays outside the repository | Supportability |

## Communication Requirements

| ID | Channel | Frequency | Deliverable | Phase / Milestone |
| --- | --- | --- | --- | --- |
| CM-001 | Chat with S01 | Once per plan, and on every stop condition | Plan acceptance, questions, final summary | All milestones |
| CM-002 | Pull request on the git host | One per milestone | Changes, review records, closed issues | All milestones |
| CM-003 | README and wiki | On each release | Run instructions, lecture step explanations | Documentation milestone |

## Conflicting Interests and Mitigations

| Conflict | Stakeholders | Mitigation |
| --- | --- | --- |
| S01 wants a resilient, well structured bot, while S02 wants code that stays simple and close to the assignment | S01, S02 | Keep the assignment's functions (`retry`, `login`, `book_class`, `get_my_bookings`) as the public API; keep helpers small and documented |
| S01 wants thorough tests and framework artifacts, while S03 wants no extra runtime dependencies | S01, S03 | Test tools are development-only extras in `pyproject.toml`; Selenium is the only runtime dependency |

## Traceability Analysis

### Business Goal Alignment

| Stakeholder | Concern | Business Case objective |
| --- | --- | --- |
| S01 | CN-001 | O1 to O5 in [BC-001] |
| S01 | CN-003 | O5, O6 in [BC-001] |
| S01 | CN-002, CN-009 | O7 in [BC-001] |
| S02 | CN-004, CN-005 | O7 in [BC-001] |
| S02 | CN-006 | O8 in [BC-001] |
| S03 | CN-007, CN-008 | O7 in [BC-001] |

## Sign-Off

| Role | Stakeholder | Status |
| --- | --- | --- |
| Product Owner | S01 | Accepted the plan in chat on 2026-10-28 |
| Reviewer | AI as stand-in for S02 | Go in RC-002, autonomous mode, not independent |

---

[BC-001]: ./business-case.md
