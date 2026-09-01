# ccopyright-register

> Prepare reviewable ordinary China software copyright registration materials from a code repository.

[简体中文](README.md) · [Start using it](#start-using-it) · [Prerequisites](#prerequisites) · [Outputs](#outputs)

Use this skill when you want an AI coding agent to inspect a software repository, organize applicant-confirmed registration facts, and prepare the application worksheet plus program/document identification materials.

It supports preparation before manual submission to the [China Copyright Protection Center](https://www.ccopyright.com.cn/). It does not fill or submit the portal, operate an applicant account, track an application, or parse correction notices.

The repository also provides the read-only `ccopyright-qa` Skill. Start there
when you are still learning the rules, deciding whether assistance is needed,
or breaking down a service quote. This guide covers material preparation only.

~~~bash
npx skills add OtterPaw-Studio/ccopyright-skill --skill ccopyright-register
~~~

Install Q&A and preparation together:

~~~bash
npx skills add OtterPaw-Studio/ccopyright-skill \
  --skill ccopyright-qa ccopyright-register
~~~

## Start using it

Open the software repository in your agent and ask for an assessment:

~~~text
Use $ccopyright-register to assess this repository for an ordinary China
software copyright registration. Do not generate materials yet. Show candidate
source boundaries, missing applicant facts, and all warnings.
~~~

Or begin the complete workflow:

~~~text
Use $ccopyright-register to prepare a draft software copyright registration
package for this repository. Create .ccopyright, preserve product source files,
and ask me only for facts the repository cannot establish safely.
~~~

For the final stage:

~~~text
Use $ccopyright-register to perform the final build, render and validate both
PDFs, create the contact sheets, and show me the human-review checklist. Wait
for my explicit confirmation before publishing a ready revision.
~~~

Registration-facing worksheets and identification materials are generated in Chinese by default.

## Prerequisites

| Requirement | Purpose | Required? |
|---|---|---|
| Python 3.10+, available as **python** | Scan, facts, worksheets, Markdown/HTML, manifests | Yes |
| Chrome or Chromium | Render identification-material PDFs | Optional until rendering |
| Poppler **pdfinfo** and **pdftotext** | Technical PDF validation | Optional until validation |
| Poppler **pdftoppm** | Page images and contact sheets | Optional |
| Git | Snapshot provenance and dirty-tree checks | Recommended |

Check the local environment:

~~~bash
python scripts/ccopyright.py preflight
~~~

No API key, portal credential, identity scan, or signing certificate is required by the local generator.

## What the skill asks you to confirm

Repository metadata is only a suggestion. You remain responsible for confirming:

- exact software full name, optional short name, and version;
- rights holders and ordering;
- completion and publication facts;
- category, original/modified status, development type, rights acquisition, and rights scope;
- source disclosure authority and source-program amount;
- ordinary program and document deposit;
- document content and real screenshots;
- requirements currently visible in the portal.

Identity numbers, identity scans, signatures, credentials, cookies, and unredacted portal screenshots must stay outside the preparation workspace.

## Workflow

1. **Assess** — read-only repository inventory and **INFO**/**WARNING** precheck.
2. **Initialize** — create **.ccopyright/** and the schema-v3 canonical fact file; existing workspaces migrate while preserving facts.
3. **Draft** — generate the copy-ready form worksheet, conditional proof checklist, source/document materials, and traceability records.
4. **Confirm** — resolve missing facts, current portal rules, source order, and unsupported document claims.
5. **Render and validate** — create A4 PDFs and check dimensions, row identity, canonical strings, hashes, and unresolved markers.
6. **Review and publish** — inspect every contact-sheet page, then explicitly publish a new immutable revision.

Repository, ownership, and IP precheck **WARNING** findings prompt review and do not block generation. Portal character conflicts, missing conditional fields, and unresolved active proof-readiness items appear as draft **WARNING** findings and block final generation; missing required facts, exceptional deposit, and failed PDF checks also stop the corresponding stage.

## Outputs

~~~text
.ccopyright/
├── facts/                 canonical application facts and requirement snapshot
├── reports/               inventory, precheck, evidence, build, render reports
├── drafts/                form worksheet and human/proof checklists
├── work/                  Markdown, HTML, PDFs, screenshots, manifests
├── qa/                    validation report, page PNGs, contact sheet
└── ready-to-submit/       timestamped human-reviewed revisions
~~~

### Application worksheet

Portal-ordered Chinese values, character counts, confirmation state, and
conditional branches. The bundled portal validation profile reports character
conflicts, unresolved conditional fields, and proof-readiness items as draft warnings, then enforces
them as final gates. It is not official authority; the current portal always
overrides it.

### Program material

An explicit ordered first-party source stream with preserved content, blank lines, comments, and tabs. Each printed row maps to its original path, line number, stream position, and hash.

### Document material

Applicant-approved documentation and real product screenshots, backed by repository evidence where practical. Missing evidence produces a warning rather than invented functionality.

### Proof checklist

External readiness items for cooperative, commissioned, assigned-task, modified, successor-acquisition, partial-rights, and other applicable branches. Proof files are not copied into the repository. Status is limited to `not-recorded`, `ready`, or `not-required`; active branches must reach an allowed ready state before final generation.

## Optional direct commands

The agent normally runs these for you:

~~~bash
python scripts/ccopyright.py init --repo /path/to/repo --workspace /path/to/repo/.ccopyright
python scripts/ccopyright.py status --workspace /path/to/repo/.ccopyright
python scripts/ccopyright.py build --repo /path/to/repo --workspace /path/to/repo/.ccopyright
python scripts/ccopyright.py build --repo /path/to/repo --workspace /path/to/repo/.ccopyright --final --render
python scripts/ccopyright.py validate --workspace /path/to/repo/.ccopyright
python scripts/ccopyright.py publish --workspace /path/to/repo/.ccopyright --human-reviewed
~~~

Full command guidance is in [references/en/workflow.md](references/en/workflow.md).
Official direct pages, the portal validation profile, and the data structure
are documented in
[references/en/official-sources.md](references/en/official-sources.md),
[references/en/portal-form.md](references/en/portal-form.md), and
[references/en/application-schema.md](references/en/application-schema.md).

## Safety and limitations

- Ordinary, non-classified deposit only; exceptional deposit stops.
- No browser filling, submission, identity verification, signature, payment, progress tracking, or correction-notice parsing.
- No legal advice, ownership determination, or acceptance guarantee.
- No automatic inference of rights holders, completion date, publication facts, or source disclosure authority.
- No identity numbers/scans, signatures, credentials, session data, or supplied portal screenshots in the workspace.
- Repository/IP findings have exactly two levels: **INFO** and **WARNING**.

Always review the current portal and every rendered page before submission.
