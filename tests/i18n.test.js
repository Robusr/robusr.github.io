// ============================================================
//  Tests: i18n.js  —  renderTemplate, tStr
//  Run:  node --test tests/i18n.test.js
// ============================================================

import { describe, it, before } from 'node:test';
import assert from 'node:assert/strict';

let renderTemplate, tStr, initI18n, getLocale, setLocale;

before(async () => {
  const mod = await import('../js/i18n.js');
  renderTemplate = mod.renderTemplate;
  tStr           = mod.tStr;
  initI18n       = mod.initI18n;
  getLocale      = mod.getLocale;
  setLocale      = mod.setLocale;

  // Seed with test data
  initI18n(
    { name: 'TestUser', githubUser: 'test', tagline: { en: 'Test', zh: '测试' }, bio: { en: 'A tester', zh: '测试者' }, skills: { en: ['JS'], zh: ['JS'] }, contact: { email: 't@t.com', github: 'gh', wechat: 'wx' } },
    {
      en: { about: 'Name: {{name}}\n---\n{{bio}}', placeholder: 'Type...', contact: '{{email}} {{github}}', help: 'Help!', langEN: 'EN', langZH: 'ZH', titleBar: 'title', sysinfo: '', welcome: '', skillsTitle: '', contactTitle: '', projectsFailed: '', projectsTitle: '', projectsEmpty: '', forkTag: '', statsFailed: '', statsTitle: '', notFound: '', projectsLoading: '', statsLoading: '' },
      zh: { about: '名字: {{name}}\n---\n{{bio}}', placeholder: '输入...', contact: '{{email}} {{github}}', help: '帮助!', langEN: 'EN', langZH: 'ZH', titleBar: 'title', sysinfo: '', welcome: '', skillsTitle: '', contactTitle: '', projectsFailed: '', projectsTitle: '', projectsEmpty: '', forkTag: '', statsFailed: '', statsTitle: '', notFound: '', projectsLoading: '', statsLoading: '' }
    }
  );
});

describe('renderTemplate', () => {

  it('replaces {{var}} with value', () => {
    assert.equal(renderTemplate('Hello {{name}}', { name: 'World' }), 'Hello World');
  });

  it('replaces multiple variables', () => {
    assert.equal(
      renderTemplate('{{greeting}} {{name}}!', { greeting: 'Hi', name: 'Robusr' }),
      'Hi Robusr!'
    );
  });

  it('keeps placeholder when variable missing', () => {
    assert.equal(renderTemplate('Hello {{name}}', {}), 'Hello {{name}}');
  });

  it('handles undefined vars object', () => {
    assert.equal(renderTemplate('Hello {{name}}'), 'Hello {{name}}');
  });

  it('handles empty template', () => {
    assert.equal(renderTemplate('', { x: 'y' }), '');
  });

});

describe('tStr', () => {

  it('returns English value by default', () => {
    assert.equal(tStr('placeholder'), 'Type...');
  });

  it('interpolates vars into template', () => {
    const out = tStr('about', { name: 'Robusr', bio: 'coder' });
    assert.match(out, /Name: Robusr/);
    assert.match(out, /coder/);
  });

  it('returns key when key not found', () => {
    assert.equal(tStr('nonexistent'), 'nonexistent');
  });

});

describe('locale', () => {

  it('defaults to en', () => {
    assert.equal(getLocale(), 'en');
  });

  it('switches to zh', () => {
    setLocale('zh');
    assert.equal(getLocale(), 'zh');
    setLocale('en'); // reset
  });

});
