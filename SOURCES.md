# Client material — source register

## Why this file exists

On 4 August 2026 we told the client that five photographs she had asked for
"are not in the archive." They were. She had uploaded them herself on
28 January 2026, into the shared Drive folder, at the very start of the project.
They had simply never been copied into `bio/images/`.

The mistake was not the search. It was making a claim about **what does not
exist** while having looked in only one of six places, without saying so.

## Rule

**No claim about what the client has or has not supplied may be made without
naming the sources checked and the date checked.**

A negative claim ("we don't have X", "that was never sent", "the archive
contains no…") is only permitted when every source below is marked CHECKED
against a date, and the claim names them. If any source is UNCHECKED, the
honest form is: "not found in [list]; [list] not yet examined."

Run `python3 tools/coverage_check.py <dir>` against any recovered source
directory to see what it holds that the site does not.

## Standing client instruction — David, WhatsApp, 23 June 2026

> "Please use only the pics from the *jkof website pics* file for the website
> and not the ones in the annotations file some of which haven't been snipped
> and tidied up."

The gallery therefore draws on source 1 only. Source 2 (Aunty Vivian's January
uploads) are phone photographs of pages from the commemorative programme: they
carry page borders, a printed "Page 07", mirrored watermark bleed-through and
burned-in captions. They are the **right photographs** — she named four of them
specifically — but they are not tidied, so they fail David's standard. They are
held in `bio/images/_unverified/` pending clean originals.

Unresolved between trustees: David says use only the 26; Aunty Vivian asks for
four photographs that are not among the 26. Not a build decision.

## Sources

| # | Location | Origin | Date supplied | Status |
|---|---|---|---|---|
| 1 | Drive: `JKOF website pics -26 pics` (`1RIaQ…to4sO`) | David / family | 23 Jun 2026 | CHECKED 4 Aug 2026 — 26 files, all on site |
| 2 | Drive: loose IMG_85xx files in `1ay0s…zyjTB` | **Aunty Vivian** | 28 Jan 2026 | CHECKED 4 Aug 2026 — 12 files, **none were on site**; 5 now added |
| 3 | Drive: `drive-download-20260201T201223Z-3-001.zip` (256 MB) | Aunty Vivian | 1 Feb 2026 | **UNCHECKED** — too large to pull in session |
| 4 | Drive: `drive-download-20260201T201812Z-3-001.zip` (103 KB) | Aunty Vivian | 1 Feb 2026 | CHECKED 4 Aug 2026 — contains BIOGRAPHY (UPDATE VERSION).docx + PDF, **not yet read** |
| 5 | Drive: `drive-download-20260201T201701Z-3-001.zip` (74 KB) | Aunty Vivian | 1 Feb 2026 | **UNCHECKED** |
| 6 | Upload: `jk_photos_batch1__1_.zip` | — | 16 Feb 2026 | CHECKED 4 Aug 2026 — 9 files, **none on site**, none match the six requests |
| 7 | Upload: `JKOF_website_annotations.docx` | Aunty Vivian | 29 Jun 2026 | CHECKED 4 Aug 2026 — 26 embedded images, all already on site |
| 8 | Drive: `Dr Onwubualili PDF`, `DR JAMES ONWUBALILI PROGRAMME Part B.pdf` | family | 30 Jan 2026 | **UNCHECKED** — memorial programme, likely source of several portraits |

## Known outstanding, by evidence

- Photograph 1, "young JK in a white long sleeve shirt" — **not found** in
  sources 1, 2, 6, 7. Sources 3, 5 and 8 not yet examined. Do not tell the
  client it does not exist.
- Table tennis team year: **the two family sources disagree.** The annotations
  document (the file David nominated for website captions) says **1966** and
  names the team. The burned-in caption on the programme scan IMG_8598 says
  **1962**. The site follows the annotations document. Do not change this
  without asking the family. On 4 Aug 2026 we briefly changed it to 1962 on the
  strength of the scan alone; that was wrong.
- Vivian's maiden name: biography gives both Eruchalu and Onyemelukwe.
  Unresolved — client question.
- Wedding year: her note says 1980; biography text says 1981. Unresolved.
- Sons named "James and David" in one section, "Emeka and David" in another.
  Unresolved.
