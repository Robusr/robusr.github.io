#!/usr/bin/env python3
"""Derive transparent line-art WebP assets from the hand-drawn IP art in "Robusr IP/".

Run from the repo root: python3 scripts/make-ip-assets.py
Requires Pillow.
"""
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Robusr IP"
OUT = ROOT / "public/assets/brand"
INK = (10, 13, 41)  # matches the navy ink in the source drawings


def ink_alpha(gray: Image.Image, floor: int, gain: float) -> Image.Image:
    """Turn a grayscale scan (white paper = 255) into an ink-alpha mask."""
    lut = []
    span = 255 - floor
    for value in range(256):
        darkness = 255 - value
        if darkness <= floor:
            lut.append(0)
        else:
            lut.append(min(255, round((darkness - floor) / span * 255 * gain)))
    return gray.point(lut)


def build(src: Path, dest: Path, max_width: int, floor: int, gain: float, margin: int, quality: int = 84) -> None:
    image = Image.open(src)
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    # Compose over white so white fills and paper both read as "no ink".
    paper = Image.new("RGBA", image.size, (255, 255, 255, 255))
    flat = Image.alpha_composite(paper, image).convert("RGB")
    alpha = ink_alpha(ImageOps.grayscale(flat), floor, gain)

    bbox = alpha.getbbox()
    if bbox:
        left, top, right, bottom = bbox
        left = max(0, left - margin)
        top = max(0, top - margin)
        right = min(alpha.width, right + margin)
        bottom = min(alpha.height, bottom + margin)
        alpha = alpha.crop((left, top, right, bottom))

    if alpha.width > max_width:
        height = round(alpha.height * max_width / alpha.width)
        alpha = alpha.resize((max_width, height), Image.LANCZOS)
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.3))

    ink = Image.new("RGBA", alpha.size, INK + (0,))
    ink.putalpha(alpha)
    OUT.mkdir(parents=True, exist_ok=True)
    ink.save(dest, "WEBP", quality=quality, alpha_quality=min(92, quality + 8), method=6)
    print(f"{dest.relative_to(ROOT)}  {ink.width}x{ink.height}  {dest.stat().st_size / 1024:.1f} KB")


build(SRC / "A.jpg", OUT / "robusr-ip-v2.webp", max_width=1100, floor=16, gain=1.35, margin=48)
build(SRC / "A.jpg", OUT / "robusr-ip-480.webp", max_width=480, floor=16, gain=1.35, margin=48, quality=78)
build(SRC / "B.PNG", OUT / "robusr-standing.webp", max_width=1040, floor=8, gain=1.5, margin=56)
build(SRC / "B.PNG", OUT / "robusr-standing-640.webp", max_width=640, floor=8, gain=1.5, margin=56)
