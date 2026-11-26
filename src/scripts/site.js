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

/* Plate carousel: one panel at a time, snap points, pager sync. */
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const plateCarousels = [...document.querySelectorAll('[data-plate-carousel]')];
plateCarousels.forEach((carousel) => {
  const plate = carousel.closest('.project-plate');
  if (!plate) return;
  const panels = [...carousel.querySelectorAll('.plate-panel')];
  const tabs = [...plate.querySelectorAll('[data-plate-tab]')];
  if (!panels.length || !tabs.length) return;

  const setActive = (index) => {
    const active = Math.max(0, Math.min(panels.length - 1, index));
    tabs.forEach((tab, i) => {
      tab.classList.toggle('is-active', i === active);
      if (i === active) tab.setAttribute('aria-current', 'true');
      else tab.removeAttribute('aria-current');
    });
  };

  carousel.addEventListener('scroll', () => {
    const width = carousel.clientWidth;
    if (!width) return;
    setActive(Math.round(carousel.scrollLeft / width));
  }, { passive: true });

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', (event) => {
      event.preventDefault();
      carousel.scrollTo({
        left: index * carousel.clientWidth,
        behavior: reduceMotion.matches ? 'auto' : 'smooth',
      });
    });
  });
});

/* Silent, looping plate videos: play only in view, and only when motion is on. */
const plateVideos = [...document.querySelectorAll('video[data-plate-video]')];
const motionButtons = [...document.querySelectorAll('[data-plate-motion]')];
if (plateVideos.length) {
  let playing = !reduceMotion.matches;
  const setVideo = (video, on) => {
    if (on) {
      const promise = video.play();
      if (promise) promise.catch(() => {});
    } else {
      video.pause();
    }
  };
  const visible = new Map();
  const syncButtons = () => motionButtons.forEach((button) => {
    button.hidden = false;
    button.textContent = playing ? button.dataset.pauseLabel : button.dataset.playLabel;
  });

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        visible.set(entry.target, entry.isIntersecting);
        setVideo(entry.target, playing && entry.isIntersecting);
      });
    }, { threshold: 0.55 });
    plateVideos.forEach((video) => observer.observe(video));
  } else {
    plateVideos.forEach((video) => setVideo(video, playing));
  }

  motionButtons.forEach((button) => {
    button.addEventListener('click', () => {
      playing = !playing;
      plateVideos.forEach((video) => setVideo(video, playing && (visible.get(video) ?? true)));
      syncButtons();
    });
  });

  reduceMotion.addEventListener?.('change', () => {
    if (reduceMotion.matches) {
      playing = false;
      plateVideos.forEach((video) => video.pause());
      syncButtons();
    }
  });
  syncButtons();
}

/* Plate lightbox: native <dialog>, with image/video and caption. */
const plateDialog = document.querySelector('[data-plate-dialog]');
if (plateDialog && typeof plateDialog.showModal === 'function') {
  const dialogMedia = plateDialog.querySelector('[data-dialog-media]');
  const dialogTitle = plateDialog.querySelector('[data-dialog-title]');
  const dialogCaption = plateDialog.querySelector('[data-dialog-caption]');
  const closeDialog = () => {
    if (plateDialog.open) plateDialog.close();
  };

  plateDialog.querySelector('[data-dialog-close]')?.addEventListener('click', closeDialog);
  plateDialog.addEventListener('click', (event) => {
    if (event.target === plateDialog) closeDialog();
  });
  plateDialog.addEventListener('close', () => {
    dialogMedia.replaceChildren();
    document.body.classList.remove('has-dialog');
  });

  document.querySelectorAll('[data-plate-media]').forEach((link) => {
    link.addEventListener('click', (event) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
      event.preventDefault();
      dialogMedia.replaceChildren();
      const videoSrc = link.getAttribute('data-video');
      if (videoSrc) {
        const video = document.createElement('video');
        video.controls = true;
        video.autoplay = true;
        video.muted = true;
        video.loop = true;
        video.playsInline = true;
        video.poster = link.getAttribute('href') || '';
        const mp4 = document.createElement('source');
        mp4.src = videoSrc;
        mp4.type = 'video/mp4';
        video.appendChild(mp4);
        const webmSrc = link.getAttribute('data-webm');
        if (webmSrc) {
          const webm = document.createElement('source');
          webm.src = webmSrc;
          webm.type = 'video/webm';
          video.appendChild(webm);
        }
        dialogMedia.appendChild(video);
        video.play().catch(() => {});
      } else {
        const image = document.createElement('img');
        image.src = link.getAttribute('href') || '';
        image.alt = link.getAttribute('data-caption') || '';
        dialogMedia.appendChild(image);
      }
      dialogTitle.textContent = link.getAttribute('data-title') || '';
      dialogCaption.textContent = link.getAttribute('data-caption') || '';
      plateDialog.showModal();
      document.body.classList.add('has-dialog');
    });
  });
}

// Upgrade the print-only cover image to its high-resolution copy when printing.
window.addEventListener('beforeprint', () => {
  document.querySelectorAll('img[data-hires]').forEach((img) => {
    const hires = img.getAttribute('data-hires');
    if (hires && img.getAttribute('src') !== hires) img.setAttribute('src', hires);
  });
});
