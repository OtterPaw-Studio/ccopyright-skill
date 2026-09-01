# Software Copyright Preparation Skill Specification

Status: Iteration 5 implementation validated; Aone publication pending
Date: 2026-09-01
Iteration 2 evidence: twelve user-supplied portal-form screenshots received on
2026-08-31. Their capture date is unknown, their coverage is partial, and the
original images are not retained in the skill because one contains personal
identity data.

Iteration 3 documentation reference: the user-facing information architecture
of the OpenMAIC bilingual README and the current skills.sh documentation/CLI.
OpenMAIC is used as a structural reference only; its product text is not copied.

## Problem

Applicants preparing a Chinese computer-software copyright registration must
turn repository facts into a consistent application worksheet, program
identification material, document identification material, and a reviewable
upload package. Ad-hoc generation is error-prone: names and dates drift,
third-party or sensitive code may be included, pagination changes between
runs, and generated claims can lose their connection to repository evidence.

## Product definition

The skill is a repository-to-submission-package workflow. It prepares,
generates, validates, and packages materials. It does not operate the official
website or manage the application after handoff.

One bilingual, self-contained bundle is required:

- `ccopyright-register.skill`: one `ccopyright-register` skill with English and
  Chinese READMEs and localized reference sets.

The `.skill` file is a ZIP-compatible archive containing a standard skill
layout with `SKILL.md` at the archive root.

## In scope

1. Capture a dated requirements snapshot from maintained references or
   user-provided field text/screenshots.
2. Read-only repository inventory for project type, version suggestions,
   languages, manifests, documentation, screenshots, tests, source candidates,
   Git state, submodules, generated/vendor areas, and symlinks.
3. Create a canonical application facts file and record which required facts
   the user has confirmed.
4. Produce an intellectual-property and sensitive-content precheck containing
   only `INFO` and `WARNING` findings. Findings never block generation and are
   not legal conclusions.
5. Produce a copy-ready application worksheet with evidence and confirmation
   status.
6. Build program identification material from an explicit ordered source-file
   list while preserving each file's original line order and content.
7. Build document identification material by adapting project facts, existing
   documentation, evidence, and real screenshots.
8. Render Markdown/HTML work products to A4 PDF when a supported Chromium
   executable is available.
9. Validate canonical names, versions, rights holders, dates, page sizes, line
   counts, numbering, source selection, placeholders, file integrity, and PDF
   text extraction.
10. Render PDF pages to review images and generate a contact-sheet HTML page
    when Poppler tools are available.
11. Publish only technically validated artifacts into a new revisioned
    `ready-to-submit` directory without overwriting an earlier revision.
12. Record input/output hashes, source snapshot, tool versions, and generation
    configuration for reproducibility.
13. Provide English and Chinese repository documentation.
14. Maintain a structured, copy-ready worksheet for portal fields observed in
    the current user-provided form evidence, while distinguishing confirmed
    observations from unknown portal constraints.
15. Provide consumer-first English and Chinese READMEs covering the outcome,
    skills.sh installation, first prompts, prerequisites, complete workflow,
    outputs, examples, safety boundaries, and frequently asked questions.
16. Keep the source Skill directory self-contained so repository installers
    that copy only the directory containing `SKILL.md` also receive scripts,
    assets, references, metadata, and both installed READMEs.
17. Keep Aone/Contextlab Git-synchronized version packages self-contained by
    declaring the complete runtime file allowlist in package metadata without
    adding Aone-only keys to Codex `SKILL.md` frontmatter.

## Out of scope

- Browser form filling or browser automation of any kind.
- Website submission, identity verification, signing, payment, or declarations.
- Application progress tracking, status polling, certificate management, or
  application-number storage.
- Parsing correction notices or automatically producing a correction response.
- Legal advice or a binding ownership determination.
- Automatically redacting, deleting, or rewriting sensitive source code.
- Automatically handling classified, military, sealed, or exceptional-deposit
  applications.
- Storing applicant identity-document numbers, identity scans, or unredacted
  portal screenshots in the repository or preparation workspace.

## Portal-form evidence model

The maintained screenshot baseline is evidence of a partial portal form, not a
claim that every current page or validation rule was captured. It establishes
the following visible dimensions for ordinary applications:

- rights acquisition: original or successor;
- software identity: full name, optional short name, and version;
- rights scope: all or partial;
- software category: application, embedded, middleware, or operating system;
- software description: original or modified, where modified includes
  translated or composite software;
