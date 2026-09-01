# Official Sources and Portal Validation Profile Specification

Status: Implemented and validated
Date: 2026-09-01

## Background

The Q&A Skill needs stronger page-level official grounding. Its first version
contained one precise registration rule and the official portal entry point,
but did not systematically route questions to the China Copyright Protection
Center's application guide, form instructions, required-files page, processing
page, FAQ, and notices.

The form walkthrough images previously supplied during product design had a
different purpose: they helped identify fields, choices, conditional branches,
and visible character counters for the registration-preparation workflow. They
were not submitted as sources to cite, are not part of the Skill, and must not
be represented as evidence or an auditable screenshot baseline.

## Goals

1. Add a small bilingual catalog of page-level official sources for
   `ccopyright-qa`.
2. Make answers distinguish an official rule, an official guide/FAQ, current
   portal content, and third-party material or inference.
3. Preserve useful form fields, branches, and length limits as a versioned
   portal validation profile rather than screenshot evidence.
4. Let QA explain the bundled profile with a currency caveat and let register
   enforce it deterministically.
5. Migrate existing register workspaces without losing applicant facts or
   current validation values.

## Non-goals

- No claim ledger, source database, or per-sentence evidence matrix.
- No automatic crawling, synchronization, refresh scheduler, OCR, image hash,
  screenshot retention, or redaction pipeline.
- No browser form filling, submission, progress tracking, or correction-notice
  parsing.
- No provider-price database or large evaluation framework.
- No legal conclusion or acceptance guarantee.

## Source model

QA uses these basis classes:

1. **Official rule** — legislation, administrative regulation, or department
   rule from an authoritative government source.
2. **Official guide or FAQ** — an operational page published by the China
   Copyright Protection Center, cited with its direct link and access date.
3. **Current portal content** — current field/help text reviewed for the user's
   application or explicitly supplied for the current question. It can
   supersede the bundled compatibility profile for that application.
4. **Third-party material or inference** — useful only for explaining that
   source's own claim or as clearly labeled guidance; it cannot establish an
   official requirement by itself.

The official-source catalog is intentionally Markdown, bilingual, and small.
It records page title, direct URL, scope, source class, review date, and a
currency note. Pages without a visible publication/update date record only the
actual access date.

## Portal validation profile

The register Skill stores `requirements.portal_validation_profile` together
with the existing `portal_field_limits`, `portal_field_minimums`, conditional
checks, and `portal_unknowns`.

The profile is implementation compatibility data:

- it is not an official source or legal rule;
- it does not retain or refer to source images, receipt history, identity data,
  or local attachment paths;
- it can be updated from the current portal after applicant review;
- unresolved operational details remain explicit in `portal_unknowns`.

Draft generation shows profile, conditional-field, and active proof-readiness
violations as warnings. Final generation rejects unresolved minimum/maximum,
conditional-field, and proof-readiness violations. Gate keys must resolve to
string facts, a minimum cannot exceed its maximum, and a minimum-only gate
constrains supplied text without making an otherwise optional field mandatory.

## Schema migration

`facts/application.json` advances from schema version 2 to version 3.

- Add `requirements.portal_validation_profile` with the bundled profile ID.
- Remove legacy `requirements.portal_evidence` from every supported schema,
  including a partially migrated file already labeled version 3.
- Preserve all applicant-provided software facts, confirmations, portal review date,
  source URLs, field limits/minimums, and unknowns.
- Treat existing limit/minimum maps as applicant-owned configuration, so a
  removed default gate remains removed when the workspace is reopened.
- Reject a schema newer than version 3 before applying any migration or
  defaults.
- Re-running `init` or `status` performs the migration in place without
  replacing user facts.

## Documentation changes

- Add `official-sources.md` in both QA reference locales.
- Update QA routing, source policy, answer contract, and user READMEs.
- Reframe register `portal-form.md` as a validation profile and update its
  schema, workflow, official-source, quality, and user documentation.
- Update root READMEs and `AGENTS.md` so maintainers do not regress to the old
  screenshot-evidence model.
- Correct earlier specs where the design inputs were inaccurately described as
  evidence, while retaining their historical implementation record.

## Acceptance criteria

1. QA archives contain both localized official-source catalogs and route
   current operational questions to them.
2. No maintained text or generated requirements snapshot claims that the form
   walkthrough images are evidence, a received screenshot set, or an audit
   baseline.
3. A schema-v2 workspace containing legacy `portal_evidence` upgrades to v3,
   removes that object, adds the profile ID, and preserves custom applicant
   values and field constraints; a supported schema-v3 file cannot retain the
   legacy object either.
4. The generated requirements snapshot names the portal validation profile,
   labels it non-authoritative, lists sources and configured gates, and contains
   no screenshot receipt/privacy history.
5. Existing length and conditional checks continue to warn in draft contexts
   and block final generation; cooperative, commissioned, assigned-task,
   modified, successor, and partial-rights proof items also require an allowed
   finite readiness status before final generation.
6. Both Skills pass tests, official validation, skills.sh discovery and
   disposable installation; both deterministic archives build identically
   twice and pass privacy/residue checks.
7. Minimum-only custom gates render in the requirements snapshot, invalid gate
   paths and inverted ranges are rejected, and published/modified/successor/
   partial branch gaps are visible as draft warnings.
8. Malformed requirement values are returned as validation errors by `status`
   rather than causing an uncaught renderer exception.

## Definition of done

The specification, plan, and tasks are complete; bilingual sources and docs are
aligned; schema migration and validation-profile behavior are tested; packaging
requires the new references; and all repository release checks pass.

## Validation record

Validated on 2026-09-01:

- Official source correction: the maintained Software Protection Regulations
  link is the Ministry of Justice [consolidated text containing the 2011 and
  2013 revisions](https://xzfg.moj.gov.cn/mobile/law/detail?LawID=581).
- Python suite: 32 tests ran; 31 passed and the opt-in PDF integration test was
  skipped as designed.
- Chromium/Poppler integration: the separately enabled PDF integration test
  passed.
- Official Skill validator: both source directories and both final extracted
  archives returned `Skill is valid!`.
- skills.sh: exactly two Skills were discovered; QA-only, register-only, and
  combined copied installations succeeded and matched the canonical sources
  byte for byte. Installed register preflight found Python, Chromium, Poppler,
  and Git.
- Archive repeatability: two consecutive builds produced identical sizes and
  SHA-256 values. `ccopyright-qa.skill` is 31,048 bytes with SHA-256
  `4e5c3617cd9fdeadcf5931e5792cf838a740eddad6ca142f50cd9e3c5e28a0ca`;
  `ccopyright-register.skill` is 82,030 bytes with SHA-256
  `e5b282fcecfa5390c65743ab97edb03c6d8bca118f36e672d97a7595d3fffb24`.
- ZIP integrity, package-manifest hashes, local links, privacy patterns,
  clipboard paths, bytecode residue, and deprecated archive names passed their
  checks.
- A complete-worktree review found and fixed conditional-proof final gating,
  residual schema-v3 portal evidence, stale register packaging, and malformed
  requirement handling. The follow-up review reported no remaining critical,
  important, or minor issue.
