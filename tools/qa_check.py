#!/usr/bin/env python3
"""Pre-push QA for the JKOF site.

Catches the specific failures that have reached the client before:
  - image src pointing at a file that does not exist
  - the same photo used twice with different captions
  - a <figure> with no caption, or a caption with no image
  - internal page links pointing at missing files
  - leftover placeholder text

Exit code 1 if any ERROR is found, so it can gate a push.

Usage: python3 tools/qa_check.py
"""

import html as html_mod
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(".")
PLACEHOLDERS = ["TBC", "TODO", "XXXX", "Lorem ipsum", "INSERT ", "[placeholder]"]
SKIP = {"image-review.html", "contact-sheet.html", "gallery-reconciliation-review.html",
        "layout-workings.html", "biography-verbatim-workings.html"}

errors, warnings = [], []


def pages():
    for p in sorted(ROOT.glob("*.html")):
        if p.name not in SKIP:
            yield p


def check_images(page, html):
    srcs = re.findall(r'<img[^>]+src="(?!https?://|data:)([^"]+)"', html)
    for src in srcs:
        target = (page.parent / src).resolve()
        if not target.exists():
            errors.append(f"{page.name}: image not found -> {src}")

    figures = re.findall(r"<figure\b.*?</figure>", html, flags=re.S)
    seen = defaultdict(list)
    for fig in figures:
        imgs = re.findall(r'<img[^>]+src="([^"]+)"', fig)
        caps = re.findall(r"<figcaption[^>]*>(.*?)</figcaption>", fig, flags=re.S)
        caption = " ".join(html_mod.unescape(re.sub(r"<[^>]+>", "", caps[0])).split()) if caps else None

        if imgs and not caption:
            errors.append(f"{page.name}: figure has no caption -> {imgs[0]}")
        if caption and not imgs:
            errors.append(f"{page.name}: caption with no image -> {caption[:60]}")
        for src in imgs:
            seen[src].append(caption)

    for src, caps in seen.items():
        if len(caps) > 1:
            uniq = {c for c in caps if c}
            if len(uniq) > 1:
                errors.append(
                    f"{page.name}: {src} used {len(caps)}x with different captions -> "
                    + " | ".join(list(uniq)[:2])
                )
            else:
                warnings.append(f"{page.name}: {src} appears {len(caps)}x")


def ahash(path):
    """Cheap average hash — catches the same photo saved under two filenames."""
    from PIL import Image, ImageOps
    img = Image.open(path)
    img = ImageOps.exif_transpose(img).convert("L").resize((8, 8), Image.Resampling.LANCZOS)
    px = list(img.convert("L").tobytes())
    avg = sum(px) / len(px)
    return "".join("1" if p > avg else "0" for p in px)


def check_duplicate_photos(page, html):
    """Same image content used twice with different captions."""
    figures = re.findall(r"<figure\b.*?</figure>", html, flags=re.S)
    by_hash = defaultdict(list)
    for fig in figures:
        caps = re.findall(r"<figcaption[^>]*>(.*?)</figcaption>", fig, flags=re.S)
        caption = " ".join(html_mod.unescape(re.sub(r"<[^>]+>", "", caps[0])).split()) if caps else "(none)"
        for src in re.findall(r'<img[^>]+src="(?!https?://|data:)([^"]+)"', fig):
            target = page.parent / src
            if target.exists():
                try:
                    by_hash[ahash(target)].append((src, caption))
                except Exception:
                    pass

    for entries in by_hash.values():
        if len(entries) < 2:
            continue
        captions = {c for _, c in entries}
        files = sorted({s.rsplit("/", 1)[-1] for s, _ in entries})
        if len(captions) > 1:
            errors.append(
                f"{page.name}: same photo under {len(files)} filenames with different "
                f"captions ({', '.join(files)}) -> " + " | ".join(sorted(captions))
            )
        else:
            warnings.append(f"{page.name}: same photo appears twice ({', '.join(files)})")


def check_links(page, html):
    hrefs = re.findall(r'href="(?!https?://|mailto:|tel:|#)([^"?#]+)', html)
    for href in hrefs:
        if not href.strip():
            continue
        target = (page.parent / href).resolve()
        if not target.exists():
            errors.append(f"{page.name}: broken link -> {href}")


def check_placeholders(page, html):
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    for token in PLACEHOLDERS:
        if token.lower() in text.lower():
            warnings.append(f"{page.name}: placeholder text '{token}'")


def main():
    checked = 0
    for page in pages():
        html = page.read_text(encoding="utf-8", errors="ignore")
        check_images(page, html)
        check_duplicate_photos(page, html)
        check_links(page, html)
        check_placeholders(page, html)
        checked += 1

    print(f"QA checked {checked} pages\n")

    for w in warnings:
        print(f"  WARN   {w}")
    for e in errors:
        print(f"  ERROR  {e}")

    if not errors and not warnings:
        print("  All clear.")
    print()

    if errors:
        print(f"FAILED — {len(errors)} error(s). Do not push.")
        return 1
    print(f"PASSED — {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
