# ccopyright-register

> Turn a software repository into a reviewable preparation package for ordinary China computer-software copyright registration.

[简体中文](README.md) · [Quick start](#quick-start) · [What it prepares](#what-it-prepares) · [Outputs](#outputs) · [Safety and scope](#safety-and-scope)

ccopyright-register helps applicants prepare, check, and organize software copyright registration materials from a code repository. Use it from your AI coding agent; it inspects the repository, asks for facts that code cannot establish, and creates a structured **.ccopyright/** workspace for review.

It is designed for preparation before manual submission to the [China Copyright Protection Center](https://www.ccopyright.com.cn/). It does not sign in, fill the browser form, submit an application, track progress, or interpret correction notices.

## Why use it?

Preparing registration material is more than exporting sixty pages of code. The software name, version, rights holders, dates, application fields, source selection, and user documentation need to agree with one another.

The skill helps you:

- inventory the repository without rewriting product source code;
- keep applicant-confirmed facts in one editable file;
- prepare a portal-ordered, copy-ready application worksheet;
- select traceable first-party source in an explicit order;
- generate program and document identification materials;
- report repository, ownership, IP, and sensitive-content observations using only **INFO** and **WARNING**;
- render and technically validate A4 PDFs when local tools are available;
- publish a human-reviewed, checksum-protected revision without overwriting earlier revisions.

## Quick start

### 1. Install with skills.sh

The repository already uses the standard nested Skill layout and is discoverable by the **skills** CLI as exactly one skill: **ccopyright-register**.

Install from GitHub once the repository is accessible:

~~~bash
npx skills add OtterPaw-Studio/ccopyright-skill --skill ccopyright-register
~~~

For a global Codex installation:

~~~bash
npx skills add OtterPaw-Studio/ccopyright-skill \
  --skill ccopyright-register \
  --agent codex \
  --global
~~~

From a local checkout, you can install it immediately:

~~~bash
npx skills add . --skill ccopyright-register
~~~

The CLI can be run through **npx** without installing it separately. See the [skills.sh CLI documentation](https://www.skills.sh/docs/cli).

### 2. Open the software repository in your agent

Start with an assessment if you are still deciding what to register:

~~~text
Use $ccopyright-register to assess this repository for an ordinary software
copyright registration. Do not generate materials yet. Show me the candidate
software identity, source boundaries, missing facts, and all warnings.
~~~

Or start the preparation workflow directly:

~~~text
Use $ccopyright-register to prepare software copyright registration materials
for this repository. Create the .ccopyright workspace, generate a draft first,
and ask me only for facts that cannot be established from the repository.
~~~

Registration-facing worksheets and identification materials are generated in Chinese by default.

### 3. Review facts before final generation

The skill will ask you to confirm information that Git history cannot prove, including:

- exact software full name, optional short name, and version;
- rights holder names and their order;
- development-completion and publication facts;
- original or successor acquisition, full or partial rights, and development type;
- ordinary program/document deposit;
- the source-program amount and its counting basis;
- current portal requirements for this application.

Draft output may contain review markers. Final output will not be generated until required facts and confirmations are complete.

### 4. Render, validate, and publish a revision

When Chrome/Chromium and Poppler are available, ask:

~~~text
Use $ccopyright-register to perform the final build, render both PDFs, validate
them, create page-review contact sheets, and show me the remaining human checks.
Do not publish a ready revision until I explicitly confirm the review.
~~~

## Prerequisites

The skill can still scan a repository and generate HTML when optional PDF tools are absent.

| Requirement | Needed for | Required? |
|---|---|---|
| An Agent Skills-compatible coding agent | Running the guided workflow | Yes |
| Node.js with **npx** | Installation through skills.sh | Only for installation |
| Python 3.10 or newer, available as **python** | Repository scan, worksheets, manifests, HTML generation, validation orchestration | Yes |
| Chrome or Chromium | Rendering HTML identification materials to PDF | Optional until PDF generation |
| Poppler **pdfinfo** and **pdftotext** | Technical PDF validation | Optional until validation |
| Poppler **pdftoppm** | Per-page PNGs and contact sheets | Optional |
| Git | Snapshot provenance and dirty-tree checks | Recommended, not required |

To see what is available on your machine, ask the skill to run its preflight check, or run this from the installed skill directory:

~~~bash
python scripts/ccopyright.py preflight
~~~

No LLM API key, portal password, identity document, or signing certificate is required by the local generator.

## What you need to provide

The repository provides implementation evidence, but it does not establish every application fact. Be ready to provide or confirm:

1. the repository and exact version being registered;
2. the applicant-approved software name and rights holders;
3. completion and publication facts;
4. development and rights-acquisition branches;
5. which first-party source may be disclosed;
6. the document type and any real screenshots to include;
7. the current portal instructions or redacted screenshots when they differ from the maintained baseline;
8. whether any required contracts, authorizations, or other proofs are ready outside the repository.

Do not place identity numbers, identity scans, signatures, portal credentials, cookies, or unredacted portal screenshots in the workspace.

## How the workflow works

| Stage | What the skill does | What you review |
|---|---|---|
| Assess | Scans manifests, source, Git state, documents, screenshots, licenses, generated/vendor areas, and sensitive patterns | Candidate version, first-party boundaries, warnings |
| Initialize | Creates **.ccopyright/** and a schema-v2 fact file | Guessed values remain unconfirmed |
| Draft | Generates the worksheet, proof checklist, source/document materials, manifests, and evidence map | Portal fields, claims, source order, missing evidence |
| Final build | Requires complete confirmed facts and ordinary deposit | Exact identity, dates, rights, text lengths, conditional branches |
| Render and validate | Produces PDFs, checks A4 size, page/row identity, canonical strings, hashes, and unresolved markers | Every rendered page in the contact sheet |
| Publish | Creates a new timestamped ready revision after explicit human review | Files that should actually be uploaded |

Warnings are advisory and never become a third severity level. A final build can still stop for missing facts or invalid material constraints; that is a completeness gate, not a legal-risk judgment.

## What it prepares

### Application worksheet

A Chinese, portal-ordered worksheet covering the visible registration fields, including:

- software identity and category;
- original/modified status;
- development type;
- rights acquisition and scope;
- completion and publication facts;
- six development/runtime environment fields;
- programming languages and source-program amount;
- purpose, industry, main functions, and technical features;
- general program/document deposit choices;
- rights holders and joint ownership.

Visible field limits and conditional branches are checked from a dated, configurable requirements snapshot. The current portal always wins over the bundled baseline.

### Program identification material

The skill builds one ordered source stream from explicitly selected first-party files. Blank lines, comments, tabs, content order, and source mapping are preserved. A manifest maps each printed row back to its path, original line number, stream position, and hash.

It supports complete material or ordinary consecutive front/back windows. Exceptional deposit is outside this workflow.

### Document identification material

The skill adapts applicant-approved documentation sections, repository evidence, and real product screenshots into a deterministic document. Unsupported claims generate warnings; the skill does not invent product functionality or pad pages with filler.

### Conditional proof checklist

The checklist changes with the application branch, including cooperative, commissioned, assigned-task, modified-software, successor-acquisition, and partial-rights cases. It records readiness only; proof PDFs stay outside the repository.

## Outputs

The default workspace is **.ccopyright/** inside the software repository:

~~~text
.ccopyright/
├── facts/                 canonical application facts and requirement snapshot
├── reports/               inventory, precheck, evidence, build, and render reports
├── drafts/                copy-ready worksheet and human checklists
├── work/                  Markdown, HTML, PDFs, assets, and traceability manifests
├── qa/                    validation reports, page PNGs, and contact sheet
└── ready-to-submit/       immutable timestamped reviewed revisions
~~~

Typical upload candidates are the program and document identification PDFs plus proof/form files required by the current portal. Manifests, evidence maps, hashes, and contact sheets are internal review artifacts unless the portal explicitly asks for them.

## Example requests

~~~text
Assess this monorepo and recommend which package should be the registration boundary.
~~~

~~~text
Prepare a draft for an unpublished, independently developed application
software product. I have not confirmed the completion date yet.
~~~

~~~text
Regenerate the materials after a version change, preserve my confirmed facts,
and show exactly what changed from the previous revision.
~~~

~~~text
Validate the existing PDFs and tell me whether the problem is missing facts,
source continuity, rendering, or a manual portal requirement.
~~~

## Safety and scope

The skill:

- never fills or submits the browser form;
- never logs in, signs, pays, or operates an applicant account;
- never tracks an application or parses correction notices;
- never claims ownership or guarantees acceptance;
- never infers rights holders, completion dates, publication facts, or disclosure authority from Git;
- never stores identity-document numbers, identity scans, signatures, credentials, or session data;
- does not automate exceptional, sealed, classified, or military deposit workflows.

Repository/IP precheck results use only **INFO** and **WARNING**. The output is preparation assistance, not legal advice.

## Managing the installed skill

List project or global skills:

~~~bash
npx skills list
npx skills list --global
~~~

Update this skill:

~~~bash
npx skills update ccopyright-register
npx skills update --global ccopyright-register
~~~

Remove it:

~~~bash
npx skills remove ccopyright-register
npx skills remove --global ccopyright-register
~~~

skills.sh documents anonymous installation telemetry. To opt out for a command:

~~~bash
DISABLE_TELEMETRY=1 npx skills add OtterPaw-Studio/ccopyright-skill \
  --skill ccopyright-register
~~~

## FAQ

### Can I use it without Chrome or Poppler?

Yes. Repository assessment, fact management, worksheets, manifests, Markdown, and HTML remain available. PDF rendering and technical PDF validation require the optional tools listed above.

### Will every warning block my package?

No. Warnings remain visible for review but do not block generation. Missing required facts, invalid portal-field constraints, unsupported exceptional deposit, or failed PDF validation can block the corresponding final stage.

### Does the skill decide who owns the software?

No. It records applicant-confirmed rights facts and highlights evidence boundaries. Ownership and legal sufficiency remain the applicant's responsibility.

### Can it reuse an existing manual?

Yes. Maintained repository documentation is preferred over generic generated prose. Claims should be mapped to implementation or other repository evidence where practical.

### Does it upload contracts or identity documents?

No. It produces a readiness checklist and keeps those documents outside **.ccopyright/**.

### Are the bundled portal fields guaranteed to be current?

No. They come from a partial screenshot baseline and maintained official references. Confirm the current portal before marking the requirements snapshot as current.

## Official references

- [China Copyright Protection Center](https://www.ccopyright.com.cn/)
- [Measures for Computer Software Copyright Registration](https://www.ncac.gov.cn/xxfb/flfg/bmgz/202410/t20241015_869486.html)
- [skills.sh documentation](https://www.skills.sh/docs)

For maintainer and contributor commands, see [AGENTS.md](AGENTS.md).
