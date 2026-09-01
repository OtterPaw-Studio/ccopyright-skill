# Repository maintenance guide

This file is for coding agents and maintainers. The root Chinese and English READMEs are user-facing and must not become build or contributor manuals.

## Product invariants

- Ship one Skill named <code>ccopyright-register</code>.
- Keep one bilingual instruction set and one deterministic implementation.
- Precheck severity is exactly <code>INFO</code> and <code>WARNING</code>.
- Do not add browser form filling, submission, progress tracking, or correction-notice parsing.
- Only ordinary, non-classified deposit is supported.
- Never retain identity numbers, identity scans, signatures, credentials, session data, or user-supplied unredacted portal screenshots.
- Treat current portal evidence as dated and partial; do not turn a screenshot observation into a permanent legal rule.

## Source layout

~~~text
skills/ccopyright-register/
  SKILL.md                   installed instruction entrypoint
  package.json               Aone/Contextlab package metadata and file allowlist
  README.md                  installed Chinese user guide (primary)
  README.en.md               installed English user guide
  agents/openai.yaml         UI metadata and invocation policy
  scripts/                   canonical CLI and implementation
  assets/                    canonical template and print CSS
  references/en/             English workflow references
  references/zh-CN/          Chinese workflow references
tools/build_skill_archives.py
tests/test_ccopyright.py
specs/001-ccopyright-skill/
dist/ccopyright-register.skill
~~~

The directory under <code>skills/ccopyright-register/</code> is the canonical, self-contained Skill source used by both skills.sh and the archive builder. Do not edit generated archive contents by hand.

## Documentation rules

- Keep <code>README.md</code> and <code>README.en.md</code> semantically aligned; Chinese is the primary language.
- Keep the two installed READMEs under <code>skills/ccopyright-register/</code> aligned as well.
- Root READMEs lead with user outcome, skills.sh installation, first prompts, prerequisites, workflow, outputs, and safety.
- Put build, test, packaging, and contributor instructions here instead of moving them back into the user quick start.
- Keep the documented skills.sh source aligned with the canonical origin, <code>OtterPaw-Studio/ccopyright-skill</code>.
- Update both language reference files when portal fields, constraints, or workflow behavior changes.

## skills.sh compatibility

The supported source layout is a nested Skill:

~~~text
skills/ccopyright-register/SKILL.md
~~~

Verify repository discovery with:

~~~bash
npx skills@latest add . --list
~~~

Expected result: exactly one discovered skill named <code>ccopyright-register</code>.

Verify a local project installation in a disposable directory before release. Select the Skill explicitly:

~~~bash
npx skills@latest add /absolute/path/to/ccopyright-skill \
  --skill ccopyright-register \
  --agent codex \
  --copy \
  --yes
~~~

A root <code>skills.sh.json</code> is not needed while the repository contains one Skill. The file controls repository-page grouping, not discovery or installation. Add it only if multiple public skills need curated grouping.

## Aone / Contextlab compatibility

Keep <code>SKILL.md</code> compatible with the Codex validator: its frontmatter
contains <code>name</code> and <code>description</code>, not Aone-only top-level
<code>version</code> or <code>files</code> keys. The adjacent
<code>package.json</code> owns the Aone package version and explicit
<code>files</code> allowlist used by Git synchronization.

Before publishing an Aone version, increment <code>package.json.version</code>
and verify the package contents from the Skill directory:

~~~bash
npm pack --dry-run --json --cache /tmp/ccopyright-npm-cache
~~~

The package must contain both READMEs, <code>agents/</code>,
<code>assets/</code>, <code>references/</code>, and <code>scripts/</code>, in
addition to <code>SKILL.md</code> and the generated/included
<code>package.json</code>. Published Contextlab versions are immutable: a Git
sync does not retrofit missing files into an existing version, so sync and
publish a higher version after changing this manifest.

## Editing and implementation

- Use <code>skills/ccopyright-register/assets/application.template.json</code> as the schema template.
- Preserve schema migration for existing workspaces.
- Keep <code>facts/application.json</code> as the only user-editable application fact source.
- Keep repository suggestions unconfirmed.
- Preserve source rows, blanks, comments, tabs, order, and path/line/hash traceability.
- Do not follow symlinks or include dependencies/generated output by default.
- Keep proof documents outside the generated workspace; record readiness metadata only.
- Draft mode may show unresolved markers. Final mode must reject missing confirmations and unresolved material constraints.

## Verification

Run unit and package tests without writing bytecode caches:

~~~bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p test_ccopyright.py -v
~~~

Run the real Chromium/Poppler integration when local tools are available:

~~~bash
CCOPYRIGHT_RUN_PDF_INTEGRATION=1 PYTHONDONTWRITEBYTECODE=1 \
  python -m unittest discover -s tests -p test_ccopyright.py \
  -k PdfIntegrationTests -v
~~~

Build the deterministic archive twice and compare the reported SHA-256 values:

~~~bash
python tools/build_skill_archives.py
python tools/build_skill_archives.py
~~~

Extract <code>dist/ccopyright-register.skill</code> to a temporary directory and run the official skill-creator <code>quick_validate.py</code> against the extracted root. Also verify:

- ZIP integrity;
- one <code>SKILL.md</code> at archive root;
- both installed READMEs and both localized reference sets;
- no deprecated <code>ccopyright.skill</code> or <code>软著.skill</code>;
- no bytecode, temporary screenshots, local clipboard paths, or identity-number-shaped data.

## Release checklist

1. Update spec, plan, and task status for behavior changes.
2. Run unit/package tests and the explicit PDF integration test.
3. Run the skills.sh discovery and disposable installation checks.
4. Rebuild the archive twice and compare hashes.
5. Run the npm dry-run and inspect the Aone/Contextlab package file list.
6. Run the official Skill validator on the extracted archive.
7. Review all four READMEs for user/developer separation and bilingual parity.
8. Report the archive path, size, hash, validation results, and canonical publication source.
