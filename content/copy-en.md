# English copy — source of truth

Snapshot: 2026-10-20. Sources: `01-identity-and-bio.md`, `02-project-cards.md`, `03-timeline.md`, `04-awards-and-media.md`, `data/profile.json`, `data/projects.json`, `sources.md`. English is the source language; Chinese and French are translations of this file.

## Meta

- Title: `Robusr Guo — AI × Engineering Builder`
- Description: `Robusr Guo is a robotics engineering student at HUST building AI tools for CAD and manufacturing, bio-inspired robots, sounding rockets, and modular robotic arms.`

## Header

- Site name: Robusr Guo
- Navigation: Work · Journey · About · Contact
- Language: English (current) · 中文 · Français

## Hero

- Label: Robotics Engineering · HUST
- Name: Robusr Guo
- Positioning: AI × Engineering builder. I turn real-world problems into working hardware, then use AI to compress the distance from idea to part.
- Intro: Robusr Guo studies in the Robotics Engineering Innovation Experimental Class at Huazhong University of Science and Technology. He started with Arduino in sixth grade in Guyuan, Ningxia, and has built a sounding rocket, a modular robotic arm, and a bat-inspired flapping-wing robot. He now builds AI tools for engineering: Vulcan turns natural language into editable SolidWorks features, and Sencillo aims to put PCB fabrication on a desk.
- Status: Currently: Vulcan · Sencillo · HUST Robotics.
- Links: GitHub · Email · Anteportal Labs
- Portrait alt: Robusr Guo at the beach

<!-- Sources: 01-identity-and-bio.md (short bio), 5.1 positioning sentence; data/profile.json. -->

## Selected Work

### 01 · Vulcan — AI × CAD — Active

- Tagline: Natural language in. Parametric SolidWorks geometry out.
- Summary: A SolidWorks add-in that turns a plain engineering request into native, editable features. The model returns a typed JSON feature tree, and a C# client executes it through the SolidWorks COM API. No exec(), no code-generation surface.
- Tech: C# · WPF · .NET 4.8 · Python · Flask · SolidWorks COM API · LLM
- Evidence: 23 stars (Oct 2026) · GPL-3.0 · Typed JSON contract
- Exit: Repository → `https://github.com/Robusr/Vulcan`

<!-- Sources: 02-project-cards.md card 1; projects.json. Star snapshot 2026-10-20. -->

### 02 · Hsiwu — Bio-inspired robotics — Complete

- Tagline: Six wing segments. Three motors. Zero lines of code.
- Summary: A bat-inspired flapping-wing robot with six wing segments, three per side. Three NE555 oscillators, one 74HC04 inverter, and three L293D bridges form the entire control law. No MCU, no firmware.
- Tech: SolidWorks · Altium · NE555 · 74HC04 · L293D · FDM
- Evidence: 8 stars (Oct 2026) · MIT · Gerber, BOM, and STEP included
- Exit: Repository → `https://github.com/Robusr/Hsiwu`

<!-- Sources: 02-project-cards.md card 2; Hsiwu README. "Six independently driven wing segments" in projects.json conflicts with three motors; this copy avoids the independence claim. See CONTENT_CONFLICTS.md. -->

### 03 · DustArrow X — Aerospace / embedded — Archive

- Tagline: A sounding rocket for the sandstorms back home.
- Summary: A 40 mm modular meteorological sounding rocket with 10 bays and 9 PCB modules. An RP2040 sensing stack, a LoRa downlink, and a PyQt5 ground station measure the vertical structure of the atmosphere during dust events.
- Tech: RP2040 · LoRa · PyQt5 · SolidWorks · EasyEDA · CFD
- Evidence: 37th CASTIC second prize · 32 tests passed · Gobi flight, 2023
- Exit: Repository → `https://github.com/Robusr/DustArrow`

<!-- Sources: 02-project-cards.md card 3; DustArrow README; 04-awards-and-media.md. Team project from Guyuan No. 1 Middle School; the page does not claim sole authorship. -->

### 04 · OnesArm — Modular robotics — v2 current

- Tagline: One arm. Twenty-four configurations.
- Summary: A modular serial robotic arm with a T/N mortise-and-tenon interface. Three interchangeable modules produce 3! × 2² = 24 layouts. The v2 platform uses stepper/CAN joints, 5 mm 5052 aluminium links, and carbon tubes.
- Tech: SolidWorks · STM32 · CAN · MATLAB · FEA
- Evidence: 38th CASTIC first prize · 24 layouts modelled · ~450 mm reach
- Exit: Repository → `https://github.com/Robusr/OnesArm`

