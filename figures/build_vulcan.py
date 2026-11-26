#!/usr/bin/env python3
"""Build the Vulcan pilot plates (A–D) as editable SVG + web derivatives.

Design system: paper / ink / one teal accent + a warm physical-render tone.
Canvas: 1600×900 viewBox, declared 183×103 mm so the journal-style audit can
measure text at final physical size. All labels are live <text>.
"""
from __future__ import annotations

import base64
import io
import json
import os
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageFont

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
CROPS = ROOT / "crops"
FONT_TTF = ROOT / "fonts" / "InterVariable.ttf"

# ---- palette ---------------------------------------------------------------
PAPER = "#FBFBF9"
SURFACE = "#FFFFFF"
INK = "#0A0D29"
TEXT = "#161616"
MUTED = "#6B6B6B"
LINE = "#D8D8D1"
LINE_SOFT = "#E8E8E2"
ACCENT = "#0F6B5F"
ACCENT_STRONG = "#0A4F46"
ACCENT_SOFT = "#E9F1EE"
WARM = "#B26A3C"
WARM_SOFT = "#F5EDE6"
RED = "#A33A2B"
CODE_BG = "#10131B"
CODE_FG = "#E8E6DF"
CODE_KEY = "#8FC7BA"
CODE_STR = "#D9A97E"
CODE_MUTED = "#8B8F9A"

FONT = "Inter, 'PingFang SC', 'Noto Sans SC', 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SFMono-Regular', Menlo, Consolas, monospace"

W, H = 1600, 900


def font(size: int, weight: int = 400) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(FONT_TTF), size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def text_w(s: str, size: int, weight: int = 400) -> float:
    f = font(size, weight)
    w = 0.0
    for ch in s:
        w += size if ord(ch) > 0x2E80 else f.getlength(ch)
    return w


def wrap(s: str, size: int, max_w: float, weight: int = 400) -> list[str]:
    words = s.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if text_w(trial, size, weight) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    # break any over-wide token (CJK prompts, long identifiers) by character
    out: list[str] = []
    for line in lines:
        if text_w(line, size, weight) <= max_w:
            out.append(line)
            continue
        chunk = ""
        for ch in line:
            if text_w(chunk + ch, size, weight) > max_w and chunk:
                out.append(chunk)
                chunk = ch
            else:
                chunk += ch
        if chunk:
            out.append(chunk)
    return out


