from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public/og/og-default.png"
PORTRAIT = ROOT / "public/assets/profile/portrait-robusr-512.jpg"

BG = (251, 251, 249)
TEXT = (22, 22, 22)
MUTED = (107, 107, 107)
ACCENT = (15, 107, 95)
LINE = (228, 228, 223)

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

def load(cands, size):
    for p in cands:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()

bold = load(BOLD_CANDIDATES, 76)
label_font = load(BOLD_CANDIDATES, 17)
body = load(REG_CANDIDATES, 31)
small = load(REG_CANDIDATES, 20)

img = Image.new("RGB", (1200, 630), BG)
d = ImageDraw.Draw(img)

# portrait
p = ImageOps.fit(Image.open(PORTRAIT).convert("RGB"), (380, 380), Image.LANCZOS, centering=(0.5, 0.42))
img.paste(p, (748, 125))

# label with letterspacing
label = "ROBOTICS ENGINEERING · HUST"
x = 72
for ch in label:
    d.text((x, 88), ch, font=label_font, fill=ACCENT)
    x += d.textlength(ch, font=label_font) + 3.2

d.text((72, 124), "Robusr Guo", font=bold, fill=TEXT)

d.text((72, 248), "AI × Engineering builder.", font=body, fill=TEXT)
d.text((72, 292), "I turn real-world problems into working hardware,", font=body, fill=MUTED)
d.text((72, 332), "then use AI to compress the distance from idea", font=body, fill=MUTED)
d.text((72, 372), "to part.", font=body, fill=MUTED)

d.line((72, 500, 660, 500), fill=LINE, width=1)
d.text((72, 522), "robusr.cn", font=small, fill=ACCENT)
d.text((72, 556), "Wuhan, China · October 2026", font=small, fill=MUTED)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(OUT, OUT.stat().st_size)
