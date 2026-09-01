# Canonical application schema (English)

`facts/application.json` is the only human-editable fact source. The current
structure is `schema_version: 3`. `init` and `status` upgrade older versions in
place, preserve existing facts and applicant-adjusted gates, leave new fields
unconfirmed, and never maintain a separate shadow copy. The v2
`requirements.portal_evidence` object is removed and migrated to a portal
validation profile with no attachment history.

## `software`

### Portal identity and classification

- `full_name`: required full name exactly as it will appear in the application.
- `short_name`: optional; leave it empty when there is no short name and do not enter a placeholder such as “none.”
- `version`: required exact version, including any intended `V` prefix, punctuation, and casing.
- `category`: `application`, `embedded`, `middleware`, or `operating-system`.
- `description.type`: `original` or `modified`. A modified program also needs `modification_summary` within the bundled 50-character gate and a `modification_basis` that records whether the prior program is registered or authorization from the original rights holder is required.
- `development_type`: `independent`, `cooperative`, `commissioned`, or `assigned-task`.
- `rights_acquisition`: `original` or `successor`; successor acquisition needs a separately confirmed basis.
- `rights_scope`: `all` or `partial`; partial rights require the scope and supporting proof.
- `completion_date`: applicant-confirmed development-completion date. Never substitute the last Git commit date.

### Publication and rights holders

- `publication.status`: `unpublished` or `published`. Published software also requires `date`, `country`, and `region`.
- `rights_holders`: ordered list of applicant-confirmed rights-holder names.
- `joint_rights_holders`: whether multiple rights holders jointly own the rights; this must agree with the list.
- Identity-document types, numbers, scans, and signatures are not part of this JSON. The applicant handles them directly in the portal.

### Environment, languages, and functionality

- `environment` has six separate fields: `development_hardware`, `runtime_hardware`, `development_os`, `development_tools`, `runtime_platform`, and `supporting_software`. The bundled profile caps each at 50 characters.
- `programming_languages`: choices selected from the portal; `other_programming_languages` contains only languages outside that list and has a bundled 120-character cap.
- `purpose` and `industry`: each has a bundled 50-character cap.
- `technical_features`: portal feature tags; `other_technical_features` has a bundled 100-character cap.
- `main_functions`: continuous application-form prose. The bundled profile checks a 500-character minimum and 1,300-character maximum, but the applicant must reconfirm it in the current portal before submission.
- `competitive_advantages` and `commercial_value`: internal helper fields outside the current portal validation profile and excluded from the copy-ready worksheet.

Every description must be grounded in the repository and approved by the applicant.

## `dates` and `snapshot`

Keep these concepts separate:

- `software.completion_date`: legal/application fact confirmed by the applicant.
- `software.publication.date`: first-publication fact, if applicable.
- `dates.code_snapshot_date`: date associated with the selected source snapshot.
- `dates.material_preparation_date`: when the materials were prepared.
- `snapshot.commit`: Git commit used as provenance, not proof of completion or ownership.
- `snapshot.include_uncommitted`: whether the selected snapshot intentionally includes working-tree changes.

For a Git `head`/`commit` snapshot with `include_uncommitted: false`, final generation verifies that every selected source file exists at and matches the configured hexadecimal commit. Use `working-tree` mode (or explicitly include uncommitted content) for a non-Git or intentionally dirty snapshot.

## `requirements`

This is a dated, configurable snapshot—not a permanent statement of portal behavior.

- `captured_at` and `source_urls`: rule provenance and the actual current-portal review date; the field name remains for workspace compatibility. Keep the date empty and do not confirm `requirements.current` until the current portal has been reviewed.
- `portal_validation_profile`: portal-compatibility profile ID; it is not an official-source or evidence identifier.
- `portal_field_limits` and `portal_field_minimums`: configured character gates. Keys must be dotted paths to string facts, and a field's minimum cannot exceed its maximum. A minimum-only gate is valid; an empty value blocks only when the field is otherwise required or conditionally required, so a minimum does not make an optional field mandatory. Removing a default gate remains effective on later runs. Draft mode emits `WARNING` for gate conflicts and unresolved conditional branches; final mode blocks.
- `portal_unknowns`: formats, sizes, choice lists, and help text not established by the profile and still requiring manual confirmation.
- `paper`: normally A4 under the maintained legal baseline.
- `program_lines_per_page` and `document_lines_per_page`: printable numbered-row targets.
- `front_pages` and `back_pages`: windows used for front/back material selection.
- `allow_short_final_page_for_complete_material`: treatment for programs/documents shorter than a full final page.
- `max_pdf_bytes`: optional current upload limit; `null` means no locally asserted limit.

Update these fields from the current portal before final generation and set `captured_at` to the actual review date.

## `source`

- `files`: explicit ordered first-party source paths relative to the repository root.
- `suggested_files`: scanner output only; final mode never substitutes it for `files`.
- `mode`: `auto`, `whole`, or `front-back`.
- `deposit_type`: this skill supports only `general`; `exceptional` stops and routes to specialist handling.
- `program_line_count`: source amount entered in the form. Confirm it against physical lines in the selected source; the generator reconciles both values.
- `program_line_count_basis`: describes the counting method; ordinary flow should normally use `selected-source-physical-lines`.
- `ordering`: explanatory note about how the ordered stream was assembled.
- `exclude_globs`: reserved for applicant notes; explicit `files` remains authoritative.

Prefer functional reading order: entry points, core domain logic, orchestration, persistence/integration, then presentation. Exclude dependencies, generated files, tests/fixtures unless materially necessary, secrets, and code the applicant cannot disclose.

## `document`

- `kind`: document type, for example `user-manual` or `design-description`.
- `title`: optional explicit title.
- `deposit_type`: this skill supports only `general`; `exceptional` stops.
- `max_display_units_per_line`: deterministic wrapping width.
- `sections`: ordered objects with `title`, `paragraphs`, and repository-relative `evidence` paths.
- `screenshots`: objects with `path`, `page`, `title`, and `caption`.
- `additional_documents`: preparation records for the portal's “add another document” branch; these do not replace the primary document identification material.

Text is approved input, not an invitation to invent claims. Missing evidence produces a `WARNING` only.

## `confirmations`

Final mode requires every confirmation key in the template to be `true`, covering:

- software name, version, classification, rights, rights holders, completion, development, and publication;
- environments, purpose, industry, technical features, and main functions;
- source selection, source amount, and ordinary-deposit choice;
- document content and the current requirements snapshot.

Confirmation means the applicant reviewed a value; it is not a legal conclusion. Conditional branches remain separately checked, including publication details, modified-software explanation, successor-acquisition basis, partial-rights scope, and proof documents for cooperative, commissioned, or assigned-task development.

## `proof_checklist` and `review`

Record readiness and non-sensitive notes only. The checklist adds items dynamically for development type, modified software, successor acquisition, partial rights, or multiple rights holders. Never store identity-document numbers or scans, signatures, credentials, portal-session data, or personal data from an unredacted portal view.

Each checklist item uses one of three statuses: `not-recorded`, `ready`, or
`not-required`. `ready` means the applicant has prepared the material outside
the repository. Use `not-required` only after the current portal was checked
and the active branch does not require a separate proof upload. Cooperative,
commissioned, assigned-task, original-holder-authorization, and successor
branches require `ready`; the bundled profile permits `not-required` only for
the current-portal-dependent previous-registration and partial-rights items.
An unresolved active proof item appears as a draft `WARNING` and blocks final
generation.