- development type: independent, cooperative, commissioned, or assigned-task;
- completion date and publication status, with conditional publication date,
  country, and region;
- six distinct environment fields: development hardware, runtime hardware,
  development operating system, development tools, runtime platform/operating
  system, and supporting software;
- programming languages, reported source-program line count, purpose, industry,
  main functions, and technical-feature tags plus other text;
- independent program and document deposit types, each general or exceptional;
- rights-holder names and whether multiple holders jointly own the copyright;
- conditional PDF proof readiness for cooperative, commissioned, assigned-task,
  modified, successor, or other applicable cases.

Visible constraints are maintained as configurable requirements rather than
permanent constants: six environment fields, purpose, industry, and modification
summary show a 50-character limit; other programming languages show 120;
other technical features show 100; main functions displays `500~1300`; and
visible upload controls accept PDF. The main-function minimum and all limits
must still be confirmed against the current portal before final generation.

The screenshots do not establish upload size, filename rules, complete tooltip
content, every option behind collapsed controls, successor/partial-rights
branches, exceptional-deposit requirements, or later signature/confirmation
pages. These remain explicit unknowns in the requirements snapshot.

## Finding and state model

Precheck findings have exactly two levels:

- `INFO`: observed facts, provenance, or suggestions.
- `WARNING`: a fact the applicant should review or confirm.

Material lifecycle is independent of finding severity:

- `draft`: required facts may be missing or unconfirmed.
- `generated`: work products exist.
- `validated`: deterministic technical checks passed.
- `ready`: the user completed the final human-review checklist and published a
  revision.

A warning never prevents a `ready` package. Missing required values can still
prevent final-mode generation because this is a completeness constraint, not a
legal-risk severity.

## User stories

### US1: Assess a repository

As an applicant, I can scan a repository without modifying it and receive an
inventory, source-code statistics, evidence candidates, and `INFO`/`WARNING`
notes.

Acceptance criteria:

- The scan does not follow symlinks outside the repository.
- Dependency caches, VCS internals, binaries, and common build outputs are not
  proposed as first-party source.
- Secret-like values are reported by kind and location without echoing their
  value.
- Git HEAD, dirty state, submodules, and discovered version suggestions are
  recorded when available.

### US2: Initialize application facts

As an applicant, I can initialize a workspace containing a human-editable JSON
facts file, a repository inventory, and precheck reports.

Acceptance criteria:

- Guessed values are suggestions and are not marked confirmed.
- Rights holder, full name, version, completion date, and source selection are
  explicitly confirmable.
- Development completion, publication, code snapshot, and preparation dates are
  stored separately.
- Personally identifying proof documents are not copied into the repository.

### US3: Generate program material

As an applicant, I can select ordered first-party source files and generate
traceable program material.

Acceptance criteria:

- File content and line order are preserved, including blank and comment lines.
- No separator or generated comment is inserted into the counted source rows.
- Every printed source row maps to a path, original line number, and content
  hash in a source manifest.
- The generator supports whole-program and front/back selection modes based on
  configurable requirements.
- Long lines remain single rows and are reported when the configured minimum
  font size may be insufficient.

### US4: Generate document material

As an applicant, I can produce project-appropriate documentation from approved
facts, sections, evidence, and real screenshots.

Acceptance criteria:

- Existing documents can be adapted instead of always rewritten.
- Claims can cite internal evidence paths in a non-submission evidence map.
- Missing evidence creates a warning rather than an invented claim.
- Screenshot paths, hashes, captions, and target pages are recorded.
- The generator never pads the document with repeated filler text.

### US5: Validate and publish

As an applicant, I can run deterministic checks and publish a new immutable
ready-to-submit revision.

Acceptance criteria:

- PDF validation checks page size, expected numbered rows, canonical strings,
  extractability, and file hashes.
- Program validation compares printed row identifiers with the source manifest.
- The review checklist remains a human action.
- Publishing requires passed technical validation and a recorded human-review
  confirmation.
- Publishing creates a new revision and never overwrites an earlier one.

### US6: Install the bilingual skill

As a user, I can install one skill that responds in English or Chinese while
using one deterministic toolchain and the matching localized references.

Acceptance criteria:

- The archive is a valid ZIP file.
- It contains one `SKILL.md`, `agents/openai.yaml`, scripts, assets,
  `README.md`, `README.en.md`, and `references/en/` plus
  `references/zh-CN/` at the archive root.
- It passes the skill validator after extraction.
- Both READMEs document installation, scope, safety boundaries, workflow, and
  examples.

### US7: Prepare a portal-aligned worksheet

