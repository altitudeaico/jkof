#!/usr/bin/env python3
"""Verify the biography page reproduces the family's document verbatim.

Compares the visible text of biography-verbatim-draft.html (or, once live,
biography.html) against the text extracted from the family's Word document.
Comparison is on normalised words: whitespace collapsed, typographic quotes
and dashes unified. Any word-level difference fails.

Usage:
    pandoc -t markdown --wrap=none SOURCE.docx -o /tmp/src.md
    python3 tools/verify_verbatim.py /tmp/src.md biography-verbatim-draft.html
"""

import difflib
import html as H
import re
import sys


def norm(text):
    text = H.unescape(text)
    for a, b in [("\u201c", '"'), ("\u201d", '"'), ("\u2018", "'"), ("\u2019", "'"),
                 ("\u2013", "-"), ("\u2014", "-"), ("\u00a0", " "), ("\\\"", '"')]:
        text = text.replace(a, b)
    text = re.sub(r"[*_]", "", text)          # markdown emphasis markers
    text = text.replace("\u2022", " ").replace("•", " ")  # bullet glyphs vs <li> markers
    return re.sub(r"\s+", " ", text).strip()


def words_from_md(path):
    return norm(open(path, encoding="utf8").read()).split()


def words_from_html(path):
    h = open(path, encoding="utf8").read()
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", h, flags=re.S)
    h = re.sub(r'<div class="notice">.*?</div>', "", h, flags=re.S)  # workings banner
    h = re.sub(r"<title>.*?</title>", "", h, flags=re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    return norm(h).split()


def main(src_md, page_html):
    a = words_from_md(src_md)
    b = words_from_html(page_html)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ops = [op for op in sm.get_opcodes() if op[0] != "equal"]

    print(f"source words: {len(a)}   page words: {len(b)}   ratio: {sm.ratio():.4f}\n")
    if not ops:
        print("VERBATIM: page text is word-for-word identical to the document.")
        return 0

    print(f"{len(ops)} difference(s):\n")
    for tag, i1, i2, j1, j2 in ops[:40]:
        src = " ".join(a[i1:i2]) or "(nothing)"
        dst = " ".join(b[j1:j2]) or "(nothing)"
        ctx = " ".join(a[max(0, i1 - 4):i1])
        print(f"  [{tag}] after '...{ctx}':")
        print(f"      document: {src[:110]}")
        print(f"      page:     {dst[:110]}\n")
    print("FAILED - the page does not reproduce the document verbatim.")
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
