# Official sources and requirement snapshots (English)

Last manually reviewed: 2026-09-01

Requirements can change, and the registration portal may require
authentication or resist automated access. Do not treat this file as a
substitute for the portal the applicant currently sees. The China Copyright
Protection Center service pages below showed no clear publication or update
date, so only the actual access date is recorded.

## Source classes

1. Legislation, regulations, and rules establish the institutional and
   material baseline.
2. Specific China Copyright Protection Center guides and FAQs explain published
   operating guidance.
3. Authenticated portal text reviewed for this application establishes dynamic
   fields and upload behavior for the current workflow.
4. Third-party material or inference cannot establish an official requirement
   by itself.

Record direct URLs, actual access/review dates, and applicant confirmation in
`facts/requirements-snapshot.md`. On conflict, pause final generation, use the
current official page and portal reviewed for the application, and update the
workspace configuration.

The [portal form validation profile](portal-form.md) contains only structured
fields, branches, and character gates. It is implementation compatibility data,
not a source class above.

## China Copyright Protection Center service pages

All pages were manually accessed on 2026-09-01:

| Page | Use |
|---|---|
| [Software-registration guide index](https://www.ccopyright.com.cn/index.php?optionid=1030) | Locate official service guidance |
| [Application notes](https://www.ccopyright.com.cn/index.php?optionid=1057) | Online filing, self-service/agent, confirmation page, certificates, and notices |
| [Application steps](https://www.ccopyright.com.cn/index.php?optionid=1079) | Published steps |
| [Required files](https://www.ccopyright.com.cn/index.php?optionid=1080) | Main files and conditional proof categories |
| [Form-filling instructions](https://www.ccopyright.com.cn/index.php?optionid=1081) | Field meaning |
| [Review flow](https://www.ccopyright.com.cn/index.php?optionid=1082) | Intake and review stages |
| [Processing time](https://www.ccopyright.com.cn/index.php?optionid=1084) | Currently displayed timing formulation |
| [Registration institution](https://www.ccopyright.com.cn/index.php?optionid=1085) | Responsible institution |
| [FAQ page 1](https://www.ccopyright.com.cn/index.php?optionid=1087&page=1) | Self-service/agency, effect of registration, and ordinary flow |
| [FAQ page 2](https://www.ccopyright.com.cn/index.php?optionid=1087&page=2) | Name, development, and material questions |
| [FAQ page 3](https://www.ccopyright.com.cn/index.php?optionid=1087&page=3) | Cooperative, commissioned, and employment development |
| [Notice ending software-copyright registration charges](https://www.ccopyright.com.cn/index.php?optionid=1571) | Official-fee policy lead; separate third-party service fees |

## Maintained legal baseline

- National People's Congress: [Copyright Law of the People's Republic of China](https://www.npc.gov.cn/c2/c30834/202011/t20201119_308796.html)
- National administrative-regulation database: [consolidated Regulations on Computer Software Protection, including the 2011 and 2013 revisions](https://xzfg.moj.gov.cn/mobile/law/detail?LawID=581)

The official [Measures for Computer Software Copyright Registration](https://www.ncac.gov.cn/xxfb/flfg/bmgz/202410/t20241015_869486.html) state, among other things:

- application materials include the application form, software identification materials, and relevant proof documents;
- identification materials include program and document material;
- the ordinary baseline uses the consecutive first and last 30 pages, or the complete material when it is under 60 pages;
- except for specified circumstances, program pages have at least 50 lines and document pages at least 30 lines;
- application documents use A4 paper;
- exceptional-deposit options exist.

The generator models the ordinary baseline only. It intentionally stops for exceptional deposit, sealing, classified/military material, or other specialist handling.

## Snapshot checklist

Before setting `confirmations.requirements.current` to `true`, confirm:

- exact application field labels and allowed values;
- current ordinary-identification-material page and row rules;
- accepted PDF format, page orientation, file-size limits, and naming constraints;
- current proof-document and signature/confirmation requirements for the applicant type;
- any special rules for multiple rights holders, commissioned/cooperative development, transfer, inheritance, foreign documents, or modified software;
- whether the application is ordinary and non-classified.

If the applicant has reviewed only the bundled validation profile, keep
`requirements.captured_at` empty. Set it to the actual review date only after
checking the current portal and confirming that the snapshot is current.

Do not store portal credentials, session cookies, identity scans, or signatures in the repository workspace.
