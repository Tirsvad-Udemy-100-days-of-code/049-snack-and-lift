# Business Case: Snack and Lift Booking Bot

## Metadata
| Key | Value |
| --- | --- |
| ID | BC-001 |
| CrossReference | [SA-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version: Snack and Lift booking bot (Udemy day 49) | [50e8331] |

---

## Executive Summary

Course participant S01 needs a Python bot that books classes at the fictional gym "Snack and Lift" (a practice site on GitHub Pages) without a human. The bot uses Selenium with its own Chrome profile, logs in, books every Tuesday and Thursday 6pm class in the next seven days, joins the waitlist when a class is full, verifies the result on the "My Bookings" page, copes with a site that fails half of its requests, and prints a clear summary. The result is a small, readable, runnable repository that other Udemy course participants (S02) can compare with their own solutions and that GitHub visitors (S03) can browse for ideas, with the assignment's function names, English, Danish and Bahasa Malaysia wiki pages and a screenshot for every lecture step.

## Methodological and Standards Foundation

- Process: the SQA and QC framework mounted at `framework/` (plan-first gate, review records, one pull request per milestone).
- Quality model: ISO/IEC 25010:2023 characteristics tag every QC criterion.
- Design: Clean Architecture in a light form (booking rules separated from the Selenium adapter), as described by the `clean-architecture` skill; the program is a command-line bot, so it has no MVVM or MVC presentation layer.
- Code: Python 3.13 or newer, Doxygen comments, `pytest` for tests, constants in `constants.py`, project configuration in `pyproject.toml`.

## Problem Statement

The Udemy lecture "Create an Automated Booking System" (100 Days of Code, day 49) asks the participant to build a Selenium bot for the Snack and Lift gym site. Solutions shared in the course Q&A are often single untested scripts without instructions, which makes them hard to run, compare and learn from. This participant also wants to keep the work as a documented, reviewed repository.

## Business Opportunity

A documented and tested solution that runs from a README gives participants a reference to compare their selectors, their retry logic and their code with. The wiki explains what each lecture step teaches, in three languages, so Danish and Malay speaking learners can follow too. The skills (waiting for dynamic content, retrying after network failures, verifying a result) apply to many other web automation tasks.

## Objectives

1. O1: Deliver a bot that starts Chrome with its own persistent profile and opens the gym site (lecture step 1).
2. O2: The bot logs in automatically and confirms the class schedule is shown (step 2).
3. O3: The bot books a Tuesday 6pm class, then checks the button state first: "Booked", "Waitlisted" or "Join Waitlist" (steps 3 and 4).
4. O4: The bot counts what it did and prints a summary, then handles every Tuesday and Thursday 6pm class with a detailed list (steps 5 and 6).
5. O5: The bot verifies the bookings on the "My Bookings" page and reports a match or a mismatch, and works at any date of the site's time travel (steps 7 and 8).
6. O6: The bot survives a 50% network failure rate with a `retry` wrapper, `login()`, `book_class()` and `get_my_bookings()` (step 9).
7. O7: Provide the repository hygiene for S02 and S03: README from the framework template, run and test instructions, `.venv` instructions, Doxygen configuration, repository description and topics.
8. O8: Provide wiki pages in English, Danish and Bahasa Malaysia that explain what each lecture step teaches, each with a screenshot.

## Scope

### In Scope

- Selenium bot for the practice site at the GitHub Pages address of appbrewery/gym, with the assignment's function names (`retry`, `login`, `book_class`, `get_my_bookings`).
- Lecture steps 1 to 9.
- Python project: `src/`, `tests/`, `docs/`, `pyproject.toml`, `constants.py`, `.gitignore`, Doxyfile, README.
- Unit tests with `pytest`; the parsing, decision, counting and retry logic is tested without a browser.
- One screenshot per lecture step, taken from a headless browser in a Docker container and used in the README and the wiki.
- Wiki in en, da and ms, published to the git host.
- Repository description and topics on `git.tirsystem.com`.

### Out of Scope

- Automating anything other than the practice site; real gym sites.
- Creating the student account automatically (the assignment does it manually once).
- A graphical user interface or a web API.
- Distribution as a package on PyPI.
- Running GUI tests on the host desktop (framework rule: container or sandbox only).

## Expected Benefits

### Tangible Benefits

- A runnable bot that prints a booking summary and a verification result.
- A test suite that protects the card parsing, booking decision and retry logic.
- Documentation (README, wiki in three languages) that a newcomer can follow without help.

### Intangible Benefits

- Learning value for S01 and S02: Selenium, explicit waits, XPath ancestors, retry patterns and verification.
- A worked example of the framework's plan, review and pull request flow on a small project.

## Strategic Alignment

The project is a learning exercise inside the 100 Days of Code bootcamp. It supports S01's goal of finishing the course with reviewed, shareable work and the S02 and S03 goal of finding clear, runnable examples.

## Success Criteria

| # | Criterion | Target | Measure |
| --- | --- | --- | --- |
| 1 | Booking rule is correct | Every Tuesday and Thursday 6pm class gets exactly one action, and a day is never decided by list position, in 100% of unit test cases | `pytest` result |
| 2 | Summary is printed | The summary lists new bookings, new waitlist entries, already booked and the total | Output of the run |
| 3 | Verification works | "Expected" equals "Found" on the My Bookings page after a run | Output of the run |
| 4 | The bot survives failures | A container run with the site's 50% failure rate reaches the verification result | Output of the run |
| 5 | Tests pass | 0 failing tests; at least 80% line coverage of the logic modules | `pytest` with coverage |
| 6 | A newcomer can run the project | README setup, run and test commands work on a clean clone | Walk-through on a clean clone by S01 |
| 7 | Documentation is complete | Screenshots for 9 of 9 lecture steps in README and in the 3 wiki languages | Count of images per page |
| 8 | Repository metadata is set | Description and at least 5 topics present | Repository API response |
| 9 | No runtime dependency beyond Selenium | `pyproject.toml` lists Selenium as the only runtime dependency | `pyproject.toml` |

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| The practice site changes its element IDs | The bot fails | Keep all selectors in `constants.py`; document the site version used; fail with a clear message |
| The site keeps its state in the browser profile, so a container run starts from an empty database | The student account is missing in the container | The container run registers the test account through the site's own form with a documented test credential, or reuses a profile volume |
| Time and booking state differ between runs | Flaky tests and screenshots | Unit tests need no browser; browser runs reset the data through the admin page first |
| The token for the git host is exposed | Account misuse | Tokens are read from the personal `.env`; never printed, imported, tested or committed |
| Autonomous mode review is not independent | A defect passes review | Stand-in decisions are marked in each `RC-*` and open to challenge in the final summary by S01 |
| Translations contain errors | Misleading wiki pages | English is authoritative; da and ms follow it page by page and S01 can correct them |

## Assumptions

- S01 is the Product Owner, the developer and the reviewer; in autonomous mode the AI acts as stand-in reviewer and records it.
- The people the project is for (S02, S03) cannot be reached for interviews; their needs come from the assignment text and S01.
- The practice site remains available at its GitHub Pages address during the project, and its admin account is the one named in the assignment.
- Docker is available for the headless browser runs.
- The target repository is the one named by `origin` unless S01 states otherwise (see the Project Plan, Open Issues).
- The idea is validated by the course assignment itself, so no riskiest-assumption test (`RA`) is planned.

## Constraints

- Python 3.13 or newer, a local `.venv`, `pyproject.toml`, `pytest`, constants in `constants.py`.
- Folder structure `src/`, `tests/`, `docs/`.
- No runtime dependency unless it is needed.
- Doxygen comments in source and a Doxyfile.
- The wiki exists in English, Danish and Bahasa Malaysia.
- Each pull request is a branch that tracks one step; the framework cannot be edited from this project.
- The PO language is English, the domain is IT.
- Credentials come from a personal `.env`, which is not part of the project.
- The Business Case sets no deadline; the Project Plan assumes 2026-10-28 to 2026-11-06.

## Cost–Benefit Assessment

The assessment is qualitative: this is an unpaid learning project, and no revenue exists to quantify.

| Costs | Benefits |
| --- | --- |
| Effort of S01 for reviewing the plan and the final summary | A reusable, tested bot and a three language learning wiki |
| AI work and compute for planning, code, screenshots and translation | A repository that S02 and S03 can read and run |
| Maintenance if the practice site changes | Practice of the framework flow on a small scope |

## Stakeholders

| Stakeholder ID (SA) | Interest in this project |
| --- | --- |
| S01 | Product Owner, developer and reviewer; wants a finished, reviewed course assignment |
| S02 | Udemy course participants; want readable, runnable code with the assignment's function names and README instructions |
| S03 | GitHub viewers; want a clear description, topics and README, and no runtime dependencies |

## Recommendation

Proceed: the scope is small, the risks have mitigations, and the narrowest first release meets all objectives.

---

[SA-001]: ./stakeholder-analysis.md
[50e8331]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/commit/50e8331bd21910a72ae56b74c9ff6a3677a709b3
