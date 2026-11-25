# robusr.cn

**Site personnel de Robusr Guo (郭沫晗)** : étudiant en génie robotique à HUST, il transforme des problèmes réels en matériel fonctionnel, puis construit des outils d'IA qui réduisent la distance entre une idée et une pièce.

[English](README.md) · [简体中文](README.zh.md) · **Français**

> Cinq projets sélectionnés, un parcours en six lignes, des prix et de la presse, et un court texte sur le passage de la fabrication de machines à celle d'outils.

![Homepage preview](public/og/og-default-v2.png)

| | |
|---|---|
| **Site en ligne** | <https://robusr.cn> |
| **Hébergement** | Cloudflare Pages, déploiement depuis `main` |
| **Stack** | Astro 7, sortie statique, sans framework client |
| **Langues** | English `/`, 简体中文 `/zh/`, Français `/fr/` |
| **Design** | mise en page éditoriale sur une colonne, 880 px maximum, une seule couleur d'accent bleu-vert profond |
| **Contrôles** | `npm run verify`, synchronisation GitHub au build, Playwright, Lighthouse |

---

## Pages du site

| Route | Langue | Notes |
|---|---|---|
| `/` | English | Entrée par défaut, `x-default` |
| `/zh/` | 简体中文 | `lang="zh-Hans"` |
| `/fr/` | Français | `lang="fr"` |
| `/404.html` | English | `noindex`, liens vers les trois langues |

Toutes les versions partagent le même modèle de contenu et le même ordre de sections. Avec JavaScript, le changement de langue conserve l'ancre courante. Aucune redirection automatique selon la langue du navigateur.

## Contenu de la page

- **Travaux sélectionnés :** Vulcan, Hsiwu, DustArrow X, OnesArm et Anteportal Labs · Sencillo, dans cet ordre fixe. Les cartes de dépôt affichent en direct les étoiles, les forks, le dernier push et la dernière version publiée sur GitHub, avec un instantané de build en secours sans JavaScript.
- **Parcours :** six lignes, d'Arduino en 2018 à HUST et Anteportal Labs en 2026.
- **Prix et presse :** premier prix du 38e CASTIC, deuxième prix du 37e CASTIC et le reportage *Young Edison* de la télévision de Shanghai.
- **Autres projets :** huit dépôts, une ligne chacun.
- **À propos :** deux paragraphes sur les tempêtes de sable de Guyuan et le passage en amont vers des outils d'IA pour la CAO et la fabrication.
- **Contact :** e-mail, GitHub, Anteportal Labs, localisation, liens de langue et signature.
- **Arrière-plan :** deux illustrations au trait de l'IP personnelle, un portrait collage en bas à droite et une silhouette debout en bas à gauche, sur un fond papier chaud avec une fine trame de points dans les marges. La silhouette apparaît à partir de 1200 px ; le mobile utilise une version 480 px du portrait.

## Pile technique

| Domaine | Choix |
|---|---|
| Framework | Astro 7, sortie statique, sans framework client |
| Styles | propriétés CSS natives, sans framework utilitaire |
| Typographie | Inter variable auto-hébergée, pile système pour le chinois |
| Images | projets en 480 et 960 px, portrait en 260 et 512 px, deux illustrations IP transparentes dimensionnées pour leur emplacement ; WebP, avec un fallback JPEG pour le portrait |
| JavaScript | environ 2,3 Ko d'amélioration progressive |
| Données GitHub | instantané produit au build depuis l'API GitHub ; rafraîchissement `/api/github` mis en cache en périphérie par une Cloudflare Pages Function |
| Confidentialité | aucune analyse, cookie, police tierce ou intégration ; les requêtes GitHub partent de Cloudflare, pas du navigateur du visiteur |
| Déploiement | Cloudflare Pages et Pages Functions, intégration Git, Node 22 |
| CI | GitHub Actions exécute `npm run verify` sur les push et les pull requests |

## Développement local

Prérequis : Node.js 22.12 ou plus récent, npm 9.6 ou plus récent.

```bash
npm ci
npm run dev       # http://localhost:4321
npm run build     # synchronise GitHub puis produit dist/
npm run preview   # prévisualiser dist/
npm run check     # cohérence du contenu, des langues, des ressources et de l'instantané GitHub
npm run sync:github # rafraîchir l'instantané GitHub versionné
npm run typecheck # astro check
npm run verify    # check + typecheck + build
```