def img_uri(path: Path) -> str:
    im = Image.open(path).convert("RGB")
    buf = io.BytesIO()
    im.save(buf, format="WEBP", quality=94, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def fit(path: Path, x: float, y: float, w: float, h: float):
    iw, ih = Image.open(path).size
    s = min(w / iw, h / ih)
    nw, nh = iw * s, ih * s
    return (x + (w - nw) / 2, y + (h - nh) / 2, nw, nh)


class Svg:
    def __init__(self, name: str):
        self.name = name
        self.parts: list[str] = []
        self.defs: list[str] = []
        self._stack: list[list[str]] = []
        self.marker_prefix = "".join(ch for ch in name.lower() if ch.isalnum())[:24]

    def add(self, s: str):
        (self._stack[-1] if self._stack else self.parts).append(s)
        return s

    def begin(self):
        self._stack.append([])

    def end_group(self, gid, cls="layer"):
        content = "".join(self._stack.pop())
        self.group(gid, content, cls)

    def text(self, x, y, s, size=17, weight=400, fill=TEXT, anchor="start",
             ls=0, opacity=1, family=FONT, extra=""):
        s = escape(str(s))
        self.add(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{ls}" opacity="{opacity}" {extra}>{s}</text>'
        )

    def lines(self, x, y, lines, size=17, weight=400, fill=TEXT, lead=1.45, anchor="start"):
        for i, line in enumerate(lines):
            self.text(x, y + i * size * lead, line, size, weight, fill, anchor)

    def rect(self, x, y, w, h, fill="none", stroke=LINE, sw=1.2, rx=4,
             opacity=1, extra=""):
        self.add(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'opacity="{opacity}" {extra}/>'
        )

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1.4, dash=None, marker=None,
             path_length=None, opacity=1):
        extra = ""
        if dash:
            extra += f' stroke-dasharray="{dash}"'
        if marker:
            extra += f' marker-end="url(#{marker})"'
        if path_length:
            extra += f' pathLength="{path_length}"'
        self.add(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}" {extra}/>'
        )

    def path(self, d, stroke=INK, sw=1.4, fill="none", marker=None, dash=None,
             path_length=None):
        extra = ""
        if marker:
            extra += f' marker-end="url(#{marker})"'
        if dash:
            extra += f' stroke-dasharray="{dash}"'
        if path_length:
            extra += f' pathLength="{path_length}"'
        self.add(
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
        )

    def arrow(self, x1, y1, x2, y2, stroke=INK, sw=1.5, dash=None, group=None):
        marker = {"#" + INK: f"{self.marker_prefix}-ink",
                  "#" + ACCENT: f"{self.marker_prefix}-accent",
                  "#" + WARM: f"{self.marker_prefix}-warm",
                  "#" + MUTED: f"{self.marker_prefix}-muted"}.get(stroke, f"{self.marker_prefix}-ink")
        self.line(x1, y1, x2, y2, stroke, sw, dash, marker, path_length=1)

    def arrow_path(self, d, stroke=INK, sw=1.5, dash=None):
        marker = {"#" + INK: f"{self.marker_prefix}-ink",
                  "#" + ACCENT: f"{self.marker_prefix}-accent",
                  "#" + WARM: f"{self.marker_prefix}-warm",
                  "#" + MUTED: f"{self.marker_prefix}-muted"}.get(stroke, f"{self.marker_prefix}-ink")
        self.path(d, stroke, sw, "none", marker, dash, path_length=1)

    def chip(self, x, y, label, fill=ACCENT_SOFT, color=ACCENT, size=15,
             stroke="none", pad_x=9, h=24):
        w = text_w(label, size, 500) + pad_x * 2
        self.rect(x, y, w, h, fill, stroke, 1, h / 2)
        self.text(x + pad_x, y + h / 2 + size * 0.36, label, size, 500, color)
        return w

    def image(self, path: Path, x, y, w, h, border=True, rx=3):
        ix, iy, nw, nh = fit(path, x, y, w, h)
        clip = f"clip-{self.marker_prefix}-{len(self.parts)}"
        self.defs.append(
            f'<clipPath id="{clip}"><rect x="{ix:.1f}" y="{iy:.1f}" width="{nw:.1f}" height="{nh:.1f}" rx="{rx}"/></clipPath>'
        )
        self.add(
            f'<image href="{img_uri(path)}" x="{ix:.1f}" y="{iy:.1f}" width="{nw:.1f}" height="{nh:.1f}" '
            f'preserveAspectRatio="xMidYMid meet" clip-path="url(#{clip})"/>'
        )
        if border:
            self.rect(ix, iy, nw, nh, "none", LINE, 1, rx)

    def group(self, gid, content: str, cls="layer"):
        self.add(f'<g id="{gid}" class="{cls}">{content}</g>')

    def render(self, body: str) -> str:
        markers = ""
        for key, color in [("ink", INK), ("accent", ACCENT), ("warm", WARM), ("muted", MUTED)]:
            markers += (
                f'<marker id="{self.marker_prefix}-{key}" markerWidth="8" markerHeight="8" '
                f'refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse">'
                f'<path d="M0,0 L8,4 L0,8 z" fill="{color}"/></marker>'
            )
        defs = "<defs>" + markers + "".join(self.defs) + "</defs>"
        return (
            f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="220mm" height="123.75mm" '
            f'viewBox="0 0 {W} {H}" role="img">\n'
            f"<title>{escape(self.name)}</title>\n"
            f'{defs}\n<rect width="{W}" height="{H}" fill="{PAPER}"/>\n{body}\n</svg>\n'
        )


def header(s: Svg, letter: str, kicker: str, title: str, subtitle: str, right: str = "VULCAN · v1.3.0"):
    # panel letter
    s.rect(56, 42, 34, 34, ACCENT, "none", 0, 3)
    s.text(73, 66, letter, 19, 600, PAPER, "middle")
    s.text(106, 58, kicker.upper(), 16, 600, ACCENT, ls=1.4)
    s.text(104, 100, title, 33, 600, INK)
    s.text(104, 132, subtitle, 18, 400, MUTED)
    s.line(56, 158, W - 56, 158, LINE, 1.2)
    s.text(W - 56, 58, right, 16, 500, MUTED, "end", ls=0.6)


def footer(s: Svg, left: str, right: str):
    s.line(56, 858, W - 56, 858, LINE_SOFT, 1)
    s.text(56, 880, left, 15.5, 400, MUTED)
    s.text(W - 56, 880, right, 15.5, 500, ACCENT, "end", ls=0.4)


def section_label(s: Svg, x, y, n, label, color=ACCENT):
    s.text(x, y, f"{n} · {label.upper()}", 16, 600, color, ls=1.2)


