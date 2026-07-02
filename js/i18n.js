// ============================================================
//  i18n — template engine, locale, personal data
// ============================================================

let personal = null;   // data/personal.json
let i18nData = null;   // data/i18n.json
let locale   = 'en';

// ---- Public API ----

export function initI18n(p, i) {
  personal = p;
  i18nData = i;
}

export function getPersonal()  { return personal; }
export function getLocale()    { return locale; }
export function setLocale(l)   { locale = l; }

// ---- Template engine  (replaces {{var}} placeholders) ----

export function renderTemplate(tmpl, vars) {
  return tmpl.replace(/\{\{(\w+)\}\}/g, (_, key) =>
    vars != null && vars[key] !== undefined ? vars[key] : `{{${key}}}`);
}

// i18n lookup with optional template variables
export function tStr(key, vars = {}) {
  const tmpl = i18nData?.[locale]?.[key];
  if (!tmpl) return key;
  return renderTemplate(tmpl, vars);
}
