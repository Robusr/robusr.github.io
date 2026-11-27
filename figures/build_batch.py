#!/usr/bin/env python3
"""Shared batch plates for Hsiwu, DustArrow, OnesArm, and Sencillo.

Reuses the Vulcan design system (paper / ink / teal + warm render tone) and
emits editable SVG sources at 1600×900. Video panels keep a reserved slot that
the ffmpeg compositor fills with the repository animation.
"""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_vulcan import (
    Svg, header, footer, section_label, W, H,
    PAPER, SURFACE, INK, TEXT, MUTED, LINE, LINE_SOFT,
    ACCENT, ACCENT_STRONG, ACCENT_SOFT, WARM, WARM_SOFT, RED,
    CODE_BG, CODE_FG, CODE_KEY, CODE_STR, CODE_MUTED,
    FONT, MONO, text_w, wrap, fit,
)

B = Path(__file__).resolve().parent / "crops" / "batch"
SRC = Path(__file__).resolve().parent / "src"


def panel(name: str, letter: str, kicker: str, title: str, subtitle: str, right: str) -> Svg:
    s = Svg(name)
    header(s, letter, kicker, title, subtitle, right)
    return s


def card(s: Svg, x, y, w, h, fill=SURFACE, rx=5):
    s.rect(x, y, w, h, fill, LINE, 1.2, rx)


def label(s: Svg, x, y, text, color=ACCENT):
    s.text(x, y, text.upper(), 16, 600, color, ls=1.2)


def body(s: Svg, x, y, lines, size=15.5, color=TEXT, lead=1.45, weight=400):
    s.lines(x, y, lines, size, weight, color, lead)


def check(s: Svg, x, y, text, color=ACCENT, size=15.5, mark="✓"):
    s.text(x, y, mark, size, 600, color)
    s.text(x + 22, y, text, size, 400, TEXT)


def cross(s: Svg, x, y, text, size=15.5):
    s.text(x, y, "×", size, 600, RED)
    s.text(x + 22, y, text, size, 400, TEXT)


def kv(s: Svg, x, y, key, value, kw=120, size=15, color=TEXT):
    s.text(x, y, key.upper(), 13, 500, MUTED, ls=0.8)
    s.text(x + kw, y, value, size, 400, color)


