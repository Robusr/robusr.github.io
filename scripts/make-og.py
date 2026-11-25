from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public/og/og-default-v3.png"
LAB = ROOT / "public/assets/lab/minilab-1440.jpg"

BG = (251, 251, 249)
TEXT = (22, 22, 22)
MUTED = (107, 107, 107)
ACCENT = (15, 107, 95)
LINE = (228, 228, 223)
DOT = (238, 238, 233)

BOLD_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
]
REG_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
]


def load(candidates, size):
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


bold = load(BOLD_CANDIDATES, 78)
label_font = load(BOLD_CANDIDATES, 16)
body = load(REG_CANDIDATES, 26)
small = load(REG_CANDIDATES, 18)
caption = load(REG_CANDIDATES, 16)

img = Image.new("RGB", (1200, 630), BG)
d = ImageDraw.Draw(img)

# Faint drafting dot grid.
for y in range(18, 630, 18):
    for x in range(18, 1200, 18):
        d.ellipse((x, y, x + 1.2, y + 1.2), fill=DOT)


def spaced(text, x, y, font, fill, tracking=3.2):
    for char in text:
        d.text((x, y), char, font=font, fill=fill)
        x += d.textlength(char, font=font) + tracking


# Corner crop marks.
for x, y, sx, sy in [(24, 24, 1, 1), (1176, 24, -1, 1), (24, 606, 1, -1), (1176, 606, -1, -1)]:
    d.line((x, y, x + 18 * sx, y), fill=LINE, width=1)
    d.line((x, y, x, y + 18 * sy), fill=LINE, width=1)

# Left column.
spaced("ROBOTICS ENGINEERING · HUST", 72, 86, label_font, ACCENT)
d.text((72, 118), "Robusr Guo", font=bold, fill=TEXT)
d.text((72, 238), "AI × Engineering builder.", font=body, fill=TEXT)

intro = [
    "Ten years in a bedroom lab, now turning",
    "real-world problems into working hardware",
    "and building AI tools for engineering.",
]
for index, line in enumerate(intro):
    d.text((72, 292 + index * 36), line, font=body, fill=MUTED)

d.line((650, 86, 650, 500), fill=LINE, width=1)

# Mini Lab plate.
plate = ImageOps.fit(Image.open(LAB).convert("RGB"), (438, 328), Image.Resampling.LANCZOS, centering=(0.5, 0.45))
d.rectangle((678, 98, 1140, 450), fill=(255, 255, 255), outline=LINE, width=1)
img.paste(plate, (690, 110))
spaced("MINI LAB · 00", 690, 70, label_font, ACCENT, tracking=2.6)
d.text((690, 468), "Fig. 00 — The bedroom workbench.", font=caption, fill=MUTED)

# Footer.
d.line((72, 520, 1128, 520), fill=LINE, width=1)
d.text((72, 542), "robusr.cn", font=small, fill=ACCENT)
d.text((72, 574), "Wuhan, China · November 2026", font=small, fill=MUTED)
d.text((1128, 542), "WHY NOT?", font=small, fill=ACCENT, anchor="ra")

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(OUT, OUT.stat().st_size)
