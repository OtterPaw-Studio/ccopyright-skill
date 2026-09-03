# Repository maintenance guide

This file is for coding agents and maintainers. Root and installed READMEs are
user-facing; do not turn them into build or contributor manuals.

## Product invariants

- Ship exactly two independently installable Skills:
  <code>ccopyright-qa</code> and <code>ccopyright-register</code>.
- Keep Chinese as the primary documentation language and maintain semantically
  aligned English guidance for both Skills.
- Preserve the shared mission: reduce information asymmetry so applicants can
  understand official work, self-service work, paid assistance, and specialist
  limits before making a choice.
- Stay neutral about third-party services. Do not claim that all service fees
  are unnecessary, repeat an observed quote as a current market price, or
  guarantee that self-service is suitable for every applicant.
- <code>ccopyright-qa</code> is read-only. It does not scan repositories, create
  workspaces, generate files, or inherit write permission from a question.
- <code>ccopyright-register</code> owns repository assessment and material
  preparation. Its precheck severity is exactly <code>INFO</code> and
  <code>WARNING</code>.
- Do not add browser form filling, submission, signing, payment, account
  operation, progress tracking, or correction-notice parsing to either Skill.
- Only ordinary, non-classified deposit is supported by the preparation Skill.
- Never retain identity numbers, identity scans, signatures, credentials,
  payment/session data, or user-supplied unredacted portal screenshots.
- Treat form-walkthrough attachments as one-time design inputs, not evidence.
  Retain only their structured field/branch/limit configuration; do not retain,
  cite, count, date, hash, or build an audit history for the images.
- Treat the portal validation profile as non-authoritative compatibility data.
  Current official pages and the applicant-reviewed portal can supersede it.
- Neither Skill provides legal advice, decides ownership or contract effect, or
  guarantees registration.

## Source layout

~~~text
skills/
  ccopyright-qa/
    SKILL.md                   read-only Q&A entrypoint
    README.md                  installed Chinese Q&A guide (primary)
    README.en.md               installed English Q&A guide
    agents/openai.yaml         UI metadata and invocation policy
    references/en/             English answering/source/topic/official-page references
    references/zh-CN/          Chinese answering/source/topic/official-page references
  ccopyright-register/
    SKILL.md                   preparation entrypoint
    README.md                  installed Chinese preparation guide (primary)
    README.en.md               installed English preparation guide
    agents/openai.yaml         UI metadata and invocation policy
    scripts/                   canonical CLI and implementation
    assets/                    canonical template and print CSS
    references/en/             English preparation references
    references/zh-CN/          Chinese preparation references
tools/build_skill_archives.py
tests/test_ccopyright.py
specs/001-ccopyright-skill/
specs/002-ccopyright-toolkit/
specs/003-qa-official-sources/
dist/ccopyright-qa.skill
dist/ccopyright-register.skill
~~~

Each directory under <code>skills/</code> is a canonical, self-contained Skill
source. A selected skills.sh installation must not depend on a sibling Skill or
repository-root runtime file. Do not edit generated archive contents by hand.

## Responsibility boundary

Route explanation, ordinary requirement questions, self-service decisions, and
redacted quote breakdowns to <code>ccopyright-qa</code>. Route repository
inventory, facts, source selection, material generation, rendering, validation,
and revision packaging to <code>ccopyright-register</code>.

For mixed requests, answer enough to support an informed decision first. Before
starting preparation, explain the write scope and obtain the user's agreement.
Loading or invoking the QA Skill never authorizes repository writes.

## Documentation rules

- Keep root <code>README.md</code> and <code>README.en.md</code> semantically
  aligned; Chinese is primary.
- Keep each installed <code>README.md</code>/<code>README.en.md</code> pair
  aligned. There are six user-facing README files in total.
- Root READMEs lead with mission, Skill selection, individual/combined
  installation, first prompts, per-Skill prerequisites, user journey, source
  currency, outputs, and safety.
- Keep contributor, testing, packaging, and release instructions here.
- Keep the documented skills.sh source
  <code>OtterPaw-Studio/ccopyright-skill</code> aligned in all user guides.
- When a shared ordinary-registration fact changes, update both QA languages
  and the corresponding register references. Keep the independent Skills
  self-contained even when that requires a small duplicated dated baseline.
- Keep the localized QA <code>official-sources.md</code> catalogs semantically
  aligned. Record direct official URLs, source class, scope, actual access date,
  and currency boundary; do not invent a publication date when a page shows
  none.
- Current fees, channels, fields, choices, upload constraints, timelines, and
  provider offerings require dated current evidence. Do not write them from
  memory into a README or reference.
- Provider names or prices observed by a user are case evidence, not permanent
  product facts or current market benchmarks.

## skills.sh compatibility

The repository uses two nested Skill entrypoints:

~~~text
skills/ccopyright-qa/SKILL.md
skills/ccopyright-register/SKILL.md
~~~

Verify discovery:

~~~bash
npx skills@latest add . --list
~~~

Expected result: exactly two Skills named <code>ccopyright-qa</code> and
<code>ccopyright-register</code>.

Verify each Skill independently in disposable directories:

~~~bash
npx skills@latest add /absolute/path/to/ccopyright-skill \
  --skill ccopyright-qa \
  --agent codex \
  --copy \
  --yes

