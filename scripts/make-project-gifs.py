#!/usr/bin/env python3
"""Build the animated project cards from the repositories' own GIFs.

Usage:
    python3 scripts/make-project-gifs.py --source /path/to/downloaded-gifs

The source GIFs are not committed to this repository. Download them from:
  Vulcan:    https://github.com/Robusr/Vulcan/blob/main/docs/assets/solidworks-plate.gif
  Hsiwu:     https://github.com/Robusr/Hsiwu/blob/main/media/photos/project/screw_movement.gif
  DustArrow: https://github.com/Robusr/DustArrow/blob/main/media/photos/project/canard_deployment.gif
  OnesArm:   https://github.com/Robusr/OnesArm/blob/main/media/gifs/onesarm_motion.gif

Sencillo has no public project repository; its GIF is an illustrative
design-target animation generated from the process described on the site.
Requires Pillow.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageSequence

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public/assets/projects"
SIZE = (400, 225)

SPECS = {
    "vulcan": {
        "source": "vulcan-solidworks-plate.gif",
        "crop": (80, 140, 1180, 760),
        "frames": (0, 5),
        "out": "vulcan-card.gif",
        "colors": 128,
    },
    "hsiwu": {
        "source": "hsiwu-screw_movement.gif",
        "crop": (0, 17, 400, 242),
        "frames": (0, 45),
        "out": "hsiwu-card.gif",
        "colors": 40,
    },
    "dustarrow": {
        "source": "dustarrow-canard_deployment.gif",
        "crop": (0, 31, 800, 481),
        "frames": (20, 50),
        "out": "dustarrow-card.gif",
        "colors": 96,
    },
    "onesarm": {
        "source": "onesarm-onesarm_motion.gif",
        "crop": (0, 50, 400, 275),
        "frames": (0, 24),
        "out": "onesarm-card.gif",
        "colors": 96,
    },
}


def save_gif(frames, durations, dest, colors):
    quantized = [frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=colors) for frame in frames]
    quantized[0].info.pop("loop", None)
    quantized[0].save(
        dest,
        save_all=True,
        append_images=quantized[1:],
        duration=durations,
        optimize=True,
        disposal=2,
    )
    # gifsicle tightens frame diffs and colour tables; keep it optional.
    import shutil, subprocess
    if shutil.which("gifsicle"):
        tmp = dest.with_suffix(".opt.gif")
        subprocess.run(["gifsicle", "-O3", "--lossy=80", "--colors", str(min(colors, 96)), str(dest), "-o", str(tmp)], check=True)
        tmp.replace(dest)
    print(f"{dest.relative_to(ROOT)}  {dest.stat().st_size / 1024:.1f} KB  {len(frames)} frames")


def build_from_source(source_dir, key, spec):
    source = source_dir / spec["source"]
    if not source.exists():
        raise FileNotFoundError(source)
    start, end = spec["frames"]
    frames, durations = [], []
    with Image.open(source) as image:
        for index, frame in enumerate(ImageSequence.Iterator(image)):
            if index < start:
                continue
            if index >= end:
                break
            cropped = frame.convert("RGB").crop(spec["crop"])
            frames.append(cropped.resize(SIZE, Image.Resampling.LANCZOS))
            durations.append(frame.info.get("duration", 80))
    save_gif(frames, durations, OUT / spec["out"], spec["colors"])


def build_sencillo():
    # An illustrative design-target loop, not a measured machine recording.
    scale = 2
    w, h = SIZE[0] * scale, SIZE[1] * scale
    paper = (251, 251, 249)
    ink = (10, 13, 41)
    copper = (190, 126, 77)
    teal = (15, 107, 95)
    line = (228, 228, 223)
    frames, durations = [], []
    steps = 48
    for step in range(steps):
        frame = Image.new("RGB", (w, h), paper)
        d = ImageDraw.Draw(frame)
        # Faint drafting grid.
        for x in range(24, w, 36):
            for y in range(24, h, 36):
                d.ellipse((x, y, x + 1, y + 1), fill=(238, 238, 233))
        # PCB and copper layout.
        board = (140, 90, 820, 450)
        d.rounded_rectangle(board, radius=16, fill=ink, outline=line, width=2)
        for y in (180, 270, 360):
            d.line((210, y, 700, y), fill=copper, width=6)
            d.ellipse((190, y - 10, 210, y + 10), fill=copper)
            d.ellipse((700, y - 10, 720, y + 10), fill=copper)
        for x in (260, 420, 580):
            d.ellipse((x - 9, 250, x + 9, 268), outline=copper, width=4)
        # The milling tool follows a serpentine isolation path.
        progress = step / (steps - 1)
        path = [(200, 130), (720, 130), (720, 225), (200, 225), (200, 315), (720, 315), (720, 405), (200, 405)]
        segments = len(path) - 1
        segment = min(segments - 1, int(progress * segments))
        local = (progress * segments) - segment
        x0, y0 = path[segment]
        x1, y1 = path[min(segments, segment + 1)]
        tx = int(x0 + (x1 - x0) * local)
        ty = int(y0 + (y1 - y0) * local)
        for index in range(segment):
            d.line((*path[index], *path[index + 1]), fill=teal, width=3)
        d.line((x0, y0, tx, ty), fill=teal, width=3)
        d.ellipse((tx - 15, ty - 15, tx + 15, ty + 15), outline=teal, width=3)
        d.line((tx - 22, ty, tx + 22, ty), fill=teal, width=1)
        d.line((tx, ty - 22, tx, ty + 22), fill=teal, width=1)
        frames.append(frame.resize(SIZE, Image.Resampling.LANCZOS))
        durations.append(80)
    save_gif(frames, durations, OUT / "anteportal-card.gif", 128)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="directory containing downloaded source GIFs")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.source:
        for key, spec in SPECS.items():
            build_from_source(args.source, key, spec)
    build_sencillo()


if __name__ == "__main__":
    main()
