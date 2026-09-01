# Implementation Plan: Official Sources and Portal Validation Profile

## 1. Record the iteration

Create this spec, plan, and task list before changing runtime behavior. Treat
the earlier form walkthrough as design input only and make the new terminology
normative for both Skills.

## 2. Strengthen QA sources

Add localized `official-sources.md` catalogs containing direct page-level
official links for the guide index, application notes, steps, required files,
form instructions, approval flow, processing time, registration institution,
FAQ pages, fee notice, registration measures, Software Protection Regulations,
and Copyright Law.

Update QA routing so factual operational questions read the catalog first.
Revise its source policy and answer guide around the four source classes in the
spec. Keep current, explicitly supplied portal text usable for the current
question, but do not treat historic design attachments as evidence.

## 3. Migrate register facts

Advance the application schema to version 3. Replace
`requirements.portal_evidence` with a simple
`requirements.portal_validation_profile` ID. Reject future schemas before any
mutation. Remove the legacy evidence object from every supported schema, merge
missing defaults, and then restore applicant-owned limit/minimum maps exactly
so custom values and removed default gates remain effective.

Rewrite the generated requirements snapshot to show:

- current portal review date and applicant confirmation;
- the non-authoritative profile ID and override rule;
- direct official source URLs;
- configured page, row, format, field-length, and unresolved constraints.

Render the union of minimum and maximum gates, validate their dotted paths and
ranges, emit draft warnings for field, branch, and conditional proof-readiness
violations, and retain final-mode blocking. Limit readiness to explicit finite
statuses and keep every proof file outside the repository.

## 4. Align documentation

Update both localized register source/schema/workflow/quality references, all
four installed READMEs, both root READMEs, `SKILL.md` entrypoints, and
`AGENTS.md`. Preserve references to real product screenshots used in a software
manual; only portal-form design-input terminology changes.

Add a short superseding note or corrected wording to specs 001 and 002 so the
repository has one consistent source model.

## 5. Extend tests and packaging

Test the v2-to-v3 migration with a legacy evidence object and custom field
limits. Assert that generated snapshots include the profile ID and exclude
legacy screenshot history. Require both localized QA official-source files in
the deterministic package builder and archive tests. Add documentation
regression checks for the old evidence phrases.

## 6. Validate and review

Run the ordinary Python suite and explicit PDF integration, validate both Skill
sources and extracted archives, discover exactly two Skills, install QA,
register, and both in disposable directories, build archives twice and compare
hashes, and run privacy/residue scans. Request a focused code review, address
findings, then record the validation results in this iteration.
