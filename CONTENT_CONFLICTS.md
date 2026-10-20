# Content conflicts and resolutions

| # | Conflict | Resolution on the site |
|---|---|---|
| 1 | Library warns the organization is `Anteportal`, while some user materials wrote `Anteporta`. | `Anteportal` everywhere; links verified 200. |
| 2 | `projects.json` says Hsiwu has "six independently driven wing segments", but the same file and README describe three motors and three L293D bridges. Six independent drives would need six motors. | Page says "six wing segments, three per side" and "three motors". The word "independently" is dropped. Tagline keeps the brief's "Six wing segments. Three motors. Zero lines of code." |
| 3 | Hsiwu license: README states MIT; GitHub reports NOASSERTION. | Page shows MIT, following the README, which is the project's own statement. |
| 4 | 37th CASTIC second prize: DustArrow README confirms the contest and TV feature but not the prize level; personal materials and search summaries say second prize. | Page uses "Second Prize" as instructed by the brief, and this file records the medium confidence. Verification before a press kit is recommended. |
| 5 | Star counts are live data; the brief fixes 23 (Vulcan) and 8 (Hsiwu) as of 2026-10-20. | Page prints "23 stars (Oct 2026)" and "8 stars (Oct 2026)" with the snapshot date. Live counts may differ. |
| 6 | OnesArm reach: 354 mm link-length sum versus about 450 mm reach. | Both describe different quantities; the page uses "~450 mm reach" from the 10,000-sample workspace result and does not present 354 mm as reach. |
| 7 | Brief status vocabulary lists Active / Complete / Archive / Pre-prototype, but OnesArm's data says "v2 current". | Added a fifth label: v2 current / v2 现行 / v2 actuelle. |
| 8 | More Work could include ten secondary repos; the brief caps it at six. | Six items in the brief's order: Huginn, Robusr-skill, Brokkr, Tanngrisnir, Argo, Lynx. |
| 9 | `robusr.cn` was suggested as the website but did not resolve on 2026-10-20. | It now resolves through Cloudflare and is the configured canonical host. GitHub Pages is retired from the build configuration. No CNAME file is used. |
| 10 | The brief's example tree nests the app under `site/`, while the repo is the user Pages site. | App lives at repo root; `base` is `/`. Documented in README and DEPLOY.md. |
| 11 | Sencillo is described as "AI × manufacturing / startup" in the library, but the team is not a registered company. | Page category is "AI × manufacturing"; copy says "student-founded team" and never calls it a company. |
