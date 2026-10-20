# Content inventory

Audit date: 2026-10-20. Production domain updated 2026-10-21. Sources: the local info library at `/Users/robusr/Desktop/Homepage information/Homepage-Info-Library/` (files 01–07, `sources.md`, `data/*.json`, `assets/`), plus live checks of every outbound link.

## Facts used directly

| Fact | Value | Source |
|---|---|---|
| Name | 郭沫晗 / Robusr Guo | 01, data/profile.json |
| University | Huazhong University of Science and Technology, School of Mechanical Science and Engineering, Robotics Engineering Innovation Experimental Class, entered 2025-09 | 01, profile.json |
| Hometown | Guyuan, Ningxia | 01 |
| Current city | Wuhan, China | 01, profile.json |
| Starting point | Arduino in sixth grade, 2018 | 01, 03 |
| Direction | AI × Engineering; AI for CAD / CAM / manufacturing | 01 |
| Team | Anteportal Labs, student-founded, not a registered company | 01, 02, profile.json |
| Vulcan | typed JSON feature tree, SolidWorks COM API, no exec(), GPL-3.0, 23 stars / 2 forks (2026-10-20) | 02, projects.json |
| Hsiwu | six wing segments, three motors, 3× NE555, 1× 74HC04, 3× L293D, no MCU, MIT, 8 stars (2026-10-20) | 02, projects.json |
| DustArrow X | 40 mm, ten bays, nine PCB modules, RP2040, LoRa, PyQt5, 32 tests, Gobi flight 2023, national second prize | 02, 04 |
| OnesArm | T/N interface, 3! × 2² = 24 layouts, STM32F103/F407, CAN, ~450 mm reach, national first prize 2024 | 02, 04 |
| Sencillo | desktop PCB fabrication, 8/8 mil, 0.8 mm copper rivets, ≤30 min, 50 × 50 mm, all design targets, pre-prototype | 02 |
| Awards | 38th CASTIC first prize 2024 (OnesArm); 37th CASTIC second prize 2023 (DustArrow); Shanghai TV Young Edison S8 2024 | 04 |
| More Work | Huginn, Robusr-skill, Brokkr, Tanngrisnir, Argo, Lynx | 02, projects.json |
| Contact | GitHub, email, Anteportal org only | 01, 06 |

## Rewritten for the page

- Hero intro condensed to roughly 55 words, third person.
- Project summaries follow problem → method → evidence → next step, 2–3 sentences, no more than six tech tags.
- About uses two first-person paragraphs (70–90 words each) derived from the long bio in 01, with no sentence repeated from the hero.
- Journey compressed to exactly six rows, as specified in the brief.
- French and Chinese copy written from the English source, not machine-translated.

## Deliberately excluded

- Family, address, birthday, exam scores, ranking, leave of absence, personal relationships.
- Bilibili, LinkedIn, X, and any unverified account.
- TV stills, competition logos, third-party paper figures, datasheet images.
- The 2026 national innovation project (participant, not lead) and the 2026-07 Ningxia Science Museum appearance (unverified).
- Any claim of a registered company, funding, sponsorship, or official partnership.

## Link checks (2026-10-20)

| URL | HTTP status | Decision |
|---|---|---|
| https://robusr.github.io | 200 | old host; no longer canonical |
| https://robusr.cn | 200 | configured canonical site |
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
| `portrait-robusr.jpg` | 1707×1280, ~200 KB | square crop 512, WebP 29 KB + JPEG 75 KB + 260 px WebP 8.8 KB |
| `vulcan-card.png` | 1200×675 | 960/480 WebP (19/7.8 KB), 960 JPEG 66 KB |
| `hsiwu-card.png` | 1200×675 | 960/480 WebP (33/12 KB), 960 JPEG 81 KB |
| `dustarrow-card.png` | 1200×675 | 960/480 WebP (8.7/3.6 KB), 960 JPEG 38 KB |
| `onesarm-card.jpg` | 1200×675 | 960/480 WebP (30/12 KB), 960 JPEG 91 KB |
| `anteportal-card.png` | 1200×675 | 960/480 WebP (17/8 KB), 960 JPEG 54 KB |
| OG image | generated | 1200×630 PNG, 245 KB |

All source images remain untouched in the info library; only copies were converted.

## Implementation note

The brief's example tree places the app under `site/`. The repository is `Robusr/robusr.github.io`, and production moved to Cloudflare Pages. The Astro app stays at the repository root with `base: /`, which keeps `dist/` publishable as-is. Content data still lives in `src/data/*.json` and is the single source for rendering.
