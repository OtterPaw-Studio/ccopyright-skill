# Software Copyright Self-Service Toolkit Specification

Status: Implemented and validated
Date: 2026-09-01
Packaging cleanup: 2026-09-03, validated

## Background

The repository began as one material-preparation Skill. The product goal is
broader: reduce information asymmetry around China computer-software copyright
registration so applicants can understand the public process, decide what they
can complete themselves, and know what work a paid service is actually adding.

The project must not replace one sales narrative with another. A third-party
service may provide legitimate convenience, drafting, communication, or manual
work. The toolkit does not label all service fees as unnecessary, quote a
market price from memory, or promise that self-service is suitable for every
case. It makes requirements, evidence, uncertainty, and choices inspectable.

User-observed provider prices motivated this iteration but are not a maintained
market-price fact. Vendor names and price ranges must not be repeated as current
claims unless checked against dated primary evidence for the specific answer.

## Product model

The repository ships exactly two independently installable Skills:

| Skill | User intent | Default behavior |
|---|---|---|
| `ccopyright-qa` | Understand requirements, fields, materials, self-service feasibility, or a supplied service quote | Read-only explanation with dated evidence and uncertainty |
| `ccopyright-register` | Assess a repository or prepare, render, validate, and package registration materials | Repository workflow using applicant-confirmed facts |

The two Skills share a mission and safety boundaries, but not runtime file
dependencies. Installing either Skill alone must produce a usable package.

## Goals

1. Add a lightweight question-answering entry point for applicants who are not
   ready to generate materials.
2. Explain which work follows from official requirements, which work can often
   be self-completed, and which work is optional paid assistance.
3. Route material-generation requests to `ccopyright-register` without making
   `ccopyright-qa` scan or write to a repository.
4. Preserve the existing registration-preparation behavior and safety model.
5. Present the repository as a two-Skill self-service toolkit in the Chinese
   primary README and aligned English README.
6. Keep both Skills discoverable and independently selectable through
   skills.sh.

## `ccopyright-qa` scope

### In scope

- Explain ordinary computer-software copyright registration concepts and the
  visible application-field model.
- Explain ordinary program and document identification materials.
- Explain conditional proof categories at a non-legal, checklist level.
- Help the user distinguish an official requirement from a convenience service,
  a provider claim, or an unresolved current-portal detail.
- Break down a quote or service description supplied by the user into described
  work items without judging the provider's motives or contract enforceability.
- Help the user decide whether to continue learning, prepare materials with
  `ccopyright-register`, or seek qualified human assistance.
- Answer in Chinese or English and use Chinese for registration-facing labels
  unless the user asks for translation.

### Out of scope

- Repository scanning, `.ccopyright/` creation, source selection, document
  generation, rendering, validation, or packaging.
- Browser form filling, submission, signing, payment, account operation,
  progress tracking, or correction-notice parsing.
- Legal advice, ownership adjudication, contract review, guaranteed outcomes,
  success-rate claims, or provider accusations.
- Scraping or maintaining a vendor-price leaderboard.
- Stating current official fees, processing time, portal fields, or upload
  constraints without a dated source or an explicit uncertainty label.
- Requesting or retaining identity numbers, identity scans, signatures,
  credentials, session data, or unredacted portal screenshots.

## Intent routing

Use `ccopyright-qa` for questions such as:

- “软件简称可以不填吗？”
- “开发完成日期应当怎么理解？”
- “我一定要找代理吗？”
- “这份服务报价具体替我做了什么？”
- “前后各连续 30 页是什么意思？”

Use `ccopyright-register` when the user asks to inspect a repository, create a
workspace, prepare a worksheet, select source, generate PDFs, validate existing
materials, or publish a reviewed revision.

If one request contains both intents, answer the conceptual question first,
then obtain the user's agreement before beginning any repository-writing
workflow. Loading the QA Skill never grants permission to write files.

## QA answer contract

Adapt the length to the question, but preserve these decisions:

1. Lead with a direct answer.
2. Identify whether the basis is an official rule, an official guide/FAQ with
   access date, current portal content reviewed for this question, or
   third-party material/inference.