def wave(s: Svg, x, y, w, h, high_ratio=0.67, cycles=3, color=ACCENT, sw=2.2, phase=0.0):
    period = w / cycles
    high = period * high_ratio
    offset = phase * period
    start_high = offset % period < high
    points = [f"M{x:.1f},{y:.1f}" if start_high else f"M{x:.1f},{y+h:.1f}"]
    transitions = []
    n0 = int(offset // period) - 1
    for n in range(n0, n0 + cycles + 3):
        for tr, is_rise in ((n * period, True), (n * period + high, False)):
            t = tr - offset
            if 0 < t < w:
                transitions.append((t, is_rise))
    transitions.sort()
    cur_y = y if start_high else y + h
    for t, rise in transitions:
        px = x + t
        points.append(f"L{px:.1f},{cur_y:.1f}")
        cur_y = y if rise else y + h
        points.append(f"L{px:.1f},{cur_y:.1f}")
    points.append(f"L{x+w:.1f},{cur_y:.1f}")
    s.path(" ".join(points), color, sw, "none")
    s.line(x, y + h + 8, x + w, y + h + 8, LINE_SOFT, 1)


def video_slot(s: Svg, x, y, w, h):
    s.rect(x, y, w, h, "#0E1118", "none", 0, 3)
    s.rect(x, y, w, h, "none", LINE, 1, 3)


# ---------------------------------------------------------------------------
# Hsiwu
# ---------------------------------------------------------------------------
def hsiwu_a():
    s = panel("Hsiwu A — system overview", "A", "System overview",
              "Three segments per wing, three analog channels",
              "A 3.7 V cell, one 5 V rail, three free-running timers, and six mirrored motors — no MCU.",
              "HSIWU · rev 1.0")

    # power card
    s.begin()
    card(s, 56, 196, 420, 112)
    label(s, 74, 222, "Power")
    boxes = [(74, "3.7 V LiPo", "1S · XH-2A"), (198, "MT3608", "boost · 5.0 V"), (326, "5.0 V rail", "4.96 V")]
    for bx, t1, t2 in boxes:
        s.rect(bx, 238, 118, 44, PAPER, LINE, 1, 3)
        s.text(bx + 8, 256, t1, 15, 600, INK)
        s.text(bx + 8, 273, t2, 12.5, 400, MUTED, family=MONO)
    s.arrow(192, 260, 198, 260, INK, 1.3)
    s.arrow(316, 260, 326, 260, INK, 1.3)
    s.text(74, 298, "Single rail · no LDO · no reverse-polarity protection", 13.5, 400, MUTED)
    s.end_group("h-a-power")

    # channels
    s.begin()
    card(s, 56, 328, 420, 300)
    label(s, 74, 354, "Three free-running channels")
    rows = [
        ("A", "U6", "U1", "M1 / M2", 382),
        ("B", "U7", "U2", "M3 / M4", 462),
        ("C", "U8", "U3", "M5 / M6", 542),
    ]
    for name, u6, u1, motors, y in rows:
        s.text(74, y, f"CH {name}", 17, 600, INK)
        s.text(74, y + 22, f"NE555 {u6} → 74HC04 → L293D {u1}", 13.5, 400, MUTED, family=MONO)
        s.text(74, y + 42, f"4.8 Hz · SA / /SA → {motors}", 13.5, 400, TEXT)
        wave(s, 310, y + 8, 148, 24, 0.67, 2, ACCENT, 2)
    s.text(74, 602, "No hard sync · trim R4/R10/R11 · 1.2–7.2 Hz", 13.5, 500, WARM)
    s.end_group("h-a-channels")

    # render
    s.begin()
    card(s, 500, 196, 1044, 470)
    label(s, 520, 222, "Bench prototype")
    s.text(520, 250, "Six actuators, three segments per wing", 22, 600, INK)
    s.image(B / "hsiwu-render.webp", 520, 268, 760, 372)
    # callouts on the right
    cx = 1300
    s.text(cx, 310, "3", 38, 600, ACCENT)
    s.text(cx + 42, 300, "segments per wing", 16, 500, TEXT)
    s.text(cx + 42, 320, "L · M · T, one motor each", 13.5, 400, MUTED)
    s.text(cx, 390, "6", 38, 600, ACCENT)
    s.text(cx + 42, 380, "mirrored motors", 16, 500, TEXT)
    s.text(cx + 42, 400, "hollow-cup geared pairs", 13.5, 400, MUTED)
    s.text(cx, 470, "0.4", 38, 600, WARM)
    s.text(cx + 78, 460, "mm lead screw", 16, 500, TEXT)
    s.text(cx + 78, 480, "nut drives the segment linkage", 13.5, 400, MUTED)
    s.text(cx, 548, "No membrane, no flight test", 14.5, 500, WARM)
    s.text(520, 650, "Skeletal linkage; the wing membrane and aerodynamic performance are not part of this build.", 13.5, 400, MUTED)
    s.end_group("h-a-render")

    # facts
    s.begin()
    facts = [("3", "independent channels", "each drives a mirrored pair"),
             ("6", "motors", "three per wing"),
             ("0", "MCU / firmware", "NE555 + 74HC04 + L293D")]
    for i, (n, t1, t2) in enumerate(facts):
        x = 500 + i * 352
        s.rect(x, 686, 332, 102, SURFACE, LINE, 1, 4)
        s.text(x + 16, 730, n, 34, 600, ACCENT if i < 2 else WARM)
        s.text(x + 58, 714, t1, 16, 600, INK)
        s.text(x + 58, 736, t2, 13.5, 400, MUTED)
    s.end_group("h-a-facts")

    # focus scan
    for i, (x, y, w, h) in enumerate([(56, 196, 420, 112), (56, 328, 420, 300),
                                      (500, 196, 1044, 470), (500, 686, 1044, 102)], 1):
        s.rect(x, y, w, h, "none", ACCENT, 3, 5, opacity=0, extra=f'id="h-a-focus{i}"')

    footer(s, "Source: Hsiwu repository README, rev 1.0.", "A · system overview")
    return s.render("\n".join(s.parts))


def hsiwu_b():
    s = panel("Hsiwu B — analog control", "B", "Analog control",
              "One 5 V rail, three free-running channels",
              "The entire control law is three NE555 astables, one 74HC04, and three L293D bridges.",
              "HSIWU · rev 1.0")

    # power path
    card(s, 56, 196, 430, 620)
    label(s, 74, 222, "Power path")
    s.text(74, 248, "3.7 V → 5.0 V", 21, 600, INK)
    nodes = [
        ("3.7 V 1S LiPo", "XH-2A U9 · switch SW2", 278),
        ("MT3608 boost", "L1 10 µH · D1 SS34 · C1/C2 22 µF", 360),
        ("5.0 V rail", "Vout ≈ 4.96 V · LED1 + R6", 460),
    ]
    for t1, t2, y in nodes:
        s.rect(74, y, 394, 58, PAPER, LINE, 1, 4)
        s.text(90, y + 24, t1, 17, 600, INK)
        s.text(90, y + 44, t2, 13.5, 400, MUTED, family=MONO)
    s.arrow(271, 336, 271, 360, INK, 1.6)
    s.arrow(271, 418, 271, 460, INK, 1.6)
    s.text(74, 548, "R1 16 kΩ / R2 2.2 kΩ feedback divider", 14, 400, MUTED)
    s.text(74, 576, "No LDO · no reverse-polarity protection", 14, 500, WARM)
    s.text(74, 604, "D1 is the boost rectifier, not a reverse diode.", 13.5, 400, MUTED)
    s.text(74, 650, "The same 5 V rail supplies the logic ICs and the motor drivers.", 13.5, 400, TEXT)
    s.text(74, 680, "3.7 V battery → boost → 5 V → three timers → six motors.", 13.5, 500, ACCENT)
    s.text(74, 746, "Schematic: Hsiwu README, Figure 2.", 13.5, 400, MUTED)

    # timing
    card(s, 516, 196, 500, 318)
    label(s, 534, 222, "Timing")
    s.text(534, 250, "Three astable channels", 21, 600, INK)
    s.text(534, 282, "f = 1.44 / ((R_A + 2 R_B) · C)", 18, 500, INK, family=MONO)
    s.text(534, 308, "duty = (R_A + R_B) / (R_A + 2 R_B)", 18, 500, INK, family=MONO)
    s.text(534, 342, "R_A ≈ 10 kΩ (100 kΩ trim set near 10 kΩ)", 14, 400, MUTED)
    s.text(534, 366, "R_B = 10 kΩ · C = 10 µF", 14, 400, MUTED)
    s.text(534, 398, "4.8 Hz · 208 ms · 67% duty", 20, 600, ACCENT)
    s.text(534, 424, "t_H ≈ 139 ms · t_L ≈ 69 ms", 14.5, 400, TEXT)
    s.text(534, 450, "trimmer range ≈ 1.2–7.2 Hz", 14, 400, MUTED)
    s.text(534, 482, "Three channels are free-running; there is no hard sync.", 13.5, 500, WARM)

    # drive
    card(s, 1046, 196, 498, 330)
    label(s, 1064, 222, "Drive")
    s.text(1064, 250, "Complementary pairs", 21, 600, INK)
    rows = [("A", "U6 → U5 → U1", "M1 / M2"), ("B", "U7 → U5 → U2", "M3 / M4"), ("C", "U8 → U5 → U3", "M5 / M6")]
    for i, (ch, path, motors) in enumerate(rows):
        y = 292 + i * 52
        s.text(1064, y, f"CH {ch}", 16, 600, ACCENT)
        s.text(1112, y, path, 14.5, 400, TEXT, family=MONO)
        s.text(1320, y, motors, 14.5, 500, INK, family=MONO)
    s.text(1064, 470, "Each L293D uses both H-bridges to drive one mirrored pair.", 13.5, 400, MUTED)
    s.text(1064, 492, "74HC04 gives /SA, /SB, /SC; the motor reverses every half-cycle.", 13.5, 400, MUTED)
    s.text(1064, 518, "Unused 74HC04 gates float in revision 1.0.", 13.5, 500, WARM)

    # timing strip
    card(s, 516, 536, 1028, 280)
    label(s, 534, 562, "Timing and phase")
    s.text(534, 586, "Design point: 4.8 Hz, 208 ms period, 67% duty; phase offsets are illustrative.", 14, 400, MUTED)
    for i, (name, y) in enumerate([("SA", 620), ("SB", 690), ("SC", 760)]):
        s.text(534, y + 8, name, 14, 600, ACCENT, family=MONO)
        wave(s, 580, y - 14, 780, 30, 0.67, 3, ACCENT, 2, phase=(0.0, 0.22, 0.55)[i])
        s.text(1370, y + 8, "high 139 ms", 12.5, 400, MUTED)
        s.text(1370, y + 24, "low 69 ms", 12.5, 400, MUTED)
    s.text(580, 800, "0", 12, 400, MUTED)
    s.text(840, 800, "208", 12, 400, MUTED)
    s.text(1100, 800, "416", 12, 400, MUTED)
    s.text(1360, 800, "624 ms", 12, 400, MUTED)
    footer(s, "Source: Hsiwu repository README, Figures 2–3, rev 1.0.", "B · analog control")
    return s.render("\n".join(s.parts))


def hsiwu_c():
    s = panel("Hsiwu C — wing drive", "C", "Wing drive",
              "Lead screw, not a crank-rocker",
              "The reference four-bar is a benchmark; the as-built segment drive is a lead screw, a traveling nut, and the same H-bridge reversal.",
              "HSIWU · rev 1.0")

    # video slot
    card(s, 56, 196, 952, 586)
    label(s, 74, 222, "As-built mechanism · CAD animation")
    s.text(74, 250, "One motor per segment; six in total", 21, 600, INK)
    video_slot(s, 80, 270, 900, 470)
    s.text(74, 760, "Motor → lead screw P = 0.4 mm → nut → segment linkage; H-bridge reverses every half-cycle.", 13.5, 400, MUTED)

    # reference
    card(s, 1032, 196, 512, 166)
    label(s, 1050, 222, "Reference")
    s.text(1050, 250, "Crank-rocker (Qi & Zhang)", 19, 600, INK)
    s.text(1050, 282, "The reference paper's four-bar", 13.5, 400, MUTED)
    s.text(1050, 304, "is a kinematic benchmark,", 13.5, 400, MUTED)
    s.text(1050, 326, "not the as-built linkage.", 13.5, 500, WARM)
    # schematic on the right
    cx, cy = 1320, 300
    s.add(f'<circle cx="{cx}" cy="{cy}" r="12" fill="none" stroke="{WARM}" stroke-width="2"/>')
    s.add(f'<line x1="{cx+12}" y1="{cy}" x2="{cx+86}" y2="{cy-30}" stroke="{WARM}" stroke-width="2"/>')
    s.add(f'<line x1="{cx+86}" y1="{cy-30}" x2="{cx+112}" y2="{cy+34}" stroke="{INK}" stroke-width="1.8"/>')
    s.add(f'<circle cx="{cx+112}" cy="{cy+34}" r="3" fill="{INK}"/>')
    s.add(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{INK}"/>')
    s.text(cx - 12, cy + 34, "crank", 12, 400, MUTED)
    s.text(cx + 54, cy - 44, "coupler", 12, 400, MUTED)
    s.text(cx + 120, cy + 16, "rocker", 12, 400, MUTED)

    # as-built
    card(s, 1032, 382, 512, 196)
    label(s, 1050, 408, "As-built")
    s.text(1050, 436, "Motor → screw → nut", 19, 600, INK)
    by = 476
    for label_text, bx in [("motor", 1050), ("lead screw", 1140), ("nut", 1260), ("linkage", 1350)]:
        s.rect(bx, by - 18, 78, 36, PAPER, LINE, 1, 3)
        s.text(bx + 39, by + 5, label_text, 12.5, 500, TEXT, "middle")
    s.arrow(1128, by, 1140, by, INK, 1.3)
    s.arrow(1218, by, 1260, by, INK, 1.3)
    s.arrow(1338, by, 1350, by, INK, 1.3)
    s.text(1050, 526, "P = 0.4 mm · H-bridge reversal each half-cycle", 14, 500, WARM)
    s.text(1050, 550, "3 segments per wing: L · M · T", 14, 400, MUTED)

    # segments
    card(s, 1032, 598, 512, 184)
    label(s, 1050, 624, "Segment map")
    s.text(1050, 652, "One motor per segment", 19, 600, INK)
    segs = [("L", "M1 / M2", "CH A"), ("M", "M3 / M4", "CH B"), ("T", "M5 / M6", "CH C")]
    for i, (seg, motors, ch) in enumerate(segs):
        y = 684 + i * 30
        s.text(1050, y, seg, 16, 600, ACCENT)
        s.text(1078, y, f"{motors}  ·  {ch}", 14, 400, TEXT, family=MONO)
    s.text(1050, 776, "70° stroke is a reference target, not measured.", 13.5, 500, WARM)

    footer(s, "Source: Hsiwu repository README, Figure 5; CAD animation from the repository.", "C · wing drive")
    return s.render("\n".join(s.parts))


def hsiwu_d():
    s = panel("Hsiwu D — bench evidence", "D", "Bench evidence",
              "Verified on the bench; not yet in the air",
              "The board and mechanism are built and tested. The membrane, flapping angle, mass, thrust, and flight are not.",
              "HSIWU · rev 1.0")

    # PCB
    card(s, 56, 196, 430, 586)
    label(s, 74, 222, "PCB")
    s.text(74, 250, "19 × 80 mm, 2 layers", 21, 600, INK)
    s.image(B / "hsiwu-pcb.webp", 92, 272, 356, 450)
    s.text(74, 746, "Custom contour · five 2 mm mounting holes", 13.5, 400, MUTED)

    # bench photo
    card(s, 506, 196, 470, 348)
    label(s, 524, 222, "Bench validation")
    s.image(B / "hsiwu-bench.webp", 524, 238, 434, 270)
    s.text(524, 528, "Tektronix TDS1001B-SC · 3.8 V / 0.05 A", 13.5, 400, MUTED)

    # verified
    card(s, 506, 560, 470, 222)
    label(s, 524, 586, "Verified")
    checks = ["5 V rail (≈ 4.96 V) and power LED", "≈ 4.8 Hz square wave on each NE555", "Complementary 74HC04 outputs", "Six motors respond on all channels", "All segments reach full stroke unloaded"]
    for i, item in enumerate(checks):
        check(s, 524, 618 + i * 28, item, ACCENT, 14)

    # not verified
    card(s, 996, 196, 548, 586)
    label(s, 1014, 222, "Not verified")
    s.text(1014, 250, "No membrane. No flight test.", 21, 600, INK)
    nots = ["Wing-membrane integration", "Flapping angle", "Wingspan", "Total mass", "Static thrust / lift", "Flight"]
    for i, item in enumerate(nots):
        cross(s, 1014, 290 + i * 30, item, 14.5)
    s.line(1014, 500, 1526, 500, LINE_SOFT, 1)
    s.text(1014, 526, "Reference values — not this prototype", 14.5, 600, WARM)
    refs = [("205 mm", "wingspan"), ("17.81 g", "mass"), ("70°", "stroke"), ("0.16 N", "lift")]
    for i, (v, k) in enumerate(refs):
        x = 1014 + (i % 2) * 250
        y = 558 + (i // 2) * 56
        s.text(x, y, v, 22, 600, WARM)
        s.text(x + 90, y, k, 13.5, 400, MUTED)
    s.text(1014, 690, "These are Qi & Zhang (2020) reference values, not measurements of this build.", 13.5, 400, MUTED)
    s.text(1014, 714, "MIT · Gerber, BOM, and STEP included.", 13.5, 500, ACCENT)
    s.text(1014, 744, "Revision 1.0 · bench-tested mechanism.", 13.5, 400, MUTED)

    footer(s, "Source: Hsiwu repository README, Figures 4 and 9; bench photos from the repository.", "D · bench evidence")
    return s.render("\n".join(s.parts))


def build_hsiwu():
    for name, fn in [("hsiwu-a", hsiwu_a), ("hsiwu-b", hsiwu_b), ("hsiwu-c", hsiwu_c), ("hsiwu-d", hsiwu_d)]:
        out = SRC / f"{name}.svg"
        out.write_text(fn(), encoding="utf-8")
        print(out, out.stat().st_size)




# ---------------------------------------------------------------------------
# DustArrow X
# ---------------------------------------------------------------------------
def dust_a():
    s = panel("DustArrow A — modular architecture", "A", "Modular architecture",
              "Nine modules, four sections, ten bays",
              "A 40 mm sounding rocket built as replaceable modules on a gold-finger and FPC backbone.",
              "DUSTARROW X · 2023")

    # sections
    card(s, 56, 196, 480, 360)
    label(s, 74, 222, "Four functional sections")
    sections = [
        ("MANEUVER", "parachute · canard", ACCENT),
        ("DETECTION", "dust · gas · CO/smoke", WARM),
        ("CONTROL", "command · exploration · data", ACCENT),
        ("POWER", "power · propulsion", WARM),
    ]
    for i, (name, modules, col) in enumerate(sections):
        y = 258 + i * 68
        s.rect(74, y, 6, 50, col, "none", 0, 1)
        s.text(94, y + 20, name, 17, 600, INK, ls=0.8)
        s.text(94, y + 42, modules, 14, 400, MUTED)
    s.text(74, 540, "9 whiteboard modules + propulsion/fin = 10 CAD bays", 14, 500, ACCENT)

    # interface
    card(s, 56, 576, 480, 210)
    label(s, 74, 602, "Replaceable interface")
    s.text(74, 630, "Gold-finger board-to-board", 17, 600, INK)
    s.image(B / "dust-modules.webp", 74, 646, 190, 120)
    s.text(284, 652, "FPC inside each bay;", 14, 400, TEXT)
    s.text(284, 672, "printed parts replaceable", 14, 400, TEXT)
    s.text(284, 692, "individually.", 14, 400, TEXT)
    s.text(284, 722, "40 mm diameter", 14, 500, WARM)
    s.text(284, 742, "9 modules · 10 bays", 14, 500, ACCENT)

    # render
    card(s, 560, 196, 984, 614)
    label(s, 580, 222, "Full airframe")
    s.text(580, 250, "40 mm modular sounding rocket", 22, 600, INK)
    s.image(B / "dust-banner.webp", 580, 268, 944, 451)
    facts = [("10", "CAD bays"), ("9", "replaceable modules"),
             ("4", "functional sections"), ("40", "mm diameter")]
    for i, (n, t1) in enumerate(facts):
        x = 580 + i * 236
        s.text(x, 752, n, 24, 600, ACCENT if i < 3 else WARM)
        s.text(x + 38, 752, t1, 12.5, 500, INK)
    s.text(580, 790, "Archived design; module names follow the January 2024 TV whiteboard; no flight log is included.", 13.5, 400, MUTED)

    for i, (x, y, w, h) in enumerate([(56, 196, 480, 360), (56, 576, 480, 210), (560, 196, 984, 614)], 1):
        s.rect(x, y, w, h, "none", ACCENT, 3, 5, opacity=0, extra=f'id="d-a-focus{i}"')

    footer(s, "Source: DustArrow repository README; module nomenclature from the TV feature; render from the repository.", "A · modular architecture")
    return s.render("\n".join(s.parts))


def dust_b():
    s = panel("DustArrow B — deployment", "B", "Deployment",
              "Nose separation, canard deployment, recovery",
              "Two mechanisms and one parachute hatch; a CAD animation, not flight footage.",
              "DUSTARROW X · 2023")

    card(s, 56, 196, 960, 586)
    label(s, 74, 222, "Canard + parachute · CAD animation")
    s.text(74, 250, "Nose separation → canard deploy → recovery", 21, 600, INK)
    video_slot(s, 80, 270, 912, 470)
    s.text(74, 760, "Mechanism study from the repository; the flight itself is shown in panel C.", 13.5, 400, MUTED)

    # sequence
    card(s, 1032, 196, 512, 250)
    label(s, 1050, 222, "Sequence")
    s.text(1050, 250, "Three mechanical events", 19, 600, INK)
    steps = [("1", "Nose separation", "parachute bay opens"),
             ("2", "Canard deployment", "two-channel air rudder"),
             ("3", "Recovery", "single servo · large-angle hatch")]
    for i, (n, t1, t2) in enumerate(steps):
        y = 292 + i * 50
        s.add(f'<circle cx="1062" cy="{y-5}" r="13" fill="{ACCENT}" stroke="none"/>')
        s.text(1062, y, n, 13, 600, PAPER, "middle")
        s.text(1084, y, t1, 16, 600, INK)
        s.text(1084, y + 18, t2, 13, 400, MUTED)

    # evidence
    card(s, 1032, 466, 512, 316)
    label(s, 1050, 492, "Evidence")
    s.text(1050, 520, "CAD study, not flight footage", 19, 600, INK)
    s.text(1050, 550, "The January 2024 flight test:", 14, 500, TEXT)
    items = ["Gobi, late autumn / early winter 2023", "Sensor section recovered", "Parachute bay and propulsion module lost", "≈ 80% recovery estimate"]
    for i, item in enumerate(items):
        s.text(1050, 578 + i * 24, "·", 14, 600, WARM)
        s.text(1066, 578 + i * 24, item, 13.5, 400, MUTED)
    s.text(1050, 700, "The animation is a mechanism study; it is not a flight record.", 13.5, 500, WARM)
    s.text(1050, 730, "No telemetry log is present in the archive.", 13.5, 400, MUTED)

    footer(s, "Source: DustArrow repository README; mechanical animation from the repository.", "B · deployment")
    return s.render("\n".join(s.parts))


def dust_c():
    s = panel("DustArrow C — launch", "C", "Flight evidence",
              "Launch from the Gobi, 2023",
              "The sensor section was recovered; the parachute bay and propulsion module were lost. The archive has no flight log.",
              "DUSTARROW X · 2023")

    card(s, 56, 196, 1080, 630)
    label(s, 74, 222, "TV excerpt · authorized")
    s.text(74, 250, "Lift-off, Gobi test flight", 22, 600, INK)
    video_slot(s, 80, 270, 1000, 506)
    s.text(74, 802, "Shanghai TV · Young Edison S8 · January 2024 · © Shanghai Media Group", 13.5, 500, WARM)

    card(s, 1164, 196, 380, 300)
    label(s, 1182, 222, "Flight facts")
    facts = [("40 mm", "airframe diameter"), ("9", "replaceable modules"), ("32", "tests passed"), ("16", "documented errata"), ("2023", "Gobi flight season"), ("80%", "recovery estimate")]
    for i, (v, k) in enumerate(facts):
        x = 1182 + (i % 2) * 186
        y = 258 + (i // 2) * 58
        s.text(x, y, v, 22, 600, ACCENT if i < 4 else WARM)
        s.text(x, y + 18, k, 12.5, 400, MUTED)
    s.text(1182, 444, "No telemetry log in the archive.", 13.5, 400, MUTED)

    card(s, 1164, 516, 380, 310)
    label(s, 1182, 542, "Context")
    s.text(1182, 570, "Wired ignition, not remote", 16.5, 600, INK)
    s.text(1182, 594, "The episode documents a test flight near", 13.5, 400, MUTED)
    s.text(1182, 613, "Guyuan. Remote ignition was replaced by", 13.5, 400, MUTED)
    s.text(1182, 632, "wired ignition; the rocket left the rail.", 13.5, 400, MUTED)
    s.text(1182, 662, "The sensor section was recovered;", 13.5, 400, MUTED)
    s.text(1182, 681, "the parachute bay and propulsion", 13.5, 400, MUTED)
    s.text(1182, 700, "module were lost.", 13.5, 400, MUTED)
    s.text(1182, 734, "This excerpt is used with permission and", 13.5, 500, WARM)
    s.text(1182, 753, "credited to Shanghai TV, Young Edison S8.", 13.5, 500, WARM)
    s.text(1182, 786, "No quantitative flight data are claimed.", 13.5, 400, MUTED)

    footer(s, "Source: DustArrow repository README and media coverage; launch excerpt © Shanghai Media Group.", "C · launch")
    return s.render("\n".join(s.parts))


def dust_d():
    s = panel("DustArrow D — telemetry", "D", "Telemetry",
              "A text stream today, a CRC-16 frame proposed",
              "RP2040 sensing, LoRa downlink, and a PyQt5 ground station. The frame is tested; the archive has no flight log.",
              "DUSTARROW X · 2023")

    # avionics
    card(s, 56, 196, 500, 560)
    label(s, 74, 222, "Avionics")
    s.text(74, 250, "RP2040 sensing stack", 20, 600, INK)
    sensors = ["MPU6050 · 6-axis IMU", "BMP280 · barometer", "ATGM336H · GNSS", "GP2Y1014AU0F · dust", "MQ-2 / MQ-135 · gas"]
    for i, item in enumerate(sensors):
        s.text(74, 286 + i * 28, "·", 14, 600, ACCENT)
        s.text(90, 286 + i * 28, item, 13.5, 400, TEXT)
    s.rect(74, 440, 180, 40, PAPER, LINE, 1, 3)
    s.text(164, 465, "RP2040", 15, 600, INK, "middle")
    s.rect(274, 440, 180, 40, PAPER, LINE, 1, 3)
    s.text(364, 465, "A39C LoRa", 15, 600, INK, "middle")
    s.arrow(254, 460, 274, 460, INK, 1.4)
    s.text(74, 512, "9600 baud · 8-N-1 · text stream", 13.5, 500, WARM, family=MONO)
    s.text(74, 540, "PyQt5 ground station", 17, 600, INK)
    s.text(74, 564, "serial acquisition · six placeholder plots", 13.5, 400, MUTED)
    s.text(74, 584, "static attitude cube · command path not wired", 13.5, 400, MUTED)
    s.text(74, 620, "9 module BOMs · 10 Gerber packages", 13.5, 400, MUTED)
    s.text(74, 650, "No firmware source or flight log in the archive.", 13.5, 500, WARM)
    s.text(74, 700, "The archived stream is free-form text:", 13.5, 400, MUTED)
    s.text(74, 722, "X…Y…GX…GY…GZ…", 14, 500, INK, family=MONO)
    s.text(74, 746, "no header · no length · no checksum", 13.5, 400, MUTED)

    # proposed frame
    card(s, 584, 196, 488, 300)
    label(s, 602, 222, "Proposed frame")
    s.text(602, 250, "CRC-16 protected", 20, 600, INK)
    fields = [("$", "0x24", 1), ("LEN", "1 B", 1), ("PAYLOAD", "0–64 B", 2), ("CRC-16", "2 B", 1), ("*", "0x2A", 1)]
    x = 602
    widths = [58, 64, 150, 82, 46]
    for (name, sub, _), w in zip(fields, widths):
        s.rect(x, 276, w, 54, PAPER, LINE, 1, 3)
        s.text(x + w / 2, 300, name, 14, 600, INK, "middle")
        s.text(x + w / 2, 318, sub, 11.5, 400, MUTED, "middle", family=MONO)
        x += w
    s.text(602, 356, "Header · length · payload · CRC-16/CCITT-FALSE · terminator", 13.5, 400, MUTED)
    s.text(602, 386, "Tested payload: struct.pack('<I5f', t, roll, pitch, a, b, c)", 13, 400, TEXT, family=MONO)
    s.text(602, 408, "= 24 bytes: u32 timestamp + five f32 values", 13, 400, MUTED)
    s.text(602, 438, "Tests: resync after noise · byte-by-byte · bad CRC · multiple frames", 13, 400, MUTED)
    s.text(602, 468, "Recommendation only; payload schema is not in the archive.", 13.5, 500, WARM)

    # attitude
    card(s, 584, 516, 488, 240)
    label(s, 602, 542, "Attitude")
    s.text(602, 570, "atan2 + complementary filter", 19, 600, INK)
    s.text(602, 602, "φ = atan2(a_y, a_z)", 16, 500, INK, family=MONO)
    s.text(602, 626, "θ = atan2(-a_x, √(a_y² + a_z²))", 16, 500, INK, family=MONO)
    s.text(602, 656, "α = τ / (τ + Δt)", 15, 400, TEXT, family=MONO)
    s.text(602, 678, "θ_k = α θ_acc,k + (1-α)(θ_{k-1} + ω_y Δt)", 14, 400, TEXT, family=MONO)
    s.text(602, 710, "Archived stream is text; the binary frame is proposed.", 13, 500, WARM)

    # ground station
    card(s, 1104, 196, 440, 560)
    label(s, 1122, 222, "Ground station")
    s.text(1122, 250, "PyQt5 prototype", 20, 600, INK)
    s.image(B / "dust-ground.webp", 1122, 266, 404, 218)
    s.text(1122, 504, "Six placeholder plots · static attitude cube", 13, 400, MUTED)
    s.text(1122, 532, "Serial 9600 8-N-1 · writes data.txt", 13, 400, MUTED)
    s.text(1122, 560, "Command buttons are not wired.", 13.5, 500, WARM)
    s.text(1122, 596, "The archived parser uses X/Y/GX/GY/GZ text.", 13, 400, MUTED)
    s.text(1122, 616, "Split frames are lost; concatenated frames", 13, 400, MUTED)
    s.text(1122, 635, "are misparsed.", 13, 400, MUTED)
    s.text(1122, 666, "The proposed CRC-16 frame is not implemented", 13, 400, MUTED)
    s.text(1122, 685, "in the archived firmware.", 13, 400, MUTED)
    s.text(1122, 720, "32 tests · 16 errata", 14, 600, ACCENT)

    footer(s, "Source: DustArrow repository README, telemetry frame tests, and ground-station source.", "D · telemetry")
    return s.render("\n".join(s.parts))


def build_dustarrow():
    for name, fn in [("dustarrow-a", dust_a), ("dustarrow-b", dust_b), ("dustarrow-c", dust_c), ("dustarrow-d", dust_d)]:
        out = SRC / f"{name}.svg"
        out.write_text(fn(), encoding="utf-8")
        print(out, out.stat().st_size)




# ---------------------------------------------------------------------------
# OnesArm
# ---------------------------------------------------------------------------
def ones_a():
    s = panel("OnesArm A — modular architecture", "A", "Modular architecture",
              "Four layers, one interface",
              "Interchangeable end effectors, links, joints, and a 4040 base; every connection is a T/N mortise-and-tenon.",
              "ONESARM · v2")

    card(s, 56, 196, 500, 560)
    label(s, 74, 222, "Four module layers")
    layers = [
        ("01", "END EFFECTORS", "gripper ≤ 50 mm · ultrasonic · gas · pen", 254),
        ("02", "LINKS", "X-X / X-Y long links · short link · M5 nodes", 352),
        ("03", "JOINTS", "45° / 90° · 42BYGH47 + FLE-42-20 1:20", 450),
        ("04", "BASE", "4040 profile · 350 W · STM32F407 · XT60", 548),
    ]
    for n, name, detail, y in layers:
        s.text(74, y, n, 13, 600, ACCENT, family=MONO)
        s.text(108, y, name, 17, 600, INK)
        s.text(108, y + 22, detail, 13.5, 400, MUTED)
        s.line(74, y + 38, 536, y + 38, LINE_SOFT, 1)
    s.text(74, 646, "T / N interface · M5 clamp · 0° or 90°", 14, 500, WARM)
    s.text(74, 676, "The drive stack is packaged inside the joint:", 13.5, 400, MUTED)
    s.text(74, 696, "motor, reducer, encoder, and CAN node.", 13.5, 400, MUTED)
    s.text(74, 726, "Same interface at every position in the chain.", 13.5, 500, ACCENT)

    card(s, 584, 196, 960, 560)
    label(s, 604, 222, "v2 platform")
    s.text(604, 250, "On a 4040 aluminium platform", 22, 600, INK)
    s.image(B / "ones-banner.webp", 604, 258, 700, 392)
    cx = 1328
    facts = [("3", "joint modules", "45° + 90° + 90°"), ("4", "DOF analysed", "AyCxBy-D"), ("450", "mm reach", "10,000 samples"), ("24", "CAD layouts", "3! × 2²")]
    for i, (n, t1, t2) in enumerate(facts):
        y = 300 + i * 92
        s.text(cx, y, n, 30, 600, ACCENT)
        s.text(cx + 64, y - 8, t1, 15.5, 600, INK)
        s.text(cx + 64, y + 12, t2, 13, 400, MUTED)
    s.text(604, 672, "Bench-mounted serial arm · no measured payload or repeatability data", 13.5, 500, WARM)
    s.text(604, 696, "24 CAD assemblies · 11 Python checks · CAN firmware is a skeleton", 13.5, 400, MUTED)
    s.text(604, 720, "v2 material only; v1 is retained for comparison.", 13.5, 400, MUTED)

    for i, (x, y, w, h) in enumerate([(56, 196, 500, 560), (584, 196, 960, 560)], 1):
        s.rect(x, y, w, h, "none", ACCENT, 3, 5, opacity=0, extra=f'id="o-a-focus{i}"')

    footer(s, "Source: OnesArm repository README, v2 material only.", "A · modular architecture")
    return s.render("\n".join(s.parts))


def ones_b():
    s = panel("OnesArm B — FCF grammar", "B", "FCF grammar",
              "One interface, three abstractions",
              "Face–channel–face: a T tenon on top, an N mortise below, two perpendicular channels, one M5 clamp.",
              "ONESARM · v2")

    # FCF chain
    card(s, 56, 196, 520, 300)
    label(s, 74, 222, "Face — channel — face")
    s.text(74, 250, "Every connection is an FCF triple", 20, 600, INK)
    boxes = [("FACE", 74, 292), ("CHANNEL", 228, 292), ("FACE", 382, 292)]
    for t, x, y in boxes:
        s.rect(x, y, 126, 66, PAPER, LINE, 1, 4)
        s.text(x + 63, y + 32, t, 14, 600, INK, "middle")
        s.text(x + 63, y + 50, "T / N" if t == "FACE" else "0° / 90°", 12, 400, MUTED, "middle", family=MONO)
    s.arrow(200, 325, 228, 325, ACCENT, 1.5)
    s.arrow(354, 325, 382, 325, ACCENT, 1.5)
    s.text(74, 396, "A long link reports 6 × 4 = 24 raw pairings;", 13.5, 400, MUTED)
    s.text(74, 416, "18 connection methods are reported.", 13.5, 400, MUTED)
    s.text(74, 446, "A short link: 4 × 4 = 16 raw; 12 reported.", 13.5, 400, MUTED)
    s.text(74, 476, "A joint: 2 × 4 = 8 · four Pro, four Con.", 13.5, 400, MUTED)

    # counts
    card(s, 600, 196, 460, 300)
    label(s, 618, 222, "Reported counts")
    s.text(618, 250, "Per module", 20, 600, INK)
    rows = [("Base", "3"), ("Long link", "18"), ("Short link", "12"), ("Joint", "8"), ("End link", "4 or 6")]
    for i, (a, b) in enumerate(rows):
        y = 292 + i * 34
        s.text(618, y, a, 14.5, 400, TEXT)
        s.text(1000, y, b, 14.5, 600, ACCENT, "end", family=MONO)
        s.line(618, y + 10, 1042, y + 10, LINE_SOFT, 1)
    s.text(618, 472, "These are reported methods, not raw face–channel products.", 13, 500, WARM)

    # chain count
    card(s, 600, 516, 460, 240)
    label(s, 618, 542, "Chain count")
    s.text(618, 570, "N₃ = 3! × 2² = 24", 28, 600, ACCENT)
    s.text(618, 606, "Three modules; base-adjacent orientation fixed.", 13.5, 400, MUTED)
    s.text(618, 626, "The remaining two choose one of two channels.", 13.5, 400, MUTED)
    s.text(618, 656, "24 CAD assemblies; AyCxBy-D is analysed.", 13.5, 500, INK)
    s.text(618, 686, "The FCF product is larger than the 24 build layouts.", 13, 400, MUTED)
    s.text(618, 710, "24 = 3! × 2², not 3! × 2³.", 13, 400, MUTED)

    # T/N detail
    card(s, 1084, 196, 460, 560)
    label(s, 1102, 222, "T / N interface")
    s.text(1102, 250, "Two perpendicular channels", 20, 600, INK)
    # top module + tenon
    s.rect(1122, 290, 180, 56, PAPER, LINE, 1, 3)
    s.text(1212, 322, "module A", 13, 600, INK, "middle")
    s.rect(1182, 346, 60, 16, WARM_SOFT, WARM, 1, 2)
    s.rect(1196, 362, 32, 18, WARM_SOFT, WARM, 1, 2)
    s.text(1252, 360, "T tenon", 12.5, 500, WARM)
    # bottom module + mortise
    s.rect(1122, 404, 180, 56, PAPER, LINE, 1, 3)
    s.text(1212, 436, "module B", 13, 600, INK, "middle")
    s.rect(1182, 388, 60, 16, ACCENT_SOFT, ACCENT, 1, 2)
    s.rect(1196, 404, 32, 18, ACCENT_SOFT, ACCENT, 1, 2)
    s.text(1252, 402, "N mortise", 12.5, 500, ACCENT)
    s.arrow(1322, 330, 1322, 380, ACCENT, 1.4)
    s.text(1334, 356, "slide X / Y", 12, 500, MUTED)
    s.text(1102, 500, "M5 clamp; four M3 holes per face.", 13.5, 400, MUTED)
    s.text(1102, 530, "0° or 90° between modules.", 13.5, 400, MUTED)
    s.text(1102, 560, "Semi-rigid: carries bending, allows small", 13.5, 400, MUTED)
    s.text(1102, 580, "deformation; the rigid-body model is an", 13.5, 400, MUTED)
    s.text(1102, 600, "approximation.", 13.5, 400, MUTED)
    s.text(1102, 642, "Dovetail tenon + half-lap cross joint", 13.5, 500, WARM)
    s.text(1102, 672, "as the geometric inspiration.", 13.5, 400, MUTED)
    s.text(1102, 710, "The Pro and Con sides are not interchangeable.", 13, 400, MUTED)

    # formula card fills the lower-left blank
    card(s, 56, 516, 520, 240)
    label(s, 74, 542, "FCF method count")
    s.text(74, 570, "Formula and the 24 build layouts", 19, 600, INK)
    s.text(74, 604, "N_com = 8^F · 18^(N_LL) · 12^(N_LS)", 17, 500, INK, family=MONO)
    s.text(74, 626, "F joint modules · N_LL long links · N_LS short links", 12.5, 400, MUTED)
    s.text(74, 660, "N₃ = 3! · 2² = 24", 24, 600, ACCENT)
    s.text(74, 684, "Base-adjacent orientation fixed; the remaining two choose 2.", 13, 400, MUTED)
    s.text(74, 716, "Reported: 18 long · 12 short · 8 joint · 3 base", 12.5, 400, TEXT, family=MONO)
    s.text(74, 738, "24 is the three-module build enumeration, not the full FCF product.", 12.5, 500, WARM)

    footer(s, "Source: OnesArm repository README, Figures 6–8; v2 material only.", "B · FCF grammar")
    return s.render("\n".join(s.parts))


def ones_c():
    s = panel("OnesArm C — layouts and MATLAB", "C", "Layouts and MATLAB",
              "24 layouts, one analysed chain",
              "Six module orders × four orientation choices; AyCxBy-D is the 4-DOF chain behind the MATLAB model.",
              "ONESARM · v2")

    # layout matrix
    card(s, 56, 196, 600, 560)
    label(s, 74, 222, "24 CAD layouts")
    s.text(74, 250, "Six orders × four orientations", 20, 600, INK)
    orders = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]
    variants = [
        ["AyBxCx", "AyBxCy", "AyByCx", "AyByCy"],
        ["AyCxBx", "AyCxBy", "AyCyBx", "AyCyBy"],
        ["ByAxCx", "ByAxCy", "ByAyCx", "ByAyCy"],
        ["ByCxAx", "ByCxAy", "ByCyAx", "ByCyAy"],
        ["CyAxBx", "CyAxBy", "CyAyBx", "CyAyBy"],
        ["CyBxAx", "CyBxAy", "CyByAx", "CyByAy"],
    ]
    for r, (order, row) in enumerate(zip(orders, variants)):
        y = 282 + r * 48
        s.text(74, y + 18, order, 12.5, 600, MUTED, family=MONO)
        for c, code in enumerate(row):
            x = 120 + c * 126
            hl = code == "AyCxBy"
            s.rect(x, y, 118, 36, ACCENT_SOFT if hl else PAPER, ACCENT if hl else LINE, 1, 3)
            s.text(x + 59, y + 22, code, 12.5, 600 if hl else 400, ACCENT_STRONG if hl else TEXT, "middle", family=MONO)
    s.text(74, 600, "AyCxBy-D is highlighted; every cell is a SolidWorks assembly.", 13, 400, MUTED)
    s.text(74, 630, "N₃ = 3! × 2² = 24; the base-adjacent orientation is fixed.", 14, 500, ACCENT)
    s.text(74, 660, "The 24 files are a three-module enumeration, not the full FCF product.", 12.5, 400, MUTED)
    # legend row in the lower left
    s.rect(74, 702, 18, 12, ACCENT_SOFT, ACCENT, 1, 2)
    s.text(102, 713, "analysed chain (AyCxBy-D)", 12.5, 400, MUTED)
    s.rect(310, 702, 18, 12, PAPER, LINE, 1, 2)
    s.text(338, 713, "remaining CAD layouts", 12.5, 400, MUTED)
    s.text(74, 740, "24 = permutations × orientation choices", 12.5, 500, INK)

    # DH table
    card(s, 680, 196, 420, 280)
    label(s, 698, 222, "Standard DH")
    s.text(698, 250, "AyCxBy-D · 4 DOF", 20, 600, INK)
    head = ["i", "dᵢ", "aᵢ", "αᵢ"]
    for j, h in enumerate(head):
        s.text(698 + j * 92, 282, h, 12.5, 600, MUTED, family=MONO)
    vals = [("1", "95", "0", "90°"), ("2", "0", "113.5", "90°"), ("3", "21.34", "88.5", "90°"), ("4", "0", "152", "0°")]
    for i, row in enumerate(vals):
        y = 310 + i * 30
        for j, v in enumerate(row):
            s.text(698 + j * 92, y, v, 14, 400, TEXT, family=MONO)
        s.line(698, y + 10, 1078, y + 10, LINE_SOFT, 1)
    s.text(698, 444, "Link sum 354 mm; ~450 mm reach from 10,000 samples.", 13, 500, ACCENT)
    s.text(698, 468, "Report order is not standard DH (errata E-01/E-02).", 12.5, 500, WARM)

    # MATLAB reading guide
    card(s, 680, 496, 420, 300)
    label(s, 698, 522, "MATLAB reading guide")
    s.text(698, 550, "Standard-DH chain", 19, 600, INK)
    # four-joint chain schematic
    base_y = 596
    s.rect(706, base_y - 22, 22, 44, PAPER, LINE, 1, 2)
    s.text(717, base_y + 42, "base", 11, 400, MUTED, "middle")
    for i in range(4):
        x = 750 + i * 66
        s.add(f'<circle cx="{x}" cy="{base_y}" r="6" fill="{ACCENT_SOFT}" stroke="{ACCENT}" stroke-width="1.4"/>')
        s.text(x, base_y - 14, f"θ{['₁','₂','₃','₄'][i]}", 11.5, 600, ACCENT, "middle", family=MONO)
        if i < 3:
            s.line(x + 6, base_y, x + 60, base_y, INK, 1.2)
            s.text(x + 34, base_y + 18, ["a₂", "a₃", "a₄"][i], 11.5, 400, MUTED, "middle", family=MONO)
    s.line(728, base_y, 744, base_y, INK, 1.2)
    s.text(736, base_y + 18, "d₁", 11.5, 400, MUTED, "middle", family=MONO)
    s.text(698, 660, "T = A₁ A₂ A₃ A₄", 15, 500, INK, family=MONO)
    s.text(698, 684, "354 mm link sum · ≈450 mm reach", 12.5, 400, MUTED)
    # legend
    s.line(698, 704, 1078, 704, LINE_SOFT, 1)
    s.text(698, 724, "—", 12, 600, ACCENT)
    s.text(716, 724, "standard DH (implemented)", 12, 400, MUTED)
    s.text(698, 746, "—", 12, 600, WARM)
    s.text(716, 746, "report order (E-01/E-02)", 12, 400, MUTED)
    s.text(698, 768, "—", 12, 600, MUTED)
    s.text(716, 768, "joint-limit conflict (E-03)", 12, 400, MUTED)

    # MATLAB simulation
    card(s, 1124, 196, 420, 560)
    label(s, 1142, 222, "MATLAB simulation")
    s.text(1142, 250, "AyCxBy-D · 4 DOF", 20, 600, INK)
    video_slot(s, 1144, 270, 380, 214)
    s.text(1142, 512, "WORKSPACE", 13, 600, MUTED, ls=0.8)
    s.text(1142, 548, "≈ 450 mm", 30, 600, ACCENT)
    s.text(1142, 570, "10,000 samples · standard DH", 12.5, 400, MUTED)
    s.text(1142, 596, "link sum 354 mm", 14, 500, INK)
    # reach bar
    s.rect(1142, 620, 380, 16, LINE_SOFT, "none", 0, 2)
    s.rect(1142, 620, 299, 16, ACCENT, "none", 0, 2)
    s.line(1142 + 380, 612, 1142 + 380, 644, WARM, 1.2)
    s.text(1142, 654, "0", 11, 400, MUTED)
    s.text(1142 + 299, 654, "354", 11, 500, ACCENT, "middle", family=MONO)
    s.text(1522, 654, "450 mm", 11, 500, WARM, "end", family=MONO)
    s.text(1142, 684, "Simulation, not measurement.", 13, 500, WARM)
    s.text(1142, 710, "Joint limits: report 0–180°; MATLAB −90–90°", 12, 400, MUTED)
    s.text(1142, 734, "No measured workspace in the archive.", 12.5, 400, MUTED)

    footer(s, "Source: OnesArm repository README, §3–4 and errata; v2 material only.", "C · layouts and MATLAB")
    return s.render("\n".join(s.parts))


def ones_d():
    s = panel("OnesArm D — FEA and control", "D", "FEA and control",
              "FEA and the control chain",
              "The v2 XY link is analysed; the CAN firmware and measured payload remain open.",
              "ONESARM · v2")

    card(s, 56, 196, 520, 560)
    label(s, 74, 222, "Structural analysis")
    s.text(74, 250, "v2 XY long link", 20, 600, INK)
    s.image(B / "ones-fea.webp", 74, 268, 380, 420)
    s.text(74, 700, "URES max 1.388 × 10⁻² mm", 14, 600, WARM)
    s.text(74, 724, "5 mm 5052 Al + 50 × 46 mm carbon tube", 13, 400, MUTED)
    s.text(74, 746, "Service load at the connection nodes", 13, 400, MUTED)

    card(s, 600, 196, 944, 300)
    label(s, 618, 222, "CAN control chain")
    s.text(618, 250, "Bus controller + three joint nodes", 20, 600, INK)
    # boxes
    s.rect(618, 286, 180, 54, PAPER, LINE, 1, 4)
    s.text(708, 310, "STM32F407", 14, 600, INK, "middle")
    s.text(708, 328, "bus controller", 12, 400, MUTED, "middle")
    for i, (x, joint) in enumerate([(860, "joint A"), (1060, "joint B"), (1260, "joint C")]):
        s.rect(x, 286, 160, 54, PAPER, LINE, 1, 4)
        s.text(x + 80, 310, joint, 14, 600, INK, "middle")
        s.text(x + 80, 328, "STM32F103 + TJA1050", 11.5, 400, MUTED, "middle", family=MONO)
        s.arrow(798 if i == 0 else x - 40, 313, x, 313, ACCENT, 1.3)
    s.text(618, 378, "Stepper driver + magnetic encoder in each joint · 350 W supply · LM2596-5.0", 13.5, 400, MUTED)
    s.text(618, 406, "No CAN bit rate, node IDs, termination, or message layout in the archive.", 13, 500, WARM)
    s.text(618, 436, "Firmware projects are CubeMX skeletons; CAN is disabled.", 13, 400, MUTED)

    card(s, 600, 516, 944, 240)
    label(s, 618, 542, "Evidence status")
    s.text(618, 570, "What exists, what is missing", 20, 600, INK)
    left = ["24 CAD layouts", "11 Python checks", "FEA reported (v2 link)", "Analysed AyCxBy-D workspace"]
    right = ["No measured payload", "No repeatability data", "No working CAN firmware", "No bit-rate / message protocol"]
    for i, item in enumerate(left):
        check(s, 618, 606 + i * 28, item, ACCENT, 13.5)
    for i, item in enumerate(right):
        cross(s, 1050, 606 + i * 28, item, 13.5)
    s.text(618, 738, "v2 material only · v1 retained for comparison · errata E-03, E-07–E-14.", 12.5, 400, MUTED)

    footer(s, "Source: OnesArm repository README, §6–7 and verification notes; v2 material only.", "D · FEA and control")
    return s.render("\n".join(s.parts))


def build_onesarm():
    for name, fn in [("onesarm-a", ones_a), ("onesarm-b", ones_b), ("onesarm-c", ones_c), ("onesarm-d", ones_d)]:
        out = SRC / f"{name}.svg"
        out.write_text(fn(), encoding="utf-8")
        print(out, out.stat().st_size)




# ---------------------------------------------------------------------------
# Sencillo
# ---------------------------------------------------------------------------
def senc_a():
    s = panel("Sencillo A — force flow", "A", "Force flow",
              "Two force loops, one frame",
              "Milling force closes through the fixed gantry; riveting force closes through the independent C-frame; the XY stage only positions.",
              "SENCILLO · design target")

    card(s, 56, 196, 700, 560)
    label(s, 74, 222, "Force-flow decoupling")
    s.text(74, 250, "Two closed loops, not one", 20, 600, INK)
    # fixed gantry / milling
    s.rect(110, 330, 210, 18, ACCENT, "none", 0, 2)
    s.rect(110, 348, 18, 178, ACCENT, "none", 0, 2)
    s.rect(302, 348, 18, 178, ACCENT, "none", 0, 2)
    s.rect(170, 330, 70, 26, PAPER, ACCENT, 1, 3)
    s.rect(190, 356, 30, 80, PAPER, ACCENT, 1, 3)
    s.text(205, 382, "Z", 12, 600, ACCENT, "middle", family=MONO)
    s.rect(160, 470, 180, 22, PAPER, LINE, 1, 2)
    s.text(250, 486, "PCB / work", 11.5, 400, MUTED, "middle")
    s.text(110, 552, "FIXED GANTRY + MILLING", 14, 600, ACCENT, ls=0.8)
    s.text(110, 574, "spindle → gantry → base", 12.5, 400, MUTED)
    # C-frame / riveting
    s.rect(480, 348, 20, 178, WARM, "none", 0, 2)
    s.rect(480, 348, 180, 20, WARM, "none", 0, 2)
    s.rect(480, 506, 180, 20, WARM, "none", 0, 2)
    s.rect(560, 368, 34, 70, PAPER, WARM, 1, 3)
    s.rect(570, 438, 14, 30, WARM, "none", 0, 2)
    s.rect(520, 470, 120, 22, PAPER, LINE, 1, 2)
    s.text(580, 486, "PCB / work", 11.5, 400, MUTED, "middle")
    s.text(480, 552, "INDEPENDENT C-FRAME", 14, 600, WARM, ls=0.8)
    s.text(480, 574, "rivet head → C-frame → base", 12.5, 400, MUTED)
    # loops
    s.path("M205,470 L205,360 L160,360 L160,330 L320,330 L320,348 L302,348", ACCENT, 1.6, "none", dash="4 4")
    s.path("M576,470 L576,438 L480,438 L480,348 L660,348 L660,506 L600,506", WARM, 1.6, "none", dash="4 4")
    s.arrow(205, 430, 205, 468, WARM, 1.5)
    s.text(213, 452, "F", 12, 600, WARM, family=MONO)
    s.arrow(576, 438, 576, 470, WARM, 1.5)
    s.text(584, 458, "F", 12, 600, WARM, family=MONO)
    s.text(74, 660, "The XY stage moves the work; it does not carry the process force.", 14, 500, INK)
    s.text(74, 690, "The two loops close independently through the base.", 13.5, 400, MUTED)
    s.text(74, 720, "Design target; no measured machine exists yet.", 13.5, 500, WARM)

    card(s, 780, 196, 764, 300)
    label(s, 798, 222, "Why two loops")
    s.text(798, 250, "Decoupling is the architecture", 20, 600, INK)
    rows = [("Milling", "spindle → fixed gantry → base"), ("Riveting", "head → independent C-frame → base"), ("Positioning", "XY stage · no process force")]
    for i, (a, b) in enumerate(rows):
        y = 292 + i * 46
        s.text(798, y, a, 15, 600, ACCENT if i < 2 else MUTED)
        s.text(930, y, b, 14, 400, MUTED)
    s.text(798, 438, "Large Z forces never pass through the positioning stage.", 13.5, 500, INK)
    s.text(798, 462, "The fixed gantry and the C-frame can be optimised separately.", 13.5, 400, MUTED)

    card(s, 780, 516, 764, 240)
    label(s, 798, 542, "Design target")
    s.text(798, 570, "8/8 mil · 0.8 mm via · ≤ 30 min", 19, 600, INK)
    chips = ["dry isolation milling", "copper-rivet vias", "offline", "pre-prototype"]
    x = 798
    for c in chips:
        x += s.chip(x, 596, c, PAPER, MUTED, 13, LINE) + 8
    s.text(798, 654, "Anteportal Labs · student-founded team", 13.5, 400, MUTED)
    s.text(798, 684, "All performance numbers are design targets, not measurements.", 13.5, 500, WARM)

    for i, (x, y, w, h) in enumerate([(56, 196, 700, 560), (780, 196, 764, 300), (780, 516, 764, 240)], 1):
        s.rect(x, y, w, h, "none", ACCENT, 3, 5, opacity=0, extra=f'id="s-a-focus{i}"')

    footer(s, "Source: Sencillo design-target material, Anteportal Labs; no public repository.", "A · force flow")
    return s.render("\n".join(s.parts))


def senc_b():
    s = panel("Sencillo B — machine layout", "B", "Machine layout",
              "Fixed gantry, independent C-frame",
              "The milling spindle rides a fixed gantry; the riveting head rides an independent C-frame; the XY stage only positions.",
              "SENCILLO · design target")

    card(s, 56, 196, 980, 560)
    label(s, 74, 222, "Two sub-frames")
    s.text(74, 250, "One bed, two structural paths", 20, 600, INK)

    # fixed gantry subfigure
    s.text(90, 292, "FIXED GANTRY", 14, 600, ACCENT, ls=0.8)
    s.rect(100, 330, 220, 18, ACCENT, "none", 0, 2)
    s.rect(100, 348, 18, 180, ACCENT, "none", 0, 2)
    s.rect(302, 348, 18, 180, ACCENT, "none", 0, 2)
    s.rect(158, 330, 70, 24, PAPER, ACCENT, 1, 3)
    s.rect(176, 354, 34, 90, PAPER, ACCENT, 1, 3)
    s.text(193, 384, "Z", 12, 600, ACCENT, "middle", family=MONO)
    s.rect(120, 470, 180, 22, PAPER, LINE, 1, 2)
    s.text(210, 486, "PCB / work", 11.5, 400, MUTED, "middle")
    s.text(90, 552, "milling spindle on Z", 12.5, 400, MUTED)

    # C-frame subfigure
    s.text(390, 292, "INDEPENDENT C-FRAME", 14, 600, WARM, ls=0.8)
    s.rect(390, 348, 20, 180, WARM, "none", 0, 2)
    s.rect(390, 348, 180, 20, WARM, "none", 0, 2)
    s.rect(390, 508, 180, 20, WARM, "none", 0, 2)
    s.rect(470, 368, 34, 70, PAPER, WARM, 1, 3)
    s.rect(480, 438, 14, 30, WARM, "none", 0, 2)
    s.rect(430, 470, 120, 22, PAPER, LINE, 1, 2)
    s.text(490, 486, "PCB / work", 11.5, 400, MUTED, "middle")
    s.text(390, 552, "rivet head on a separate C", 12.5, 400, MUTED)

    # plan view
    s.text(620, 292, "BED PLAN", 14, 600, MUTED, ls=0.8)
    s.rect(620, 330, 390, 210, PAPER, LINE, 1, 3)
    s.rect(650, 360, 330, 18, ACCENT_SOFT, ACCENT, 1, 2)
    s.text(815, 374, "fixed gantry beam", 11.5, 500, ACCENT, "middle")
    s.rect(660, 430, 34, 70, WARM_SOFT, WARM, 1, 2)
    s.text(677, 468, "C", 12, 600, WARM, "middle")
    s.rect(730, 430, 220, 60, SURFACE, LINE, 1, 2)
    s.text(840, 466, "XY stage / PCB", 12, 400, MUTED, "middle")
    s.text(620, 566, "The positioning stage is mechanically separate from both force paths.", 13, 400, MUTED)

    card(s, 1060, 196, 484, 560)
    label(s, 1078, 222, "Why it matters")
    s.text(1078, 250, "Compliance stays out of XY", 19, 600, INK)
    s.text(1078, 284, "Milling force", 15, 600, ACCENT)
    s.text(1078, 306, "closes through the fixed gantry.", 13.5, 400, MUTED)
    s.text(1078, 338, "Riveting force", 15, 600, WARM)
    s.text(1078, 360, "closes through the independent C-frame.", 13.5, 400, MUTED)
    s.text(1078, 392, "Positioning", 15, 600, MUTED)
    s.text(1078, 414, "carries no process force; only the work.", 13.5, 400, MUTED)
    s.line(1078, 450, 1526, 450, LINE_SOFT, 1)
    s.text(1078, 478, "Axes", 13, 600, MUTED, ls=0.8)
    axes = [("X", "gantry / bed", ACCENT), ("Y", "gantry / bed", ACCENT), ("Z", "spindle / rivet head", WARM)]
    for i, (ax, desc, col) in enumerate(axes):
        y = 506 + i * 30
        s.text(1078, y, ax, 15, 600, col, family=MONO)
        s.text(1110, y, desc, 13.5, 400, MUTED)
    s.text(1078, 618, "Design target · not measured.", 13.5, 500, WARM)
    s.text(1078, 648, "The machine is pre-prototype as of October 2026.", 13.5, 400, MUTED)

    footer(s, "Source: Sencillo design-target material, Anteportal Labs; no public repository.", "B · machine layout")
    return s.render("\n".join(s.parts))


def senc_c():
    s = panel("Sencillo C — error budget", "C", "Error budget",
              "An error budget for 8/8 mil",
              "Eight contributors, RSS 27.5 µm against a 50 µm budget; 22.5 µm margin. Design targets, not measurements.",
              "SENCILLO · design target")

    card(s, 56, 196, 900, 560)
    label(s, 74, 222, "3σ error contributions")
    s.text(74, 250, "Eight allowances, root-sum-square", 20, 600, INK)
    rows = [
        ("Thermal drift", "preheat 30 min · 20 ± 2 °C", 20, WARM),
        ("Lead-screw lead error", "C5 ground · full closed loop", 12, ACCENT),
        ("Guide-rail straightness", "MGN12H P · preload", 8, ACCENT),
        ("Fixture repeatability", "taper pin · floating clamp", 8, ACCENT),
        ("Vibration / EMI", "isolation · shielding · optocoupler", 6, MUTED),
        ("Closed-loop steady state", "1 µm grating · PID + feedforward", 5, ACCENT),
        ("Bearing axial play", "7602 preload", 4, MUTED),
        ("Spindle runout", "MSIY-3060 · assembly calibration", 3, MUTED),
    ]
    for i, (name, control, value, col) in enumerate(rows):
        y = 294 + i * 42
        s.text(74, y, name, 14.5, 500, TEXT)
        s.text(74, y + 17, control, 11.5, 400, MUTED)
        s.rect(310, y - 9, 500, 16, LINE_SOFT, "none", 0, 2)
        s.rect(310, y - 9, value / 20 * 500, 16, col, "none", 0, 2)
        s.text(824, y + 4, f"{value} µm", 12.5, 600, col, family=MONO)
    s.text(74, 660, "RSS = √(20² + 12² + 8² + 8² + 6² + 5² + 4² + 3²) = 27.5 µm", 14, 500, ACCENT)
    s.text(74, 686, "The budget is 50 µm; the design margin is 22.5 µm.", 13.5, 400, MUTED)
    s.text(74, 716, "Each bar is a design allowance, not a measured error.", 13.5, 500, WARM)

    card(s, 984, 196, 560, 560)
    label(s, 1002, 222, "Budget")
    s.text(1002, 272, "27.5 µm", 52, 600, ACCENT)
    s.text(1002, 300, "root-sum-square (3σ)", 13.5, 400, MUTED)
    s.line(1002, 326, 1526, 326, LINE_SOFT, 1)
    stats = [("50 µm", "budget"), ("22.5 µm", "margin")]
    for i, (v, k) in enumerate(stats):
        y = 360 + i * 44
        s.text(1002, y, v, 24, 600, INK)
        s.text(1110, y, k, 14, 400, MUTED)
    # budget bar
    s.text(1002, 468, "RSS vs budget", 13, 600, MUTED, ls=0.8)
    s.rect(1002, 486, 500, 28, LINE_SOFT, "none", 0, 3)
    s.rect(1002, 486, 275, 28, ACCENT, "none", 0, 3)
    s.line(1002 + 500, 478, 1002 + 500, 522, WARM, 1.4)
    s.text(1002, 536, "0", 12, 400, MUTED)
    s.text(1002 + 500, 536, "50 µm", 12, 400, WARM, "end", family=MONO)
    s.text(1002, 570, "The 50 µm budget is the machine allowance; 8/8 mil is the process target.", 13.5, 400, MUTED)
    s.text(1002, 598, "No measured error budget exists for this pre-prototype.", 13.5, 500, WARM)
    s.text(1002, 630, "Target: dry isolation milling + in-machine copper-rivet vias.", 13, 400, MUTED)
    s.text(1002, 656, "≤ 30 min per board · 0.8 mm vias.", 13, 400, MUTED)
    s.text(1002, 700, "Design target · October 2026.", 13, 500, WARM)

    footer(s, "Source: Sencillo design-target figures, Anteportal Labs; all values are targets, not measurements.", "C · error budget")
    return s.render("\n".join(s.parts))


def senc_d():
    s = panel("Sencillo D — constraint compiler", "D", "Constraint compiler",
              "Constraint compilation, five gates",
              "A 7B offline model turns intent into a JSON schema; deterministic CAM turns Gerber/ODB++ into a process IR; five gates must pass.",
              "SENCILLO · design target")

    card(s, 56, 196, 650, 560)
    label(s, 74, 222, "Pipeline")
    s.text(74, 250, "Intent and geometry converge on an IR", 19, 600, INK)
    boxes = [
        ("Natural-language intent", "constraint parsing", 74, 288, 260),
        ("Gerber / ODB++", "board geometry", 370, 288, 260),
        ("7B offline model", "JSON Schema constrained", 74, 380, 260),
        ("Deterministic CAM", "tool, offset, tabs", 370, 380, 260),
        ("Process IR", "ordered operations + machine state", 74, 472, 556),
        ("G1–G5 gates", "validate", 74, 564, 260),
        ("Postprocessor", "machine commands", 370, 564, 260),
    ]
    for t, desc, x, y, w in boxes:
        s.rect(x, y, w, 56, PAPER, LINE, 1, 4)
        s.text(x + 12, y + 22, t, 14, 600, INK)
        s.text(x + 12, y + 42, desc, 11.5, 400, MUTED)
    s.arrow(204, 344, 204, 380, ACCENT, 1.4)
    s.arrow(500, 344, 500, 380, ACCENT, 1.4)
    s.arrow(204, 436, 204, 472, ACCENT, 1.4)
    s.arrow(500, 436, 500, 472, ACCENT, 1.4)
    s.arrow(352, 500, 370, 500, ACCENT, 1.4)
    s.arrow(204, 528, 204, 564, ACCENT, 1.4)
    s.arrow(500, 528, 500, 564, ACCENT, 1.4)
    s.arrow(334, 592, 370, 592, ACCENT, 1.4)
    s.path("M334,620 L334,640 L60,640 L60,500", WARM, 1.4, "none", dash="4 4")
    s.text(74, 668, "Fail: reject with rule, coordinate, minimal fix.", 13, 500, WARM)
    s.text(74, 696, "No implementation of the 24-layout/constraint compiler is in the archive.", 12.5, 400, MUTED)
    s.text(74, 724, "Design target only.", 13, 500, WARM)

    card(s, 730, 196, 814, 560)
    label(s, 748, 222, "Five validation gates")
    s.text(748, 250, "Every plan must pass all five", 20, 600, INK)
    gates = [
        ("G1", "Sheet / board bounds", "the board and all features fit the work envelope"),
        ("G2", "Geometric interference", "no tool, clamp, or rivet head collision"),
        ("G3", "Rivet clearance", "via and rivet keep-out around traces and holes"),
        ("G4", "Locking / interlock", "fixture and tool changes are interlocked"),
        ("G5", "Thermal budget", "preheat and process window stay in budget"),
    ]
    for i, (g, name, desc) in enumerate(gates):
        y = 292 + i * 62
        s.add(f'<circle cx="762" cy="{y-5}" r="14" fill="{ACCENT}" stroke="none"/>')
        s.text(762, y, g, 11, 600, PAPER, "middle", family=MONO)
        s.text(788, y, name, 15.5, 600, INK)
        s.text(788, y + 19, desc, 12.5, 400, MUTED)
        s.text(1526, y, "target", 11.5, 600, ACCENT, "end", family=MONO)
    s.text(748, 636, "A failure returns the rule, coordinate, and a minimal repair.", 13.5, 500, WARM)
    s.text(748, 666, "The five gates are design targets; no measured machine or compiler exists.", 13.5, 400, MUTED)
    s.text(748, 700, "Deterministic CAM remains separate from the model.", 13.5, 500, INK)
    s.text(748, 730, "The model never emits machine code directly.", 13.5, 400, MUTED)

    footer(s, "Source: Sencillo design-target material, Anteportal Labs; five-gate names from the supplied figures.", "D · constraint compiler")
    return s.render("\n".join(s.parts))


def build_sencillo():
    for name, fn in [("sencillo-a", senc_a), ("sencillo-b", senc_b), ("sencillo-c", senc_c), ("sencillo-d", senc_d)]:
        out = SRC / f"{name}.svg"
        out.write_text(fn(), encoding="utf-8")
        print(out, out.stat().st_size)


if __name__ == "__main__":
    build_hsiwu()
    build_dustarrow()
    build_onesarm()
    build_sencillo()
