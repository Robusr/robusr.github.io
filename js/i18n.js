// ============================================================
//  i18n.js — Template engine, locale, personal data accessors
//
//  Seeded by initI18n() at boot. All other modules import tStr()
//  and the accessors to get localised strings and personal data.
// ============================================================

let _personal  = null;   // data/personal.json
let _i18nData  = null;   // data/i18n.json
let _locale    = 'en';

// ---- Template engine ----

/** Replace {{var}} placeholders in a template string. */
export function renderTemplate(tmpl, vars) {
  return tmpl.replace(/\{\{(\w+)\}\}/g, (_, key) =>
    vars[key] !== undefined ? vars[key] : `{{${key}}}`);
}

/** Locale-keyed i18n lookup with optional template variables. */
export function tStr(key, vars = {}) {
  const tmpl = _i18nData?.[_locale]?.[key];
  if (!tmpl) return key;
  return renderTemplate(tmpl, vars);
}

// ---- Init ----

/** Seed the module with fetched JSON data. Call once at boot. */
export function initI18n(personalData, i18nData) {
  _personal = personalData;
  _i18nData = i18nData;
}

// ---- Accessors ----

export function getLocale()          { return _locale; }
export function setLocale(lang)      { _locale = lang; }
export function getPersonal()        { return _personal; }
