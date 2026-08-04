#!/usr/bin/env python3
"""Photo audit document — point-by-point response to the client's note.

Shows what was wrong, what was corrected, and for photographs not held in the
archive, the nearest image we do have (with its reference number).

Usage: python3 tools/build_audit.py
"""

from pathlib import Path

from PIL import Image, ImageOps
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Image as RLImage, KeepTogether, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

NAVY = colors.HexColor("#12314f")
GREEN = colors.HexColor("#1a4f38")
GOLD = colors.HexColor("#b8860b")
GREY = colors.HexColor("#5a5a5a")
RULE = colors.HexColor("#d8d8d8")

THUMBS = Path("build/audit")
THUMBS.mkdir(parents=True, exist_ok=True)

# (heading, requested, was_showing, action, status, nearest_ref, nearest_file, nearest_note)
ITEMS = [
    ("1. Young JK — Schoolboy years",
     "Young JK in a white long-sleeve shirt.",
     "The Mallorca 2002 holiday photograph, which already appeared elsewhere in the gallery under its own caption.",
     "Incorrect entry removed.",
     "NOT IN ARCHIVE",
     21, "6.2.jpg",
     "Nearest we hold: a formal studio portrait of JK as a young man in jacket and tie. "
     "Already in use as &ldquo;Freshman &mdash; University of Ibadan, 1970&rdquo;."),

    ("2. Postgraduate Medical School — London",
     "Hammersmith Hospital in the background, JK in a white coat.",
     "The Spain 2003 holiday photograph, also already in the gallery under its own caption.",
     "Incorrect entry removed.",
     "NOT IN ARCHIVE",
     None, None,
     "No photograph in the 52 we hold shows a hospital building or a white coat."),

    ("3. Graduation — Academic regalia",
     "JK in a red academic gown, holding a scroll showing GOLD MEDAL.",
     "David&rsquo;s MBBS graduation, 2008 — a duplicate of an image already captioned correctly.",
     "Incorrect entry removed.",
     "NOT IN ARCHIVE",
     14, "5.4.jpg",
     "The only graduation photograph of JK himself: black gown with his mother, Ibadan 1975. "
     "No red gown and no scroll visible."),

    ("4. Wedding day — JK and Vivian",
     "The 1980 wedding photograph.",
     "JK with friends in London, duplicated from elsewhere in the gallery.",
     "Incorrect entry removed.",
     "NOT IN ARCHIVE",
     20, "6.1.jpg",
     "Nearest we hold: JK and Vivian as a young couple, around 1979. Not a wedding photograph."),

    ("5. Family at wedding ceremony",
     "To be deleted — one of the four previously withdrawn.",
     "Nothing. The file had been deleted but the page still pointed at it, so it showed as an empty box.",
     "Entry removed and the broken reference cleared.",
     "RESOLVED",
     None, None, None),

    ("6. Professional portrait — Consultant years",
     "JK in a blue suit, from the original gallery.",
     "A photograph of JK&rsquo;s parents, Rev. James Onwubalili and Madame Adeline Onwubalili.",
     "Incorrect entry removed.",
     "NOT IN ARCHIVE",
     None, None,
     "No portrait of JK in a blue suit appears among the 52 photographs we hold."),
]


