<div align="center">

# Software Copyright Self-Service Toolkit

> **Understand the rules first. Build the materials with confidence.**

[![Agent Skills](https://img.shields.io/badge/Agent_Skills-2-2F81F7)](https://agentskills.io)
[![中文 / English](https://img.shields.io/badge/Docs-中文%20%2F%20English-5B5BD6)](README.md)
[![Privacy First](https://img.shields.io/badge/Privacy-First-16865C)](#safety-and-scope)

Not sure whether a requirement is official, what an agency fee actually covers,<br>
or how your source code, manual, and application facts are supposed to line up?

[Choose a Skill](#two-skills-one-path) · [One-minute install](#one-minute-install) · [First use](#first-use) · [How the work unfolds](#how-the-work-unfolds) · [Safety](#safety-and-scope)

**Ordinary deposit** · **Manual submission** · **Privacy first** · **No legal conclusions**

</div>

---

## Why we built it

The hard part of software copyright registration is often not finding a template. It is working out whether a claim comes from a rule, a service guide, the authenticated portal, or a provider's own marketing. Once preparation starts, a different set of questions appears: which source belongs in the material, whether the manual is backed by the repository, and which facts only the applicant can confirm.

That is why the toolkit has two Skills. `ccopyright-qa` helps you understand the question; `ccopyright-register` turns confirmed facts and real source code into reviewable material. Install either one on its own, or start with Q&A and decide later whether to prepare the material yourself.

Third-party services can still be useful. Organizing material, drafting, formatting, data entry, and human communication all take work. The toolkit does not decide whether a service is “worth it.” It separates official requirements, work you can do yourself, what the provider is actually delivering, and questions that still need specialist judgment.

Both Skills stop before submission to the [China Copyright Protection Center](https://www.ccopyright.com.cn/). They do not sign in, fill or submit browser forms, track applications, or interpret correction notices.

## Two Skills, one path

| | **ccopyright-qa** | **ccopyright-register** |
|---|---|---|
| Best for | Rules, fields, materials, self-service decisions, redacted quotes | Repository assessment, fact worksheets, source/document material, PDF validation |
| How it works | Read-only answers with sources, dates, conditions, and anything still unverified | Read-only assessment first; writes to `.ccopyright/` only after approval |
| Writes files | Never | Yes, but never silently changes product source |
| Local dependencies | No Python, Chrome, or Poppler for ordinary use | Python required; Chrome and Poppler for the PDF workflow |
| Typical opening | “Can the short name be blank?” “Do I need an agency?” | “Assess this repository.” “Generate source, manual, and PDFs.” |

If you are unsure, use this rule of thumb:

- **You only need an answer**: install **ccopyright-qa**.
- **You need repository work**: install **ccopyright-register**.
- **You are not sure yet**: install both and start with Q&A.

## One-minute install

### Recommended: install both Skills

```bash
npx skills add OtterPaw-Studio/ccopyright-skill \
  --skill ccopyright-qa ccopyright-register
```

### Install only one

```bash
# Read-only Q&A
npx skills add OtterPaw-Studio/ccopyright-skill --skill ccopyright-qa

# Material preparation
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

The **skills** CLI runs through **npx**. See the [skills.sh CLI documentation](https://www.skills.sh/docs/cli) for installation, updates, removal, and anonymous install statistics. To opt out for one installation:

```bash
DISABLE_TELEMETRY=1 npx skills add OtterPaw-Studio/ccopyright-skill \
  --skill ccopyright-qa ccopyright-register
```

## First use

After installation, just describe what you need. You can copy one of these prompts or adapt it to your situation.

### Ask about the rules without generating files

```text
Use $ccopyright-qa to explain the materials normally needed for ordinary China
software copyright registration. Separate the legal baseline, current portal
details I still need to verify, and work I can perform myself.
```

### Assess the repository without generating material

```text
Use $ccopyright-register to assess this repository for ordinary China software
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

## How the work unfolds

```mermaid
flowchart LR
    A[Rule, material, or quote question] --> B[ccopyright-qa]
    B --> C{Continue self-service?}
    C -->|Yes| D[ccopyright-register repository assessment]
    C -->|Need help| E[Define the paid service scope]
    D --> F[Confirm facts and source boundary]
    F --> G[Generate and validate material]
    G --> H[Page-by-page human review]
    H --> I[Manual submission in the current portal]
```

| Stage | What you do | What remains afterward |
|---|---|---|
| Ask first | Raise a question about a rule, field, material, or quote | A sourced answer, anything still unverified, and a practical next step |
| Inspect the repository | Point to the repository you plan to register | Source/document inventory, candidate boundary, evidence map, and **INFO/WARNING** precheck |
| Fill the gaps | Confirm facts the code cannot prove | Schema-v3 facts and an unresolved-item checklist |
| Prepare material | Confirm source order and manual content | Form worksheet, program/document material, proof checklist, and traceability |
| Validate | Check current portal requirements and complete the needed confirmations | A4 PDFs, pagination/hash/field checks, page images, and contact sheets |
| Final review | Inspect the final material page by page | A timestamped `ready-to-submit` revision without overwriting earlier work |

### Material workspace

**ccopyright-register** creates this workspace in the target repository:

```text
.ccopyright/
├── facts/                 canonical application facts and requirement snapshot
├── reports/               inventory, precheck, evidence, build, render reports
├── drafts/                copy-ready worksheet and human checklists
├── work/                  Markdown, HTML, PDFs, assets, and traceability manifests
├── qa/                    validation reports, page PNGs, and contact sheet
└── ready-to-submit/       immutable timestamped reviewed revisions
```

Program material is built from explicitly selected first-party files while preserving original blank lines, comments, tabs, content, and order. Every printed row maps to its original path, line number, stream position, and hash. Document material uses applicant-approved documentation, repository evidence, and real product screenshots; missing evidence produces a warning rather than invented functionality.

Full guides: [material preparation](skills/ccopyright-register/README.en.md) · [read-only Q&A](skills/ccopyright-qa/README.en.md)

## Sources, quotes, and uncertainty

**ccopyright-qa** distinguishes four basis classes:

1. official legislation, regulation, or rule;
2. a specific China Copyright Protection Center guide or FAQ with access date;
3. current redacted portal text explicitly reviewed for this application;
4. material establishing only a third party's own claim, or a clearly labeled inference or practice suggestion.

Fees, channels, fields, upload limits, processing times, and provider prices change. The Skill does not treat an old value as current; when it cannot find a current source, it says so plainly.

A quote you provide is used only to understand that particular offer, not as a current market benchmark. The toolkit does not call a price “fair,” “unfair,” or “a scam” without scope and evidence. It breaks the offer down into official work, work you still need to do, provider deliverables, and the conditions behind its promises.

The preparation Skill's fields, conditional branches, and character gates are an updateable portal-compatibility profile—not Q&A evidence and not a permanent official rule.

## Safety and scope

Neither Skill:

- fills or submits a browser form;
- logs in, signs, pays, or operates an applicant account;
- tracks an application or parses correction notices;
- determines ownership or contract enforceability or guarantees registration;
- stores identity numbers or scans, signatures, credentials, payment data, or session data;
- automates exceptional deposit, sealing, classified, or military workflows.

**ccopyright-qa** is read-only: it does not scan repositories or generate files. **ccopyright-register** tells you where it will write and waits for approval before using `.ccopyright/`; it never silently changes product source. The toolkit helps with understanding and preparation, not legal advice.

Repository, ownership, and IP prechecks use exactly **INFO** and **WARNING** to prompt human review, not to make legal conclusions. Current portal constraints, required facts, ordinary-deposit selection, and PDF validation remain final-stage gates.

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

### Can I generate material without Chrome or Poppler?

Repository assessment, fact worksheets, traceability, Markdown, and HTML remain available. PDF rendering and technical validation require the corresponding tools.

### Must every WARNING be removed?

No. Repository, ownership, and IP precheck warnings prompt review and do not block generation. Current portal constraints, active proof branches, required facts, ordinary-deposit selection, and PDF validation can block final generation.

## Official references

- [Q&A official page-level source catalog](skills/ccopyright-qa/references/en/official-sources.md)
- [China Copyright Protection Center software-registration guide](https://www.ccopyright.com.cn/index.php?optionid=1030)
- [Measures for Computer Software Copyright Registration](https://www.ncac.gov.cn/xxfb/flfg/bmgz/202410/t20241015_869486.html)
- [Consolidated Regulations on Computer Software Protection](https://xzfg.moj.gov.cn/mobile/law/detail?LawID=581)
- [skills.sh documentation](https://www.skills.sh/docs)

For maintainer and contributor commands, see [AGENTS.md](AGENTS.md).
