#!/usr/bin/env python3
"""
Generate a hardcoded ASCII pixel-art logo from text.

Renders the target string with a monospace font at a small bitmap
size, binarises, and emits a JavaScript LOGO_ART array ready to
paste into index.html.

Usage:
    python3 scripts/ascii_gen.py
    python3 scripts/ascii_gen.py "YOURNAME" 100 14 18

Dependencies: Pillow (pip install Pillow)
"""

import sys
from PIL import Image, ImageDraw, ImageFont

TEXT       = sys.argv[1] if len(sys.argv) > 1 else 'Robusr'
WIDTH      = int(sys.argv[2]) if len(sys.argv) > 2 else 100
HEIGHT     = int(sys.argv[3]) if len(sys.argv) > 3 else 13
FONT_SIZE  = int(sys.argv[4]) if len(sys.argv) > 4 else 18
THRESH_BIAS = 0.5  # lower = more foreground


def main():
    img = Image.new('L', (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(img)

    # Try Menlo (macOS), fall back to default
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', FONT_SIZE)
    except Exception:
        font = ImageFont.load_default()

    # Centre the text
    bbox = draw.textbbox((0, 0), TEXT, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (WIDTH - tw) // 2
    y = (HEIGHT - th) // 2 - bbox[1]
    draw.text((x, y), TEXT, fill=255, font=font)

    pixels = list(img.getdata())
    nonzero = [p for p in pixels if p > 10]
    thresh = (sum(nonzero) / len(nonzero)) * THRESH_BIAS if nonzero else 128

    lines = []
    for row in range(HEIGHT):
        line = ''
        for col in range(WIDTH):
            idx = row * WIDTH + col
            line += '#' if pixels[idx] > thresh else ' '
        lines.append(line)

    widths = set(len(l) for l in lines)
    print(f'// {len(lines)} lines, widths={widths}, thresh={thresh:.0f}',
          file=sys.stderr)
    print('const LOGO_ART = [')
    for l in lines:
        print(f"'{l}',")
    print("].join('\\n');")


if __name__ == '__main__':
    main()
