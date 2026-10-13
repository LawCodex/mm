# Myanmar — LawCodex

Part of [LawCodex](https://github.com/LawCodex). **Status: minimal — only the 2008 Constitution
(English text) could be obtained reliably.**

## Contents

| File | Description |
|---|---|
| `constitution/2008-constitution-en.md` | Constitution of the Republic of the Union of Myanmar (2008), English text of the bilingual edition printed by the Printing & Publishing Enterprise, Ministry of Information (September 2008), as published on the Pyidaungsu Hluttaw (Union Parliament) website. Preamble, 15 chapters, 457 sections and 5 schedules. Text as adopted in 2008; the amendments of 2015 (Law No. 45/2015) are **not** incorporated. |

### Status of the 2008 Constitution

Front matter `status: unknown`. Since 1 February 2021 the Constitution's status is contested:
the military authorities declared a state of emergency under its sections 417–418 and have
continued to invoke it, while the Committee Representing Pyidaungsu Hluttaw (CRPH) declared it
abolished on 31 March 2021 and proclaimed a Federal Democracy Charter. LawCodex takes no
position; the file reproduces the text as published.

### Language

The authoritative text is in Burmese. The Burmese pages of the same PDF use a legacy non-Unicode
font (Win* family) and extract as Latin gibberish (e.g. `zGJUpnf;ykHtajccHOya'`), so they were
not published (no garbled text). The English text is the version printed by the Ministry of
Information; front matter marks it `translation: true`.

## Sources and gaps

| Source | Result |
|---|---|
| Myanmar Law Information System, `www.mlis.gov.mm` (official, Union Attorney General's Office) | Not reachable from our network (TCP timeouts, HTTPS and HTTP, 2026-10-12/13). Internet Archive copies of its pages contain only the page shell (law texts are loaded by JavaScript/POST requests that the Archive did not capture); 26 archived JSON provision lists are fragmentary (section first lines only) and were not used. |
| Union Attorney General's Office (`www.oag.gov.mm`, `www.uago.gov.mm`) | Not reachable. |
| Pyidaungsu Hluttaw (`pyidaungsu.hluttaw.mm`), Internet Archive | Constitution PDF (used — archived copy `https://web.archive.org/web/20170622204415/http://pyidaungsu.hluttaw.mm/uploads/pdf/constitution-2008.pdf`); a handful of bill/law PDFs, not a systematic collection. |

Not covered: all Union laws, State/Region laws, regulations — would require access to MLIS
(e.g. an MLIS export, or network access to `mlis.gov.mm`) with Unicode Burmese text.

Retrieved 2026-10-13. The Constitution is an official government text.

## Regenerate

```sh
# download the archived PDF (see URL above) to ../_raw/mm/c-my.pdf, then:
python scripts/mm_convert.py ../_raw/mm/c-my.pdf constitution/2008-constitution-en.md
```
