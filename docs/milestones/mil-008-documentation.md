# MIL-008 Documentation, wiki and release

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-008 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version | [50e8331] |

---

## Purpose

Decide whether the repository is ready for S02 and S03: README, Doxygen output, wiki in three languages with screenshots, and final checks.

## Deliverable

Final README with a screenshot per lecture step, Doxygen configuration that builds, wiki pages in English, Danish and Bahasa Malaysia that explain what each lecture step gained, and the final summary.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | README has the 9 screenshots, setup, run and test instructions | All present; `check-readme.sh` exits 0 | Anything missing |
| 2 | The wiki has the same page set in `en`, `da` and `ms`, each step page with its screenshot | Three languages, same pages | A page or a language is missing |
| 3 | `bash framework/scripts/check-languages.sh` and `check-plan.sh` report no finding | Exit code 0 | Exit code 1 |
| 4 | Tests pass with at least 80% coverage of the logic modules and `doxygen Doxyfile` has no warnings | Both true | Either false |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-007 | Needs all nine lecture steps and screenshots |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O7, O8, success criteria 6, 7 | [BC-001] |
| CN-005, CN-006, CN-007 | [SA-001] |

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
| 1 | Finish the README | Add the nine screenshots, the project layout, the Doxygen instructions and the links to the wiki to `README.md`; run `check-readme.sh`. | No | O7 |
| 2 | Write the English wiki | Write `docs/wiki/` pages in English: Home, Getting Started, one page per lecture step (what the step gained, with its screenshot), Troubleshooting and the sidebar and footer. | No | O8 |
| 3 | Translate the wiki to Danish | Write the same page set in Danish as `<Page>-da.md`, following the English text page by page. | No | O8 |
| 4 | Translate the wiki to Bahasa Malaysia | Write the same page set in Bahasa Malaysia as `<Page>-ms.md`, following the English text page by page. | No | O8 |
| 5 | Install the wiki publishing workflow | Copy `templates/ci/publish-wiki.yml` and `templates/ci/sync-milestones.yml` to `.gitea/workflows/` so the wiki and milestones reach the git host after the merge. | No | O8 |
| 6 | Final checks and summary | Run every framework check script, the full test suite and Doxygen, verify the issues are closed, and prepare the final summary for S01. | No |  |

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
[SA-001]: ../stakeholder-analysis.md
[50e8331]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/commit/50e8331bd21910a72ae56b74c9ff6a3677a709b3
