#!/usr/bin/env python3
"""Check a directory of client-supplied images against what the site holds.

Answers one question honestly: which images in this source are NOT on the site?

This exists because on 4 August 2026 we told the client five photographs "were
not in the archive" after searching one folder out of six. Run this against
every source before making any claim about what the client has supplied, and
record the result in SOURCES.md.

Usage:
    python3 tools/coverage_check.py <source_dir> [more_dirs...]
"""

import sys
from pathlib import Path

from PIL import Image, ImageOps

SITE = Path("bio/images")
EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp"}
NEAR = 6  # hamming distance treated as the same photograph


def ahash(path):
    try:
        import pillow_heif
        pillow_heif.register_heif_opener()
    except ImportError:
        pass
    img = ImageOps.exif_transpose(Image.open(path)).convert("L")
    img = img.resize((8, 8), Image.Resampling.LANCZOS)
    px = list(img.tobytes())
    avg = sum(px) / len(px)
    return "".join("1" if p > avg else "0" for p in px)


def dist(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)


def load(directory):
    out = {}
    for p in sorted(Path(directory).rglob("*")):
        if p.is_file() and p.suffix.lower() in EXTS:
            try:
                out[p] = ahash(p)
            except Exception as exc:
                print(f"  ! could not read {p.name}: {exc}")
    return out


def main(dirs):
    site = load(SITE)
    print(f"Site holds {len(site)} images\n")

    total_missing = 0
    for d in dirs:
        src = load(d)
        print(f"{d}: {len(src)} images")
        missing = []
        for path, h in src.items():
            if not any(dist(h, sh) <= NEAR for sh in site.values()):
                missing.append(path.name)
        if missing:
            total_missing += len(missing)
            print(f"  NOT ON SITE ({len(missing)}):")
            for name in missing:
                print(f"    - {name}")
        else:
            print("  all present on site")
        print()

    if total_missing:
        print(f"{total_missing} supplied image(s) are not on the site.")
        print("Do not claim anything is 'not supplied' until these are reviewed.")
        return 1
    print("Every image in the checked sources appears on the site.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