# ---------------------------------------------------------------------------
# Panel A — system loop (animated)
# ---------------------------------------------------------------------------
def panel_a():
    s = Svg("Vulcan A — system loop")
    header(s, "A", "System loop", "One sentence becomes a native feature tree",
           "The model fills a typed schema; the server validates it; you confirm; the client executes native SolidWorks features.")
    plate = CROPS / "vulcan-plate-crop.png"

    # ---- stage 1: prompt
    s.begin()
    s.rect(56, 196, 286, 196, SURFACE, LINE, 1.2, 5)
    s.text(74, 222, "1 · DESCRIBE", 16, 600, ACCENT, ls=1.2)
    s.text(74, 250, "Natural language", 22, 600, INK)
    s.rect(74, 264, 250, 74, PAPER, LINE, 1, 4)
    prompt = "在前视基准面拉伸 200×100×20 的安装板，四角各打一个直径 10 mm 的通孔"
    for i, ln in enumerate(wrap(prompt, 14.5, 222, 400)):
        s.add(f'<text x="86" y="{286 + i*22}" font-family="{FONT}" font-size="14.5" fill="{TEXT}">{escape(ln)}</text>')
    s.rect(74, 348, 110, 26, ACCENT, "none", 0, 3)
    s.text(129, 366, "开始生成", 15, 600, PAPER, "middle")
    s.text(196, 366, "streamed over SSE", 14.5, 400, MUTED)
    s.text(74, 390, "Chinese, English, or French input", 14.5, 400, MUTED)
    s.rect(56, 196, 286, 196, "none", ACCENT, 2.2, 5, opacity=0, extra='id="a-focus1"')
    s.end_group("a-prompt")

    s.group("a-arrow1", f'<line x1="342" y1="294" x2="384" y2="294" stroke="{INK}" stroke-width="1.6" marker-end="url(#{s.marker_prefix}-ink)" pathLength="1"/>')

    # ---- stage 2: server
    s.begin()
    s.rect(390, 196, 302, 196, SURFACE, LINE, 1.2, 5)
    s.text(408, 222, "2 · PARAMETERIZE", 16, 600, ACCENT, ls=1.2)
    s.text(408, 250, "Flask server", 22, 600, INK)
    s.rect(408, 266, 266, 42, PAPER, LINE, 1, 4)
    s.text(420, 283, "Versioned SolidWorks domain prompt", 15.5, 500, TEXT)
    s.text(420, 300, "prepended to the request", 14.5, 400, MUTED)
    s.rect(408, 316, 266, 42, PAPER, LINE, 1, 4)
    s.text(420, 333, "Provider adapter", 15.5, 500, TEXT)
    s.text(420, 350, "OpenAI-compatible · Anthropic", 14.5, 400, MUTED)
    s.text(408, 382, "REST / JSON", 14.5, 500, WARM)
    s.text(500, 382, "·", 14.5, 400, MUTED)
    s.text(514, 382, "SSE fallback", 14.5, 500, WARM)
    s.rect(390, 196, 302, 196, "none", ACCENT, 2.2, 5, opacity=0, extra='id="a-focus2"')
    s.end_group("a-server")

    s.group("a-arrow2", f'<line x1="692" y1="294" x2="734" y2="294" stroke="{INK}" stroke-width="1.6" marker-end="url(#{s.marker_prefix}-ink)" pathLength="1"/>')

    # ---- stage 3: model / typed JSON
    s.begin()
    s.rect(740, 196, 332, 236, SURFACE, LINE, 1.2, 5)
    s.text(758, 222, "3 · GENERATE", 16, 600, ACCENT, ls=1.2)
    s.text(758, 250, "Any compatible model", 22, 600, INK)
    s.text(758, 273, "Returns typed JSON — never code", 14.5, 400, MUTED)
    s.rect(758, 288, 296, 112, CODE_BG, "none", 0, 3)
    code = [
        ('{', CODE_FG),
        ('  "feature_type": "extrude",', CODE_KEY),
        ('  "params": {', CODE_FG),
        ('    "shape": "rectangle",', CODE_STR),
        ('    "length": 200, "width": 100,', CODE_STR),
        ('    "depth": 20', CODE_STR),
        ('  }', CODE_FG),
    ]
    for i, (ln, col) in enumerate(code):
        s.add(f'<text id="a-code-{i}" x="770" y="{310 + i*14.2}" font-family="{MONO}" font-size="13.5" fill="{col}">{escape(ln)}</text>')
    s.text(758, 418, "No exec() · no generated code surface", 14.5, 500, ACCENT)
    s.rect(740, 196, 332, 236, "none", ACCENT, 2.2, 5, opacity=0, extra='id="a-focus3"')
    s.end_group("a-model")

    s.group("a-arrow3", f'<line x1="1072" y1="314" x2="1114" y2="314" stroke="{INK}" stroke-width="1.6" marker-end="url(#{s.marker_prefix}-ink)" pathLength="1"/>')

    # ---- stage 4: gates
    s.begin()
    s.rect(1120, 196, 210, 196, SURFACE, LINE, 1.2, 5)
    s.text(1138, 222, "4 · VALIDATE", 16, 600, ACCENT, ls=1.2)
    s.text(1138, 250, "Two gates", 22, 600, INK)
    s.rect(1138, 266, 174, 40, ACCENT_SOFT, ACCENT, 1, 4)
    s.text(1152, 291, "✓  Schema check", 16, 600, ACCENT_STRONG)
    s.rect(1138, 314, 174, 40, WARM_SOFT, WARM, 1, 4)
    s.text(1152, 339, "✓  Human confirm", 16, 600, WARM)
    s.text(1138, 376, "editable preview", 14.5, 400, MUTED)
    s.rect(1120, 196, 210, 196, "none", ACCENT, 2.2, 5, opacity=0, extra='id="a-focus4"')
    s.end_group("a-gate")

    s.group("a-arrow4", f'<line x1="1330" y1="294" x2="1372" y2="294" stroke="{INK}" stroke-width="1.6" marker-end="url(#{s.marker_prefix}-ink)" pathLength="1"/>')

    # ---- stage 5: execute
    s.begin()
    s.rect(1378, 196, 166, 196, SURFACE, LINE, 1.2, 5)
    s.text(1396, 222, "5 · EXECUTE", 16, 600, ACCENT, ls=1.2)
    s.text(1396, 250, "C# COM", 22, 600, INK)
    s.text(1396, 274, "native feature APIs", 14.5, 400, MUTED)
    s.rect(1396, 292, 130, 26, PAPER, LINE, 1, 3)
    s.text(1404, 309, "FeatureExtrusion3", 13.5, 400, TEXT, family=MONO)
    s.rect(1396, 324, 130, 26, PAPER, LINE, 1, 3)
    s.text(1404, 341, "FeatureCut4", 13.5, 400, TEXT, family=MONO)
    s.text(1396, 378, "confirmed tree only", 14, 500, WARM)
    s.rect(1378, 196, 166, 196, "none", ACCENT, 2.2, 5, opacity=0, extra='id="a-focus5"')
    s.end_group("a-exec")

    s.group("a-arrow5", f'<path d="M1461,392 L1461,458" fill="none" stroke="{INK}" stroke-width="1.4" marker-end="url(#{s.marker_prefix}-ink)" pathLength="1" stroke-dasharray="4 4"/>')

    # ---- render card
    s.begin()
    s.rect(56, 458, 956, 340, SURFACE, LINE, 1.2, 5)
    s.text(74, 484, "REAL OUTPUT · SOLIDWORKS 2025", 16, 600, ACCENT, ls=1.2)
    s.text(74, 510, "A native plate, not a screenshot of a mesh", 20, 600, INK)
    s.add('<g id="a-render-img" style="transform-box: fill-box; transform-origin: center;">')
    ix, iy, iw, ih = fit(plate, 74, 534, 450, 250)
    clip = "clip-a-plate"
    s.defs.append(f'<clipPath id="{clip}"><rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="3"/></clipPath>')
    s.add(f'<image href="{img_uri(plate)}" x="{ix}" y="{iy}" width="{iw}" height="{ih}" preserveAspectRatio="xMidYMid meet" clip-path="url(#{clip})"/>')
    s.rect(ix, iy, iw, ih, "none", LINE, 1, 3)
    s.add('</g>')
    # evidence column right
    ex = 570
    s.text(ex, 560, "200 × 100 × 20", 38, 600, INK)
    s.text(ex, 584, "millimetres · base extrude", 15, 400, MUTED)
    s.line(ex, 600, 980, 600, LINE_SOFT, 1)
    facts = [
        ("4×", "Ø10 mm through holes"),
        ("1×", "editable native feature tree"),
        ("0", "lines of generated code executed"),
    ]
    for i, (big, small) in enumerate(facts):
        y = 630 + i * 48
        s.text(ex, y, big, 22, 600, WARM if i < 2 else ACCENT)
        s.text(ex + 38, y, small, 15.5, 400, TEXT)
    s.text(ex, 776, "Captured from the installed add-in", 14, 400, MUTED)
    s.rect(56, 458, 956, 340, "none", ACCENT, 2.2, 5, opacity=0, extra='id="a-focus6"')
    s.end_group("a-render")

    # ---- feature tree / evidence
    s.begin()
    s.rect(1032, 458, 512, 340, SURFACE, LINE, 1.2, 5)
    s.text(1050, 484, "NATIVE FEATURE TREE", 16, 600, ACCENT, ls=1.2)
    s.text(1050, 510, "Editable, not a mesh or a macro", 21, 600, INK)
    tree = [
        ("Mounting plate", 0, True),
        ("Sketch1 · 200 × 100", 1, False),
        ("Base-Extrude · 20 mm", 1, False),
        ("Cut-Extrude ×4 · Ø10 THRU", 1, False),
        ("Fillet · all edges", 1, False),
    ]
    for i, (label, depth, bold) in enumerate(tree):
        y = 548 + i * 34
        if i == 0:
            s.rect(1050, y - 18, 6, 18, ACCENT, "none", 0, 1)
        else:
            s.add(f'<line x1="1064" y1="{y-26}" x2="1064" y2="{y-8}" stroke="{LINE}" stroke-width="1"/>')
            s.add(f'<line x1="1064" y1="{y-8}" x2="1078" y2="{y-8}" stroke="{LINE}" stroke-width="1"/>')
        s.text(1050 + depth * 28, y, label, 17 if bold else 16, 600 if bold else 400,
               INK if bold else TEXT, family=MONO if not bold else FONT)
    s.line(1050, 720, 1526, 720, LINE_SOFT, 1)
    chips = [("no exec()", ACCENT), ("two gates", ACCENT), ("GPL-3.0", MUTED), ("typed JSON", WARM)]
    x = 1050
    for label, col in chips:
        cw = s.chip(x, 736, label, ACCENT_SOFT if col == ACCENT else (WARM_SOFT if col == WARM else PAPER),
                    col, 14.5, LINE if col == MUTED else "none")
        x += cw + 8
    s.text(1050, 788, "Only the confirmed tree reaches the COM modeler.", 14.5, 500, MUTED)
    s.rect(1032, 458, 512, 340, "none", ACCENT, 2.2, 5, opacity=0, extra='id="a-focus7"')
    s.end_group("a-tree")

    return s.render("\n".join(s.parts))


