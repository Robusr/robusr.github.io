// ============================================================
//  tests/i18n.test.js — renderTemplate, tStr, locale unit tests
//  Run:  node --test tests/i18n.test.js
// ============================================================

import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';

import {
  initI18n, renderTemplate, tStr,
  getLocale, setLocale, getPersonal,
} from '../js/i18n.js';

// Seed the module with test data before each test
beforeEach(() => {
  initI18n(
    { name: 'TestUser', tagline: { en: 'Hello', zh: '你好' } },
    {
      en: { greeting: 'Hi {{name}}!', plain: 'Hello world' },
      zh: { greeting: '你好 {{name}}！', plain: '你好世界' },
    },
  );
  setLocale('en');
});

// ---- renderTemplate ----

describe('renderTemplate', () => {
  it('replaces {{var}} placeholders', () => {
    assert.equal(renderTemplate('Hello {{name}}', { name: 'World' }), 'Hello World');
  });

  it('replaces multiple variables', () => {
    assert.equal(
      renderTemplate('{{greeting}} {{name}}!', { greeting: 'Hi', name: 'Robusr' }),
      'Hi Robusr!',
    );
  });

  it('leaves missing variables untouched', () => {
    assert.equal(renderTemplate('{{missing}}', {}), '{{missing}}');
  });

  it('returns empty string for empty template', () => {
    assert.equal(renderTemplate('', {}), '');
  });

  it('partial replacement — some vars missing', () => {
    assert.equal(
      renderTemplate('{{a}} {{b}}', { a: '1' }),
      '1 {{b}}',
    );
  });
});

// ---- tStr ----

describe('tStr', () => {
  it('looks up key in current locale', () => {
    assert.equal(tStr('plain'), 'Hello world');
  });

  it('interpolates variables from personal data', () => {
    assert.equal(tStr('greeting', { name: getPersonal().name }), 'Hi TestUser!');
  });

  it('returns key as-is when missing', () => {
    assert.equal(tStr('nonexistent'), 'nonexistent');
  });

  it('returns key as-is when i18n data is unavailable', () => {
    initI18n(null, null);
    assert.equal(tStr('anything'), 'anything');
  });
});

// ---- locale ----

describe('locale', () => {
  it('defaults to en', () => {
    assert.equal(getLocale(), 'en');
  });

  it('setLocale switches language', () => {
    setLocale('zh');
    assert.equal(getLocale(), 'zh');
    assert.equal(tStr('plain'), '你好世界');
  });

  it('getPersonal returns seeded data', () => {
    assert.equal(getPersonal().name, 'TestUser');
  });
});
