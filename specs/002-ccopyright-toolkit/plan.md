# Implementation Plan: Two-Skill Self-Service Toolkit

## Repository layout

~~~text
skills/
  ccopyright-qa/
    SKILL.md
    README.md
    README.en.md
    agents/openai.yaml
    references/
      zh-CN/
        answering-guide.md
        registration-baseline.md
        source-policy.md
        topic-map.md
      en/
        answering-guide.md
        registration-baseline.md
        source-policy.md
        topic-map.md
  ccopyright-register/
    ... existing self-contained preparation Skill ...
specs/
  001-ccopyright-skill/
  002-ccopyright-toolkit/
tools/build_skill_archives.py
tests/test_ccopyright.py
dist/
  ccopyright-qa.skill
  ccopyright-register.skill
~~~

## Skill boundary

`ccopyright-qa` is instruction-and-reference only. It performs no deterministic
file transformation, so it does not add scripts or assets. Its entrypoint routes
questions by topic, language, evidence currency, and requested outcome. It
loads only the relevant localized reference.

`ccopyright-register` retains repository assessment and material preparation.
Its existing CLI, schema, rendering, validation, and publication behavior do
not move into the QA Skill.

## QA reference design

- `answering-guide.md`: concise answer contract, neutrality, self-service and
  paid-service explanation, quote-breakdown behavior, and escalation.
- `source-policy.md`: official-source priority, date/currency requirements,
  citation behavior, validation-profile boundary, and conflict handling.
- `official-sources.md`: bilingual page-level official catalog added by
  specification 003.
- `topic-map.md`: question classification and routing to the minimum relevant
  reference or to `ccopyright-register`.
- `registration-baseline.md`: small dated ordinary-registration baseline from
  maintained official rules; the portal validation profile is explained as
  compatibility data rather than authority.

The baseline is duplicated only where an independently installed QA Skill needs
it. Maintainer instructions require updating the matching register reference
and both languages when a shared fact changes.

## Documentation

Rewrite the root Chinese and English READMEs as toolkit guides:

1. mission and neutrality;
2. choose-a-Skill table;
3. install QA, register, or both;
4. first prompts for each route;
5. per-Skill prerequisites;
6. user journey from question to preparation;
7. outputs and privacy boundaries;
8. source currency and FAQ.

Keep the installed `ccopyright-register` READMEs correct by replacing the old
“exactly one Skill” repository statement. Add concise installed READMEs for
`ccopyright-qa`.

Update `AGENTS.md` to make two Skills a product invariant, document the new
layout and parity rules, verify exactly two discovered Skills, test independent
and combined installations, build two archives, and remove Aone publication
from the active release gate for this iteration.

## Packaging

Refactor the deterministic archive builder around package configurations. Each
configuration supplies its Skill root, archive name, locales, and required
entries. The register archive includes its implementation and assets; the QA
archive contains only its own user and reference resources. The 2026-09-03
cleanup removes the legacy register `package.json`, including its personal
package name and private registry address, from the source and built archive.

Both archives receive a generated `PACKAGE-MANIFEST.json`, stable timestamps,
stable ordering, normalized file permissions, integrity testing, and SHA-256
reporting.

## Verification

1. Python unit and package tests.
2. Existing explicit Chromium/Poppler integration for register.
3. Official Skill validator against both source directories and both extracted
   archives.
4. skills.sh discovery showing exactly two names.
5. Disposable copy installations of QA alone, register alone, and both
   together; compare installed contents with canonical directories.
6. QA archive and register archive built twice with identical bytes and hashes.
7. ZIP integrity and required-entry checks for both archives.
8. README link and bilingual-navigation checks.
9. Privacy scan for retained screenshot paths, clipboard paths,
   identity-number-shaped data, credentials, bytecode, and placeholders.

## Migration and compatibility

- Existing `ccopyright-register` users keep the same Skill name and workflow.
- The root install command must select a Skill explicitly now that discovery
  returns two.
- Users may install both with one `--skill ccopyright-qa
  ccopyright-register` invocation, as supported by the current skills CLI.
- No `skills.sh.json` is required for discovery. A pack configuration can be a
  later product decision and is not introduced in this iteration.
- Aone/Contextlab synchronization and publishing remain outside this iteration.
  The legacy registry manifest and its coverage test have been removed; the
  existing archive test verifies that neither Skill ships `package.json`.
