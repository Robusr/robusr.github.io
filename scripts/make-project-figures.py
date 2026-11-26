#!/usr/bin/env python3
"""Build the four-panel academic figure plates.

Sources are downloaded from the project repositories into /tmp; the
whitepaper page renders come from the local PDF. The committed outputs
live in public/assets/projects/figures/.

Usage:
    python3 scripts/make-project-figures.py \
      --assets /tmp/project-assets \
      --gifs /tmp/project-gifs \
      --pdf-pages /tmp/sencillo-pages

Requires Pillow; uses ffmpeg + gifsicle when available for the new GIFs.
"""
import argparse
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageSequence

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public/assets/projects/figures"
SIZE = (800, 450)
PAPER = (251, 251, 249)
INK = (10, 13, 41)
TEAL = (15, 107, 95)
COPPER = (184, 115, 51)


def font(size, bold=False):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def contain(src, dest, quality=90):
    image = Image.open(src).convert("RGB")
    fitted = ImageOps.contain(image, SIZE, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", SIZE, PAPER)
    canvas.paste(fitted, ((SIZE[0] - fitted.width) // 2, (SIZE[1] - fitted.height) // 2))
    canvas.save(dest, "WEBP", quality=quality, method=6)
    print(f"{dest.name}  {dest.stat().st_size / 1024:.1f} KB")


def cover(src, dest, quality=88, centering=(0.5, 0.5)):
    image = Image.open(src).convert("RGB")
    fitted = ImageOps.fit(image, SIZE, Image.Resampling.LANCZOS, centering=centering)
    fitted.save(dest, "WEBP", quality=quality, method=6)
    print(f"{dest.name}  {dest.stat().st_size / 1024:.1f} KB")


def crop_pdf(src, box, dest, quality=92):
    image = Image.open(src).convert("RGB").crop(box)
    fitted = ImageOps.contain(image, SIZE, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", SIZE, PAPER)
    canvas.paste(fitted, ((SIZE[0] - fitted.width) // 2, (SIZE[1] - fitted.height) // 2))
    canvas.save(dest, "WEBP", quality=quality, method=6)
    print(f"{dest.name}  {dest.stat().st_size / 1024:.1f} KB")


def copy_gif(src, dest, fallback_frame=0, optimize=True):
    shutil.copyfile(src, dest)
    with Image.open(src) as image:
        image.seek(fallback_frame)
        frame = image.convert("RGB")
        frame.save(dest.with_suffix(".webp"), "WEBP", quality=90, method=6)
    if optimize and shutil.which("gifsicle"):
        tmp = dest.with_suffix(".opt.gif")
        subprocess.run(["gifsicle", "-O3", "--lossy=80", str(dest), "-o", str(tmp)], check=True)
        tmp.replace(dest)
    print(f"{dest.name}  {dest.stat().st_size / 1024:.1f} KB")


def nose_gif(frames_dir, dest):
    frames = sorted(frames_dir.glob("frame-*.png"))[:33]
    out_frames, durations = [], []
    for frame in frames:
        image = Image.open(frame).convert("RGB")
        image = ImageOps.fit(image, (400, 225), Image.Resampling.LANCZOS, centering=(0.5, 0.45))
        out_frames.append(image.convert("P", palette=Image.Palette.ADAPTIVE, colors=96))
        durations.append(125)
    out_frames[0].info.pop("loop", None)
    out_frames[0].save(dest, save_all=True, append_images=out_frames[1:], duration=durations, optimize=True, disposal=2)
    if shutil.which("gifsicle"):
        tmp = dest.with_suffix(".opt.gif")
        subprocess.run(["gifsicle", "-O3", "--lossy=80", "--colors", "96", str(dest), "-o", str(tmp)], check=True)
        tmp.replace(dest)
    Image.open(dest).seek(0)
    with Image.open(dest) as gif:
        gif.seek(gif.n_frames - 1)
        gif.convert("RGB").resize(SIZE, Image.Resampling.LANCZOS).save(dest.with_suffix(".webp"), "WEBP", quality=90, method=6)
    print(f"{dest.name}  {dest.stat().st_size / 1024:.1f} KB  {len(out_frames)} frames")


def force_flow_frame(progress, width, height):
    scale = 2
    w, h = width * scale, height * scale
    image = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(image)

    def S(value):
        return int(round(value * scale))

    title = font(S(18), True)
    label = font(S(14), True)
    small = font(S(9))
    d.text((S(24), S(18)), "FORCE-FLOW DECOUPLING", font=title, fill=INK)
    d.text((S(24), S(44)), "Milling and riveting close inside the frame; XY only positions.", font=small, fill=(107, 107, 107))

    def loop(cx, cy, color, name):
        left, right = S(cx - 115), S(cx + 115)
        top, bottom = S(cy - 65), S(cy + 65)
        d.rounded_rectangle((left, top, right, bottom), radius=S(12), outline=color, width=S(2))
        d.text((left, top - S(26)), name, font=label, fill=color)
        perimeter = 2 * ((right - left) + (bottom - top))
        position = (progress * perimeter) % perimeter
        if position < right - left:
            x, y = left + position, top
        elif position < (right - left) + (bottom - top):
            x, y = right, top + (position - (right - left))
        elif position < 2 * (right - left) + (bottom - top):
            x, y = right - (position - (right - left) - (bottom - top)), bottom
        else:
            x, y = left, bottom - (position - 2 * (right - left) - (bottom - top))
        d.ellipse((x - S(5), y - S(5), x + S(5), y + S(5)), fill=color)
        d.line((left, top, left + S(22), top), fill=color, width=S(3))
        d.line((right, bottom, right - S(22), bottom), fill=color, width=S(3))
        size = S(6)
        d.polygon([(S(cx) + size, top), (S(cx) - size, top - size), (S(cx) - size, top + size)], fill=color)
        d.polygon([(right, S(cy) + size), (right - size, S(cy) - size), (right + size, S(cy) - size)], fill=color)
        d.polygon([(S(cx) - size, bottom), (S(cx) + size, bottom - size), (S(cx) + size, bottom + size)], fill=color)
        d.polygon([(left, S(cy) - size), (left - size, S(cy) + size), (left + size, S(cy) + size)], fill=color)

    loop(190, 215, TEAL, "MILLING FORCE")
    loop(450, 215, COPPER, "RIVETING FORCE")
    d.line((S(320), S(120), S(320), S(300)), fill=(180, 180, 174), width=S(1))
    d.text((S(320) - S(62), S(310)), "XY: POSITIONING ONLY", font=small, fill=(107, 107, 107))
    return image.resize((width, height), Image.Resampling.LANCZOS)

def force_flow_gif(dest):
    frames, durations = [], []
    for step in range(48):
        frame = force_flow_frame(step / 47, 640, 360)
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=64))
        durations.append(80)
    frames[0].info.pop("loop", None)
    frames[0].save(dest, save_all=True, append_images=frames[1:], duration=durations, optimize=True, disposal=2)
    if shutil.which("gifsicle"):
        tmp = dest.with_suffix(".opt.gif")
        subprocess.run(["gifsicle", "-O3", "--lossy=80", "--colors", "64", str(dest), "-o", str(tmp)], check=True)
        tmp.replace(dest)
    force_flow_frame(1, *SIZE).save(dest.with_suffix(".webp"), "WEBP", quality=90, method=6)
    print(f"{dest.name}  {dest.stat().st_size / 1024:.1f} KB  48 frames")


def vulcan_flow_gif(src, dest):
    with Image.open(src) as image:
        n = image.n_frames
        indices = sorted(set(round(4 + i * (n - 5) / 11) for i in range(12)))
        frames, durations = [], []
        for index in indices:
            image.seek(index)
            frame = image.convert("RGB").crop((0, 0, image.width, round(image.width * 9 / 16)))
            frames.append(frame.resize((400, 225), Image.Resampling.LANCZOS).convert("P", palette=Image.Palette.ADAPTIVE, colors=96))
            durations.append(333)
    frames[0].info.pop("loop", None)
    frames[0].save(dest, save_all=True, append_images=frames[1:], duration=durations, optimize=True, disposal=2)
    if shutil.which("gifsicle"):
        tmp = dest.with_suffix(".opt.gif")
        subprocess.run(["gifsicle", "-O3", "--lossy=80", "--colors", "96", str(dest), "-o", str(tmp)], check=True)
        tmp.replace(dest)
    with Image.open(dest) as gif:
        gif.seek(gif.n_frames - 1)
        gif.convert("RGB").resize(SIZE, Image.Resampling.LANCZOS).save(dest.with_suffix(".webp"), "WEBP", quality=90, method=6)
    print(f"{dest.name}  {dest.stat().st_size / 1024:.1f} KB  {len(frames)} frames")


def hsiwu_control_panel(dest):
    scale = 2
    w, h = SIZE[0] * scale, SIZE[1] * scale
    image = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(image)

    def S(value):
        return int(round(value * scale))

    title = font(S(18), True)
    subtitle = font(S(10))
    box_font = font(S(11), True)
    note = font(S(9))
    d.text((S(26), S(20)), "ANALOG CONTROL ARCHITECTURE", font=title, fill=INK)
    d.text((S(26), S(46)), "No MCU. No firmware. Timing and drive are entirely analog.", font=subtitle, fill=(107, 107, 107))

    def box(x, y, w_, h_, text, color, fill=(255, 255, 255)):
        d.rounded_rectangle((S(x), S(y), S(x + w_), S(y + h_)), radius=S(4), fill=fill, outline=color, width=S(1))
        d.text((S(x + 8), S(y + 8)), text, font=box_font, fill=INK)

    box(26, 92, 140, 44, "3.7 V LiPo", TEAL)
    box(190, 92, 250, 44, "MT3608 boost 7.35 V / LDO 5 V", TEAL)
    box(26, 188, 220, 54, "3× NE555 astable ~4.8 Hz", TEAL)
    box(276, 188, 170, 54, "74HC04 inverter", TEAL)
    box(476, 188, 200, 54, "3× L293D H-bridge", TEAL)
    box(476, 282, 200, 44, "3× wing motors", COPPER)
    box(26, 282, 420, 44, "Power, timing and phase splitting stay on the custom PCB", (228, 228, 223), fill=PAPER)
    d.line((S(166), S(114), S(190), S(114)), fill=INK, width=S(2))
    d.line((S(136), S(242), S(276), S(242)), fill=INK, width=S(2))
    d.line((S(446), S(242), S(476), S(242)), fill=INK, width=S(2))
    d.line((S(576), S(242), S(576), S(282)), fill=INK, width=S(2))
    d.text((S(26), S(352)), "Source logic: 3 oscillators, 1 inverter, 3 H-bridges; no programmed controller.", font=note, fill=(107, 107, 107))
    image.resize(SIZE, Image.Resampling.LANCZOS).save(dest, "WEBP", quality=92, method=6)
    print(f"{dest.name}  {dest.stat().st_size / 1024:.1f} KB")



def onesarm_layouts_panel(dest):
    scale = 2
    w, h = SIZE[0] * scale, SIZE[1] * scale
    image = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(image)

    def S(value):
        return int(round(value * scale))

    title = font(S(18), True)
    formula = font(S(34), True)
    body_font = font(S(12))
    small = font(S(10))
    d.text((S(26), S(20)), "MODULAR COMBINATIONS", font=title, fill=INK)
    d.text((S(26), S(52)), "FCF interface: connecting face → connecting channel → connecting face.", font=body_font, fill=(107, 107, 107))
    d.text((S(26), S(104)), "N3 = 3! · 2² = 24", font=formula, fill=TEAL)
    for index, name in enumerate(["Joint", "Long link", "End link"]):
        x = S(28 + index * 245)
        d.rounded_rectangle((x, S(210), x + S(205), S(286)), radius=S(5), fill=(255, 255, 255), outline=TEAL, width=S(2))
        d.text((x + S(12), S(222)), name, font=body_font, fill=INK)
        d.text((x + S(12), S(252)), "2 perpendicular channels", font=small, fill=(107, 107, 107))
    for index in range(24):
        x = S(36 + (index % 12) * 62)
        y = S(330 + (index // 12) * 32)
        d.ellipse((x, y, x + S(10), y + S(10)), fill=TEAL if index < 24 else (228, 228, 223))
    d.text((S(26), S(402)), "3 module orders × 2 channel choices for each of the two non-base modules.", font=small, fill=(107, 107, 107))
    image.resize(SIZE, Image.Resampling.LANCZOS).save(dest, "WEBP", quality=92, method=6)
    print(f"{dest.name}  {dest.stat().st_size / 1024:.1f} KB")


def fea_gif(src, dest):
    image = Image.open(src).convert("RGB")
    frames, durations = [], []
    steps = 40
    for step in range(steps):
        zoom = 1.0 + 0.08 * (step / (steps - 1))
        width = round(image.width / zoom)
        height = round(image.height / zoom)
        left = (image.width - width) // 2
        top = (image.height - height) // 2
        cropped = image.crop((left, top, left + width, top + height))
        frames.append(ImageOps.fit(cropped, (400, 225), Image.Resampling.LANCZOS, centering=(0.5, 0.5)).convert("P", palette=Image.Palette.ADAPTIVE, colors=96))
        durations.append(100)
    frames[0].info.pop("loop", None)
    frames[0].save(dest, save_all=True, append_images=frames[1:], duration=durations, optimize=True, disposal=2)
    if shutil.which("gifsicle"):
        tmp = dest.with_suffix(".opt.gif")
        subprocess.run(["gifsicle", "-O3", "--lossy=80", "--colors", "96", str(dest), "-o", str(tmp)], check=True)
        tmp.replace(dest)
    with Image.open(dest) as gif:
        gif.seek(gif.n_frames - 1)
        gif.convert("RGB").resize(SIZE, Image.Resampling.LANCZOS).save(dest.with_suffix(".webp"), "WEBP", quality=90, method=6)
    print(f"{dest.name}  {dest.stat().st_size / 1024:.1f} KB  {len(frames)} frames")



def hsiwu_gif(src, dest):
    with Image.open(src) as image:
        frames, durations = [], []
        for index, frame in enumerate(ImageSequence.Iterator(image)):
            if index >= 45:
                break
            cropped = frame.convert("RGB").crop((0, 17, 400, 242)).resize((400, 225), Image.Resampling.LANCZOS)
            frames.append(cropped.convert("P", palette=Image.Palette.ADAPTIVE, colors=48))
            durations.append(frame.info.get("duration", 67))
    frames[0].info.pop("loop", None)
    frames[0].save(dest, save_all=True, append_images=frames[1:], duration=durations, optimize=True, disposal=2)
    if shutil.which("gifsicle"):
        tmp = dest.with_suffix(".opt.gif")
        subprocess.run(["gifsicle", "-O3", "--lossy=80", "--colors", "48", str(dest), "-o", str(tmp)], check=True)
        tmp.replace(dest)
    frames[0].convert("RGB").resize(SIZE, Image.Resampling.LANCZOS).save(dest.with_suffix(".webp"), "WEBP", quality=90, method=6)
    print(f"{dest.name}  {dest.stat().st_size / 1024:.1f} KB  {len(frames)} frames")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets", type=Path, required=True)
    parser.add_argument("--gifs", type=Path, required=True)
    parser.add_argument("--pdf-pages", type=Path, required=True)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    A, G, P = args.assets, args.gifs, args.pdf_pages

    # Vulcan
    vulcan_flow_gif(G / "vulcan-ui-generate-flow.gif", OUT / "vulcan-a.gif")
    contain(A / "vulcan-architecture.png", OUT / "vulcan-b.webp")
    contain(A / "vulcan-pipeline.png", OUT / "vulcan-c.webp")
    with Image.open(G / "vulcan-solidworks-plate.gif") as image:
        image.seek(0)
        frame = image.convert("RGB").crop((80, 140, 1180, 760))
        frame.save("/tmp/vulcan-result.png")
    cover("/tmp/vulcan-result.png", OUT / "vulcan-d.webp")

    # Hsiwu
    hsiwu_gif(G / "hsiwu-screw_movement.gif", OUT / "hsiwu-a.gif")
    hsiwu_control_panel(OUT / "hsiwu-b.webp")
    contain(A / "hsiwu-colored_version.png", OUT / "hsiwu-c.webp")
    contain(A / "hsiwu-line_drawing.png", OUT / "hsiwu-d.webp")

    # DustArrow
    nose_gif(A / "mp4-8fps", OUT / "dustarrow-a.gif")
    with Image.open(G / "dustarrow-cfd_demo.gif") as image:
        image.seek(min(64, image.n_frames - 1))
        image.convert("RGB").save("/tmp/dustarrow-cfd.png")
    cover("/tmp/dustarrow-cfd.png", OUT / "dustarrow-b.webp")
    cover(A / "dustarrow-tv_still_launch.png", OUT / "dustarrow-c.webp", quality=88, centering=(0.55, 0.5))
    contain(A / "dustarrow-system_architecture.png", OUT / "dustarrow-d.webp")

    # OnesArm (v2 only)
    contain(A / "onesarm-banner.jpg", OUT / "onesarm-a.webp")
    contain(A / "onesarm-fig5-7_fcf_structure.png", OUT / "onesarm-b.webp")
    onesarm_layouts_panel(OUT / "onesarm-c.webp")
    fea_gif(A / "onesarm-fig5-3_v2_fea_displacement.png", OUT / "onesarm-d.gif")

    # Sencillo: animated force-flow + three whitepaper figures
    force_flow_gif(OUT / "sencillo-a.gif")
    crop_pdf(P / "hi-10.png", (220, 1020, 1500, 1660), OUT / "sencillo-b.webp")
    crop_pdf(P / "hi-27.png", (150, 320, 1500, 1015), OUT / "sencillo-c.webp")
    crop_pdf(P / "hi-22.png", (150, 270, 1500, 980), OUT / "sencillo-d.webp")


if __name__ == "__main__":
    main()