As an applicant, I can prepare the visible current portal fields and receive
conditional proof guidance without storing identity-document data.

Acceptance criteria:

- Original/modified status, development type, rights acquisition, rights scope,
  software category, and program/document deposit type remain separate fields.
- Published software requires publication date, country, and region; unpublished
  software does not.
- Modified software requires a short modification summary and a declared basis.
- Cooperative, commissioned, and assigned-task development produces the
  corresponding external-PDF checklist item.
- The worksheet reports visible field lengths and final mode rejects missing or
  out-of-range portal values while draft generation remains available.
- The reported source-program line count records its basis; a selected-source
  basis is checked against the generated source stream.
- Exceptional deposit stops this ordinary workflow rather than being generated
  automatically.
- Rights-holder names may be retained for material consistency, but identity
  numbers and unredacted proof images are never stored.

### US8: Install and start as an end user

As an applicant, I can install one complete Skill through skills.sh and follow
the bilingual README without knowing how this repository is built.

Acceptance criteria:

- `npx skills add OtterPaw-Studio/ccopyright-skill --skill
  ccopyright-register` discovers exactly one Skill after the repository is
  published at the documented source.
- A skills.sh project installation contains `SKILL.md`, scripts, assets,
  localized references, UI metadata, and both installed READMEs.
- The installed CLI can run `preflight` without relying on files outside the
  installed Skill directory.
- Both root READMEs lead with user outcome, installation, first interaction,
  prerequisites, workflow, outputs, examples, safety, and FAQ.
- Build, test, packaging, and release instructions are separated into
  `AGENTS.md` for maintainers.
- The documentation uses the canonical skills.sh source
  `OtterPaw-Studio/ccopyright-skill`, matching the configured Git origin.

### US9: Publish a complete Aone version package

As a maintainer, I can synchronize the same Skill to Aone and publish a new
version whose file tree contains the complete runtime rather than only
`SKILL.md` and `package.json`.

Acceptance criteria:

- `skills/ccopyright-register/package.json` contains a semver version and an
  explicit allowlist for `SKILL.md`, both READMEs, `agents/`, `assets/`,
  `references/`, and `scripts/`.
- An npm dry-run from the Skill directory lists all maintained source files and
  no files outside the Skill directory.
- `SKILL.md` remains valid under the official Codex Skill validator.
- The deterministic `.skill` archive also contains `package.json`.
- An existing incomplete Aone version is not treated as mutable; the repaired
  package is synchronized and published under a higher version.

## Non-functional requirements

- Python scripts use only the standard library.
- Commands avoid shells for paths derived from user configuration.
- Repository scanning is bounded and skips files above a configurable size.
- Work products do not contain local absolute paths unless explicitly intended
  for internal reports.
- Maintained portal evidence contains no applicant name, identity number, or
  unredacted screenshot.
- Final PDFs and ready-to-submit files contain no unresolved placeholders.
- Build output is reproducible enough to detect pagination drift: input hashes,
  configuration, renderer path/version, and output hashes are recorded.
- The bilingual bundle contains only one copy of each deterministic script and
  template.
- Tests cover a small repository, mixed evidence, a warning-producing file,
  source continuity, document generation, archive construction, and optional
  end-to-end PDF rendering when local tools exist.
- Existing schema-version-1 workspaces are upgraded without replacing confirmed
  values; new portal fields remain unconfirmed until reviewed.
- `skills/ccopyright-register/` is independently installable and contains all
  runtime files; archive construction does not depend on a sibling shared
  source directory.

## Definition of done

The implementation is complete when the spec, plan, and tasks are present; the
single bilingual skill and both READMEs are written; deterministic tooling
passes its tests; the skill bundle validates and extracts; and
`dist/ccopyright-register.skill` is generated. Iteration 2 additionally requires
schema migration, portal-field conditional tests, privacy-safe reference
material, and a deterministic rebuild of the archive.

Iteration 3 additionally requires bilingual consumer documentation, a
self-contained skills.sh-compatible source directory, an isolated CLI install
smoke test, archive validation, and a maintainer-only `AGENTS.md`.

Iteration 4 makes Chinese the primary README language, retains English as
`README.en.md`, records the canonical GitHub SSH origin, and adds repository
ignore rules for generated, local-install, cache, secret, and applicant-material
workspaces.

Iteration 5 adds an Aone/Contextlab package manifest beside `SKILL.md`. The
manifest owns the Aone version and complete file allowlist while the
`SKILL.md` frontmatter remains portable across Codex and skills.sh.

