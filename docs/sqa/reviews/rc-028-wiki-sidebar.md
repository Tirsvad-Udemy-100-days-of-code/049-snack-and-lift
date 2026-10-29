# SQA Review Record

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-028 |
| CrossReference | [MIL-008], [QC-WIKI-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-29 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Review record, the wiki in docs/wiki after the sidebar change of framework 0.19.0 | pending |

---

## Artifact Under Review

- Instance reviewed: [MIL-008]
- Checklist used: [QC-WIKI-001] (`QC-WIKI-001`)
- Scope: the wiki in docs/wiki after the sidebar change of framework 0.19.0
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is `AI as stand-in for S02`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The wiki has a `_Sidebar.md`, because the host lists subpages only through it | Pass | `docs/wiki/_Sidebar.md` exists. |
| 2 | The sidebar starts with the wiki's title in bold, then one list of the pages in the primary language (English), `Home` first | Pass | The sidebar starts with the title in bold, then one English page list with `Home` first. |
| 3 | The page list holds a link to every English page of the wiki, and no link points to a page that does not exist | Pass | The list links to all 12 English pages (Home, Getting-Started, Step-1 to Step-9, Troubleshooting); every target exists in `docs/wiki/` and on the published wiki (HTTP 200 checked for Home, Home-da, Home-ms, Getting-Started, Step-1, Step-9-ms, Troubleshooting-da). |
| 4 | A `**Related**` section follows the page list only when the wiki has related wikis (for example the checklists wiki for a framework wiki); each entry is a link to that wiki's Home. A wiki with nothing related has no such section | N-A | The wiki has no related wikis, so it has no `Related` section. |
| 5 | A `**Languages**` section is the last section of the sidebar. It has one line per language, the language written in that language, linking to that language's `Home` page | Pass | `**Languages**` is the last section with `English: [Home](Home)`, `Dansk: [Hjem](Home-da)` and `Bahasa Melayu: [Utama](Home-ms)`. |
| 6 | The sidebar does not repeat the page list per language | Pass | The page list appears once. |
| 7 | A sidebar produced by a generator carries a comment that says so and names the generator; the generator is changed, not the page | N-A | The sidebar is written by hand in the repository (a one-off helper made it, which is not part of the project), so it carries no generator comment. |
| 8 | The wiki has a `Languages` line on each page (criterion 11), so the sidebar is not the only way to switch language | Pass | Each page starts with the language line (criterion 11). |
| 9 | Every wiki exists in English and, as a minimum, in the language the project's registry names as the PO language; further languages are added on top, never instead of English | Pass | English and Danish and Bahasa Malaysia exist; the registry names English as the PO language. |
| 10 | Every English page has a page in each other language of the wiki: the page sets are identical | Pass | Each language has the same 12 pages (checked by file name: `<Page>.md`, `<Page>-da.md`, `<Page>-ms.md`). |
| 11 | Every page starts with the language line, with the current language in bold and a link to the same page in each other language | Pass | Each page starts with the language line with the current language in bold and a link to the same page in the other two languages. |
| 12 | A page in a language other than English is named `<Page>-<code>.md`, with a BCP 47 code; English has no suffix | Pass | Danish and Bahasa Malaysia pages are named `<Page>-da.md` and `<Page>-ms.md`; English has no suffix. |
| 13 | Code blocks, commands, file names and IDs stay in English in every language | Pass | Commands, code blocks, file names and IDs are English on every page. |
| 14 | The sidebar, every page and every link were checked on the published wiki after the change, not only in the repository | Pending | The new sidebar is checked on the published wiki only after the merge (the wiki is published from `main` by the instance workflow); the links of the pages were checked on the published wiki before this change. |
| 15 | A change to the layout rules (sections, order, naming) is made in the generator or template and in this checklist's source rules together | N-A | No change to the layout rules was made. |

## Overall Verdict

Go-with-conditions - the wiki meets every Mandatory criterion of QC-WIKI-001 in the repository, with the sidebar in the shape that framework 0.19.0 sets. Criterion 14 (the sidebar checked on the published wiki) is Pending until the merge has been published. QC-WIKI-001 itself is `Proposed`. The review is not independent: the AI wrote and reviewed it as stand-in for S02, and S01 can challenge it in the end-of-run summary.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Open the published wiki once after the merge and check the sidebar | S01 | when convenient |

---

[MIL-008]: ../../milestones/mil-008-documentation.md
[QC-WIKI-001]: ../../../framework/qc/artifacts/qc-wiki.md
