# Content inventory

Audit date: 2026-10-20. Production domain updated 2026-10-21. Link checks re-verified 2026-10-22. GitHub snapshot refreshed 2026-11-26. Sources: the local info library at `/Users/robusr/Desktop/Homepage information/Homepage-Info-Library/` (files 01–07, `sources.md`, `data/*.json`, `assets/`), plus live checks of every outbound link and the public GitHub API.

## Facts used directly

| Fact | Value | Source |
|---|---|---|
| Name | 郭沫晗 / Robusr Guo | 01, data/profile.json |
| University | Huazhong University of Science and Technology, School of Mechanical Science and Engineering, Robotics Engineering Innovation Experimental Class, entered 2025-09 | 01, profile.json |
| Hometown | Guyuan, Ningxia | 01 |
| Current city | Wuhan, China | 01, profile.json |
| Starting point | Bedroom mechatronics workshop at 13 (2018) | 03, profile.json |
| Direction | AI × Engineering; AI for CAD / CAM / manufacturing | 01 |
| Team | Anteportal Labs, student-founded, not a registered company | 01, 02, profile.json |
| Vulcan | typed JSON feature tree, SolidWorks COM API, no exec(), GPL-3.0, 26 stars / 3 forks (2026-11-26), release v1.3.0 | 02, projects.json, github.json |
| Hsiwu | six wing segments, three motors, 3× NE555, 1× 74HC04, 3× L293D, no MCU, MIT, 9 stars / 2 forks (2026-11-26) | 02, projects.json, github.json |
| DustArrow X | 40 mm, ten bays, nine PCB modules, RP2040, LoRa, PyQt5, 32 tests, Gobi flight 2023, national second prize | 02, 04 |
| OnesArm | T/N interface, 3! × 2² = 24 layouts, STM32F103/F407, CAN, ~450 mm reach, national first prize 2024 | 02, 04 |
| Sencillo | desktop PCB fabrication, 8/8 mil, 0.8 mm copper rivets, ≤30 min, 50 × 50 mm, all design targets, pre-prototype | 02 |
| Awards | 38th CASTIC first prize 2024 (OnesArm); 37th CASTIC second prize 2023 (DustArrow); Shanghai TV Young Edison S8 2024 | 04 |
| More Work | Huginn, Robusr-skill, Lynx, Gungnir | 02, projects.json, GitHub profile 2026-11-26 |
| Mini Lab | Bedroom workbench photo, full-width section 00 after the Hero and before Selected Work; paper mat with `Fig. 00`; 480/960/1440 WebP and 1440 JPEG fallback; EXIF stripped and warm graded | minilab.jpeg, supplied 2026-11-26 |
| OG card | 1200×630 `og-default-v3.png` with the Mini Lab plate and the site tagline | scripts/make-og.py, 2026-11-26 |
| Contact | GitHub, email, Anteportal org only | 01, 06 |

## Rewritten for the page

- Hero intro is two short third-person sentences: ten years as a bedroom geek and the mechatronics workshop at 13.
- Project summaries follow problem → method → evidence → next step, 2–3 sentences, no more than six tech tags.
- About uses one first-person paragraph supplied by Robusr on 2026-11-26, with English and French translations; the Chinese text is the source for that paragraph.
- Journey compressed to exactly six rows, as specified in the brief.
- Mini Lab is a photo-only section after the Hero, numbered 00 and placed before Selected Work, with a one-line caption and localized alt text; the published files have no EXIF metadata.
- French and Chinese copy is translated from the English source, except the About paragraph, which was supplied in Chinese and translated into English and French.

## Deliberately excluded

- Family, address, birthday, exam scores, ranking, leave of absence, personal relationships; the About paragraph's art-teacher sentence is the owner-requested exception.
- Bilibili, LinkedIn, X, and any unverified account.
- TV stills, competition logos, third-party paper figures, datasheet images.
- The 2026 national innovation project (participant, not lead) and the 2026-07 Ningxia Science Museum appearance (unverified).
- Any claim of a registered company, funding, sponsorship, or official partnership.

## Link checks (2026-10-20)

| URL | HTTP status | Decision |
|---|---|---|
| https://robusr.github.io | 404 | retired; no longer canonical |
| https://robusr.cn | 200 | configured canonical site |
| https://www.robusr.cn | 200 | duplicate host; needs a 301 Redirect Rule |
| https://github.com/Robusr | 200 | use |
| https://github.com/Robusr/Vulcan | 200 | use |
| https://github.com/Robusr/Hsiwu | 200 | use |
| https://github.com/Robusr/DustArrow | 200 | use |
| https://github.com/Robusr/OnesArm | 200 | use |
| https://github.com/Anteportal | 200 | use |
| https://www.kankanews.com/detail/LMwVGm9WB2z | 200 | use as media link |
| mailto:Robusr@outlook.com | format valid | use |

## Asset checks

| Asset | Original | Use on site |
|---|---|---|
| `portrait.JPG` | 3072×4096, 13.4 MB | 4:5 crop 512×644: WebP 56 KB, JPEG 73 KB, 260 px WebP 21 KB |
| `Robusr_A.jpg` | 1396×1080, 116 KB | trimmed 850×891, transparent WebP 56 KB, used as the site watermark |
| `vulcan-card.png` | 1200×675 | 960/480 WebP (19/7.8 KB), 960 JPEG 66 KB |
| `hsiwu-card.png` | 1200×675 | 960/480 WebP (33/12 KB), 960 JPEG 81 KB |
| `dustarrow-card.png` | 1200×675 | 960/480 WebP (8.7/3.6 KB), 960 JPEG 38 KB |
| `onesarm-card.jpg` | 1200×675 | 960/480 WebP (30/12 KB), 960 JPEG 91 KB |
| `anteportal-card.png` | 1200×675 | 960/480 WebP (17/8 KB), 960 JPEG 54 KB |
| OG image | generated | 1200×630 PNG, 305 KB |

All source images remain untouched in the info library; only copies were converted.

## Implementation note

The brief's example tree places the app under `site/`. The repository is `Robusr/robusr.github.io`, and production moved to Cloudflare Pages. The Astro app stays at the repository root with `base: /`, which keeps `dist/` publishable as-is. Content data still lives in `src/data/*.json` and is the single source for rendering.
