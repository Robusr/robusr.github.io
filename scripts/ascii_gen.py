#!/usr/bin/env python3
"""
Generate a row-shift italic ASCII pixel-art logo with per-letter colours.

Renders text upright, binarises, then applies a progressive row-shift
to create a clean slanted-block italic effect (no font distortion).

Usage:
    python3 scripts/ascii_gen.py
    python3 scripts/ascii_gen.py "Robusr" 80 13 20 2

Dependencies: Pillow (pip install Pillow)
"""

import sys
from PIL import Image, ImageDraw, ImageFont

TEXT        = sys.argv[1] if len(sys.argv) > 1 else 'Robusr'
CANVAS_W    = int(sys.argv[2]) if len(sys.argv) > 2 else 80
CANVAS_H    = int(sys.argv[3]) if len(sys.argv) > 3 else 13
FONT_SIZE   = int(sys.argv[4]) if len(sys.argv) > 4 else 20
SLANT       = int(sys.argv[5]) if len(sys.argv) > 5 else 2
THRESH_BIAS = 0.42
COLORS      = ['#FF6188','#FC9867','#FFD866','#A9DC76','#78DCE8','#AB9DF2']


def main():
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', FONT_SIZE)
    except Exception:
        font = ImageFont.load_default()

    # ---- Render upright text ----
    txt_w, txt_h = 200, CANVAS_H + 4
    full_img = Image.new('L', (txt_w, txt_h), 0)
    full_draw = ImageDraw.Draw(full_img)
    full_draw.text((2, 0), TEXT, fill=255, font=font)
    bbox = full_img.getbbox()
    if bbox:
        full_img = full_img.crop(bbox)

    # ASCII width (reserve room for row-shift)
    ascii_w = min(CANVAS_W - SLANT * CANVAS_H, full_img.width)
    ascii_h = CANVAS_H

    scaled = full_img.resize((ascii_w, ascii_h), Image.LANCZOS)
    pixels = list(scaled.getdata())
    nonzero = [p for p in pixels if p > 15]
    thresh = (sum(nonzero) / len(nonzero)) * THRESH_BIAS if nonzero else 100

    # ---- Upright ASCII ----
    upright = []
    for row in range(ascii_h):
        line = ''
        for col in range(ascii_w):
            idx = row * ascii_w + col
            line += '#' if pixels[idx] > thresh else ' '
        upright.append(line)

    # ---- Row-shift slant ----
    total_w = ascii_w + SLANT * (ascii_h - 1)
    slanted = []
    for row, line in enumerate(upright):
        left_pad = SLANT * row
        slanted.append(
            ' ' * left_pad + line +
            ' ' * (total_w - left_pad - len(line))
        )

    # Trim empty lines
    while slanted and not slanted[0].strip():
        slanted.pop(0)
    while slanted and not slanted[-1].strip():
        slanted.pop()

    # ---- Per-letter boundaries ----
    letter_bounds = []
    for i in range(len(TEXT)):
        pfx = Image.new('L', (txt_w, txt_h), 0)
        pd = ImageDraw.Draw(pfx)
        pd.text((2, 0), TEXT[:i+1], fill=255, font=font)
        if bbox: pfx = pfx.crop(bbox)
        pfx_s = pfx.resize((ascii_w, ascii_h), Image.LANCZOS)

        prv = Image.new('L', (txt_w, txt_h), 0)
        if i > 0:
            pv = ImageDraw.Draw(prv)
            pv.text((2, 0), TEXT[:i], fill=255, font=font)
            if bbox: prv = prv.crop(bbox)
        prv_s = prv.resize((ascii_w, ascii_h), Image.LANCZOS) if i > 0 \
                else Image.new('L', (ascii_w, ascii_h), 0)

        pd_data = list(pfx_s.getdata())
        pv_data = list(prv_s.getdata())

        min_c, max_c = 9999, -1
        for y in range(ascii_h):
            for x in range(ascii_w):
                idx = y * ascii_w + x
                if pd_data[idx] > 25 and (i == 0 or pv_data[idx] <= 25):
                    if x < min_c: min_c = x
                    if x > max_c: max_c = x
        letter_bounds.append(
            (TEXT[i], min_c if min_c < 9999 else 0, max_c + 1)
        )

    # Merge with midpoints
    adjusted = []
    prev_end = 0
    for letter, start, end in letter_bounds:
        if adjusted:
            mid = (prev_end + start) // 2
            adjusted[-1] = (adjusted[-1][0], adjusted[-1][1], mid)
            start = mid
        start = max(start, prev_end)
        end = max(end, start + 1)
        adjusted.append((letter, start, end))
        prev_end = end

    splits = [end for _, _, end in adjusted[:-1]]

    # ---- Output ----
    print(f'// {len(slanted)} lines x {total_w} cols, '
          f'slant={SLANT} chars/row, thresh={thresh:.0f}',
          file=sys.stderr)
    for letter, start, end in adjusted:
        print(f'//   {letter}: cols {start}-{end} ({end-start} wide)',
              file=sys.stderr)

    print('const LOGO_UP = [')
    for l in slanted:
        print(f"'{l}',")
    print('];')
    print(f'const LOGO_UP_SPLITS = {splits};')
    print(f'const LOGO_COLORS = {COLORS};')
    print(f'const LOGO_UP_WIDTH = {total_w};')
    print(f'const LOGO_SLANT = {SLANT};')
    print(f"const LOGO_DIR = 'forward';")
    print(f'const LOGO_ROWS = {len(slanted)};')


if __name__ == '__main__':
    main()