`npm run verify` synchronise l'instantané GitHub, puis enchaîne le contrôle du contenu, le contrôle de types et le build ; le build rafraîchit à nouveau l'instantané et produit quatre pages HTML. `dist/` est ignoré par Git et reconstruit en CI. Si GitHub est injoignable, `npm run sync:github` et `npm run build` conservent l'instantané existant ; définir `GITHUB_TOKEN` augmente la limite de l'API. `/api/github` est servi par Cloudflare Pages Functions et n'existe pas dans `astro preview` ; la page utilise alors l'instantané.

## Modèle de contenu

Tous les textes visibles sont pilotés par les données.

| Chemin | Rôle |
|---|---|
| `src/data/profile.json` | nom, positionnement, introduction, statut, liens, portrait, paragraphes À propos |
| `src/data/projects.json` | cinq projets phares avec textes par langue, technologies, preuves et statut |
| `src/data/timeline.json` | six lignes de parcours |
| `src/data/awards.json` | trois prix et mentions presse |
| `src/data/more-work.json` | huit projets secondaires |
| `src/data/github.json` | instantané généré : étoiles, forks, dernier push et dernière version de chaque dépôt suivi |
| `src/i18n/en.json`, `zh.json`, `fr.json` | libellés d'interface, titres meta et descriptions |
| `content/copy-en.md` | manuscrit source en anglais |
| `content/copy-zh.md`, `copy-fr.md` | traductions chinoise et française |
| `content/glossary.md` | terminologie partagée |

L'anglais est la source de vérité. Pour modifier le contenu :

1. Modifier ensemble le manuscrit anglais et `src/data`.
2. Mettre à jour les champs chinois et français dans le même commit.
3. Garder les mêmes nombres de sections, chiffres, liens et chemins d'images dans les trois langues.
4. Lancer `npm run sync:github` après avoir ajouté, renommé ou retiré un dépôt suivi.
5. Lancer `npm run verify` et vérifier les trois routes.

`src/data/github.json` est généré ; ne pas le modifier à la main. `npm run sync:github` lit les liens des projets phares et des autres projets, puis enregistre étoiles, forks, dernier push et dernière version. Le hook `prebuild` le rafraîchit avant chaque build et conserve l'ancien fichier si GitHub est injoignable.

## Structure du projet

```text
.
├── src/
│   ├── components/   Header, Hero, ProjectList, Journey, Awards, MoreWork, About, Footer, LanguageSwitcher
│   ├── data/         profile, projects, timeline, awards, more-work, instantané GitHub
│   ├── i18n/         en, zh, fr et types partagés
│   ├── layouts/      Base.astro : head, hreflang et JSON-LD
│   ├── pages/        index, zh/index, fr/index, 404, sitemap.xml, robots.txt
│   ├── scripts/      amélioration progressive et rafraîchissement GitHub
│   └── styles/       tokens.css, global.css
├── functions/        Cloudflare Pages Function pour /api/github
├── public/           images, illustrations IP, favicon, image OG, _headers, _redirects
├── content/          manuscrits et glossaire
├── scripts/          contrôle du contenu, synchronisation GitHub, générateurs OG et IP, scripts QA
├── qa/               rapports Lighthouse, cohérence et mise en page
├── screenshots/      captures pleine page à 1440, 1024, 768 et 390 px
├── Robusr IP/        scans sources des illustrations de fond
├── .github/          workflow de vérification
└── .nvmrc            version de Node pour les builds locaux
```

## Vérification

| Contrôle | Résultat |
|---|---|
| Build et contrôles | `npm run verify` passe : contenu, `astro check` sans erreur, 4 pages |
| Synchronisation GitHub | l'instantané couvre 12 dépôts ; Vulcan résout v1.3.0 ; le test local du gestionnaire `/api/github` a renvoyé 24 dépôts publics et la version Vulcan ; un point d'accès simulé a mis la carte à 99 étoiles et v9.9.9 dans un contrôle Playwright le 2026-11-26 |
| Production | `/`, `/zh/`, `/fr/` renvoient 200 ; HTTP redirige vers HTTPS ; `www` renvoie 200 et attend encore un 301 |
| Lighthouse mobile, aperçu local (2026-10-22) | Performance 99, Accessibilité 100, Best Practices 100, SEO 100 dans les trois langues |
| Lighthouse mobile, production (2026-10-22) | EN 97/100/92/100, ZH 98/100/92/100, FR 99/100/92/100 |
| LCP / CLS, production | LCP 1,8–2,2 s ; CLS 0–0,069, mesuré avant le correctif `aspect-ratio` du portrait |
| Largeurs de mise en page | 1440, 1024, 768 et 390 px, sans débordement horizontal |
| JavaScript désactivé | tout le contenu reste lisible ; les cartes GitHub utilisent l'instantané |
| Liens externes | GitHub et les liens presse renvoient 200 |