## Iteration 2 validation record

- All 19 test cases passed across the ordinary and explicit integration runs:
  the ordinary suite reported 18 passed and one intentionally skipped PDF
  case, and that PDF case passed when explicitly enabled.
- The enabled PDF integration rendered and validated both identification PDFs
  with local Chromium/Poppler and exercised revisioned publication.
- Two consecutive archive builds produced the same 70,920-byte file with
  SHA-256 `78913c6dc0fc2862a58f77697cfd8694935bdced078e0dd2bf63af53827a3876`.
- The extracted archive passed the official `quick_validate.py` skill
  validator.
- A repository audit found no retained clipboard paths, temporary screenshot
  paths, or 18-character identity-number-shaped values.

## Iteration 3 validation record

- Current skills CLI (`skills` 1.5.23 during validation) discovered exactly one
  source Skill named `ccopyright-register`.
- An isolated project installation using `--skill ccopyright-register --agent
  codex --copy --yes` produced a byte-identical copy of the self-contained
  source directory. The installed CLI successfully ran `preflight` and `init`.
- The ordinary test suite reported 18 passed and one intentionally skipped PDF
  case; the PDF case passed when explicitly enabled with local Chromium and
  Poppler.
- Two consecutive builds produced the same 75,050-byte archive with SHA-256
  `255b559bd17aafc710fdbf5a068f09ce4e77c1f9d434040c14472a93d9310b53`.
- The source Skill and extracted archive passed the official
  `quick_validate.py`; ZIP integrity and README local links also passed.
- The final privacy scan found no clipboard paths, temporary screenshot paths,
  or 18-character identity-number-shaped values.
- The canonical repository owner is now `OtterPaw-Studio`; both root READMEs
  use `OtterPaw-Studio/ccopyright-skill` in remote skills.sh examples.

## Iteration 4 validation record

- Root and installed `README.md` files are Chinese primary entrypoints;
  `README.en.md` contains the matching English guide, and all local language
  links resolve to the renamed files.
- User-facing introductions lead with applicant outcome and repository workflow;
  language support remains navigation and output behavior rather than product
  feature positioning.
- User-facing README emphasis uses Markdown bold syntax instead of inline HTML
  `code` or `strong` tags for consistent rendering across documentation hosts.
- The repository was initialized on branch `main`; fetch and push for `origin`
  both resolve to `git@github.com:OtterPaw-Studio/ccopyright-skill.git`.
- Targeted ignore checks cover `dist/`, `.ccopyright/`, local skills.sh copies,
  secrets, Python caches, editor state, logs, and temporary files without
  broadly excluding source, documentation, PDFs, or dependency lockfiles other
  than the generated `skills-lock.json`.
- The ordinary suite reported 18 passed and one intentionally skipped PDF case;
  the PDF integration passed when explicitly enabled outside the GUI sandbox.
- Current skills.sh discovery found exactly one Skill named
  `ccopyright-register`; source and extracted archives both passed the official
  Skill validator.
- Two consecutive builds produced the same 74,939-byte, 21-entry archive with
  SHA-256 `5a58c34d8f4f45acd33a17d8ce1af35a04c5d5c1639409ee6a8e601698b06768`.
- The final privacy scan found no clipboard paths, temporary screenshot paths,
  or 18-character identity-number-shaped values.

## Iteration 5 validation record

- `npm pack --dry-run --json` produced
  `shuangchi-gsc-ccopyright-register@0.0.3` with 21 files: `SKILL.md`,
  `package.json`, both READMEs, UI metadata, both assets, all localized
  references, and both scripts.
- The ordinary Python suite reported 19 passed and one intentionally skipped
  PDF case; the explicitly enabled Chromium/Poppler PDF integration passed.
- Current skills.sh (`skills` 1.5.23 during validation) discovered exactly one
  Skill and a disposable copied installation was byte-identical before
  execution; its installed CLI successfully ran `preflight`.
- The source Skill and extracted archive passed the official Codex Skill
  validator. ZIP integrity passed, and two consecutive builds produced the
  same 75,385-byte, 22-entry archive with SHA-256
  `705bef0d3830e7eb269780e766533592ab8923d07012c2fffce74810fa74acc8`.
- The privacy scan found no clipboard paths, temporary screenshot paths,
  18-character identity-number-shaped values, or placeholder evaluation text.
- Aone Git synchronization and publication of immutable version `0.0.3` remain
  pending external actions; version `0.0.2` is expected to retain its original
  two-file tree.
