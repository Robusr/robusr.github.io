#!/usr/bin/env python3
"""
Generate a hardcoded ASCII pixel-art logo block from name.png.

Usage:
    python3 scripts/ascii_gen.py > /tmp/logo.txt

Then copy the LOGO_ART array from stdout into index.html.

Dependencies: Pillow (pip install Pillow)
"""

from PIL import Image
import sys

IMG_PATH = 'name.png'
MAX_WIDTH = 96
V_CORR = 0.85
THRESHOLD_BIAS = 0.45   # lower = more foreground detail


def main():
    img = Image.open(IMG_PATH).convert('RGBA')

    # Auto-crop transparent borders
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        print(f'// Auto-cropped: {bbox[0]},{bbox[1]} -> {bbox[2]},{bbox[3]}  '
              f'({img.width}x{img.height})', file=sys.stderr)

    ratio = img.height / img.width
    width = min(MAX_WIDTH, img.width)
    height = max(8, int(width * ratio * V_CORR))

    # Composite onto black
    bg = Image.new('RGBA', (width, height), (0, 0, 0, 255))
    resized = img.resize((width, height), Image.LANCZOS)
    bg.paste(resized, (0, 0), resized)

    # Collect luminance values (alpha-gated)
    pixels = list(bg.getdata())
    lums = []
    for r, g, b, a in pixels:
        if a < 128:
            lums.append(0)
        else:
            lums.append(0.299 * r + 0.587 * g + 0.114 * b)

    # Adaptive threshold (mean of foreground * bias)
    nonzero = [lum for lum in lums if lum > 2]
    threshold = (sum(nonzero) / len(nonzero)) * THRESHOLD_BIAS if nonzero else 50

    print(f'// {width}x{height} chars, threshold={threshold:.1f}, '
          f'bias={THRESHOLD_BIAS}', file=sys.stderr)

    # Emit LOGO_ART JavaScript array
    print('const LOGO_ART = [')
    for row in range(height):
        line = ''
        for col in range(width):
            idx = row * width + col
            line += '#' if lums[idx] > threshold else ' '
        print(f"'{line}',")
    print("].join('\\n');")


if __name__ == '__main__':
    main()
