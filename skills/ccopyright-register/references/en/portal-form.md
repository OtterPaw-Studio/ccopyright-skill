# Portal form field baseline (English)

## Evidence scope

This baseline comes from twelve China Copyright Protection Center software-registration form screenshots supplied by the user on 2026-08-31. Their original capture date is unknown and their coverage is partial. The skill does not retain the images; one contained personal identity data, and neither the applicant name nor identity number was retained in this analysis.

This file records only visible fields, choices, conditional branches, and UI limits. Before final generation, update `requirements` in `facts/application.json` from the current portal, set `requirements.captured_at`, and have the applicant confirm `confirmations.requirements.current`.

## Visible fields and choices

- Rights acquisition: `original` or `successor`.
- Required full name and version; optional short name. Leave the short name empty rather than entering a placeholder for “none.”
- Rights scope: `all` or `partial`.
- Software category: `application`, `embedded`, `middleware`, or `operating-system`.
- Software description: `original` or `modified`, where modified includes translated or composite software.
- Development type: `independent`, `cooperative`, `commissioned`, or `assigned-task`.
- Completion date and publication status; published software exposes first-publication date, country, and region.
- Six environment fields: development hardware, runtime hardware, development OS, development tools, runtime platform/OS, and supporting software.
- Programming languages, source-program line count, purpose, industry, and main functions.
- Technical-feature tags plus other text. Visible tags include APP, games, education, finance, medical, geographic information, cloud computing, information security, big data, AI, VR, 5G, mini programs, IoT, and smart city.
- Independent general/exceptional deposit choices for program and document materials.
- Rights-holder list and a joint-ownership yes/no choice.

## Visible limits

| Field | Visible limit |
|---|---:|
| Modification/translation/composition summary | 50 characters |
| Each of the six environment fields | 50 characters |
| Other programming languages | 120 characters |
| Purpose | 50 characters |
| Industry | 50 characters |
| Main functions | UI displays 500–1300 characters |
| Other technical features | 100 characters |

The `500–1300` range comes from the visible counter; confirm the current help text and validation behavior. The screenshots do not expose the source-line counting definition. The default basis is physical lines in the selected first-party source stream, with an explicit applicant-confirmed-total alternative.

## Conditional branches

- `published` requires date, country, and region; `unpublished` does not.
- `modified` requires a summary of at most 50 characters and a registered/authorization-required basis.
- `cooperative` exposes a cooperative-development agreement PDF upload.
- `commissioned` exposes a commissioned-development agreement PDF upload.
- `assigned-task` exposes a project task document or ownership-contract PDF upload.
- A multiple-holder list must agree with the joint-ownership choice.
- General program deposit visibly requests the first and last 30 consecutive source pages as PDF.
- General document deposit visibly requests the first and last 30 consecutive pages of any one document as PDF and allows additional documents.
- Other related proof controls allow additional PDFs.

The skill does not generate exceptional-deposit material. Selecting exceptional program or document deposit stops the ordinary workflow.

## Not established by these screenshots

- PDF size, filename, orientation, and upload-count limits;
- complete help-tooltip text;
- full successor-acquisition and partial-rights branches;
- current exceptional-deposit requirements;
- later confirmation, signature, declaration, and submission pages;
- additional category, language, or feature choices not shown here.

## Privacy boundary

The worksheet retains only normalized rights-holder names needed for consistency. Country/region, entity type, and identity-document type may be manual review items, but never store identity numbers, identity scans, unredacted portal screenshots, signatures, credentials, or session data in the repository. Conditional proofs record external readiness only and are not copied into `.ccopyright/`.