def thumb(filename, tag):
    src = Path("bio/images") / filename
    out = THUMBS / f"{tag}.jpg"
    img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    img.thumbnail((520, 520), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (520, 520), (243, 243, 240))
    canvas.paste(img, ((520 - img.width) // 2, (520 - img.height) // 2))
    canvas.save(out, "JPEG", quality=80, optimize=True)
    return out


def main():
    ss = getSampleStyleSheet()
    S = lambda n, **kw: ParagraphStyle(n, parent=ss["Normal"], **kw)

    h_title = S("t", fontName="Times-Bold", fontSize=20, leading=24, textColor=NAVY)
    h_sub = S("s", fontName="Times-Italic", fontSize=11, leading=15, textColor=GREY)
    h_item = S("i", fontName="Times-Bold", fontSize=12.5, leading=16, textColor=GREEN,
               spaceBefore=2, spaceAfter=3)
    body = S("b", fontSize=9.3, leading=13.6, textColor=colors.HexColor("#333"),
             alignment=TA_LEFT)
    label = S("l", fontName="Helvetica-Bold", fontSize=6.8, leading=9,
              textColor=GOLD, spaceAfter=1)
    badge = S("bd", fontName="Helvetica-Bold", fontSize=7.6, leading=10,
              textColor=colors.white, alignment=1)
    refcap = S("rc", fontName="Helvetica-Bold", fontSize=8, leading=11,
               textColor=NAVY, alignment=1)
    note = S("n", fontSize=8.6, leading=12.4, textColor=GREY)

    story = [
        Paragraph("Biography Photographs &mdash; Audit and Corrections", h_title),
        Paragraph("James Kenechukwu Onwubalili Foundation &nbsp;&middot;&nbsp; "
                  "prepared in response to your note on the left-hand column", h_sub),
        Spacer(1, 4 * mm),
        Paragraph(
            "Every one of the six points you raised has been actioned. In each case the photograph "
            "on the page was a <b>duplicate of another image already in the gallery</b>, carrying a caption "
            "that did not belong to it. Those entries have been removed, so each photograph now appears "
            "once, under its correct caption.",
            body),
        Spacer(1, 2 * mm),
        Paragraph(
            "We then checked all <b>52 photographs</b> in the archive against your five descriptions. "
            "None of the five is among them &mdash; they appear never to have been sent to us. "
            "Where a related image exists, it is shown below with its reference number.",
            body),
        Spacer(1, 5 * mm),
    ]

    for idx, (head, requested, was, action, status, ref, fname, nearest) in enumerate(ITEMS):
        left = [
            Paragraph(head, h_item),
            Paragraph("YOU ASKED FOR", label),
            Paragraph(requested, body),
            Spacer(1, 1.6 * mm),
            Paragraph("WHAT THE PAGE WAS SHOWING", label),
            Paragraph(was, body),
            Spacer(1, 1.6 * mm),
            Paragraph("ACTION TAKEN", label),
            Paragraph(action, body),
        ]
        if nearest:
            left += [Spacer(1, 1.6 * mm), Paragraph(nearest, note)]

        badge_colour = GREEN if status == "RESOLVED" else colors.HexColor("#9c5a00")
        chip = Table([[Paragraph(status, badge)]], colWidths=[30 * mm], rowHeights=[6 * mm])
        chip.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), badge_colour),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
        ]))

        right = [chip]
        if ref and fname:
            right += [
                Spacer(1, 2.5 * mm),
                RLImage(str(thumb(fname, f"i{idx}")), width=30 * mm, height=30 * mm),
                Spacer(1, 1 * mm),
                Paragraph(f"Reference {ref}", refcap),
            ]

        row = Table([[left, right]], colWidths=[128 * mm, 34 * mm])
        row.setStyle(TableStyle([
            ("VALIGN", (0, 0), (0, 0), "TOP"),
            ("VALIGN", (1, 0), (1, 0), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (0, 0), 6 * mm),
            ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
        ]))
        story.append(KeepTogether(row))

    story += [
        Spacer(1, 5 * mm),
        Paragraph("What we need from you", h_item),
        Paragraph(
            "The five photographs above, whenever convenient. A numbered reference sheet of all 52 "
            "photographs we currently hold is attached separately &mdash; if any of the five is in fact "
            "already there and we have misread it, please just quote the number.",
            body),
        Spacer(1, 4 * mm),
        Paragraph("Two small queries on the text", h_item),
        Paragraph(
            "&bull;&nbsp; The family notes give your maiden name as both <b>Eruchalu</b> and "
            "<b>Onyemelukwe</b>. Which should the biography use?<br/>"
            "&bull;&nbsp; Your note refers to the wedding as <b>1980</b>; the biography text currently "
            "says <b>1981</b>. Which is correct?<br/>"
            "&bull;&nbsp; The text names the sons as &ldquo;James and David&rdquo; in one place and "
            "&ldquo;Emeka and David&rdquo; in another. Please confirm how they should be named.",
            body),
    ]

    SimpleDocTemplate(
        "JKOF-Photo-Audit.pdf", pagesize=A4,
        topMargin=16 * mm, bottomMargin=14 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
        title="JKOF Biography Photographs — Audit and Corrections",
        author="Altitude AI Consulting",
    ).build(story)

    print("Built JKOF-Photo-Audit.pdf")


if __name__ == "__main__":
    main()
