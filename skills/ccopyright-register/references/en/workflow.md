# Workflow and commands (English)

Use absolute paths when the repository and preparation workspace are different. The examples below assume commands run from the installed skill directory.

## 1. Check local capabilities

```bash
python scripts/ccopyright.py preflight
```

Python is sufficient for scanning and HTML generation. Chrome/Chromium is required for PDF rendering. `pdfinfo` and `pdftotext` are required for technical PDF validation; `pdftoppm` adds visual-review pages.

## 2. Assess without initializing

```bash
python scripts/ccopyright.py scan \
  --repo /absolute/path/to/repository \
  --output /absolute/path/to/repository-review.json
```

This writes JSON plus a sibling Markdown report. Findings are only `INFO` and `WARNING`. The scanner does not decide ownership and does not modify repository content.

## 3. Initialize the workspace

```bash
python scripts/ccopyright.py init \
  --repo /absolute/path/to/repository \
  --workspace /absolute/path/to/repository/.ccopyright
```

Do not use `--force` after the applicant has edited `facts/application.json` unless they explicitly want to replace it. Re-running `init` without `--force` refreshes the inventory while preserving the application facts file.

`init` creates the schema-v2 fact template and a privacy-safe `facts/requirements-snapshot.md`. Existing schema-v1 workspaces are upgraded in place: existing facts are preserved, new fields are added, and new confirmation flags remain `false`.

## 4. Complete canonical facts

Edit `.ccopyright/facts/application.json`, then inspect completeness:

```bash
python scripts/ccopyright.py status \
  --workspace /absolute/path/to/repository/.ccopyright
```

Keep guesses unconfirmed. Review every item against the [portal-form evidence baseline](portal-form.md): name/version, category, original or modified status, development type, rights acquisition and scope, rights holders, completion/publication facts, six environment fields, languages, purpose, industry, main functions, technical features, source amount, and deposit method. Final mode also requires ordered source files, document sections, and all required confirmation flags.

`status` reports ordinary missing values, conditional-branch gaps, and portal-field constraint violations. Conditional branches cover published or modified software, successor acquisition, partial rights, and cooperative, commissioned, or assigned-task development. Identity-document numbers, identity scans, and signatures never enter the workspace.

## 5. Generate a draft

```bash
python scripts/ccopyright.py build \
  --repo /absolute/path/to/repository \
  --workspace /absolute/path/to/repository/.ccopyright
```

Draft mode may retain unresolved markers and report portal-length or branch issues; resolve them before final mode. Review these before final mode:

- `drafts/form-worksheet.md`
- `drafts/proof-checklist.md`
- `reports/precheck.md`
- `reports/evidence-map.md`
- `work/program-manifest.json`
- `work/document-manifest.json`
- generated Markdown and HTML in `work/`

## 6. Final build and rendering

```bash
python scripts/ccopyright.py build \
  --repo /absolute/path/to/repository \
  --workspace /absolute/path/to/repository/.ccopyright \
  --final \
  --render
```

If Chrome is not auto-discovered, add `--chrome /absolute/path/to/chrome`. Rendering can also be repeated separately:

```bash
python scripts/ccopyright.py render \
  --workspace /absolute/path/to/repository/.ccopyright \
  --chrome /absolute/path/to/chrome
```

`reports/render-report.json` records renderer identity and PDF hashes.

This skill stops when either program or document identification material uses exceptional deposit; it prepares only the ordinary flow. Cooperative, commissioned, assigned-task, modified-software, successor-acquisition, and partial-rights branches add corresponding proof-checklist items, but the tool does not decide whether a document is legally sufficient.

## 7. Validate

```bash
python scripts/ccopyright.py validate \
  --workspace /absolute/path/to/repository/.ccopyright
```

Read `qa/validation-report.md`, then inspect the PNG pages and `contact-sheet.html` under `qa/`. A technical pass does not replace human review.

## 8. Publish a revision

After checking every item in `drafts/final-review-checklist.md`:

```bash
python scripts/ccopyright.py publish \
  --workspace /absolute/path/to/repository/.ccopyright \
  --human-reviewed
```

The command creates a new timestamped directory under `ready-to-submit/`. It never overwrites an older revision. The directory includes the two PDFs, copy-ready worksheets/checklists, an application-facts snapshot, a generation manifest, and checksums. Confirm which files the current portal actually requests; internal manifests and QA artifacts are not upload defaults.

## Workspace lifecycle

```text
draft -> generated -> validated -> ready
```

- `draft`: facts can be incomplete.
- `generated`: draft or final work products exist.
- `validated`: current rendered PDFs passed deterministic checks.
- `ready`: a human-reviewed immutable revision was published.

Changing material-driving facts after validation invalidates publication until build, render, and validation are repeated.
