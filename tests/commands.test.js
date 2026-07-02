// ============================================================
//  Tests: commands.js  —  matchNaturalLanguage
//  Run:  node --test tests/commands.test.js
// ============================================================

import { describe, it, before } from 'node:test';
import assert from 'node:assert/strict';

let matchNaturalLanguage;

before(async () => {
  // matchNaturalLanguage is a pure function — no DOM needed.
  // But commands.js imports from ui.js which needs DOM.
  // So we mock document to satisfy the import chain.
  globalThis.document = {
    createElement: (_tag) => {
      let text = '';
      return {
        set textContent(val) { text = String(val ?? ''); },
        get innerHTML() {
          return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        },
      };
    },
  };
  // Pre-seed i18n to avoid undefined access in tStr calls during import
  const i18nMod = await import('../js/i18n.js');
  i18nMod.initI18n(
    { name: 'X', githubUser: 'x', tagline: { en: '', zh: '' }, bio: { en: '', zh: '' }, skills: { en: [], zh: [] }, contact: { email: '', github: '', wechat: '' } },
    { en: { about:'',placeholder:'',contact:'',help:'',langEN:'',langZH:'',titleBar:'',sysinfo:'',welcome:'',skillsTitle:'',contactTitle:'',projectsFailed:'',projectsTitle:'',projectsEmpty:'',forkTag:'',statsFailed:'',statsTitle:'',notFound:'',projectsLoading:'',statsLoading:'' }, zh: { about:'',placeholder:'',contact:'',help:'',langEN:'',langZH:'',titleBar:'',sysinfo:'',welcome:'',skillsTitle:'',contactTitle:'',projectsFailed:'',projectsTitle:'',projectsEmpty:'',forkTag:'',statsFailed:'',statsTitle:'',notFound:'',projectsLoading:'',statsLoading:'' } }
  );

  const mod = await import('../js/commands.js');
  matchNaturalLanguage = mod.matchNaturalLanguage;
});

describe('matchNaturalLanguage — English', () => {

  it('"who are you" → about', () => {
    assert.equal(matchNaturalLanguage('who are you'), 'about');
  });

  it('"what is your name" → about', () => {
    assert.equal(matchNaturalLanguage('what is your name'), 'about');
  });

  it('"what can you do" → skills', () => {
    assert.equal(matchNaturalLanguage('what can you do'), 'skills');
  });

  it('"show me your projects" → projects', () => {
    assert.equal(matchNaturalLanguage('show me your projects'), 'projects');
  });

  it('"how to contact you" → contact', () => {
    assert.equal(matchNaturalLanguage('how to contact you'), 'contact');
  });

  it('"show stats" → stats', () => {
    assert.equal(matchNaturalLanguage('show stats'), 'stats');
  });

  it('random text → null', () => {
    assert.equal(matchNaturalLanguage('blarg blarg'), null);
  });

});

describe('matchNaturalLanguage — Chinese', () => {

  it('"你是谁" → about', () => {
    assert.equal(matchNaturalLanguage('你是谁'), 'about');
  });

  it('"你会什么" → skills', () => {
    assert.equal(matchNaturalLanguage('你会什么'), 'skills');
  });

  it('"看看你的项目" → projects', () => {
    assert.equal(matchNaturalLanguage('看看你的项目'), 'projects');
  });

  it('"怎么联系你" → contact', () => {
    assert.equal(matchNaturalLanguage('怎么联系你'), 'contact');
  });

});
