# ADR-0003 Browser runs and screenshots in a Docker container

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0003 |
| CrossReference | [BC-001], [MIL-002], [MIL-003] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version | pending |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

The bot drives a real browser and every lecture step needs a screenshot. The framework forbids testing a GUI on the host desktop because it takes the user's mouse and keyboard (`framework/process/gui-testing.md`). Options:

1. Run Chrome on the host desktop.
2. Run headless Chromium in a Docker container (Linux).
3. Run in Windows Sandbox.

## Decision

Option 2. A Dockerfile builds an image with Python, Chromium and its driver; the bot takes a headless option, so the same code runs on the host for users who want it. The practice site keeps its data in the browser profile, so a container run keeps the `chrome_profile` folder in a Docker volume.

## Consequences

**Positive:**

- No interference with the user's desktop; reproducible runs for S02.
- Screenshots are made the same way each time.

**Negative:**

- Docker is needed for the real-browser runs and screenshots (unit tests need no Docker).
- The image download is large.

## Affected Artifacts

- [BC-001] — risk of non-reproducible runs
- [MIL-002] — builds the image
- [MIL-003] — first container run

---

[BC-001]: ../business-case.md
[MIL-002]: ../milestones/mil-002-scaffold.md
[MIL-003]: ../milestones/mil-003-login.md