Les chiffres Lighthouse précèdent le module GitHub en direct et doivent être remesurés pour ce build. Best Practices vaut 92 en production parce que Cloudflare injecte encore le beacon Web Analytics et que la CSP le bloque. Email Address Obfuscation et Managed robots.txt restent aussi appliqués en périphérie : la page en ligne diffère donc du build local. Ces réglages appartiennent à la zone, pas au dépôt. Résultats en ligne dans `qa/lighthouse-live-summary.json`.

Preuves complètes : [QA.md](QA.md). Captures : [screenshots/](screenshots/). Rapports Lighthouse bruts : [qa/](qa/).

Les scripts QA utilisent Playwright, à installer séparément avec `npm install --no-save playwright@1.64.1`. L'image OG se régénère avec `python3 scripts/make-og.py` ; les illustrations de fond se régénèrent depuis `Robusr IP/` avec `python3 scripts/make-ip-assets.py`. Les deux générateurs nécessitent Pillow.

## Déploiement

Le site est hébergé sur Cloudflare Pages : <https://robusr.cn>. Le projet se construit avec `npm run build` et publie `dist/`. `astro.config.mjs` définit le site canonique ; les URL canoniques, hreflang, Open Graph, JSON-LD, `sitemap.xml` et `robots.txt` en dérivent.

1. Connecter le dépôt à Cloudflare Pages.
2. Définir `npm run build`, `dist` et `NODE_VERSION=22`.
3. Ajouter `robusr.cn` comme domaine personnalisé et activer HTTPS.
4. Pousser sur `main` ; Cloudflare Pages reconstruit automatiquement.

Cloudflare Pages déploie le dossier `functions/` avec `dist/`, donc `/api/github` ne nécessite pas de Worker séparé. La fonction lit les métadonnées publiques des dépôts avec un cache de périphérie de 10 minutes ; définir éventuellement `GITHUB_TOKEN` pour augmenter la limite de GitHub. Sans Functions, ou en cas d'échec, la page conserve l'instantané de build.

`public/_headers` ajoute les en-têtes de sécurité et de cache. Cloudflare Pages ne peut pas rediriger par hôte depuis `_redirects` ; le fichier ne fait que documenter cette limite. `www.robusr.cn` répond actuellement en 200 ; une Redirect Rule doit le renvoyer en 301 vers l'apex. GitHub Pages est retiré ; désactiver le site dans les réglages du dépôt s'il est encore activé. Voir [DEPLOY.md](DEPLOY.md).

## Règles de contenu

- Les ressources sous `/assets/` et `/og/` sont mises en cache un an. En cas de modification d'image, écrire un nouveau nom de fichier et mettre à jour toutes les références.
- Chaque chiffre, prix, lien et statut de projet doit remonter à la bibliothèque d'information ou à une source publique.
- Les chiffres de Sencillo sont des objectifs de conception et doivent rester signalés comme tels.
- Les étoiles et les forks se rafraîchissent au build et via `/api/github` ; l'instantané de `src/data/github.json` sert de secours sans JavaScript. Ne pas le modifier à la main ; lancer `npm run sync:github`.
- Quand le contenu visible change, mettre à jour `contentDate` dans `src/data/profile.json` ; `sitemap.xml` l'utilise comme `lastmod`.
- Lancer `npm run verify` avant de pousser. GitHub Actions exécute la même commande.
- Ne pas ajouter de détails familiaux, d'adresse, de date de naissance, de notes, de classement ou de relations privées.
- Ne pas utiliser d'images de télévision, de logos de concours, de figures d'articles tiers ou de comptes non vérifiés.

## Documentation du projet

| Document | Rôle |
|---|---|
| [DELIVERY.md](DELIVERY.md) | rapport de livraison en chinois |
| [DEPLOY.md](DEPLOY.md) | Cloudflare Pages, domaine, DNS, HTTPS et retour arrière |
| [QA.md](QA.md) | cohérence, accessibilité, liens, Lighthouse et preuves de production |
| [content-inventory.md](content-inventory.md) | faits audités et vérification des liens |
| [CONTENT_GAPS.md](CONTENT_GAPS.md) | lacunes de contenu non résolues |
| [CONTENT_CONFLICTS.md](CONTENT_CONFLICTS.md) | conflits et résolutions |

## Crédits

Le portrait et les deux illustrations au trait de l'IP personnelle sont fournis par Robusr. Les deux dessins servent d'arrière-plan à faible opacité. Les images de projets viennent des dépôts de chaque projet et de la page de l'organisation Anteportal Labs. Le site n'utilise pas d'images de télévision, de logos de concours ni de figures d'articles tiers. Les étoiles, forks, dates de dernier push et versions GitHub proviennent de l'API publique GitHub et sont mis en cache en périphérie.
