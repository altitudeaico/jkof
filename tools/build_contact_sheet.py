#!/usr/bin/env python3
"""Build a numbered photo reference PDF for JKOF.

Every photo in bio/images/ gets a permanent reference number. The client can
then say "14 is wrong, use 31" instead of describing photos in prose.

Usage:  python3 tools/build_contact_sheet.py
Output: JKOF-Photo-Reference.pdf  +  photo-index.csv
"""

import csv
from pathlib import Path

from PIL import Image, ImageOps
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Image as RLImage, Paragraph, SimpleDocTemplate,
                               Spacer, Table, TableStyle)

IMAGES = Path("bio/images")
THUMBS = Path("build/thumbs")
COLS = 3
THUMB_PX = 440
CELL_W = 58 * mm
IMG_H = 46 * mm

NAVY = colors.HexColor("#1a4f38")
GOLD = colors.HexColor("#b8860b")


def ordered_files():
    """JPGs first (the original family set), then the WhatsApp batch."""
    def key(p):
        stem = p.stem
        try:
            parts = [int(x) for x in stem.split(".")]
        except ValueError:
            parts = [999]
        return (0 if p.suffix.lower() == ".jpg" else 1, parts, stem)

    return sorted(
        [p for p in IMAGES.iterdir() if p.suffix.lower() in (".jpg", ".jpeg")],
        key=key,
    )


def make_thumb(src, number):
    THUMBS.mkdir(parents=True, exist_ok=True)
    out = THUMBS / f"{number:03d}.jpg"
    img = Image.open(src)
    img = ImageOps.exif_transpose(img).convert("RGB")
    img.thumbnail((THUMB_PX, THUMB_PX), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (THUMB_PX, THUMB_PX), (245, 245, 243))
    canvas.paste(img, ((THUMB_PX - img.width) // 2, (THUMB_PX - img.height) // 2))
    canvas.save(out, "JPEG", quality=72, optimize=True)
    return out


def main():
    files = ordered_files()
    styles = getSampleStyleSheet()

    num_style = ParagraphStyle("num", parent=styles["Normal"], fontName="Helvetica-Bold",
                               fontSize=19, leading=22, textColor=NAVY, alignment=1, spaceAfter=1)
    file_style = ParagraphStyle("file", parent=styles["Normal"], fontName="Helvetica",
                                fontSize=5.5, leading=7, textColor=colors.HexColor("#999"), alignment=1)
    title_style = ParagraphStyle("title", parent=styles["Heading1"], fontName="Helvetica-Bold",
                                 fontSize=17, textColor=NAVY, alignment=1, spaceAfter=4)
    intro_style = ParagraphStyle("intro", parent=styles["Normal"], fontSize=9.5,
                                 leading=14, alignment=1, textColor=colors.HexColor("#444"))

    story = [
        Paragraph("JKOF Photo Reference", title_style),
        Paragraph(
            "Every photograph in the archive, with a permanent reference number.<br/>"
            "To request a change, please quote the number &mdash; for example: "
            "<b>&ldquo;Schoolboy photo should be 27, not 18.&rdquo;</b>",
            intro_style),
        Spacer(1, 6 * mm),
    ]

    index_rows = []
    row, data = [], []

    for n, path in enumerate(files, start=1):
        thumb = make_thumb(path, n)
        index_rows.append({"number": n, "filename": path.name})
        row.append([
            RLImage(str(thumb), width=CELL_W - 6 * mm, height=IMG_H),
            Spacer(1, 1.5 * mm),
            Paragraph(str(n), num_style),
            Paragraph(path.name, file_style),
        ])
        if len(row) == COLS:
            data.append(row)
            row = []

    if row:
        while len(row) < COLS:
            row.append([Spacer(1, 1)])
        data.append(row)

    table = Table(data, colWidths=[CELL_W] * COLS, repeatRows=0)
    table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#dddddd")),
    ]))
    story.append(table)

    SimpleDocTemplate(
        "JKOF-Photo-Reference.pdf", pagesize=A4,
        topMargin=12 * mm, bottomMargin=12 * mm,
        leftMargin=10 * mm, rightMargin=10 * mm,
        title="JKOF Photo Reference",
    ).build(story)

    with open("photo-index.csv", "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["number", "filename"])
        writer.writeheader()
        writer.writerows(index_rows)

    print(f"Built JKOF-Photo-Reference.pdf and photo-index.csv ({len(files)} photos)")


if __name__ == "__main__":
    main()
