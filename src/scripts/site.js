const header = document.querySelector('[data-header]');
if (header) {
  const update = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
  update();
  window.addEventListener('scroll', update, { passive: true });
}

const hash = window.location.hash;
if (hash) {
  document.querySelectorAll('a[data-anchor-link]').forEach((link) => {
    const base = link.getAttribute('data-base');
    if (base) link.setAttribute('href', base + hash);
  });
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
