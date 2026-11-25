from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public/og"
LAB = ROOT / "public/assets/lab/minilab-1440.jpg"

BG = (251, 251, 249)
TEXT = (22, 22, 22)
MUTED = (107, 107, 107)
ACCENT = (15, 107, 95)
LINE = (228, 228, 223)
DOT = (238, 238, 233)

LATIN_BOLD = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
]
LATIN_REG = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
]
CJK_BOLD = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]
CJK_REG = [
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]


def load(candidates, size):
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


LOCALES = {
    "en": {
        "file": "og-default-v3.png",
        "label": "ROBOTICS ENGINEERING · HUST",
        "name": "Robusr Guo",
        "role": "AI × Engineering builder.",
        "intro": [
            "Ten years in a bedroom lab, now turning",
            "real-world problems into working hardware",
            "and building AI tools for engineering.",
        ],
        "plate": "MINI LAB · 00",
        "caption": "Fig. 00 — The bedroom workbench.",
        "date": "Wuhan, China · November 2026",
        "cjk": False,
    },
    "zh": {
        "file": "og-default-v3-zh.png",
        "label": "华中科技大学 · 机器人工程",
        "name": "郭沫晗",
        "role": "AI × 工程建造者。",
        "intro": [
            "十年卧室极客，把真实问题",
            "做成能运行的硬件，再用 AI",
            "压缩从想法到零件的距离。",
        ],
        "plate": "迷你实验室 · 00",
        "caption": "图 00 — 卧室工作台。",
        "date": "武汉 · 2026 年 11 月",
        "cjk": True,
    },
    "fr": {
        "file": "og-default-v3-fr.png",
        "label": "GÉNIE ROBOTIQUE · HUST",
        "name": "Robusr Guo",
        "role": "Bâtisseur IA × ingénierie.",
        "intro": [
            "Dix ans dans une chambre-labo,",
            "des problèmes réels transformés en",
            "matériel, puis des outils d’IA.",
        ],
        "plate": "MINI LAB · 00",
        "caption": "Fig. 00 — L’établi de la chambre.",
        "date": "Wuhan, Chine · novembre 2026",
        "cjk": False,
    },
}


def spaced(draw, text, x, y, font, fill, tracking):
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        x += draw.textlength(char, font=font) + tracking


def build(locale_code):
    spec = LOCALES[locale_code]
    if spec["cjk"]:
        bold = load(CJK_BOLD, 78)
        label_font = load(CJK_REG, 16)
        body = load(CJK_REG, 26)
        small = load(CJK_REG, 18)
        caption = load(CJK_REG, 16)
        tracking = 1.2
    else:
        bold = load(LATIN_BOLD, 78)
        label_font = load(LATIN_BOLD, 16)
        body = load(LATIN_REG, 26)
        small = load(LATIN_REG, 18)
        caption = load(LATIN_REG, 16)
        tracking = 3.2

    latin_small = load(LATIN_REG, 18)
    img = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(img)

    for y in range(18, 630, 18):
        for x in range(18, 1200, 18):
            d.ellipse((x, y, x + 1.2, y + 1.2), fill=DOT)

    for x, y, sx, sy in [(24, 24, 1, 1), (1176, 24, -1, 1), (24, 606, 1, -1), (1176, 606, -1, -1)]:
        d.line((x, y, x + 18 * sx, y), fill=LINE, width=1)
        d.line((x, y, x, y + 18 * sy), fill=LINE, width=1)

    spaced(d, spec["label"], 72, 86, label_font, ACCENT, tracking)
    d.text((72, 118), spec["name"], font=bold, fill=TEXT)
    d.text((72, 238), spec["role"], font=body, fill=TEXT)
    for index, line in enumerate(spec["intro"]):
        d.text((72, 292 + index * 36), line, font=body, fill=MUTED)

    d.line((650, 86, 650, 500), fill=LINE, width=1)

    plate = ImageOps.fit(Image.open(LAB).convert("RGB"), (438, 328), Image.Resampling.LANCZOS, centering=(0.5, 0.45))
    d.rectangle((678, 98, 1140, 450), fill=(255, 255, 255), outline=LINE, width=1)
    img.paste(plate, (690, 110))
    spaced(d, spec["plate"], 690, 70, label_font, ACCENT, tracking)
    d.text((690, 468), spec["caption"], font=caption, fill=MUTED)

    d.line((72, 520, 1128, 520), fill=LINE, width=1)
    d.text((72, 542), "robusr.cn", font=latin_small, fill=ACCENT)
    d.text((72, 574), spec["date"], font=small, fill=MUTED)
    d.text((1128, 542), "WHY NOT?", font=latin_small, fill=ACCENT, anchor="ra")

    dest = OUT / spec["file"]
    img.save(dest, "PNG", optimize=True)
    print(dest, dest.stat().st_size)


OUT.mkdir(parents=True, exist_ok=True)
for code in LOCALES:
    build(code)
