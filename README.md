# 🏋️ Snack and Lift Booking Bot

A Selenium bot that books classes at the fictional gym "Snack and Lift" for you: it logs in, books every Tuesday and Thursday 6pm class, joins the waitlist when a class is full, verifies the result on the "My Bookings" page and survives a site that fails half of its requests. It is the solution to day 49 of Udemy's *100 Days of Code: The Complete Python Pro Bootcamp*, written for course participants who want to compare solutions and for visitors who browse for ideas.

## 📚 Table of Contents

- [Overview](#-overview)
- [Requirements](#-requirements)
- [Setup](#-setup)
- [Run](#-run)
- [Lecture steps and screenshots](#-lecture-steps-and-screenshots)
- [Tests](#-tests)
- [License](#-license)
- [Links](#-links)
- [Appendix: Project documents](#-appendix-project-documents)

## 🧭 Overview

The bot follows the nine steps of the lecture on the practice site [Snack and Lift][gym]:

1. Setup, Chrome profile and basic navigation.
2. Automated login.
3. Book the upcoming Tuesday class.
4. Check if a class is already booked.
5. Add counters and a summary.
6. Book every Tuesday and Thursday class.
7. Verify the classes on the "My Bookings" page.
8. Time travel quality assurance.
9. Add resilience against network failures (`retry`, `login`, `book_class`, `get_my_bookings`).

The repository is organised like this:

| Folder or file | What it is for |
| --- | --- |
| `src/snack_and_lift/` | The bot. `domain/` holds the rules with no Selenium, `application/` holds `retry`, `login`, `book_class` and `get_my_bookings`, `infrastructure/` drives the browser, `constants.py` holds every constant |
| `tests/` | `pytest` tests; the unit tests need no browser |
| `docs/` | Project documents, wiki pages (English, Danish, Bahasa Malaysia) and the screenshots of the lecture steps |
| `Dockerfile` | A Linux image with headless Chromium for real-browser runs and screenshots |
| `Doxyfile` | Doxygen configuration for the source comments |

## 📋 Requirements

- Python 3.13 or newer.
- Selenium (the only runtime dependency; it is installed by `pip` and finds the browser driver itself).
- Google Chrome or Chromium to run the bot on your own machine.
- `pytest` and `pytest-cov` for the tests (development extra only).
- Docker, only if you want to run the bot or take screenshots without opening a window on your desktop.
- Doxygen, only to build the source documentation.

## 🛠️ Setup

Create a local virtual environment, upgrade `pip` and install the project with the test tools:

```bash
python -m venv .venv
```

Activate it:

```bash
# Linux and macOS
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Leave the environment with `deactivate`. The folder `.venv` is ignored by git.

## ▶️ Run

### Your gym account

The bot never contains a password. Register your own account once, by hand, as the lecture does: run the bot with `--keep-open` so Chrome stays open (the `chrome_profile` folder keeps the site's data between runs), click "Join Today... Or Tomorrow" and register with an e-mail such as `yourname@test.com` and a password you remember (not a trivial one such as `12346`, Chrome warns about those). Then give the bot the account through two environment variables:

```bash
# Linux and macOS
export SNACK_AND_LIFT_EMAIL="yourname@test.com"
export SNACK_AND_LIFT_PASSWORD="your password"
```

```powershell
# Windows PowerShell
$env:SNACK_AND_LIFT_EMAIL = "yourname@test.com"
$env:SNACK_AND_LIFT_PASSWORD = "your password"
```

### Start the bot

With the environment active:

```bash
snack-and-lift
```

or, without installing the command:

```bash
python -m snack_and_lift
```

To keep your desktop free, run it in the Docker container (headless Chromium):

```bash
docker build -t snack-and-lift .
docker run --rm snack-and-lift
```

## 📸 Lecture steps and screenshots

Each step has a wiki page that explains what it teaches, in [English](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/wiki/Home), [Dansk](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/wiki/Home-da) and [Bahasa Melayu](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/wiki/Home-ms). Only the screenshot of step 1 is in the repository yet: the others need a run with a real gym account, which the maintainer makes with `--screenshot-dir` (see [Getting started](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/wiki/Getting-Started)). Until then their images do not show.

| Step | Wiki page | Screenshot |
| --- | --- | --- |
| 1 | [Setup and navigation](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/wiki/Step-1) | ![Step 1](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-1.png) |
| 2 | [Automated login](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/wiki/Step-2) | ![Step 2](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-2.png) |
| 3 | [Book the next Tuesday class](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/wiki/Step-3) | ![Step 3](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-3.png) |
| 4 | [Check if a class is booked](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/wiki/Step-4) | ![Step 4](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-4.png) |
| 5 | [Counters and summary](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/wiki/Step-5) | ![Step 5](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-5.png) |
| 6 | [Every Tuesday and Thursday class](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/wiki/Step-6) | ![Step 6](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-6.png) |
| 7 | [Verify on My Bookings](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/wiki/Step-7) | ![Step 7](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-7.png) |
| 8 | [Time travel QA](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/wiki/Step-8) | ![Step 8](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-8.png) |
| 9 | [Resilience (retry)](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/wiki/Step-9) | ![Step 9](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-9.png) |

## 🧪 Tests

```bash
python -m pytest
```

Coverage of the logic modules is checked with `python -m pytest --cov`. Tests that need a real browser are marked `browser` and run in the Docker container; all other tests need neither a browser nor the network.

Build the source documentation with Doxygen:

```bash
doxygen Doxyfile
```

## 📄 License

GNU Affero General Public License v3.0, see [LICENSE][license].

## 🔗 Links

- [Repository][repository]
- [Documentation][documentation]
- [Issue tracker][issues]

## 📎 Appendix: Project documents

The documents a newcomer needs, in reading order.

| Document | What it tells you |
| --- | --- |
| [AGENTS.md][agents] | The rules AI agents follow in this repository |
| [Business Case][BC-001] | Why the project exists, its scope and success criteria |
| [Stakeholder Analysis][SA-001] | Who is involved; the stakeholder IDs used for owners and reviewers |
| [Project Plan][PP-001] | The gateways and their schedule |
| [Milestones][milestones] | One document per gateway: Go/No-Go criteria and tasks |
| [Artifact registry][registry] | Where each artifact type lives, the next version, the PO language and domain |
| [Domain dictionary][DICT-001] | The PO terms and the IT terms |
| [Traceability matrix][TM-001] | How the artifacts link and when each was last reviewed |
| [Framework README][framework-readme] | The framework this project uses |
| [Framework changelog][framework-changelog] | What changed in each framework release |

---

[gym]: https://appbrewery.github.io/gym/
[license]: ./LICENSE
[repository]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift
[documentation]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/wiki
[issues]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/issues
[agents]: ./AGENTS.md
[BC-001]: ./docs/business-case.md
[SA-001]: ./docs/stakeholder-analysis.md
[PP-001]: ./docs/project-plan.md
[milestones]: ./docs/milestones/
[registry]: ./docs/artifact-registry.md
[DICT-001]: ./docs/dictionary.md
[TM-001]: ./docs/sqa/traceability-matrix.md
[framework-readme]: ./framework/README.md
[framework-changelog]: ./framework/CHANGELOG.md
