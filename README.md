# robusr.github.io

Personal homepage of Robusr Guo (郭沫晗), built with Astro and deployed to GitHub Pages.

Three static pages share one content model:

- `/` — English (default)
- `/zh/` — 简体中文
- `/fr/` — Français

## Stack

- Astro 7, static output, no client framework
- Self-hosted Inter variable font (`@fontsource-variable/inter`), system CJK stack
- One small progressive-enhancement script (header border, anchor-preserving language switch, optional language hint)
- Images pre-converted to WebP with JPEG fallbacks; no third-party CDN, analytics, or embeds

## Local development

Requirements: Node.js >= 22.22 and npm >= 9.6.

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # static output in dist/
npm run preview   # preview the build at http://localhost:4321
```

## Content

All visible copy is data-driven:

- `src/data/profile.json` — identity, positioning, intro, about, links, portrait
- `src/data/projects.json` — five featured projects with `copy` fields per locale
- `src/data/timeline.json`, `src/data/awards.json`, `src/data/more-work.json`
- `src/i18n/en.json`, `zh.json`, `fr.json` — UI labels and meta
- `content/copy-en.md` is the English source of truth; `copy-zh.md` and `copy-fr.md` are translations
- `content/glossary.md` — shared terminology

Sencillo figures are design targets and are labeled as such in the UI. Star counts are snapshots dated October 2026.

## Structure

```text
src/
  components/   Header, Hero, ProjectList, Journey, Awards, MoreWork, About, Footer, LanguageSwitcher
  data/         profile, projects, timeline, awards, more-work
  i18n/         en, zh, fr
  layouts/      Base.astro (head, SEO, JSON-LD)
  pages/        index, zh/index, fr/index, 404
  scripts/      site.js
  styles/       tokens.css, global.css
public/         assets, favicon, og, robots.txt, sitemap.xml
content/        copy-en, copy-zh, copy-fr, glossary
scripts/        make-og.py (regenerates the OG image)
```

## Deployment

See [DEPLOY.md](DEPLOY.md). The GitHub Actions workflow is `.github/workflows/deploy.yml`. Publishing requires pushing to `main` and enabling Pages; neither is done automatically by this branch.

## Verification

See [QA.md](QA.md) for the three-language consistency check, accessibility review, link checks, screenshots, and Lighthouse results.

## Content notes

- [content-inventory.md](content-inventory.md) — audited facts and link checks
- [CONTENT_GAPS.md](CONTENT_GAPS.md) — unresolved items
- [CONTENT_CONFLICTS.md](CONTENT_CONFLICTS.md) — conflicts and their resolutions