npx skills@latest add /absolute/path/to/ccopyright-skill \
  --skill ccopyright-register \
  --agent codex \
  --copy \
  --yes
~~~

Verify a combined installation. Current skills CLI accepts multiple names after
one <code>--skill</code> flag:

~~~bash
npx skills@latest add /absolute/path/to/ccopyright-skill \
  --skill ccopyright-qa ccopyright-register \
  --agent codex \
  --copy \
  --yes
~~~

The installed copies must match their canonical source directories before any
runtime command generates local caches. Run the installed register CLI
<code>preflight</code>; QA intentionally has no script smoke test.

A root <code>skills.sh.json</code> is not required for discovery. Do not add a
pack or grouping file unless a later requirement explicitly defines curated
pack behavior.

## QA editing rules

- Keep <code>ccopyright-qa</code> instruction-and-reference only unless a future
  repeated deterministic operation clearly justifies a script.
- Preserve the answer contract: direct answer, evidence type/date, material
  conditions, uncertainty, self-service next step, and paid-help scope when
  relevant. Do not force a long template on a one-fact question.
- Classify each QA basis as an official rule, official guide/FAQ with access
  date, current portal content explicitly reviewed for the question, or
  third-party material/inference. Use the page-level official catalog.
- The register portal validation profile is not QA evidence. It can explain a
  local gate only with a non-authoritative/current-portal caveat.
- Search snippets and provider marketing may locate or describe a source but do
  not establish an official requirement.
- Analyze only redacted user-supplied quotes by default. Current cross-provider
  price research requires an explicit user request and current evidence.
- Never add legal risk scores. QA explains basis and uncertainty in plain
  language; register prechecks remain the only INFO/WARNING classification.
- Route file-generation requests to <code>ccopyright-register</code>; do not
  reproduce its workflow in QA.

## Register editing rules

- Use
  <code>skills/ccopyright-register/assets/application.template.json</code> as
  the schema template and preserve migration for existing workspaces.
- Schema v3 uses <code>requirements.portal_validation_profile</code> and must
  remove legacy <code>requirements.portal_evidence</code> without losing user
  facts, field limits, minimums, unknowns, or confirmations.
- Keep <code>facts/application.json</code> as the only user-editable canonical
  application fact source.
- Keep repository suggestions unconfirmed.
- Preserve source rows, blanks, comments, tabs, order, and path/line/hash
  traceability.
- Do not follow symlinks or include dependencies/generated output by default.
- Keep proof documents outside the generated workspace; record readiness
  metadata only.
- Draft mode may show unresolved markers. Final mode must reject missing
  confirmations and unresolved material constraints.

## Aone / Contextlab status

Aone/Contextlab synchronization and publication are outside the active
two-Skill iteration. The legacy register <code>package.json</code> has been
removed; neither installable Skill requires an npm/registry manifest. Keep
personal publisher identifiers and private registry configuration out of both
Skill directories. Do not synchronize or publish unless the user explicitly
resumes that work.

## Deterministic archives

<code>tools/build_skill_archives.py</code> builds both archives from their
canonical directories. It must:

- reject symlinks;
- ignore bytecode and machine metadata;
- require each Skill's entrypoint, UI metadata, both installed READMEs, and both
  localized reference sets;
- include register scripts/assets without a registry <code>package.json</code>;
- write stable timestamps, ordering, permissions, manifests, and hashes;
- remove deprecated <code>ccopyright.skill</code> and
  <code>软著.skill</code> outputs.

Build twice and compare every reported hash:

~~~bash
python tools/build_skill_archives.py
python tools/build_skill_archives.py
~~~

Expected outputs are <code>dist/ccopyright-qa.skill</code> and
<code>dist/ccopyright-register.skill</code>.

## Verification

Run ordinary tests without bytecode caches:

~~~bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover \
  -s tests -p test_ccopyright.py -v
~~~

Run the real register PDF integration when Chromium and Poppler are available:

~~~bash
CCOPYRIGHT_RUN_PDF_INTEGRATION=1 PYTHONDONTWRITEBYTECODE=1 \
  python -m unittest discover -s tests -p test_ccopyright.py \
  -k PdfIntegrationTests -v
~~~

Run the official skill-creator <code>quick_validate.py</code> against both
source directories and both extracted archive roots. Also verify:

- ZIP integrity for both archives;
- one <code>SKILL.md</code> at each archive root;
- QA has no accidental script/runtime dependency;
- register contains its canonical scripts and assets;
- all local README links resolve;
- exactly two skills.sh discovery results;
- QA-only, register-only, and combined copied installations;
- installed register <code>preflight</code> execution;
- no placeholder text, bytecode, retained portal-form design images, clipboard/temp paths,
  credentials, or identity-number-shaped data.

## Release checklist

1. Update the applicable spec, plan, and task statuses.
2. Review responsibility routing and all six user-facing READMEs.
3. Run ordinary and explicit PDF tests.
4. Run skills.sh discovery plus QA-only, register-only, and combined installs.
5. Build both archives twice and compare hashes.
6. Run both source and extracted-archive Skill validators.
7. Check ZIP integrity, README links, package contents, and privacy patterns.
8. Report both archive paths, sizes, hashes, validation results, and canonical
   skills.sh publication source.