def panel_b():
    s = Svg("Vulcan B — deployed architecture")
    header(s, "B", "Deployed architecture", "Three processes, one typed contract",
           "Only the client runs beside SolidWorks. The server and the model can run locally, in Docker, or behind a tunnel.")

    cols = [
        (56, 520, "WINDOWS WORKSTATION", "beside SolidWorks"),
        (604, 520, "VULCAN SERVER", "Python 3.10+ · Flask 3"),
        (1152, 392, "LLM PROVIDER", "OpenAI-compatible or Anthropic"),
    ]
    for x, w, name, sub in cols:
        s.rect(x, 196, w, 560, "none", LINE, 1.1, 5)
        s.text(x + 18, 222, name, 16, 600, ACCENT, ls=1.2)
        s.text(x + 18, 242, sub, 14.5, 400, MUTED)

    # client column
    s.rect(78, 266, 476, 82, SURFACE, LINE, 1, 4)
    s.text(94, 292, "SolidWorks 2025", 19, 600, INK)
    s.text(94, 314, "Part · assembly · drawing · COM API", 15, 400, MUTED)
    s.text(94, 334, "the document and the modeler live here", 14.5, 400, MUTED)

    s.rect(78, 364, 476, 98, SURFACE, LINE, 1, 4)
    s.text(94, 390, "Vulcan add-in", 19, 600, INK)
    s.text(94, 412, "CommandManager tab · task pane · status window", 15, 400, MUTED)
    s.text(94, 432, "DPAPI settings · editable JSON preview", 15, 400, MUTED)
    s.text(94, 450, "human confirmation gate", 14.5, 600, WARM)

    s.rect(78, 478, 476, 82, SURFACE, LINE, 1, 4)
    s.text(94, 504, "COM executor", 19, 600, INK)
    s.text(94, 526, "FeatureExtrusion3 · FeatureCut4 · FeatureFillet3", 14.5, 400, MUTED, family=MONO)
    s.text(94, 546, "native features only — no exec()", 14.5, 500, ACCENT)

    # task pane inset
    s.rect(78, 580, 210, 156, SURFACE, LINE, 1, 4)
    s.image(CROPS / "vulcan-taskpane-crop.png", 82, 584, 202, 144, border=False)
    s.text(300, 596, "Operator surface", 16, 600, INK)
    s.text(300, 618, "The task pane is the primary surface.", 14.5, 400, MUTED)
    s.text(300, 637, "A modal panel is the fallback.", 14.5, 400, MUTED)
    
    s.text(300, 690, "DPAPI-encrypted key", 14.5, 500, WARM)
    s.text(300, 710, "stored on this machine", 14, 400, MUTED)

    # server column
    s.rect(626, 266, 476, 64, SURFACE, LINE, 1, 4)
    s.text(642, 292, "HTTP API", 19, 600, INK)
    s.text(642, 314, "POST /api/v1/generate · SSE /stream", 14.5, 400, MUTED, family=MONO)

    s.rect(626, 344, 476, 78, SURFACE, LINE, 1, 4)
    s.text(642, 370, "Prompt assembly", 19, 600, INK)
    s.text(642, 392, "versioned SolidWorks domain prompt", 15, 400, MUTED)
    s.text(642, 411, "prepended to the user request", 14.5, 400, MUTED)

    s.rect(626, 436, 476, 78, SURFACE, LINE, 1, 4)
    s.text(642, 462, "Provider adapter", 19, 600, INK)
    s.text(642, 484, "OpenAI chat completions", 15, 400, MUTED)
    s.text(642, 503, "Anthropic Messages API", 15, 400, MUTED)

    s.rect(626, 528, 476, 78, SURFACE, LINE, 1, 4)
    s.text(642, 554, "Validation + limits", 19, 600, INK)
    s.text(642, 576, "envelope · feature params · units", 15, 400, MUTED)
    s.text(642, 595, "bearer token · per-IP rate limit", 14.5, 400, MUTED)

    s.text(626, 640, "The server never touches the document.", 15, 500, ACCENT)
    s.text(626, 664, "It returns a validated feature tree;", 14.5, 400, MUTED)
    s.text(626, 683, "preview and execution are client-side.", 14.5, 400, MUTED)

    # provider column
    s.rect(1174, 266, 348, 94, SURFACE, LINE, 1, 4)
    s.text(1190, 292, "OpenAI-compatible", 19, 600, INK)
    s.text(1190, 314, "OpenAI · DeepSeek · Qwen", 15, 400, MUTED)
    s.text(1190, 333, "Qiniu Cloud · vLLM · Ollama", 15, 400, MUTED)
    s.text(1190, 350, "any /chat/completions endpoint", 14, 400, MUTED)

    s.rect(1174, 376, 348, 94, SURFACE, LINE, 1, 4)
    s.text(1190, 402, "Anthropic Messages", 19, 600, INK)
    s.text(1190, 424, "provider = anthropic", 14.5, 400, MUTED, family=MONO)
    s.text(1190, 443, "adapter sends only max_tokens", 14.5, 400, MUTED)
    s.text(1190, 461, "current Claude models reject", 14, 400, MUTED)
    s.text(1190, 478, "temperature / top_p", 14, 400, MUTED)

    s.rect(1174, 486, 348, 86, PAPER, LINE, 1, 4)
    s.text(1190, 512, "Returns typed JSON", 19, 600, INK)
    s.text(1190, 534, "feature tree · no code", 15, 400, MUTED)
    s.text(1190, 553, "swappable without a rebuild", 14.5, 500, WARM)

    s.text(1174, 606, "The model is a replaceable", 15, 400, MUTED)
    s.text(1174, 625, "component, not the product.", 15, 400, MUTED)

    # arrows
    s.arrow(576, 314, 604, 314, INK, 1.6)
    s.text(590, 304, "prompt", 13, 500, MUTED, "middle")
    s.arrow(1124, 314, 1174, 314, INK, 1.6)
    s.text(1149, 304, "prompt", 13, 500, MUTED, "middle")
    s.arrow(1174, 450, 1124, 450, ACCENT, 1.6)
    s.text(1149, 440, "JSON", 13, 500, ACCENT, "middle")
    s.arrow(604, 413, 576, 413, ACCENT, 1.6)
    s.text(590, 403, "JSON", 13, 500, ACCENT, "middle")
    s.line(316, 462, 316, 478, INK, 1.4, marker=f"{s.marker_prefix}-ink")
    s.text(326, 474, "confirm", 13, 500, WARM)

    # bottom
    s.line(56, 780, W - 56, 780, LINE_SOFT, 1)
    s.text(56, 806, "DEPLOYMENT", 16, 600, ACCENT, ls=1.2)
    chips = ["local", "Docker", "reverse proxy", "tunnel"]
    x = 190
    for c in chips:
        x += s.chip(x, 788, c, PAPER, MUTED, 14.5, LINE) + 8
    s.text(760, 806, "Client must be Windows + SolidWorks 2025 · server can run anywhere", 15, 400, MUTED)
    footer(s, "Source: Vulcan repository README, v1.3.0.", "B · deployed architecture")
    return s.render("\n".join(s.parts))


