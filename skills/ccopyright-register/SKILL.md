---
name: ccopyright-register
description: Prepare China computer-software copyright registration materials from a code repository. Use for 软件著作权, 软著, China software copyright, ccopyright.com.cn preparation, repository/IP prechecks, application worksheets, source-code or document identification materials, PDF validation, and ready-to-submit packaging. Do not use it to submit forms, track applications, or parse correction notices.
---

# China Software Copyright Material Preparation

Prepare a reviewable registration-material package from repository evidence and applicant-confirmed facts. Treat the workflow as document engineering, not legal advice or an ownership determination.

## Language routing

- Respond in the user's language. Use Chinese by default when the request is in Chinese and English when it is in English.
- For a Chinese workflow, read only the relevant files under `references/zh-CN/`; for an English workflow, read only the corresponding files under `references/en/`. Load both only for translation or comparison.
- Registration-facing worksheets and identification materials should normally remain in Chinese even when the surrounding explanation is English, unless the current official requirement says otherwise.

## Start here

1. Resolve the repository root and choose a workspace, normally `<repo>/.ccopyright`.
2. Read the applicable [English workflow](references/en/workflow.md) or [中文流程](references/zh-CN/workflow.md), then run `python scripts/ccopyright.py preflight`.
3. Identify the requested mode:
   - **Assess**: scan only; do not initialize or generate unless asked.
   - **Prepare**: initialize facts, generate drafts, and help the user resolve missing facts.
   - **Validate**: inspect existing generated materials and run deterministic checks.
   - **Regenerate**: preserve facts and previous ready revisions, then rebuild changed outputs.
4. Before changing repository files, explain that the preparation workspace is the only intended write target.

## Non-negotiable boundaries

- Never fill or submit a browser form, sign a declaration, pay a fee, or operate an applicant account.
- Never track application status or parse a correction notice.
- Never present output as legal advice, guaranteed acceptance, or a binding ownership conclusion.
- Keep ownership/IP precheck findings to exactly `INFO` and `WARNING`. A warning is review guidance and never a generation blocker.
- Keep completeness gates separate: final mode may stop when required facts are missing or unconfirmed.
- Never infer rights holders, development-completion date, publication facts, or authority to disclose source code from Git history.
- Never copy identity documents, identity numbers, signatures, user-supplied portal screenshots, or other proof scans into the repository. Record checklist status and non-sensitive notes only.
- Do not follow symlinks, include dependency/vendor/generated code by default, echo detected secrets, or silently modify source files.
- Stop and direct the user to the appropriate specialist process for classified, military, sealed, or exceptional-deposit material.

## Canonical workflow

Use `facts/application.json` as the only canonical application-facts source. Repository guesses remain unconfirmed suggestions.

1. Capture a requirements snapshot. Prefer the applicant's current portal text or screenshots, then current official sources. Read the applicable `official-sources.md` and `portal-form.md`. Distinguish the evidence receipt date from the actual portal review/capture date; do not confirm currency until the latter is known.
2. Run the read-only scan and initialize the workspace.
3. Review `reports/precheck.md` and schema-v2 `facts/application.json` with the user. `init` and `status` migrate schema v1 in place without confirming new fields. Ask only for facts that cannot be established safely.
4. Select first-party source files in deliberate functional order. Preserve every selected line, including blanks, comments, and tabs.
5. Draft document sections from implemented behavior and map each material claim to repository evidence. Use real screenshots only.
6. Build draft materials first. Drafts must display unresolved markers rather than invent values.
7. After confirmations are true, run final build, render to PDF, validate, and inspect the page contact sheets.
8. Publish a new revision only after the user completes the human-review checklist and explicitly confirms it.

Each language directory contains `workflow.md`, `application-schema.md`, `portal-form.md`, `material-preparation.md`, `quality-checks.md`, and `official-sources.md`. Read only the files needed for the current step.

## Interaction rules

- Group missing-fact questions into a short checklist. Do not ask for values already present and confirmed.
- Explain every suggestion with its source, such as `package.json`, `pyproject.toml`, or Git HEAD.
- When the current portal conflicts with the maintained baseline, update `requirements` and `requirements-snapshot.md`; the current portal wins.
- Treat portal evidence as partial unless every relevant branch and help text was captured. Keep unresolved limits or choices in `requirements.portal_unknowns`.
- Generate a copy-ready worksheet in portal order, but never create fields for identity-document numbers, scans, signatures, credentials, or portal-session data.
- Show source-selection boundaries before final generation, especially front/back cut points.
- Report warnings without hiding them, but do not demand that every warning be removed.
- Distinguish upload candidates (PDFs and currently required proof/form files) from internal review artifacts (manifests, evidence map, hashes, contact sheets).
- End with paths to the latest revision, validation result, remaining warnings, and any manual portal steps.

## Tooling

Run all commands from the installed skill directory or call the script by absolute path:

```bash
python scripts/ccopyright.py --help
```

The generator uses only the Python standard library. PDF rendering requires a local Chrome/Chromium executable; PDF text/page validation uses Poppler (`pdfinfo`, `pdftotext`, and optionally `pdftoppm`). If optional tools are absent, retain the generated HTML and explain the precise missing capability.