<!-- Sources: 02-project-cards.md card 4; OnesArm README. -->

### 05 · Anteportal Labs · Sencillo — AI × manufacturing — Pre-prototype

- Tagline: From vibe coding to vibe making.
- Summary: A desktop PCB fabrication center from Anteportal Labs, a student-founded team. It combines dry isolation milling with in-machine copper-rivet vias. All performance figures are design targets; the project is pre-prototype as of October 2026.
- Tech: CAM · CNC isolation milling · Copper rivet vias · Constrained generation · Offline
- Evidence flag: Design target, not measured
- Evidence: 8/8 mil traces · 0.8 mm copper-rivet vias · ≤30 min per board
- Exit: Organization → `https://github.com/Anteportal`

<!-- Sources: 02-project-cards.md card 5; Anteportal profile README. Design targets only. Student-founded team, not a registered company. -->

## Journey

- 2018 — Started with Arduino in sixth grade; turned his bedroom into an electronics workshop.
- 2019–2022 — Built an ultrasonic rangefinder, a writing robot, an RFID cabinet lock, an indoor environment monitor, and a Raspberry Pi website.
- 2023 — DustArrow: from a solid-rocket thrust logger to a full sounding rocket, avionics, telemetry, and a Gobi flight test.
- 2023 — 37th China Adolescents Science and Technology Innovation Contest, Second Prize.
- 2024 — 38th CASTIC, First Prize for OnesArm; featured on Shanghai TV’s Young Edison.
- 2025–2026 — Entered HUST’s Robotics Engineering Innovation Experimental Class; open-sourced Vulcan and Hsiwu; founded Anteportal Labs and started Sencillo.

<!-- Sources: 03-timeline.md one-page version; 04-awards-and-media.md. -->

## Awards & Media

- 2024 — First Prize, 38th China Adolescents Science and Technology Innovation Contest (CASTIC) — OnesArm
- 2023 — Second Prize, 37th CASTIC — DustArrow X
- 2024 — Shanghai TV, Young Edison, Season 8 (2024) — watch the feature: `https://www.kankanews.com/detail/LMwVGm9WB2z`

<!-- Sources: 04-awards-and-media.md. CASTIC spelled out at first occurrence. No competition logos or TV stills. -->

## More Work

- Huginn — AI agent for automated data statistics and analysis — Python — `https://github.com/Robusr/Huginn`
- Robusr-skill — A digital twin skill distilled from personal memory and persona — Agent skills — `https://github.com/Robusr/Robusr-skill`
- Brokkr — Dexterous hand with real-time hand posture recognition and motion control — Hardware / vision — `https://github.com/Robusr/Brokkr`
- Tanngrisnir — Two-wheeled self-balancing vehicle based on STM32F103C8T6 — C / embedded — `https://github.com/Robusr/Tanngrisnir`
- Argo — Quantitative Engineering Design Methods course design — MATLAB — `https://github.com/Robusr/Argo`
- Lynx — Perception fusion SDK for low-speed autonomous vehicles — Python — `https://github.com/Robusr/Lynx`

<!-- Sources: 02-project-cards.md "More work"; projects.json secondary. Six items, as specified in the brief. -->

## About

I grew up in Guyuan, Ningxia, where sandstorms can drop visibility below 5 meters. That is why my first serious project was a sounding rocket rather than a web app: I wanted to measure the atmosphere I could not see through. DustArrow grew from a thrust logger into a modular rocket with 10 bays, 9 PCB modules, and a ground station. The question was always the same: what is actually happening up there?

At HUST I moved upstream. Vulcan turns a sentence into a feature tree a mechanical engineer can keep editing. Sencillo tries to put a PCB fabrication center on a desk. The through-line is the same: find a problem I have seen, build the machine, then build the tool that lets the next person build it faster. The tools are the projects I want to leave behind.

<!-- Sources: 01-identity-and-bio.md long bio; appendix A seed copy, revised to remove repetition with the hero. -->

## Footer

- Contact: Robusr@outlook.com · github.com/Robusr · github.com/Anteportal
- Location: Wuhan, China
- Last updated: October 2026
- Language: English (current) · 中文 · Français
- Signature: Why not?

<!-- Sources: 04-awards-and-media.md; data/profile.json. No private information. -->