# ---------------------------------------------------------------------------
# Panel C — operator workflow (animated)
# ---------------------------------------------------------------------------
def panel_c():
    s = Svg("Vulcan C — operator workflow")
    header(s, "C", "Operator workflow", "From a sentence to a native plate",
           "The operator describes the part, reviews the editable tree, then executes it. Three real surfaces, one confirmation gate.")

    pane = CROPS / "vulcan-taskpane-crop.png"
    plate = CROPS / "vulcan-plate-crop.png"

    # ---- step 1
    s.begin()
    s.rect(56, 196, 468, 566, SURFACE, LINE, 1.2, 6)
    s.text(78, 224, "01 · DESCRIBE", 16, 600, ACCENT, ls=1.2)
    s.text(78, 254, "Write the request", 22, 600, INK)
    s.text(78, 277, "Chinese, English, or French", 14.5, 400, MUTED)
    s.rect(78, 292, 424, 330, PAPER, LINE, 1, 4)
    s.image(pane, 84, 298, 412, 318, border=False)
    s.text(78, 648, "The task pane is the primary surface.", 15, 500, TEXT)
    s.text(78, 670, "The prompt asks for a 200 × 100 × 20 mm plate", 14.5, 400, MUTED)
    s.text(78, 689, "with four Ø10 through holes.", 14.5, 400, MUTED)
    s.rect(56, 196, 468, 566, "none", ACCENT, 2.2, 6, opacity=0, extra='id="c-focus1"')
    s.end_group("c-step1")

    s.group("c-arrow1", f'<line x1="528" y1="470" x2="568" y2="470" stroke="{INK}" stroke-width="1.6" marker-end="url(#{s.marker_prefix}-ink)" pathLength="1"/>')

    # ---- step 2
    s.begin()
    s.rect(576, 196, 448, 566, SURFACE, LINE, 1.2, 6)
    s.text(598, 224, "02 · REVIEW", 16, 600, ACCENT, ls=1.2)
    s.text(598, 254, "Edit the feature tree", 22, 600, INK)
    s.text(598, 277, "Live schema validation in the preview", 14.5, 400, MUTED)
    s.rect(598, 292, 404, 330, CODE_BG, "none", 0, 4)
    s.text(612, 314, "JSON 特征树", 14, 500, CODE_MUTED, family=FONT)
    s.text(988, 314, "valid", 13, 600, CODE_KEY, "end", extra='id="c-valid"' )
    lines = [
        ('{', CODE_FG),
        ('  "model_name": "Mounting plate",', CODE_FG),
        ('  "features": [', CODE_FG),
        ('    { "feature_type": "extrude",', CODE_KEY),
        ('      "name": "Base",', CODE_FG),
        ('      "params": {', CODE_FG),
        ('        "plane": "前视基准面",', CODE_STR),
        ('        "shape": "rectangle",', CODE_STR),
        ('        "length": 200, "width": 100,', CODE_STR),
        ('        "depth": 20 } },', CODE_STR),
        ('    { "feature_type": "cut",', CODE_KEY),
        ('      "name": "Hole 1",', CODE_FG),
        ('      "params": { "diameter": 10,', CODE_STR),
        ('        "through_all": true,', CODE_STR),
        ('        "center_x": 90, "center_y": 40 } }', CODE_STR),
        ('  ]', CODE_FG),
        ('}', CODE_FG),
    ]
    for i, (ln, col) in enumerate(lines):
        s.add(f'<text id="c-code-{i}" x="612" y="{340 + i*16.2}" font-family="{MONO}" font-size="14.2" fill="{col}">{escape(ln)}</text>')
    s.text(598, 648, "One of the four holes is shown; the full response", 14.5, 400, MUTED)
    s.text(598, 667, "repeats the cut at the other corners.", 14.5, 400, MUTED)
    s.text(598, 689, "Nothing is written until Execute.", 14.5, 600, WARM)
    s.rect(576, 196, 448, 566, "none", ACCENT, 2.2, 6, opacity=0, extra='id="c-focus2"')
    s.end_group("c-step2")

    s.group("c-arrow2", f'<line x1="1028" y1="470" x2="1068" y2="470" stroke="{INK}" stroke-width="1.6" marker-end="url(#{s.marker_prefix}-ink)" pathLength="1"/>')

    # ---- step 3
    s.begin()
    s.rect(1076, 196, 468, 566, SURFACE, LINE, 1.2, 6)
    s.text(1098, 224, "03 · EXECUTE", 16, 600, ACCENT, ls=1.2)
    s.text(1098, 254, "Get native features", 22, 600, INK)
    s.text(1098, 277, "C# COM modeler, no code generation", 14.5, 400, MUTED)
    s.rect(1098, 292, 424, 330, PAPER, LINE, 1, 4)
    s.add('<g id="c-render-img" style="transform-box: fill-box; transform-origin: center;">')
    s.image(plate, 1104, 298, 412, 318, border=False)
    s.add('</g>')
    s.text(1098, 648, "Native SolidWorks feature tree", 15, 500, TEXT)
    s.text(1098, 670, "Base-Extrude · Cut-Extrude ×4 · Fillet", 14.5, 400, MUTED, family=MONO)
    s.text(1098, 689, "Editable, not a mesh or a macro.", 14.5, 600, ACCENT)
    s.rect(1076, 196, 468, 566, "none", ACCENT, 2.2, 6, opacity=0, extra='id="c-focus3"')
    s.end_group("c-step3")

    # ---- bottom strip
    s.rect(56, 786, 1488, 46, ACCENT_SOFT, "none", 0, 4)
    s.text(74, 815, "DESCRIBE", 15, 600, ACCENT, ls=1.4)
    s.text(168, 815, "→", 15, 400, ACCENT)
    s.text(196, 815, "REVIEW", 15, 600, ACCENT, ls=1.4)
    s.text(276, 815, "→", 15, 400, ACCENT)
    s.text(304, 815, "EXECUTE", 15, 600, ACCENT, ls=1.4)
    s.text(392, 815, "The human confirmation gate sits between review and execution.", 15, 500, ACCENT_STRONG)
    s.text(W - 74, 815, "Captured from the installed add-in", 14, 400, MUTED, "end")
    footer(s, "Source: Vulcan repository README, v1.3.0; UI captures from the installed add-in.", "C · operator workflow")
    return s.render("\n".join(s.parts))


