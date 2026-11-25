# Texte français

Instantané : 2026-11-26. Traduction de `content/copy-en.md`, qui reste la source de vérité. Sources : `01-identity-and-bio.md`, `02-project-cards.md`, `03-timeline.md`, `04-awards-and-media.md`, `data/profile.json`, `data/projects.json`.

## Meta

- Titre : `Robusr Guo — Bâtisseur IA × ingénierie`
- Description : `Robusr Guo est étudiant en génie robotique à HUST. Il conçoit des outils d’IA pour la CAO et la fabrication, des robots bio-inspirés, des fusées-sondes et des bras robotiques modulaires.`

## En-tête

- Nom du site : Robusr Guo
- Navigation : Travaux · Parcours · À propos · Contact
- Langue : English · 中文 · Français (actuelle)

## Hero

- Sur-titre : Génie robotique · HUST
- Nom : Robusr Guo
- Accroche : Bâtisseur IA × ingénierie. Je transforme des problèmes réels en matériel fonctionnel, puis j’utilise l’IA pour réduire la distance entre une idée et une pièce.
- Présentation : Robusr Guo, geek de chambre depuis dix ans, est étudiant dans la classe expérimentale d’innovation en génie robotique de l’Université des sciences et technologies de Huazhong (HUST). À 13 ans, il a transformé sa chambre en atelier de mécatronique.
- Statut : Actuellement : Vulcan · Sencillo · HUST Robotics.
- Liens : GitHub · E-mail · Anteportal Labs
- Alt du portrait : Robusr Guo sous un ginkgo en automne

## Travaux sélectionnés

<!-- Les étoiles, forks, dernier push et dernière version GitHub sont rendus depuis src/data/github.json et rafraîchis par /api/github ; le manuscrit ne fixe pas les compteurs. -->

### 01 · Vulcan — IA × CAO — Actif

- Accroche : Langage naturel en entrée. Géométrie paramétrique SolidWorks en sortie.
- Résumé : Un module complémentaire pour SolidWorks qui transforme une demande d’ingénierie en fonctions natives et modifiables. Le modèle renvoie un arbre de fonctions JSON typé, et un client C# l’exécute via l’API COM de SolidWorks. Pas d’exec(), pas de surface de génération de code.
- Technologies : C# · WPF · .NET 4.8 · Python · Flask · SolidWorks COM API · LLM
- Preuve : GPL-3.0 · contrat JSON typé
- Version : v1.3.0
- Sortie : Dépôt → `https://github.com/Robusr/Vulcan`

### 02 · Hsiwu — Robotique bio-inspirée — Terminé

- Accroche : Six segments d’aile. Trois moteurs. Zéro ligne de code.
- Résumé : Un robot à ailes battantes inspiré de la chauve-souris, avec six segments d’aile, trois par côté. Trois oscillateurs NE555, un inverseur 74HC04 et trois ponts L293D forment toute la loi de commande. Pas de MCU, pas de firmware.
- Technologies : SolidWorks · Altium · NE555 · 74HC04 · L293D · FDM
- Preuve : MIT · Gerber, BOM et STEP inclus
- Sortie : Dépôt → `https://github.com/Robusr/Hsiwu`

### 03 · DustArrow X — Aérospatial / embarqué — Archivé

- Accroche : Une fusée-sonde pour les tempêtes de sable de chez moi.
- Résumé : Une fusée-sonde météorologique modulaire de 40 mm, avec 10 compartiments et 9 modules PCB. Une pile de capteurs RP2040, une liaison descendante LoRa et une station sol PyQt5 mesurent la structure verticale de l’atmosphère pendant les épisodes de poussière.
- Technologies : RP2040 · LoRa · PyQt5 · SolidWorks · EasyEDA · CFD
- Preuve : 2e prix du 37e CASTIC · 32 tests réussis · vol dans le Gobi, 2023
- Sortie : Dépôt → `https://github.com/Robusr/DustArrow`

### 04 · OnesArm — Robotique modulaire — v2 actuelle

- Accroche : Un bras. Vingt-quatre configurations.
- Résumé : Un bras robotique série modulaire doté d’une interface à tenon et mortaise T/N. Trois modules interchangeables produisent 3! × 2² = 24 configurations. La plateforme v2 utilise des articulations pas-à-pas/CAN, des liens en aluminium 5052 de 5 mm et des tubes en carbone.
- Technologies : SolidWorks · STM32 · CAN · MATLAB · FEA
- Preuve : 1er prix du 38e CASTIC · 24 configurations modélisées · portée d’environ 450 mm
- Sortie : Dépôt → `https://github.com/Robusr/OnesArm`

