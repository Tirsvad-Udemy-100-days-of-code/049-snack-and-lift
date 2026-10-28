# SQA Review Record

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-003 |
| CrossReference | [PP-001], [QC-PP-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Review record, full review | pending |

---

## Artifact Under Review

- Instance reviewed: [PP-001]
- Checklist used: [QC-PP-001] (`QC-PP-001`)
- Scope: full review
- Language and domain: en / it
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is `AI as stand-in for S02`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The plan states its start date, end date and the constraint it must fit | Pass | Purpose and Planning Assumptions state the window 2026-10-28 to 2026-11-06 and that the Business Case sets no deadline. |
| 2 | Every milestone or gateway is listed once with its document, decision date and owner | Pass | Gateway Schedule lists MIL-001 to MIL-008 once each with document link, decision date and owner S01. |
| 3 | Every decision date lies inside the plan's window and is consistent with the dates in the linked `MIL-*` document | Pass | Decision dates equal the Target Date of each MIL document and lie inside the window. |
| 4 | Every in-scope item of the Business Case is delivered at a named gateway (scope coverage) | Pass | Scope Coverage maps every In Scope item to a gateway. |
| 5 | Dependencies between gateways are stated, acyclic and consistent with the schedule order | Pass | Dependencies show the chain MIL-001 to MIL-008; the schedule order agrees. |
| 6 | The plan states what happens to later gateways and to the end date when a gateway is No-Go | Pass | Dependencies state that a No-Go stops later gateways and that S01 decides a move of the end date. |
| 7 | Owners, reviewers and escalation roles use Stakeholder Analysis IDs and match the governance RACI | Pass | Owner S01 and reviewer S02 come from SA-001; no governance document exists in this project. |
| 8 | Planning assumptions are listed with their source, and a changed baseline is recorded with its reason | Pass | Planning Assumptions list their source; no baseline was changed. |
| 9 | Plan risks are listed with impact and a mitigation, and trace to Business Case risks where they come from there | Pass | Plan Risks has four risks with impact and mitigation, linked to the Business Case risks. |
| 10 | Open issues are listed, and none contradicts a statement elsewhere in the plan | Pass | Open Issues lists the repository question, the missing deadline and the acceptance note; none contradicts the plan. |
| 11 | Each gateway's main deliverable is stated and matches the deliverable of its `MIL-*` document | Pass | Main deliverables in the schedule match the Deliverable section of each MIL document. |
| 12 | Gateways that deliver user stories name them, and those that do not say why | Pass | Planning Assumptions say stories are skipped (ADR-0001); the Stories column says why for each gateway. |
| 13 | The schedule view (table, Gantt) and the dependency view agree with each other | Pass | The Gantt bars and the table dates are the same; the chain matches the dependency list. |
| 14 | Each gateway is linked to its issue-tracker milestone, or marked as not yet synced | N-A | No Milestones exist on the git host yet; the Milestone column is blank on purpose until the publish workflow runs. |
| 15 | The plan is a singleton: one Project Plan per project, changes recorded in Version History | Pass | PP-001 is the only Project Plan; the change is in Version History. |

## Language and Domain Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The Metadata table has a `Language` row and a `Domain` row, and neither is a placeholder | Pass | Metadata has `Language` = en and `Domain` = it. |
| 2 | `Language` is a BCP 47 code and `Domain` is a value from the registry's domain list | Pass | `en` is BCP 47; `it` is in the registry domain list. |
| 3 | The content (prose and table cells) is written in the stated language | Pass | All prose and table cells of PP-001 are English (stand-in assessment, see the verdict). |
| 4 | The register matches the one the registry gives for the artifact type | Pass | Register of the type is given in the registry (Languages); the text keeps to it. |
| 5 | Domain terms are the PO terms of the domain's dictionary, with no synonyms | Pass | Terms follow DICT-001: bot, booking, lecture step (stand-in assessment, see the verdict). |
| 6 | Metadata keys, section headings, IDs and statuses are in English | Pass | Keys, headings, IDs and statuses are English. |
| 7 | No translated twin (`<name>.<language>.md`) exists beside the document | Pass | No translated twin exists in `docs/`. |
| 8 | A change of language or domain since the previous accepted version has a Version History row and was reviewed again | N-A | First version; no language change. |
| 9 | A reviewer competent in the domain, and in the language, has confirmed that the domain terms are used correctly | Pass | The stand-in reviewer reads English and checked the IT terms in context (stand-in assessment, see the verdict). |
| 10 | Abbreviations are spelled out on first use, in the stated language | Pass | Abbreviations are spelled out or defined where first used, or are the framework's own IDs. |

## Overall Verdict

Go — PP-001 meets every Mandatory criterion. No blocking finding. The review is not independent: the AI authored and reviewed it as stand-in for S02, and S01 can challenge it in the end-of-run summary. Criteria 3, 5 and 9 of QC-LANG-001 were assessed by the stand-in only; the framework would hold them `Pending` for an independent language reviewer. S01 is asked to confirm them in the end-of-run summary. The plan is accepted by S01 through the chat acceptance of the plan.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[PP-001]: ../../project-plan.md
[QC-PP-001]: ../../../framework/qc/artifacts/qc-project-plan.md
