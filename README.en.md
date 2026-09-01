# Software Copyright Self-Service Toolkit

**Understand the rules first. Build the materials with confidence.**

> Turn public but fragmented, difficult, and changeable registration information into source-aware answers and a reviewable material-preparation workflow.

[简体中文](README.md) · [Choose a Skill](#two-skills-one-path) · [Quick install](#one-minute-install) · [First use](#first-use) · [Full workflow](#from-question-to-submission-ready-material) · [Safety](#safety-and-scope)

**Ordinary deposit** · **Manual submission** · **Privacy first** · **No legal conclusions**

---

## What this project solves

Much of software copyright registration is public rather than mysterious, but the information is scattered across rules, service guides, FAQs, and the authenticated portal. This project provides two independently installable Agent Skills so you can understand first and act second:

| Find the basis | Understand the service | Build the materials |
|---|---|---|
| Separate rules, service guidance, current portal behavior, and third-party claims | See what a service fee actually buys without treating an agency as officially mandatory | Generate traceable, testable, human-reviewable materials from a code repository |

The goal is to reduce information asymmetry, not to claim that every third-party service lacks value. Organization, drafting, formatting, data entry, and human communication can involve real work. You should be able to see the official work, what you can complete yourself, actual paid deliverables, and issues that still need specialist judgment before making your own choice.

Both Skills support understanding and preparation before manual handling with the [China Copyright Protection Center](https://www.ccopyright.com.cn/). They do not sign in, fill or submit a browser form, track an application, or interpret correction notices.

## Two Skills, one path

| | **ccopyright-qa** | **ccopyright-register** |
|---|---|---|
| Best for | Rules, fields, materials, self-service decisions, or service quotes | Repository assessment, material generation, or material validation |
| Default behavior | Read-only answer with source, date, conditions, and unknowns | Assess first, then prepare inside `.ccopyright/` |
| Writes files | Never | Only after the user agrees to the workspace scope |
| Local dependencies | No Python, Chrome, or Poppler for ordinary use | Python required; Chrome and Poppler for the PDF workflow |
| Typical request | “Can the short name be blank?” “Do I need an agency?” | “Assess this repository.” “Generate source, manual, and PDFs.” |

The shortest decision rule:

- **You only need an answer**: use **ccopyright-qa**.
- **You need repository work**: use **ccopyright-register**.
- **You are not sure yet**: install both and start with Q&A.

```text
Question → ccopyright-qa → self-service/paid-help decision → ccopyright-register → human review → current portal
```

## One-minute install

### Recommended: install both Skills

```bash
npx skills add OtterPaw-Studio/ccopyright-skill \
  --skill ccopyright-qa ccopyright-register
```

### Install only one

Q&A:

```bash
npx skills add OtterPaw-Studio/ccopyright-skill --skill ccopyright-qa
```

Material preparation:

```bash
npx skills add OtterPaw-Studio/ccopyright-skill --skill ccopyright-register
```

### Install globally for Codex

```bash
npx skills add OtterPaw-Studio/ccopyright-skill \
  --skill ccopyright-qa ccopyright-register \
  --agent codex \
  --global
```

From a local checkout:

```bash
npx skills add . --skill ccopyright-qa ccopyright-register
```

The **skills** CLI runs through **npx** without a separate global installation. See the [skills.sh CLI documentation](https://www.skills.sh/docs/cli) for installation, updates, removal, and anonymous telemetry. To opt out for one installation:

```bash
DISABLE_TELEMETRY=1 npx skills add OtterPaw-Studio/ccopyright-skill \
  --skill ccopyright-qa ccopyright-register
```

## First use

Copy the prompt closest to what you need now.

### Ask what is required

```text
Use $ccopyright-qa to explain the materials normally needed for ordinary China
software copyright registration. Separate the legal baseline, current portal
details I still need to verify, and work I can perform myself.
```

### Assess the repository without generating files

```text
Use $ccopyright-register to assess this repository for ordinary software
copyright registration. Do not generate materials yet. Show the candidate
software identity, source boundary, missing facts, and every warning.
```

### Start a draft directly

```text
Use $ccopyright-register to prepare registration materials for this repository.
Explain the write scope, create the .ccopyright workspace, generate a draft,
and ask only for facts the repository cannot safely establish.
```

### Break down a service quote

```text
Use $ccopyright-qa to break down this service quote after I have removed
identity, order, and payment information. Identify each deliverable, work I
still need to do, and questions I should ask the provider.
```

Registration-facing worksheets and identification material use Chinese by default.

## Prerequisites

| Requirement | **ccopyright-qa** | **ccopyright-register** |
|---|:---:|:---:|
| Agent Skills-compatible AI agent | Required | Required |
| Node.js with **npx** | Installation only | Installation only |
| Access to current official pages | For current-state questions | To confirm current portal requirements |
| Python 3.10+, available as **python** | Not needed | Required |
| Chrome or Chromium | Not needed | For PDF generation |
| Poppler | Not needed | For PDF validation and contact sheets |
| Git | Not needed | Recommended, not required |

The Q&A Skill needs no repository, portal account, or local generation tools. Without PDF tools, the preparation Skill can still scan a repository and create fact worksheets, Markdown, and HTML.

Ask **ccopyright-register** to run its preflight, or run this in its installed directory:

```bash
python scripts/ccopyright.py preflight
```

The local generator needs no additional LLM API key, portal password, identity document, or signing certificate.

---

## From question to submission-ready material

| Stage | What the user does | What the Skill does | Result |
|---|---|---|---|
| 1. Understand | Ask about a rule, material, or service | **ccopyright-qa** separates sources, dates, conditions, and unknowns | An informed self-service decision |
| 2. Assess | Choose the code repository | **ccopyright-register** inventories source, Git, docs, licenses, and sensitive patterns read-only | Candidate registration boundary and precheck |
| 3. Confirm | Supply facts the code cannot prove | Maintain the canonical schema-v3 `facts/application.json` | Traceable application worksheet |
| 4. Generate | Confirm source order and document content | Build worksheet, program/document material, proof checklist, and traceability | Draft material and internal review files |
| 5. Validate | Resolve required facts and current portal constraints | Render A4 PDFs and check pagination, hashes, field gates, and unresolved items | Technical results and page contact sheets |
| 6. Review | Inspect every page and explicitly confirm | Create a timestamped revision without overwriting earlier work | Human-reviewed `ready-to-submit` revision |

### How answer sources are classified

**ccopyright-qa** distinguishes four basis classes:

1. official legislation, regulation, or rule;
2. a specific China Copyright Protection Center guide or FAQ with access date;
3. current redacted portal text explicitly reviewed for this application;
4. material establishing only a third party's own claim, or a clearly labeled inference or practice suggestion.

Current fees, channels, fields, upload limits, processing times, and provider prices must not be answered from memory. When a current source does not support the value, the Skill marks it unverified.

The preparation Skill's fields, conditional branches, and character gates are an updateable portal-compatibility profile—not Q&A evidence and not a permanent official rule.

### How to read the repository precheck

Repository, ownership, and IP prechecks use only **INFO** and **WARNING**. They prompt human review, are not legal conclusions, and never block material generation by themselves. Git and configuration files can suggest facts but cannot establish rights holders, completion dates, publication facts, or authority to disclose source.

## What gets generated

**ccopyright-register** creates this workspace in the target repository:

```text
.ccopyright/
├── facts/                 canonical application facts and requirement snapshot
├── reports/               inventory, precheck, evidence, build, and render reports
├── drafts/                copy-ready worksheet and human checklists
├── work/                  Markdown, HTML, PDFs, assets, and traceability manifests
├── qa/                    validation reports, page PNGs, and contact sheet
└── ready-to-submit/       immutable timestamped reviewed revisions
```

Primary outputs include:

- a portal-ordered application worksheet;
- program identification material preserving original blanks, comments, tabs, content, and order;
- document identification material based on real documentation, repository evidence, and product screenshots;
- conditional proof-readiness items for cooperative, commissioned, assigned-task, modified, successor, and other applicable branches;
- source traceability, evidence mapping, hashes, and human checklists;
- A4 PDFs, per-page images, and contact sheets when local tools are available.

Typical upload candidates are the program/document PDFs and proof/form files required by the current portal. Traceability manifests, evidence maps, hashes, and contact sheets remain internal review artifacts by default.

Full guides: [material preparation](skills/ccopyright-register/README.en.md) · [Q&A](skills/ccopyright-qa/README.en.md)

## Understanding third-party services

The project does not label a price “fair,” “unfair,” or “a scam” without defined scope and evidence. The Q&A Skill separates:

- work required by a rule or the current portal;
- fact confirmation, material organization, and portal operation the applicant may perform;
- drafting, formatting, material production, data entry, communication, or reminders offered by a provider;
- start events, scope, and conditions behind “expedited,” “guaranteed,” or “refund on failure” claims;
- ownership disputes, complex contracts, exceptional deposit, or classified cases that genuinely need specialist judgment.

A quote observed by a user can support analysis of that case but is not stored as a current market price. A provider page establishes only what that provider displayed on the access date, not an official necessity or an industry-wide price.

---

## Safety and scope

Neither Skill:

- fills or submits a browser form;
- logs in, signs, pays, or operates an applicant account;
- tracks an application or parses correction notices;
- determines ownership or contract enforceability or guarantees registration;
- stores identity numbers or scans, signatures, credentials, payment data, or session data;
- automates exceptional deposit, sealing, classified, or military workflows.

**ccopyright-qa** is read-only and does not scan repositories or generate files. **ccopyright-register** explains its write scope before using `.ccopyright/` and never silently changes product source. Answers and outputs are informational and preparatory assistance, not legal advice.

## Managing installed Skills

```bash
# List
npx skills list
npx skills list --global

# Update
npx skills update ccopyright-qa ccopyright-register

# Remove
npx skills remove ccopyright-qa ccopyright-register
```

## FAQ

### Which Skill should I install first?

Install **ccopyright-qa** for questions or to decide whether to buy assistance. Install **ccopyright-register** when you need repository material work. Install both when unsure.

### Are Q&A answers guaranteed to be current?

No. Rules can be amended, and service pages and authenticated portal behavior can change. Re-check the specific official page and current portal for fees, forms, channels, timelines, and upload constraints; the configured validation profile does not replace that check.

### Will Q&A tell me whether a service fee is worth it?

It does not make the value choice for you. It explains the work covered by the fee, work you still need to perform, promises needing clarification, and items that are not established as official requirements.

### Can I generate material without Chrome or Poppler?

Repository assessment, fact worksheets, traceability, Markdown, and HTML remain available. PDF rendering and technical validation require the corresponding tools.

### Must every WARNING be removed?

No, but the source matters:

- repository, ownership, and IP **precheck warnings** prompt review and do not block generation;
- portal character conflicts, missing conditional fields, and unresolved active proof-readiness items appear as draft **WARNING** findings and block final generation;
- exceptional deposit, missing or unconfirmed required facts, and failed PDF validation also stop the corresponding final stage.

## Official references

- [Q&A official page-level source catalog](skills/ccopyright-qa/references/en/official-sources.md)
- [China Copyright Protection Center software-registration guide](https://www.ccopyright.com.cn/index.php?optionid=1030)
- [Measures for Computer Software Copyright Registration](https://www.ncac.gov.cn/xxfb/flfg/bmgz/202410/t20241015_869486.html)
- [Consolidated Regulations on Computer Software Protection](https://xzfg.moj.gov.cn/mobile/law/detail?LawID=581)
- [skills.sh documentation](https://www.skills.sh/docs)

For maintainer and contributor commands, see [AGENTS.md](AGENTS.md).
