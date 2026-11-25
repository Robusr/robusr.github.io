const header = document.querySelector('[data-header]');
if (header) {
  const update = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
  update();
  window.addEventListener('scroll', update, { passive: true });
}

const navLinks = [...document.querySelectorAll('.site-nav a[href^="#"]')];
if (navLinks.length && 'IntersectionObserver' in window) {
  const navTargets = navLinks
    .map((link) => {
      const href = link.getAttribute('href');
      return href ? document.querySelector(href) : null;
    })
    .filter(Boolean);

  if (navTargets.length) {
    const setActive = (id) => {
      navLinks.forEach((link) => {
        const active = link.getAttribute('href') === `#${id}`;
        link.classList.toggle('is-active', active);
        if (active) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    };

    const observer = new IntersectionObserver((entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (visible) setActive(visible.target.id);
    }, { rootMargin: '-30% 0px -55% 0px', threshold: [0, 0.25, 0.5, 1] });

    navTargets.forEach((target) => observer.observe(target));

    const contactLink = navLinks.find((link) => link.getAttribute('href') === '#contact');
    const updateBottom = () => {
      if (!contactLink) return;
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 8) {
        setActive('contact');
      }
    };
    window.addEventListener('scroll', updateBottom, { passive: true });
    updateBottom();
  }
}

const anchorLinks = document.querySelectorAll('a[data-anchor-link]');
if (anchorLinks.length) {
  const syncAnchors = () => {
    const hash = window.location.hash;
    anchorLinks.forEach((link) => {
      const base = link.getAttribute('data-base');
      if (base) link.setAttribute('href', base + hash);
    });
  };
  syncAnchors();
  window.addEventListener('hashchange', syncAnchors);
}

const hint = document.querySelector('[data-lang-hint]');
if (hint) {
  let dismissed = false;
  try { dismissed = sessionStorage.getItem('lang-hint-dismissed') === '1'; } catch (e) {}
  const lang = (navigator.language || '').toLowerCase();
  if (!dismissed && (lang.startsWith('zh') || lang.startsWith('fr'))) hint.hidden = false;
  const close = hint.querySelector('[data-lang-hint-close]');
  if (close) {
    close.addEventListener('click', () => {
      hint.hidden = true;
      try { sessionStorage.setItem('lang-hint-dismissed', '1'); } catch (e) {}
    });
  }
}

const liveRoots = document.querySelectorAll('[data-live-repo]');
if (liveRoots.length) {
  const dateFormat = new Intl.DateTimeFormat(document.documentElement.lang || 'en', {
    dateStyle: 'medium',
    timeZone: 'UTC',
  });
  const releaseNodes = new Map();
  document.querySelectorAll('[data-release-repo]').forEach((node) => {
    releaseNodes.set(node.getAttribute('data-release-repo'), node);
  });

  const apply = (payload) => {
    if (!payload?.repos) return;
    liveRoots.forEach((root) => {
      const repo = root.getAttribute('data-live-repo');
      const stats = payload.repos[repo];
      if (!stats) return;
      root.classList.add('is-live');

      const stars = root.querySelector('[data-live="stars"]');
      if (stars && stats.stars !== undefined) stars.textContent = String(stats.stars);
      const forks = root.querySelector('[data-live="forks"]');
      if (forks && stats.forks !== undefined) forks.textContent = String(stats.forks);

      if (stats.pushedAt) {
        const stamp = root.querySelector('[data-live="pushed"]');
        const date = new Date(stats.pushedAt);
        if (stamp && !Number.isNaN(date.valueOf())) {
          stamp.textContent = dateFormat.format(date);
          stamp.setAttribute('datetime', stats.pushedAt);
        }
      }

      const release = payload.releases?.[repo];
      const releaseNode = releaseNodes.get(repo);
      if (release?.tag && releaseNode) {
        releaseNode.textContent = release.tag;
        if (release.url) releaseNode.setAttribute('href', release.url);
        releaseNode.hidden = false;
      }
    });
  };

  const load = async () => {
    if (navigator.connection?.saveData) return;
    // astro preview serves no Pages Functions; skip the request to keep local QA console-clean.
    const host = window.location.hostname;
    if (host === 'localhost' || host === '127.0.0.1' || host === '::1' || window.location.protocol === 'file:') return;
    const now = Date.now();
    try {
      const cached = JSON.parse(sessionStorage.getItem('github-live-v1') || 'null');
      if (cached && now - cached.at < 300000) {
        apply(cached.payload);
        return;
      }
    } catch (e) {}

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 5000);
    try {
      const response = await fetch('/api/github', {
        signal: controller.signal,
        headers: { Accept: 'application/json' },
      });
      if (!response.ok) return;
      const payload = await response.json();
      apply(payload);
      try { sessionStorage.setItem('github-live-v1', JSON.stringify({ at: now, payload })); } catch (e) {}
    } catch (e) {
      // Keep the build-time snapshot when the endpoint is unavailable.
    } finally {
      clearTimeout(timer);
    }
  };

  const schedule = () => (window.requestIdleCallback
    ? window.requestIdleCallback(load, { timeout: 2500 })
    : setTimeout(load, 1200));
  if (document.readyState === 'complete') schedule();
  else window.addEventListener('load', schedule, { once: true });
}
