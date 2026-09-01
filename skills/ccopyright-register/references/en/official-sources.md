# Official sources and requirement snapshots (English)

Requirements can change, and the registration portal may require authentication or resist automated access. Do not treat this file as a substitute for the current portal.

## Source priority

1. Current field text, help text, downloadable templates, and upload constraints visible to the applicant at [China Copyright Protection Center](https://www.ccopyright.com.cn/).
2. Current official rules from the [National Copyright Administration of China](https://www.ncac.gov.cn/).
3. User-provided current screenshots or copied portal text when automated retrieval is unavailable.
4. The maintained baseline below, explicitly marked with its capture date.

Record URLs, access/capture date, and any user-provided evidence in `facts/requirements-snapshot.md`. When sources conflict, pause final generation and ask the applicant which current portal instruction applies.

The bundled [portal-form evidence baseline](portal-form.md) is derived from 12 user screenshots received on 2026-08-31. It establishes only visible fields, conditional branches, counters, and PDF hints. The originals and their personal data are not included in the skill, and the receipt date is not represented as the portal capture date. Unshown dropdown values, help popovers, file-size/naming rules, and similar details remain in `portal_unknowns`.

## Maintained legal baseline

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

If the applicant has reviewed only the bundled screenshot baseline, keep `requirements.captured_at` empty. Set it to the actual review date only after checking the current portal and then confirming that the snapshot is current.

Do not store portal credentials, session cookies, identity scans, or signatures in the repository workspace.
