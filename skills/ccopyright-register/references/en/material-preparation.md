# Preparing identification materials (English)

## Three design properties

### Source continuity

Source continuity means the selected files form one explicit ordered stream and every printed row preserves its original file content and order. Blank lines, comments, and tabs remain rows; the generator does not insert counted separator comments. `program-manifest.json` maps each `Pnnnnnn` row to its path, original line number, stream position, and content hash.

Continuity does not mean unrelated files become one legal source file. It is a traceable material-selection convention. Review front/back cut points whenever the complete ordered stream exceeds the configured capacity.

### Evidence mapping

Evidence mapping connects a documentation claim or section to repository paths that support it: implementation modules, routes, schemas, tests, existing manuals, or real screenshots. `reports/evidence-map.md` is an internal review aid. It helps reviewers distinguish implemented behavior from unsupported prose; it is not an upload requirement unless the current portal says otherwise.

### Reusable rendering

Reusable rendering separates semantic content and manifests from presentation. The same approved rows can produce Markdown, deterministic print HTML, PDF, text-extraction checks, and page-review images without rewriting the underlying facts. This makes pagination changes visible and regeneration repeatable.

## Program material

1. Inspect scanner suggestions, then create an explicit ordered `source.files` list.
2. Confirm every selected file is first-party, part of the registered version, and safe to disclose.
3. Use `whole` when all rows fit the configured front/back capacity. Use `front-back` for the configured leading and trailing windows; `auto` chooses between them by size.
4. Do not reformat, minify, beautify, translate, redact, or pad selected code. If disclosure requires redaction or exceptional deposit, stop this standard workflow.
5. Treat a long-line warning as a visual-review signal. The row remains one row; verify that it is readable in the rendered PDF.

The form's “source-program amount” is not the same thing as the number of pages in the deposited identification material. With `selected-source-physical-lines`, the generator requires the reported value to equal physical lines in the ordered selected stream. With `applicant-confirmed-total`, it displays both the applicant-confirmed total and the selected-stream count so the applicant can confirm the counting basis and material boundary. The bundled portal profile does not establish the official counting definition, so never auto-confirm the scanner suggestion as an application fact.

This skill supports ordinary program deposit only and generates either the complete material or the configured consecutive front/back windows. Exceptional deposit stops the workflow.

The manifest—not a visual file header—is the authoritative map back to original files. Headers, footers, material IDs, and page metadata are outside the source-content span.

## Document material

Choose a document type that actually exists for the software, such as a user manual or design description. Prefer adapting maintained repository documents over generating generic prose.

- Describe implemented workflows, boundaries, inputs, outputs, permissions, and error behavior.
- Keep applicant-approved terms consistent with the application worksheet.
- Give each substantive section at least one evidence path where practical.
- Never pad pages with duplicated claims or filler.
- Preserve a short final page when the complete document is shorter; report it for review instead of fabricating text.

This skill supports ordinary document deposit only. The primary document is generated as complete material or consecutive front/back windows. Portal “add another document” entries are tracked in `additional_documents`, but are not silently merged into the primary identification-material PDF.

## Screenshots

Use only real screenshots from the registered version. Remove or avoid credentials, private URLs, personal information, internal account identifiers, production customer data, debug overlays, and unrelated desktop chrome. Record the original path, hash, caption, and target page. The tool renders at most one screenshot rail per page and warns about conflicting assignments.

## Consistency

The software full name, exact version, and rights-holder string are generated from one canonical facts file and repeated in both materials. If any canonical value changes, rebuild and validate both PDFs together.