### 05 · Anteportal Labs · Sencillo — IA × fabrication — Pré-prototype

- Accroche : Du vibe coding au vibe making.
- Résumé : Un centre de fabrication de PCB de bureau développé par Anteportal Labs, une équipe fondée par des étudiants. Il associe fraisage sec par isolation et vias à rivets de cuivre intégrés à la machine. Tous les chiffres de performance sont des objectifs de conception ; le projet est au stade de pré-prototype en octobre 2026.
- Technologies : CAM · CNC isolation milling · Copper rivet vias · Constrained generation · Offline
- Mention de preuve : Objectif de conception, non mesuré
- Preuve : pistes 8/8 mil · vias à rivets de cuivre de 0,8 mm · ≤ 30 min par carte
- Sortie : Organisation → `https://github.com/Anteportal`

## Parcours

- 2018 — À 13 ans, il a transformé sa chambre en atelier de mécatronique.
- 2019–2022 — A construit un télémètre à ultrasons, un robot écrivain, une serrure RFID, une station de mesure d’ambiance et un site hébergé sur Raspberry Pi.
- 2023 — DustArrow : d’un enregistreur de poussée à une fusée-sonde complète, avec avionique, télémétrie et essai en vol dans le Gobi.
- 2023 — 2e prix du 37e Concours national chinois d’innovation scientifique et technologique pour les adolescents.
- 2024 — 1er prix du 38e CASTIC pour OnesArm ; portrait dans l’émission Young Edison de la télévision de Shanghai.
- 2026 — Entrée dans la classe expérimentale d’innovation en génie robotique de HUST.

## Prix et presse

- 2024 — Premier prix, 38e Concours national chinois d’innovation scientifique et technologique pour les adolescents (CASTIC) — OnesArm
- 2023 — Deuxième prix, 37e CASTIC — DustArrow X
- 2024 — Télévision de Shanghai, Young Edison, saison 8 (2024) — regarder le reportage : `https://www.kankanews.com/detail/LMwVGm9WB2z`

## Autres projets

- Huginn — Agent IA pour l’analyse et la statistique automatisées de données — Python — `https://github.com/Robusr/Huginn`
- Robusr-skill — Compétence de jumeau numérique distillée de la mémoire et de la personnalité — Compétences d’agent — `https://github.com/Robusr/Robusr-skill`
- Lynx — SDK de fusion perceptive pour véhicules autonomes à basse vitesse — Python — `https://github.com/Robusr/Lynx`
- Gungnir — Copilote IA pour la simulation de guerre commerciale : moteur déterministe de trésorerie et couche de stratégie LLM — Python · LLM — `https://github.com/Robusr/Gungnir`

<!-- Sources : 02-project-cards.md « More work » ; projects.json secondary ; profil GitHub au 2026-11-26. Quatre éléments choisis par l’auteur. -->

## À propos

L’hiver de mes 17 ans, des camarades passionnés de moteurs à propergol haute énergie m’ont demandé de leur construire un banc d’essai simple pour acquérir la poussée et un système d’allumage à distance. Au moment où j’ai appuyé sur le bouton et où le propergol au sucre s’est enflammé en jaillissant, j’ai eu l’impression d’être Homer dans October Sky, rompant avec les traditions et la stabilité de Coalwood : dans cette ville si petite qu’il n’en restait que le nom, j’ai décidé de construire des fusées. Mon père est professeur d’art ; la lampe sur pied dont il se servait pour peindre de longs rouleaux de paysage a été installée dans ma chambre. Du calcul quantitatif de la courbe de von Kármán sous MATLAB et de l’analyse qualitative CFD d’un modèle idéal, à la topologie d’assemblage des PCB du corps de fusée modulaire et aux tests de perte de trames LoRa, chaque raidisseur et chaque amplificateur opérationnel en ingénierie système est un point concret où la théorie abstraite devient ingénierie. De l’intention à la forme, c’est comme les tons d’encre brûlée, dense, lourde, pâle et claire sous le pinceau de mon père : un paysage d’un seul geste, qui donne un sens à mon exploration.

<!-- Sources : texte chinois fourni par Robusr le 2026-11-26 ; l’anglais et le français sont des traductions. -->

## Pied de page

- Contact : Robusr@outlook.com · github.com/Robusr · github.com/Anteportal
- Lieu : Wuhan, Chine
- Dernière mise à jour : novembre 2026
- Langue : English · 中文 · Français (actuelle)
- Signature : Why not?
