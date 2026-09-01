# Implementation Plan

## Architecture

The repository keeps one self-contained skill identity with bilingual
references and deterministic tooling in the same installable directory. A
packaging script turns that directory into one ZIP-compatible `.skill` bundle;
skills.sh can install the source directory directly without a packaging step.

```text
skills/
  ccopyright-register/        Self-contained source used by skills.sh and archive
    SKILL.md                  Instructions and language routing
    package.json              Aone version metadata and package file allowlist
    README.md                 Installed Chinese user guide (primary)
    README.en.md              Installed English user guide
    scripts/ccopyright.py     Workflow CLI
    scripts/ccopyright_core.py Repository, material, PDF, and publishing logic
    assets/material.css       Deterministic print layout
    assets/application.template.json
    references/en/            English workflow references
    references/zh-CN/         Chinese workflow references
tools/build_skill_archives.py
tests/
dist/
```

The installed bundle exposes one CLI:

```bash
python scripts/ccopyright.py <command>
```

Commands:

- `preflight`: report tool availability and versions.
- `scan`: produce repository inventory and INFO/WARNING findings.
- `init`: create a preparation workspace and application JSON.
- `status`: report required-field and confirmation completeness.
- `build`: generate worksheet, evidence map, program/document Markdown and HTML,
  manifests, and optionally PDFs.
- `validate`: validate generated PDFs and create QA reports/review pages.
- `publish`: create a new revisioned ready-to-submit directory after technical
  validation and explicit human-review confirmation.

## Data model

`facts/application.json` is the canonical user-editable source. It separates:

- canonical software identity;
- applicant and rights-holder facts;
- completion, publication, snapshot, and preparation dates;
- requirements snapshot;
- ordered source selection;
- document sections, evidence paths, and screenshots;
- confirmation flags.

Machine-generated repository facts remain in
`reports/repository-inventory.json`; suggestions are copied into the application
file without confirmation.

Iteration 2 upgrades `facts/application.json` to schema version 2. It adds
portal-aligned controlled values, six separate environment fields, publication
country/region, source-program line-count metadata, independent program/document
deposit types, joint-ownership state, visible character limits, and a
privacy-safe portal-evidence descriptor. Version-1 workspaces are merged with
the version-2 template; existing values are preserved and coarse legacy
environment values are carried forward for review.

Portal field-length and conditional completeness checks are final-mode gates,
not structural JSON errors, so incomplete applications can still generate
draft worksheets. Exceptional deposit is outside the supported ordinary flow
and stops material generation with a specialist-process message.

## Material generation

Program material uses an ordered source stream. Selection is either the whole
stream or configurable front/back page windows. Each row receives a material
identifier, while path, original line number, and hash stay in a separate
manifest. No source content is modified.

Document material wraps approved headings and paragraphs into deterministic
numbered rows using East Asian display-width accounting. Screenshots occupy a
separate page rail and never replace numbered text rows. Short final pages are
reported according to configurable requirements; text is not fabricated.

## Rendering and validation

The builder writes Markdown and print-specific HTML. `render` uses an explicitly
provided or auto-discovered Chromium-family executable without a shell.
Validation uses Poppler command-line tools when installed, compares extracted
row identifiers with manifests, checks A4 dimensions and canonical strings, and
generates per-page PNGs plus an HTML contact sheet.

## Publication

Validation results are written to `qa/validation-report.json`. `publish`
requires a passing report and an explicit `--human-reviewed` flag. It creates a
timestamped revision directory and a checksum manifest, preserving every prior
revision.

## Portal worksheet and conditional proofs

The application worksheet follows the visible portal order and renders both
controlled choices and text lengths. It labels optional fields, distinguishes
confirmed values from review values, and keeps internal-only notes out of the
portal-field section. Proof readiness is metadata only: conditional cooperation,
commission, assigned-task, modification authorization, and successor documents
are listed without copying their PDFs into the repository.

The generated requirements snapshot records the maintained screenshot baseline,
its partial scope, its unknown capture date, the fact that originals are not
retained, visible limits, and unresolved portal constraints. Current-portal
confirmation remains a required user action.

## Language routing and packaging

The single `SKILL.md` routes interaction and reference loading by the user's
language. The self-contained source and archive include both READMEs, both
localized reference sets, and one copy of the scripts and CSS. Archive entries
use stable timestamps and ordering so rebuilding unchanged inputs produces an
identical archive.

## Verification

1. Python unit tests for repository inventory, secret redaction, config
   initialization, continuity manifests, document lines, and publication gates.
2. Optional integration test with installed Chrome/Chromium and Poppler.
3. `quick_validate.py` against the extracted bilingual bundle.
4. ZIP integrity and required-entry assertions for
   `ccopyright-register.skill`.
5. Repeated-build hash comparison proving deterministic packaging.
6. Schema-v1 migration, portal conditional completeness, character-limit,
   source-line-count, exceptional-deposit, dynamic-proof, and privacy tests.
7. npm dry-run inspection proving the Aone/Contextlab version package contains
   every runtime resource while the official Codex Skill validator still
   accepts `SKILL.md`.

## Iteration 2 completion

The schema-v2 template, in-place migration, portal-aligned worksheet,
privacy-safe evidence snapshot, conditional proof list, ordinary-deposit
boundary, and bilingual references are implemented. Unit/package tests, the
explicit Chromium/Poppler integration test, deterministic archive rebuild, and
official skill validation all pass.

## Iteration 3: user documentation and skills.sh

1. Use a consumer-first README structure: outcome, shortest installation path,
   first prompt, prerequisites, workflow, outputs, examples, boundaries, FAQ.
2. Keep English and Chinese root guides semantically aligned, and expand the
   two installed guides with the same operating model.
3. Move scripts and assets into `skills/ccopyright-register/` so repository
   installers copy the full runtime.
4. Put contributor, test, deterministic build, privacy audit, and release
   details in root `AGENTS.md`.
5. Verify current skills.sh discovery and an isolated `--copy` installation,
   then run the installed CLI from the copied directory.
6. Re-run unit/PDF tests, deterministic packaging, ZIP inspection, and the
   official Skill validator.

## Iteration 3 completion

All four user-facing READMEs now cover the applicant journey, the canonical
Skill source is independently installable through skills.sh, and maintenance
instructions live in `AGENTS.md`. Isolated discovery, copy installation,
installed `preflight`/`init`, tests, PDF integration, deterministic packaging,
ZIP integrity, local-link checks, privacy audit, and official validation pass.
Only the public GitHub owner placeholder remains for publication-time
substitution.

## Iteration 5: complete Aone package contents

1. Keep portable Skill discovery metadata in `SKILL.md` and Aone package
   version/file-selection metadata in the adjacent `package.json`.
2. Explicitly allowlist both READMEs, UI metadata, assets, localized references,
   scripts, and `SKILL.md` for the Contextlab package.
3. Add package-manifest coverage and archive-entry assertions.
4. Run npm dry-run inspection, the Python suite, deterministic archive rebuild,
   skills.sh discovery/install checks, and official Skill validation.
5. Synchronize and publish a higher Aone version; do not expect the existing
   incomplete version to change retroactively.
