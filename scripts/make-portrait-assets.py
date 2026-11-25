#!/usr/bin/env python3
"""Regrade the portrait into v3 assets for the paper palette.

Usage:
    python3 scripts/make-portrait-assets.py

Reads the published 512 px portrait and writes 512 JPEG/WebP and 260 WebP
without EXIF metadata.
"""
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "public/assets/profile/portrait-robusr-512-v2.jpg"
OUT = ROOT / "public/assets/profile"
WARM = (252, 245, 235)


def resize(image: Image.Image, width: int) -> Image.Image:
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def main() -> None:
    image = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
    image = ImageEnhance.Color(image).enhance(0.97)
    image = Image.blend(image, Image.new("RGB", image.size, WARM), 0.04)

    image.save(OUT / "portrait-robusr-512-v3.jpg", "JPEG", quality=90, optimize=True, progressive=True)
    image.save(OUT / "portrait-robusr-512-v3.webp", "WEBP", quality=88, method=6)
    resize(image, 260).save(OUT / "portrait-robusr-260-v3.webp", "WEBP", quality=86, method=6)

    for name in ("portrait-robusr-512-v3.jpg", "portrait-robusr-512-v3.webp", "portrait-robusr-260-v3.webp"):
        path = OUT / name
        print(f"{path.relative_to(ROOT)}  {path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