3. Explain applicable conditions and what remains unknown.
4. State what the applicant can do next without purchasing a service.
5. When relevant, explain what human or paid assistance may add without
   portraying it as officially mandatory.
6. Route to `ccopyright-register` only when the user wants material work.

Do not force every short answer into a long template. A one-fact question may
need only a concise answer, its basis, and a currency caveat.

## Evidence and currency

Use the source that directly supports the claim:

1. Current official legislation, regulations, and rules for legal/material
   baselines.
2. Specific China Copyright Protection Center guides and FAQs for public
   operating guidance.
3. Current authenticated portal text or redacted current text explicitly
   supplied for this question for dynamic UI behavior.
4. Third-party material or inference only for that source's own claim or as
   clearly labeled guidance.

The maintained legal baseline includes the official Measures for Computer
Software Copyright Registration. It supports the ordinary material categories,
program/document definition, consecutive-page baseline, proof categories, A4
format, and the existence of exceptional deposit. The current portal controls
operational details that are not established by that rule.

The earlier form walkthrough was design input only. Specification 003 preserves
its extracted fields, branches, and limits as a non-authoritative portal
validation profile; the attachments are not Q&A evidence or a source to cite.

## Safety and neutrality

- Do not claim that every third-party service is an information scam.
- Do not call a fee reasonable or unreasonable without a defined scope and
  evidence; explain the purchased work instead.
- Do not promise “zero-cost acceptance,” “guaranteed registration,” or similar
  outcomes.
- Do not infer ownership, permission to disclose source, completion dates, or
  publication facts.
- When a question turns on disputed ownership, a contract, classified material,
  exceptional deposit, or another specialist issue, state the limit and suggest
  qualified human help.

## User stories and acceptance criteria

### US1: Understand a requirement

As an applicant, I can ask a plain-language question and receive a direct,
source-aware explanation without starting a repository workflow.

- The answer separates known requirements from uncertain portal details.
- Time-sensitive claims include a source date or an explicit need to verify.
- The Skill does not create files or ask for sensitive identity data.

### US2: Decide whether to self-serve

As an applicant, I can understand which steps I can perform myself and what a
paid service may add.

- The answer describes work items rather than declaring all services valuable
  or worthless.
- Official requirements are not confused with a provider's bundled offering.
- The answer never guarantees acceptance.

### US3: Understand a supplied quote

As an applicant, I can provide a redacted quote and receive a neutral breakdown.

- The Skill analyzes only supplied, non-sensitive terms unless current vendor
  research is explicitly requested and available.
- It marks missing scope, deliverables, assumptions, and outcome promises for
  clarification without making a legal contract determination.
- It does not retain identity, account, signature, or payment information.

### US4: Move from learning to preparation

As an applicant, I can be routed from an answer to the existing preparation
workflow when I decide to proceed.

- `ccopyright-qa` names `ccopyright-register` and explains why it is the next
  Skill.
- It does not imply that the preparation Skill has already scanned or changed
  the repository.
- `ccopyright-register` remains independently installable and behaviorally
  unchanged unless this iteration explicitly updates shared documentation.

### US5: Install the toolkit

As a user, I can discover exactly two Skills and install either one or both.

- skills.sh discovery returns `ccopyright-qa` and `ccopyright-register` only.
- Each installed directory contains its own `SKILL.md`, localized guidance,
  UI metadata, and user README files.
- Both Skill entrypoints pass the official Skill validator.
- The deterministic archive builder produces one `.skill` archive per Skill.
- Neither installed Skill nor its archive contains a registry `package.json`;
  Skill identity and discovery remain in `SKILL.md`.

## Non-functional requirements

- Chinese remains the primary documentation language; English content remains
  semantically aligned.
- `ccopyright-qa` needs no Python, browser, or PDF dependency for ordinary use.
- References are loaded progressively by topic and language.
- No Skill depends on files outside its own directory after installation.
- Archive builds are deterministic and reject symlinks.
- The repository contains no retained screenshots, identity-number-shaped data,
  credentials, or generated Python bytecode.
