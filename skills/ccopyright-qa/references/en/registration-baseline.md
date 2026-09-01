# Ordinary registration Q&A baseline

Last reviewed: 2026-09-01

## Main official sources

- National Copyright Administration of China: [Measures for Computer Software
  Copyright Registration](https://www.ncac.gov.cn/xxfb/flfg/bmgz/202410/t20241015_869486.html)
- China Copyright Protection Center: [software-registration guide index](https://www.ccopyright.com.cn/index.php?optionid=1030)
- This Skill: [official page-level source catalog](official-sources.md)

The rule supports the ordinary material baseline below. Re-check the current
portal for its form, channel, fees, templates, and upload requirements whenever
an answer depends on those operational details.

## Ordinary baseline directly supported by the rule

- The China Copyright Protection Center is the software registration body.
- An applicant should be the software copyright owner or a natural person,
  legal person, or other organization that acquired the copyright by
  inheritance, transfer, or succession.
- Software submitted for registration should be independently developed or a
  permitted modification with important functional or performance improvement.
- Main application material includes the required application form, software
  identification material, and relevant proof documents.
- Identification material includes program and document material. The ordinary
  baseline uses the consecutive first and last 30 pages of source and one
  document, or the complete material when it is under 60 pages. Except for
  specified circumstances, program pages have at least 50 lines and document
  pages at least 30 lines.
- Conditional proof can include identity proof, an ownership contract or task
  document, permission from the original copyright owner, and evidence of
  inheritance, transfer, or succession.
- The form is completed in Chinese, foreign proof receives a Chinese
  translation, and application files use A4 paper.
- The rule also defines exceptional deposit and sealing; those are outside this
  project's ordinary material-generation workflow.

Link the specific official rule when using these facts; do not cite only
“official requirements.”

## What the rule does not establish

The rule alone does not establish the current:

- complete online form and choices;
- account, identity-verification, or electronic-signature operation;
- PDF size, naming, or upload count;
- official fee item or amount;
- practical processing time, certificate format, or delivery arrangement;
- price, scope, success rate, or expedited ability of any provider.

Use the catalog's specific current official page or current redacted portal
text explicitly supplied for this question.

## Whether a third-party service is mandatory

The rule lists the form, identification material, and relevant proof documents
as the main materials; it does not list purchasing a third-party service as an
application material. That supports only the limited statement that an agency
service is not one of the materials named by this rule. It does not prove that
every applicant is suited to complete self-service or that human assistance has
no value.

Continue by separating the required official work, what the applicant can do,
the labor a provider actually offers, and whether complex ownership or special
handling calls for qualified human support.

## The portal validation profile is not official authority

Profile ID: `ccpc-form-profile-v1`

The companion `ccopyright-register` Skill uses the compact profile below to
catch form problems early. QA may explain what is checked locally, but the
profile is not an official source. State “bundled validation value; confirm the
current portal before submission” whenever giving a configured number.

The profile covers full/optional short name/version, rights acquisition and
scope, category, original/modified status, development type, completion and
publication, six environment fields, languages, source amount, purpose,
industry, main functions, technical features, ordinary/exceptional deposit,
rights holders, and the joint-ownership choice.

| Configured field | Local gate |
|---|---:|
| Modification/translation/composition summary | 50 characters maximum |
| Each of six environment fields | 50 characters maximum |
| Other programming languages | 120 characters maximum |
| Purpose | 50 characters maximum |
| Industry | 50 characters maximum |
| Main functions | 500–1,300 characters |
| Other technical features | 100 characters maximum |

Conditional checks include first-publication date/country/region for published
software; explanation and basis for modified software; corresponding
agreement/task-file review for cooperative, commissioned, or assigned-task
development; consistency between multiple rights holders and the joint choice;
and stopping the ordinary workflow for exceptional program or document
deposit.

The profile does not establish PDF size/naming/orientation/count, complete help
text, all dynamic successor-acquisition or partial-rights fields, exceptional
deposit detail, or later confirmation/signature pages. Use a specific current
official page or the portal reviewed for this application to confirm them.
