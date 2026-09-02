<div align="center">

# ccopyright-register

> **Prepare reviewable ordinary China software copyright registration materials from a code repository.**

**Repository assessment** · **Fact confirmation** · **Material generation** · **PDF validation** · **Human review**

[简体中文](README.md) · [What it is for](#what-it-is-for) · [Start using it](#start-using-it) · [Outputs](#outputs) · [Safety and limitations](#safety-and-limitations)

</div>

---

`ccopyright-register` turns a real software repository into registration material. It first inspects the source, documentation, and repository state; then it puts applicant-confirmed facts into a worksheet and prepares the program and document identification material.

It only covers preparation before manual submission to the [China Copyright Protection Center](https://www.ccopyright.com.cn/). It does not fill or submit the portal, operate an applicant account, track an application, or parse correction notices.

The repository also provides the read-only `ccopyright-qa` Skill. Start there
when you are still learning the rules, deciding whether assistance is needed,
or breaking down a service quote. This guide covers material preparation only.

## What it is for

| What you want to do | How it handles it |
|---|---|
| “First tell me whether this repository is usable” | Inspect source, docs, Git, licenses, and sensitive patterns read-only; list candidate boundaries and **INFO/WARNING** findings |
| “Start a draft” | Explain where it will write, create `.ccopyright/`, organize facts, and generate the worksheet and identification material |
| “Show me what is still missing” | Render A4 PDFs, check pagination, hashes, field limits, and unresolved items, then create contact sheets |
| “Keep a human-reviewed revision” | After explicit confirmation, publish a timestamped `ready-to-submit` revision without overwriting an earlier draft |

Use `ccopyright-qa` for rules, agency questions, or service-quote breakdowns. Portal login, automatic submission, payment, application tracking, and correction-notice parsing are outside this Skill.

## Install

~~~bash
npx skills add OtterPaw-Studio/ccopyright-skill --skill ccopyright-register
~~~

Install Q&A and preparation together:

~~~bash
npx skills add OtterPaw-Studio/ccopyright-skill \
  --skill ccopyright-qa ccopyright-register
~~~

## Start using it

Open the repository in your agent. You can start with assessment only:

~~~text
Use $ccopyright-register to assess this repository for an ordinary China
software copyright registration. Do not generate materials yet. Show candidate
source boundaries, missing applicant facts, and all warnings.
~~~

If you have already decided to prepare the material yourself, start with a draft:

~~~text
Use $ccopyright-register to prepare a draft software copyright registration
package for this repository. Create .ccopyright, preserve product source files,
and ask me only for facts the repository cannot establish safely.
~~~

After the draft is confirmed, move to the final build:

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

Repository metadata is useful as a clue, but it cannot establish the following facts. The applicant must confirm them:

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

1. **Assess**: inspect the repository read-only and produce an **INFO**/**WARNING** precheck.
2. **Initialize**: create **.ccopyright/** and its single fact file; an existing workspace is migrated without discarding its facts.
3. **Draft**: generate the form worksheet, conditional proof checklist, source/document material, and traceability records.
4. **Confirm**: fill in missing facts and check the current portal, source order, and document evidence.
5. **Render and validate**: create A4 PDFs and check dimensions, source-line mapping, fields, hashes, and unresolved markers.
6. **Review and publish**: inspect every contact-sheet page, then explicitly publish a new revision without overwriting the previous one.

Repository, ownership, and IP **WARNING** findings are reminders; they do not block a draft on their own. Final generation is blocked only by unresolved portal limits, conditional proofs, required facts, exceptional-deposit selection, or failed PDF checks.

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

Chinese form values are arranged in portal order, together with character counts, confirmation state, and conditional branches. The bundled profile warns about character conflicts, missing conditional fields, and proof readiness in a draft, then blocks unresolved items in the final build. It is a compatibility check, not official authority; the current portal always takes priority.

### Program material

Only explicitly selected first-party source is used. Original content, blank lines, comments, and tabs are preserved, and every printed row maps back to its file, line number, stream position, and hash.

### Document material

Only applicant-approved documentation and real product screenshots are used, with important claims tied back to repository evidence where practical. Missing evidence produces a warning; the Skill does not invent product functionality.

### Proof checklist

For cooperative, commissioned, assigned-task, modified, successor-acquisition, partial-rights, and similar cases, the checklist records what must be prepared outside the repository. Proof files are not copied in. Status is limited to `not-recorded`, `ready`, or `not-required`; every active branch must reach an allowed ready state before final generation.

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
- Repository and IP prechecks use only two levels: **INFO** and **WARNING**.

The applicant still needs to check the current portal and review every rendered page before submission.