- Aone/Contextlab synchronization and publication are outside this iteration.

## Definition of done

This iteration is complete when the new spec, plan, and tasks are recorded;
`ccopyright-qa` is implemented with bilingual user guidance and references;
root documentation and maintainer instructions describe the two-Skill product;
skills.sh discovers and installs both Skills independently and together; both
entrypoints validate; both deterministic archives build twice with identical
hashes; and the test and privacy checks pass.

## Validation record

This is the original validation record for specification 002. The subsequent
official-source/schema-v3 baseline is recorded in
[specification 003](../003-qa-official-sources/spec.md#validation-record).

Validated on 2026-09-01:

- Python suite: 23 tests ran in the ordinary invocation; 22 passed and the
  opt-in PDF integration test was skipped as designed.
- Chromium/Poppler integration: the explicit PDF integration test passed.
- Official Skill validator: both source directories and both extracted archive
  roots returned `Skill is valid!`.
- skills CLI 1.5.23 discovery: exactly `ccopyright-qa` and
  `ccopyright-register` were found.
- skills.sh installation: QA alone, register alone, and both together completed
  successfully with `--agent codex --copy --yes`; installed contents matched
  the canonical Skill directories byte for byte.
- Installed register preflight: Python, Chromium, `pdfinfo`, `pdftotext`,
  `pdftoppm`, and Git were available.
- README validation: local links resolved across all six user-facing READMEs.
- Archive repeatability: two consecutive builds produced identical bytes and
  hashes, and both archives passed ZIP integrity checks.
- Privacy and residue audit: no retained clipboard paths, temporary screenshot
  paths, identity-number-shaped data, placeholders, Python bytecode, or
  `__pycache__` directories were found in maintained sources.

Release artifacts:

| Archive | Size | SHA-256 | Entries |
|---|---:|---|---:|
| `dist/ccopyright-qa.skill` | 24,171 bytes | `2d2996e9befe3cc7aa65d41e2db391ad6209ab5f86e5890ff008b569807334fc` | 13 |
| `dist/ccopyright-register.skill` | 75,942 bytes | `a6cee60c7fd3617fddeef641aa218460ad2c41091b25213d9313ce66469acf11` | 22 |

## Packaging cleanup validation (2026-09-03)

Removed the legacy `skills/ccopyright-register/package.json` from the canonical
Skill directory and archive requirements. Updated the existing archive test to
reject that file in both packages and removed the obsolete registry-manifest
coverage test. Maintainer guidance and historical Aone task status now reflect
the removal.

The [official skills CLI format guidance](https://github.com/vercel-labs/skills#creating-skills),
accessed on 2026-09-03, defines Skills through `SKILL.md` with `name` and
`description`. The local installation checks below confirm that this repository
does not need a registry manifest for discovery or installation.

- Ordinary Python suite: 31 tests ran; 30 passed and the opt-in PDF integration
  was skipped. The explicit Chromium/Poppler integration passed separately.
- Official Skill validator: both source directories and both extracted archive
  roots passed.
- skills CLI 1.5.23: exactly two Skills discovered; QA-only, register-only, and
  combined copied installations matched their canonical directories. Both
  installed register copies completed `preflight` successfully.
- Two consecutive archive builds produced identical hashes. ZIP integrity,
  entry hashes, source-content parity, and absence of `package.json` passed for
  both archives. All six README files passed the local-link checks.
- Removed publisher/registry values were absent from current project files and
  both archives. The residue scan found no unexpected matches; an existing
  synthetic migration-test path was reviewed as test input.

Updated release artifacts, from the canonical skills.sh source
`OtterPaw-Studio/ccopyright-skill`:

| Archive | Size | SHA-256 | Entries |
|---|---:|---|---:|
| `dist/ccopyright-qa.skill` | 31,884 bytes | `26f5240abde0c35230972b434f717598495811dda6569f4fa95240f486a483f6` | 15 |
| `dist/ccopyright-register.skill` | 82,473 bytes | `dde705ba3b789aef7169babdaafe427884a190324eda43ec4da5e416eecf4810` | 21 |
