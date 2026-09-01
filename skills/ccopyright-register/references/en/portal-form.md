# Portal form validation profile (English)

Profile ID: `ccpc-form-profile-v1`

## Purpose and boundary

This file records fields, choices, conditional branches, and UI counters
extracted from a form walkthrough during product design. It is a portal
compatibility profile for catching form problems early—not an official source,
legal rule, or screenshot evidence collection. The Skill bundles no raw form
images and records no attachment-receipt history.

Before final generation, use the [current official sources](official-sources.md)
and the portal actually reviewed by the applicant to update `requirements` in
`facts/application.json`, set the real `requirements.captured_at`, and confirm
`confirmations.requirements.current`. A current-portal conflict overrides this
profile for the application.

## Configured fields and choices

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

## Bundled validation gates

| Field | Configured limit |
|---|---:|
| Modification/translation/composition summary | 50 characters |
| Each of the six environment fields | 50 characters |
| Other programming languages | 120 characters |
| Purpose | 50 characters |
| Industry | 50 characters |
| Main functions | UI displays 500–1300 characters |
| Other technical features | 100 characters |

The `500–1300` range is a bundled compatibility gate; confirm current help text
and validation behavior. The profile does not establish the official
source-program counting definition. The default basis is physical lines in the
selected first-party source stream, with an explicit applicant-confirmed-total
alternative.

Draft generation reports minimum/maximum violations as `WARNING`; final
generation blocks until the applicant corrects the value or updates the profile
from the current portal. A minimum constrains supplied text only and does not by
itself make an optional field mandatory. Base and conditional rules determine
whether an empty field is required.

## Conditional branches

- `published` requires date, country, and region; `unpublished` does not.
- `modified` requires a summary of at most 50 characters and a registered/authorization-required basis.
- `successor` requires acquisition details; confirm the exact type and proof controls in the current portal.
- `partial` requires rights-scope details; confirm the exact rights choices in the current portal.
- `cooperative` configures review of a cooperative-development agreement PDF.
- `commissioned` configures review of a commissioned-development agreement PDF.
- `assigned-task` configures review of a project task document or ownership-contract PDF.
- A multiple-holder list must agree with the joint-ownership choice.
- General program deposit is configured as the first and last 30 consecutive source pages in PDF.
- General document deposit is configured as the first and last 30 consecutive pages of any one document in PDF and allows additional documents.
- Other related proof controls record readiness for additional PDFs.

Unresolved conditional fields and active proof-readiness items appear as draft
`WARNING` findings and block final generation. Proof files remain outside the
repository; only the finite readiness status is recorded. The skill does not
generate exceptional-deposit material. Selecting exceptional program or
document deposit stops the ordinary workflow.

## Not established by the profile

- PDF size, filename, orientation, and upload-count limits;
- complete help-tooltip text;
- full successor-acquisition and partial-rights branches;
- current exceptional-deposit requirements;
- later confirmation, signature, declaration, and submission pages;
- the current complete category, language, or feature choice lists.

## Privacy boundary

The worksheet retains only normalized rights-holder names needed for consistency. Country/region, entity type, and identity-document type may be manual review items, but never store identity numbers, identity scans, unredacted portal screenshots, signatures, credentials, or session data in the repository. Conditional proofs record external readiness only and are not copied into `.ccopyright/`.
