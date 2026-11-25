#!/usr/bin/env python3
"""Derive web assets for the bedroom mini lab photo.

Usage:
    python3 scripts/make-minilab-assets.py [/path/to/minilab.jpeg]

Without an argument, reads "minilab.jpeg" from the repository root.
Requires Pillow. The saved files carry no EXIF metadata.
"""
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else ROOT / "minilab.jpeg"
OUT = ROOT / "public/assets/lab"
WIDTHS = (480, 960, 1440)
WARM = (252, 245, 235)


def resize(image: Image.Image, width: int) -> Image.Image:
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def main() -> None:
    image = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
    # A gentle warm, slightly desaturated grade so the photo sits with the paper palette.
    image = ImageEnhance.Color(image).enhance(0.94)
    image = Image.blend(image, Image.new("RGB", image.size, WARM), 0.035)
    OUT.mkdir(parents=True, exist_ok=True)

    for width in WIDTHS:
        dest = OUT / f"minilab-{width}.webp"
        resize(image, width).save(dest, "WEBP", quality=82, method=6)
        print(f"{dest.relative_to(ROOT)}  {dest.stat().st_size / 1024:.1f} KB")

    dest = OUT / "minilab-1440.jpg"
    resize(image, 1440).save(dest, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"{dest.relative_to(ROOT)}  {dest.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