def panel_d():
    s = Svg("Vulcan D — contract and lifecycle")
    header(s, "D", "Contract & lifecycle", "The contract is the safety boundary",
           "A typed JSON feature tree crosses every boundary. Two gates stand between the model and the document.")

    # code panel
    s.rect(56, 196, 900, 470, CODE_BG, "none", 0, 6)
    s.text(78, 224, "response.json · abridged", 15, 500, CODE_MUTED, family=MONO)
    s.text(934, 224, "typed", 14, 600, CODE_KEY, "end")
    code = [
        ('{', CODE_FG, 0),
        ('  "model_name": "Mounting plate",', CODE_FG, 0),
        ('  "features": [', CODE_FG, 0),
        ('    { "feature_type": "extrude",', CODE_KEY, 0),
        ('      "name": "Base",', CODE_FG, 0),
        ('      "params": {', CODE_FG, 0),
        ('        "plane": "前视基准面",', CODE_STR, 1),
        ('        "shape": "rectangle",', CODE_STR, 0),
        ('        "length": 200, "width": 100,', CODE_STR, 0),
        ('        "depth": 20', CODE_STR, 0),
        ('      } },', CODE_FG, 0),
        ('    { "feature_type": "cut",', CODE_KEY, 0),
        ('      "name": "Hole 1",', CODE_FG, 0),
        ('      "params": { "shape": "circle",', CODE_STR, 0),
        ('        "diameter": 10, "through_all": true,', CODE_STR, 0),
        ('        "center_x": 90, "center_y": 40 } }', CODE_STR, 0),
        ('  ]', CODE_FG, 0),
        ('}', CODE_FG, 0),
    ]
    for i, (ln, col, warn) in enumerate(code):
        y = 258 + i * 19.2
        s.text(78, y, ln, 15.2, 400, col, family=MONO)
    s.text(78, 626, "Envelope · ordered features · params in millimetres · units normalized at the COM boundary", 14.5, 400, CODE_MUTED)
    s.text(78, 648, "Model output is data, never code. The server validates it; the client previews it.", 14.5, 400, CODE_FG)

    # lifecycle
    s.rect(984, 196, 560, 470, SURFACE, LINE, 1.2, 6)
    s.text(1006, 224, "REQUEST LIFECYCLE", 16, 600, ACCENT, ls=1.2)
    s.text(1006, 254, "Seven stages, three lanes", 21, 600, INK)
    stages = [
        ("1", "Natural language", "task pane request", ACCENT),
        ("2", "Prompt assembly", "domain prompt + user text", ACCENT),
        ("3", "Model call", "returns typed JSON", WARM),
        ("4", "Recovery", "strip fences, extract object", MUTED),
        ("5", "Validation", "envelope + params", ACCENT),
        ("6", "Preview + confirm", "human gate", WARM),
        ("7", "COM execution", "native feature APIs", ACCENT),
    ]
    for i, (n, name, detail, col) in enumerate(stages):
        y = 288 + i * 44
        s.add(f'<circle cx="1020" cy="{y-5}" r="12" fill="{col if i in (2,5) else PAPER}" stroke="{col}" stroke-width="1.2"/>')
        s.text(1020, y, n, 13, 600, PAPER if i in (2,5) else col, "middle")
        s.text(1042, y - 4, name, 16.5, 600, INK)
        s.text(1042, y + 13, detail, 13.5, 400, MUTED)
        if i in (4, 5):
            s.rect(1320, y - 12, 84, 22, WARM_SOFT if i == 5 else ACCENT_SOFT, "none", 0, 3)
            s.text(1362, y + 3, "GATE" if i == 5 else "CHECK", 13.5, 600, WARM if i == 5 else ACCENT, "middle", ls=0.6)
    # latency bar
    s.text(1006, 612, "LATENCY", 14, 600, MUTED, ls=1.2)
    bar_y = 624
    widths = [40, 52, 286, 34, 34, 30, 34]
    labels = ["1", "2", "3", "4", "5", "6", "7"]
    x = 1006
    for i, (wd, lab) in enumerate(zip(widths, labels)):
        col = WARM if i == 2 else (ACCENT if i in (0, 1, 6) else LINE)
        s.rect(x, bar_y, wd - 2, 16, col if i == 2 else (ACCENT_SOFT if i in (0, 1, 6) else PAPER), LINE, 1, 2)
        s.text(x + (wd - 2) / 2, bar_y + 12, lab, 13.5, 600, WARM if i == 2 else (ACCENT if i in (0, 1, 6) else MUTED), "middle")
        x += wd
    s.text(1006, 654, "The model call dominates latency; everything else is local (ms).", 13.5, 400, MUTED)

    # bottom band
    s.rect(56, 694, 1488, 132, ACCENT_SOFT, "none", 0, 6)
    s.text(78, 722, "WHAT KEEPS IT SAFE", 16, 600, ACCENT, ls=1.2)
    safety = [
        ("Schema validation", "envelope + feature params checked on both sides"),
        ("Human confirmation", "nothing reaches the document until confirmed"),
        ("No exec()", "the model returns data, not code"),
        ("Native output", "editable SolidWorks features, not a mesh"),
    ]
    for i, (head, body) in enumerate(safety):
        x = 78 + i * 366
        s.text(x, 754, head, 17, 600, ACCENT_STRONG)
        s.lines(x, 776, wrap(body, 14, 330), 14, 400, ACCENT_STRONG, 1.35)
    footer(s, "Source: Vulcan repository README, v1.3.0.", "D · contract and lifecycle")
    return s.render("\n".join(s.parts))


def main():
    SRC.mkdir(parents=True, exist_ok=True)
    for name, fn in [("vulcan-a", panel_a), ("vulcan-b", panel_b),
                     ("vulcan-c", panel_c), ("vulcan-d", panel_d)]:
        out = SRC / f"{name}.svg"
        out.write_text(fn(), encoding="utf-8")
        print(out, out.stat().st_size)


if __name__ == "__main__":
    main()
