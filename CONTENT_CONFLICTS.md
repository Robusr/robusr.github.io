# Content conflicts and resolutions

| # | Conflict | Resolution on the site |
|---|---|---|
| 1 | Library warns the organization is `Anteportal`, while some user materials wrote `Anteporta`. | `Anteportal` everywhere; links verified 200. |
| 2 | `projects.json` says Hsiwu has "six independently driven wing segments", but the same file and README describe three motors and three L293D bridges. Six independent drives would need six motors. | Page says "six wing segments, three per side" and "three motors". The word "independently" is dropped. Tagline keeps the brief's "Six wing segments. Three motors. Zero lines of code." |
| 3 | Hsiwu license: README states MIT; GitHub reports NOASSERTION. | Page shows MIT, following the README, which is the project's own statement. |
| 4 | 37th CASTIC second prize: DustArrow README confirms the contest and TV feature but not the prize level; personal materials and search summaries say second prize. | Page uses "Second Prize" as instructed by the brief, and this file records the medium confidence. Verification before a press kit is recommended. |
| 5 | Star counts are live data; the brief fixed 23 (Vulcan) and 8 (Hsiwu) as of 2026-10-20. | Resolved: the page renders stars, forks, last push, and the latest release from `github.json`, then refreshes them from `/api/github`. No count is hard-coded in the copy. |
| 6 | OnesArm reach: 354 mm link-length sum versus about 450 mm reach. | Both describe different quantities; the page uses "~450 mm reach" from the 10,000-sample workspace result and does not present 354 mm as reach. |
| 7 | Brief status vocabulary lists Active / Complete / Archive / Pre-prototype, but OnesArm's data says "v2 current". | Added a fifth label: v2 current / v2 现行 / v2 actuelle. |
| 8 | More Work could include ten secondary repos; the brief capped it at six. | Reduced to four on 2026-11-26 at the owner's request: Huginn, Robusr-skill, Lynx, Gungnir. |
| 9 | `robusr.cn` was suggested as the website but did not resolve on 2026-10-20. | It now resolves through Cloudflare and is the configured canonical host. GitHub Pages is retired from the build configuration. No CNAME file is used. |
| 10 | The brief's example tree nests the app under `site/`, while the repo is the user Pages site. | App lives at repo root; `base` is `/`. Documented in README and DEPLOY.md. |
| 11 | Sencillo is described as "AI × manufacturing / startup" in the library, but the team is not a registered company. | Page category is "AI × manufacturing"; copy says "student-founded team" and never calls it a company. |
| 12 | The earlier brief excluded family details, but the owner supplied an About paragraph naming his father, an art teacher. | The paragraph is included at the owner's request; the README content rule now records this single exception. |
| 13 | The earlier content rule excluded TV stills, but the owner requested a DustArrow launch moment. | One authorized still from the repository's TV clip appears as Fig. 03C; its caption and README credits name Shanghai TV, Young Edison S8. |
| 14 | Sencillo has no public repository; the owner supplied design-target figures and authorized their use without citation. | Fig. 05 uses owner-supplied design-target material; it is labeled "Design-target figures; not measured" and carries no document citation. |
