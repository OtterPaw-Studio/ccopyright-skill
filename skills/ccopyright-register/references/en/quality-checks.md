# Quality checks and review gates (English)

## Precheck is advisory

Repository and IP/sensitive-content precheck findings use only:

- `INFO`: observed provenance, exclusions, or suggestions.
- `WARNING`: something the applicant should inspect or confirm.

Warnings never block generation and are not legal conclusions. Typical warnings include a dirty working tree, secret-like pattern location, private-network reference, undecodable text, symlink, missing evidence, or screenshot assignment issue. Secret values are not echoed in reports.

## Completeness is a separate gate

Final build stops when canonical required values or required confirmations are missing. This is a document-completeness rule, not a third risk severity. Draft generation remains available so the user can review structure without fabricated facts.

Schema v2 also checks constraints visible in the portal evidence: each of the six environment fields, purpose, and industry is at most 50 characters; other languages are at most 120; other technical features are at most 100; a modification summary is at most 50; and main functions are 500–1,300 characters. Conditional values must be complete for published or modified software, successor acquisition, and partial rights. Items in `requirements.portal_unknowns` remain unverified and require a final manual check in the current portal.

Program and document deposit methods must both be ordinary; exceptional deposit stops. Under `selected-source-physical-lines`, the reported amount must match physical lines in the selected source. Under `applicant-confirmed-total`, the applicant must confirm the total-count basis and its boundary relative to the selected identification material. The multiple-rights-holder list must agree with the joint-ownership choice.

## Deterministic PDF checks

Validation verifies, where local tools permit:

- both expected PDF files exist and are A4 within tolerance;
- PDF page counts match manifests;
- every extracted `Pnnnnnn` or `Dnnnnn` row ID appears in manifest order;
- each page has its configured numbered-row count, except a configured complete-material final page;
- canonical software name, version, and rights holder are extractable;
- final PDFs do not contain draft or unresolved markers;
- configured file-size limits are respected;
- output hashes and renderer details are recorded.
- a commit-based source snapshot actually matches every selected working-tree file unless uncommitted content was explicitly included.

Program row IDs prove that the PDF matches the generated source manifest. The row manifest records original path, line, stream order, and hash; it is an internal audit artifact.

## Visual review remains mandatory

Open the contact sheets and inspect every page for clipping, unreadably small source, broken glyphs, blank pages, screenshot scaling, accidental private data, headers/footers, and page order. Text extraction cannot detect all layout failures.

Then review:

- exact full name, version punctuation, and rights-holder order;
- category, original/modified status, development type, rights acquisition, and rights scope;
- completion and publication facts, including first-publication date, country, and region when applicable;
- all six environment fields, languages, source amount, purpose, industry, main functions, and technical features for direct portal copying;
- source disclosure authority and source-selection cut points;
- claims versus actual behavior;
- applicant-prepared contracts, authorizations, task documents, or acquisition proof required by conditional branches;
- portal-specific file names, size limits, and required attachments.

Visual review must also confirm that no unnecessary personal data appears. In particular, never include identity numbers or scans, signatures, accounts, cookies, or personal data from user-submitted screenshots. The proof checklist stores readiness and non-sensitive notes only.

## Publication integrity

Publication requires a passing validation report, unchanged application-facts fingerprint, unchanged PDF hashes, a final (not draft) build, and explicit `--human-reviewed`. Every publish creates a new revision with `generation-manifest.json` and `SHA256SUMS`.

Do not upload internal files by default. The current portal determines which PDFs, form output, signature/confirmation pages, and proof documents are required.
