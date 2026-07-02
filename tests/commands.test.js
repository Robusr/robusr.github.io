// ============================================================
//  tests/commands.test.js — matchNaturalLanguage unit tests
//  Run:  node --test tests/commands.test.js
// ============================================================

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

// Minimal DOM mock satisfies transitive imports (ui.js, commands.js)
global.document = {
  createElement(tag) {
    const el = { _text: '' };
    Object.defineProperty(el, 'textContent', { set(v) { el._text = v; } });
    Object.defineProperty(el, 'innerHTML', {
      get() { return el._text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); },
      set(v) { el._html = v; },
    });
    return el;
  },
};
global.window = { matchMedia() { return { matches: false }; } };

const { matchNaturalLanguage } = await import('../js/commands.js');

// ---- English patterns ----

describe('matchNaturalLanguage — English', () => {
  it('"Who are you?" → about', () => {
    assert.equal(matchNaturalLanguage('Who are you?'), 'about');
  });

  it('"What is your name?" → about', () => {
    assert.equal(matchNaturalLanguage('What is your name?'), 'about');
  });

  it('"What can you do?" → skills', () => {
    assert.equal(matchNaturalLanguage('What can you do?'), 'skills');
  });

  it('"Show me your projects" → projects', () => {
    assert.equal(matchNaturalLanguage('Show me your projects'), 'projects');
  });

  it('"How can I contact you?" → contact', () => {
    assert.equal(matchNaturalLanguage('How can I contact you?'), 'contact');
  });

  it('"Tell me about yourself" → about', () => {
    assert.equal(matchNaturalLanguage('Tell me about yourself'), 'about');
  });

  it('"Give me your stats" → stats', () => {
    assert.equal(matchNaturalLanguage('Give me your stats'), 'stats');
  });

  it('"What commands are available?" → help', () => {
    assert.equal(matchNaturalLanguage('What commands are available?'), 'help');
  });
});

// ---- Chinese patterns ----

describe('matchNaturalLanguage — Chinese', () => {
  it('"你是谁？" → about', () => {
    assert.equal(matchNaturalLanguage('你是谁？'), 'about');
  });

  it('"你叫什么名字？" → about', () => {
    assert.equal(matchNaturalLanguage('你叫什么名字？'), 'about');
  });

  it('"你会什么？" → skills', () => {
    assert.equal(matchNaturalLanguage('你会什么？'), 'skills');
  });

  it('"你的技能有哪些？" → skills', () => {
    assert.equal(matchNaturalLanguage('你的技能有哪些？'), 'skills');
  });

  it('"怎么联系你？" → contact', () => {
    assert.equal(matchNaturalLanguage('怎么联系你？'), 'contact');
  });

  it('"看看你的项目" → projects', () => {
    assert.equal(matchNaturalLanguage('看看你的项目'), 'projects');
  });

  it('"介绍一下你自己" → about', () => {
    assert.equal(matchNaturalLanguage('介绍一下你自己'), 'about');
  });

  it('"你的GitHub统计数据" → projects (github match wins)', () => {
    assert.equal(matchNaturalLanguage('你的GitHub统计数据'), 'projects');
  });
});

// ---- No match ----

describe('matchNaturalLanguage — no match', () => {
  it('random text returns null', () => {
    assert.equal(matchNaturalLanguage('asdfghjkl'), null);
  });

  it('"Hello" returns null', () => {
    assert.equal(matchNaturalLanguage('Hello'), null);
  });
});
