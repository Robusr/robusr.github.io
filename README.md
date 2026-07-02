# Robusr's Utopia

[ [中文](./README.zh-CN.md) ]

A macOS Terminal-style personal homepage that simulates an interactive
shell session.  Visitors can type commands or ask natural-language
questions to learn about me, browse my GitHub projects, and view live
profile statistics -- all inside a frosted-glass terminal window.

![Terminal Screenshot](./assets/img/example.png)

## Features

- **macOS terminal window** with traffic-light title bar, rounded
  corners, and backdrop-blur glassmorphism over a fullscreen background
- **Oh My Zsh style prompt** (`$ ~`) with command history navigable via
  Arrow-Up / Arrow-Down
- **Typewriter-effect responses** -- output is printed character by
  character for a realistic terminal feel
- **ASCII pixel-art logo** rendered in italic with per-letter rainbow
  colours (generated offline via Pillow)
- **Dual-language i18n** -- English by default, toggle to Chinese with
  the `lang` command
- **Live GitHub integration** -- fetches public repository list and
  profile stats from the GitHub API at page load
- **Natural-language matching** -- ask "Who are you?", "What can you
  do?", or "Show me your projects" in either English or Chinese
- **Responsive layout** -- adapts to mobile viewports with smaller
  fonts and tighter margins
- **Single static site** -- no framework, no bundler, no external
  dependencies at runtime

## Commands

| Command | Aliases | Description |
|---|---|---|
| `help` | `h`, `?` | Show the full command list |
| `about` | `whoami` | Display personal bio |
| `skills` | `skill` | List technical skills |
| `contact` | -- | Show email, GitHub, and WeChat |
| `projects` | `project`, `portfolio` | List public GitHub repositories (live) |
| `stats` | `status` | Show GitHub profile overview (live) |
| `lang` | `zh`, `en` | Toggle between English and Chinese |
| `clear` | `cls` | Clear the terminal screen |

You can also ask questions naturally (e.g. "What can you do?",
"Who are you?", "How to reach you?").

## Project Structure

```
.
├── index.html              # HTML skeleton (38 lines)
├── css/
│   └── style.css           # All styles (221 lines)
├── js/
│   └── main.js             # Terminal engine, i18n, commands (677 lines)
├── assets/
│   └── img/
│       ├── Street.jpg      # Fullscreen background
│       ├── Robusr.jpeg     # Favicon
│       └── example.png     # README screenshot
├── scripts/
│   └── ascii_gen.py        # Offline ASCII logo generator (Pillow)
├── .gitignore
└── README.md
```

## Customisation

### Personal Info

Edit the `personalInfo` object at the top of [js/main.js](js/main.js):

```javascript
const personalInfo = {
  name:    'YourName',
  tagline: { en: "...", zh: "..." },
  bio:     { en: "...", zh: "..." },
  skills:  { en: [...], zh: [...] },
  contact: { email: '...', github: '...', wechat: '...' },
};
```

### ASCII Logo

The pixel-art logo is pre-computed and stored as a `LOGO_UP` constant.
To regenerate it after changing the text, run:

```bash
python3 scripts/ascii_gen.py "YourName"
```

Then copy the printed `LOGO_UP` / `LOGO_UP_SPLITS` / `LOGO_COLORS`
blocks into [js/main.js](js/main.js).

Requirements: Python 3 with [Pillow](https://python-pillow.org/)
(`pip install Pillow`).

### Background Image

Replace `assets/img/Street.jpg` with your own image.  Update the URL in
[css/style.css](css/style.css) (`.bg` rule) if you change the filename.

## Deployment

This site is designed for **GitHub Pages**.  Push the repository to
`<username>.github.io` and enable Pages in the repository settings
(root directory, main branch).  No build step is required.

For other static hosts (Netlify, Vercel, Cloudflare Pages), point the
deploy directory at the repository root.

## Tech Stack

| Layer | Technology |
|---|---|
| Markup | HTML5 |
| Styling | CSS3 (Flexbox, backdrop-filter, custom scrollbars) |
| Logic | Vanilla JavaScript (ES2020+) |
| Font | Fira Code / Menlo / Consolas / SF Mono (system stack) |
| API | GitHub REST API (unauthenticated, public data) |
| Logo gen | Python 3 + Pillow (offline) |

## License

This project is for personal use.  Feel free to adapt it for your own
homepage.
