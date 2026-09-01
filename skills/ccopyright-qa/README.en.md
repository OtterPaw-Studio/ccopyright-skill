# ccopyright-qa

> Understand software copyright registration before deciding to self-serve,
> purchase assistance, or begin material preparation.

[简体中文](README.md) · [Quick start](#quick-start) · [What to ask](#what-to-ask) · [How answers are verified](#how-answers-are-verified) · [Safety and scope](#safety-and-scope)

`ccopyright-qa` is a read-only Q&A Skill for ordinary China computer-software
copyright registration. It explains fields, materials, conditional branches,
self-service paths, and redacted service quotes supplied by the user.

Its purpose is not to prove that every third-party service lacks value. It
helps you see what is official, what you can complete yourself, what work a
service is offering, and which issues genuinely need specialist judgment.

## Quick start

### 1. Install the Q&A Skill

~~~bash
npx skills add OtterPaw-Studio/ccopyright-skill --skill ccopyright-qa
~~~

Install both Skills when you also want repository-based material preparation:

~~~bash
npx skills add OtterPaw-Studio/ccopyright-skill \
  --skill ccopyright-qa ccopyright-register
~~~

From a local checkout:

~~~bash
npx skills add . --skill ccopyright-qa
~~~

### 2. Ask directly

~~~text
Use $ccopyright-qa to explain the materials normally needed for China software
copyright registration. Separate the legal baseline, current portal details I
still need to verify, and work I can perform myself.
~~~

~~~text
Use $ccopyright-qa to explain the consecutive first and last 30-page rule.
Give me the official basis and review date, and do not generate any files.
~~~

~~~text
Use $ccopyright-qa to break down this redacted service quote. Identify each
deliverable, what I still need to do, and questions I should ask the provider.
~~~

## Prerequisites

Ordinary Q&A needs only an Agent Skills-compatible AI agent. It does not require
Python, Chrome, Poppler, a code repository, or a portal account.

For current fees, channels, forms, upload constraints, timelines, or provider
offerings, the agent needs access to the corresponding current primary page.
When it cannot access one, the Skill marks the current value unverified instead
of substituting an old value from memory.

## What to ask

- how to understand the full name, optional short name, version, or completion
  date;
- distinctions among original/modified status, development type, rights
  acquisition, and rights scope;
- the main categories of ordinary application material;
- the legal baseline for program and document identification material;
- proof categories associated with cooperation, commission, assigned tasks,
  modification, or successor acquisition;
- whether a question looks suitable for self-service and what human assistance
  may add;
- deliverables and ambiguous promises in a redacted quote;
- whether to verify further or move into material preparation.

Use `ccopyright-register` instead when you want repository inspection, source
selection, manual/PDF generation, or material validation.

## How answers are verified

Answers distinguish among:

1. official legislation, regulation, or rule and the scope it supports;
2. a specific China Copyright Protection Center guide or FAQ with access date;
3. current redacted portal text explicitly reviewed or supplied for this
   application;
4. material that establishes only a third party's own claim, or a clearly
   labeled inference/practice suggestion.

The bundled [official page-level source
catalog](references/en/official-sources.md) links directly to legislation,
application notes, steps, required files, form instructions, review flow,
processing time, FAQs, and the fee notice. When a page shows no publication
date, the catalog records only the actual access date.

The fields and character gates in `ccopyright-register` are a portal
compatibility profile, not Q&A evidence or a permanent rule. QA can explain
what it checks, while labeling it as a local value that requires current-portal
confirmation.

## Agencies and service fees

The Skill does not decide that a price is “worth it” or “not worth it.” It
separates:

- officially required materials and actions;
- fact confirmation, material organization, and portal operation you may be
  able to perform yourself;
- organization, drafting, formatting, data entry, communications, or reminders
  offered by a provider;
- ownership disputes, complex contracts, exceptional deposit, or classified
  material needing specialist judgment;
- undefined scope in “expedited,” “guaranteed,” or “refund on failure” claims.

A provider page establishes only what that provider displayed on a particular
date. It does not automatically establish a market price or official
requirement. Unless you explicitly ask for current market research, the Skill
analyzes only the redacted quote you supply.

## Moving from Q&A to preparation

When you decide to self-prepare, continue with:

~~~text
Use $ccopyright-register to assess this repository for ordinary software
copyright registration. Scan only and list candidate registration boundaries,
missing facts, and every warning before generating anything.
~~~

`ccopyright-register` explains its write scope before using `.ccopyright/` to
produce worksheets, source/document material, and validation output. Loading
`ccopyright-qa` never authorizes file writes.

## Safety and scope

This Skill:

- does not scan or modify repositories and does not generate application files;
- does not fill, submit, sign, or pay through a browser;
- does not operate accounts, track progress, or parse correction notices;
- does not determine ownership, interpret contract enforceability, or
  guarantee registration;
- does not maintain a provider-price leaderboard or report a current price from
  memory;
- does not collect identity numbers/scans, signatures, credentials, payment
  data, or session data;
- does not handle exceptional deposit, sealing, classified, or military flows.

For complex ownership, contract disputes, or special deposit, it states the
limit and suggests qualified human support. Answers are informational and
preparatory assistance, not legal advice.

## FAQ

### Will it tell me whether I should hire an agency?

It helps you evaluate scope and complexity but does not make the value choice
for you. It separates official work, self-service work, provider deliverables,
and unresolved conditions.

### Can I upload a service contract for review?

It can break down redacted service descriptions and deliverables but does not
decide contract enforceability. Remove identity, order, payment, account, and
signature data first; consult a qualified professional for legal rights and
obligations.

### Are bundled answers guaranteed to be current?

No. Rules can be amended, and service pages and portal behavior can change.
Check the catalog's specific official page and the current portal for fees,
forms, channels, timelines, and upload constraints; a configured validation
value does not replace that check.

### Can it generate source material and a manual?

No. Install and use `ccopyright-register`.

## Official references

- [Official page-level source catalog](references/en/official-sources.md)
- [China Copyright Protection Center software-registration guide](https://www.ccopyright.com.cn/index.php?optionid=1030)
- [Measures for Computer Software Copyright Registration](https://www.ncac.gov.cn/xxfb/flfg/bmgz/202410/t20241015_869486.html)
- [skills.sh documentation](https://www.skills.sh/docs)
