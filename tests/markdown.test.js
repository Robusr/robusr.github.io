// ============================================================
//  tests/markdown.test.js — parseMarkdown unit tests
//  Run:  node --test tests/markdown.test.js
// ============================================================

import { describe, it, before } from 'node:test';
import assert from 'node:assert/strict';

// Minimal document mock so ui.js (transitive import) doesn't crash
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

const { parseMarkdown } = await import('../js/markdown.js');

// ---- Inline formatting ----

describe('parseMarkdown — inline', () => {
  it('bold (**text**)', () => {
    assert.match(parseMarkdown('**hello**'), /<span class="bold">hello<\/span>/);
  });

  it('italic (*text*)', () => {
    assert.match(parseMarkdown('*hello*'), /<span class="dim">hello<\/span>/);
  });

  it('nested bold + italic (**bold *and italic***)', () => {
    const out = parseMarkdown('**bold *and italic***');
    assert.match(out, /<span class="bold">/);
    assert.match(out, /<span class="dim">/);
  });

  it('inline code (`code`)', () => {
    assert.match(parseMarkdown('use `Array.map()` here'), /<code>Array\.map\(\)<\/code>/);
  });

  it('link [text](url)', () => {
    const out = parseMarkdown('[GitHub](https://github.com)');
    assert.match(out, /<a href="https:\/\/github\.com"/);
    assert.match(out, /class="accent"/);
    assert.match(out, />GitHub<\/a>/);
  });
});

// ---- Block-level ----

describe('parseMarkdown — block', () => {
  it('heading # / ## / ###', () => {
    assert.match(parseMarkdown('# Title'), /<span class="bold">Title<\/span>/);
    assert.match(parseMarkdown('## Sub'), /<span class="bold">Sub<\/span>/);
  });

  it('unordered list (-)', () => {
    const out = parseMarkdown('- one\n- two');
    assert.match(out, /<ul>/);
    assert.match(out, /<li>one<\/li>/);
    assert.match(out, /<li>two<\/li>/);
    assert.match(out, /<\/ul>/);
  });

  it('ordered list (1.)', () => {
    const out = parseMarkdown('1. first\n2. second');
    assert.match(out, /<ol>/);
    assert.match(out, /<li>first<\/li>/);
    assert.match(out, /<\/ol>/);
  });
});

// ---- Code blocks ----

describe('parseMarkdown — code blocks', () => {
  it('fenced code block with copy button', () => {
    const out = parseMarkdown('```\nconst x = 1;\n```');
    assert.match(out, /code-block/);
    assert.match(out, /copy-btn/);
    assert.match(out, /<pre><code>/);
    assert.match(out, /const x = 1;/);
  });

  it('HTML in code block is escaped', () => {
    const out = parseMarkdown('```\n<div>text</div>\n```');
    assert.match(out, /&lt;div&gt;/);
  });
});

// ---- Edge cases ----

describe('parseMarkdown — edge cases', () => {
  it('empty string', () => {
    assert.equal(parseMarkdown(''), '');
  });

  it('null / undefined', () => {
    assert.equal(parseMarkdown(null), '');
    assert.equal(parseMarkdown(undefined), '');
  });

  it('plain text passes through', () => {
    assert.equal(parseMarkdown('hello world'), 'hello world');
  });

  it('HTML in plain text is escaped', () => {
    const out = parseMarkdown('<script>alert(1)</script>');
    assert.match(out, /&lt;script&gt;/);
    assert.equal(out.includes('<script>'), false);
  });

  it('bold stripped when unsupported (newline inside)', () => {
    // ** uses .+? which doesn't span newlines — the literal falls through
    assert.equal(parseMarkdown('**line1\nline2**'), '**line1\nline2**');
  });

  it('mixed bold and link', () => {
    const out = parseMarkdown('**[link](url)**');
    assert.match(out, /<span class="bold">/);
    assert.match(out, /<a href="url"/);
  });
});
