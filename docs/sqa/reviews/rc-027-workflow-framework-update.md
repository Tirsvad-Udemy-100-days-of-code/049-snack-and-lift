# SQA Review Record

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-027 |
| CrossReference | [MIL-008], [QC-WF-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-29 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Review record, the workflow sync-milestones.yml after the framework update to 0.18.0 and the removal of publish-wiki.yml | [2cfcd02] |

---

## Artifact Under Review

- Instance reviewed: [MIL-008]
- Checklist used: [QC-WF-001] (`QC-WF-001`)
- Scope: the workflow sync-milestones.yml after the framework update to 0.18.0 and the removal of publish-wiki.yml
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is `AI as stand-in for S02`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The file meets the YAML checklist ([QC-YML-001]) | Pending | `yamllint` is not installed on the stand-in's machine, so the YAML checklist QC-YML-001 was not run; the files parse (actionlint reads them) and use 2-space indentation. |
| 2 | The file is in `.gitea/workflows/` or `.github/workflows/` with the extension `.yml` or `.yaml`, and the same workflow does not exist in both directories | Pass | `sync-milestones.yml` is in `.gitea/workflows/` with the extension `.yml` and not in `.github/workflows/`. `publish-wiki.yml` was removed (see the verdict). |
| 3 | The file declares `name`, `on` and `jobs`; `on` lists explicit events and, where it matters, `branches` or `paths` | Pass | The file declares `name`, `on` and `jobs`; `on` lists `push` on `main` with `paths`, and `workflow_dispatch`. |
| 4 | A header comment states the purpose, the triggers, the inputs, the secrets it needs, what it changes outside the repository, and the decision or milestone it implements | Pass | The header states the purpose, triggers, secrets, what changes outside the repository and the installation steps (from the framework template); the decision is MIL-008 task 5. The added step has its own comment. |
| 5 | Every job and step has a descriptive `name`, unique within its job | Pass | Every step has a descriptive name. |
| 6 | The file passes `actionlint` (or the project's workflow validation test) and the tool version is stated | Pass | `actionlint` 1.7.12 reports no finding (exit code 0). |
| 7 | Every job declares `permissions` explicitly with the least access that works (`contents: read` or none by default); write access only on the job that needs it | Pass | The job sets `contents: read`. |
| 8 | Every action used is pinned to a full commit SHA or an exact release tag, never to a branch; a moving major tag (`@v1`) is accepted only for an action published by the same organisation under a stated release policy | Pass | `actions/checkout@v4.2.2` is an exact release tag. |
| 9 | No secret is written in the file; a secret is read as `secrets.NAME`, passed to a step through `env:`, never placed on a command line or echoed | Pass | The file reads `secrets.TOKEN_FOR_GITEA_ISSUES` only; no secret value is in the repository. The token reaches git through `GIT_CONFIG_*` environment variables, never a command line. |
| 10 | Untrusted text (`inputs.*`, event fields such as a title, branch name or label, step outputs derived from them) is never interpolated into a `run:` script; it is passed through `env:` and used as a quoted variable | Pass | No `run:` block interpolates `inputs.*` or event text; `DRY_RUN` is passed through `env:`. |
| 11 | A trigger that gives a run secrets or a write token on code from a fork or an untrusted branch (`pull_request_target`, `workflow_run`) does not check out or execute that code | Pass | The workflow does not use `pull_request_target` or `workflow_run`. |
| 12 | A workflow that changes state outside the repository (release, tag, publish, sync, deploy) is started by hand or by a protected branch, and a manual run defaults to a dry run with an explicit input to apply | Pass | It runs on a push to `main` or by hand; the manual run defaults to a dry run. |
| 13 | The token the workflow uses has only the scope the job needs, and where the host's built-in token is enough it is used instead of a personal token | Pending | The scope of the token is set by S01; the dry run on 2026-10-28 got HTTP 403 on the framework repository, so the token lacks read access to it. |
| 14 | Every job sets `runs-on` to an explicit label and `timeout-minutes` | Pass | The job sets `runs-on: ubuntu-latest` and `timeout-minutes: 15`. |
| 15 | `concurrency` is set where two runs would conflict: a check cancels the older run (`cancel-in-progress: true`); a publishing job queues (`cancel-in-progress: false`) | Pass | `concurrency` is set with `cancel-in-progress: false`. |
| 16 | Triggers are filtered (`branches`, `paths`, `types`) so the workflow runs only for the changes it concerns | Pass | The triggers are filtered by `branches: [main]` and `paths`. |
| 17 | Tools and dependencies are installed at pinned versions; a version is a workflow input with a default or a value in one place | Pass | The workflow installs nothing itself; `curl` and `jq` are checked by the framework script. |
| 18 | A dependency cache is used where the install is slow enough to matter | N-A | No dependency is installed that a cache would speed up. |
| 19 | A failing step names the tool, the file and the reason in its log (annotation or `::error::` line) | Pending | Not verified: the log messages come from the framework script and the reusable workflow, which the stand-in did not run. |
| 20 | A `run:` block is within the limit on embedded program text of criterion 7 of [QC-YML-001]; a longer script is a file (`tools/`, or a shared repository fetched at a pinned ref) that the step calls with one command, and the workflow passes its settings through `env:` | Pass | Each `run:` block is one command; the logic is in `framework/scripts/ci-publish-milestones.sh`. |
| 21 | Logic used by more than one workflow or repository is a reusable workflow (`workflow_call`) or a composite action; each input has a `description`, a `type` and a `default` where one is sensible | Pass | The workflow calls one framework script; the input of `workflow_dispatch` has a description, type and default. |
| 22 | Every workflow feature used is verified on the instance that runs it, and the host and version are recorded; a feature the target hosts differ on is noted in the header | Pending | A dry run on the instance (2026-10-28, run 3034, branch `fix-sync-milestones-submodule`) passed the HTTPS rewrite and then failed with 403 on the framework repository, so the feature is not yet verified end to end. |
| 23 | A reusable workflow states, in its header, how a caller pins it and the script it fetches, so the workflow and its script are the same release | N-A | The file is not a reusable workflow. |
| 24 | A static test of the repository's workflows exists and runs on every pull request: valid YAML, required keys, explicit permissions and runner, no inline script above the limit | N-A | No static test of the workflows exists in this project; the checks are `actionlint` on request. |

## Overall Verdict

Go-with-conditions - the milestone workflow is the framework template (0.18.0) plus one step that fetches the framework submodule over HTTPS, and it passes `actionlint`. `publish-wiki.yml` is removed because the framework retired the caller: the instance publishes `docs/wiki/` with its own scoped workflow (RC-022 reviewed the old caller). Mandatory criteria 1 (`yamllint` was not run) and 22 (feature checked on the instance) are Pending: the token lacks read access to the framework repository. The review is not independent: the AI wrote and reviewed it as stand-in for S02, and S01 can challenge it in the end-of-run summary.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Give the token `TOKEN_FOR_GITEA_ISSUES` read access to the repository TirSystem/SQA-QC-Framework, create the secret in the organization and run the workflow once by hand with dry_run on | S01 | before the next merge to main |
| Run `yamllint` on `.gitea/workflows/` | S01 | when convenient |

---

[MIL-008]: ../../milestones/mil-008-documentation.md
[QC-WF-001]: ../../../framework/qc/code/qc-workflow.md
[2cfcd02]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/commit/2cfcd0258897aeb90cea48baf59a8af258df19dd
