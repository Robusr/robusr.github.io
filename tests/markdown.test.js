// ============================================================
//  Tests: markdown.js  —  parseMarkdown, escapeHTML
//  Run:  node --test tests/markdown.test.js
// ============================================================

import { describe, it, before } from 'node:test';
import assert from 'node:assert/strict';

let parseMarkdown;

before(async () => {
  // Mock document.createElement so escapeHTML works in Node.js
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
  const mod = await import('../js/markdown.js');
  parseMarkdown = mod.parseMarkdown;
});

describe('parseMarkdown', () => {

  describe('inline formatting', () => {
    it('**bold** → <span class="bold">', () => {
      const out = parseMarkdown('this is **bold** text');
      assert.match(out, /<span class="bold">bold<\/span>/);
    });

    it('*italic* → <span class="dim">', () => {
      const out = parseMarkdown('this is *italic* text');
      assert.match(out, /<span class="dim">italic<\/span>/);
    });

    it('**bold *nested* italic**', () => {
      const out = parseMarkdown('**bold *and italic***');
      assert.match(out, /<span class="bold">bold <span class="dim">and italic<\/span><\/span>/);
    });

    it('*italic **nested** bold*', () => {
      const out = parseMarkdown('*italic **and bold***');
      assert.match(out, /<span class="dim">italic <span class="bold">and bold<\/span><\/span>/);
    });

    it('`code` → <code>', () => {
      const out = parseMarkdown('use `const x = 1` here');
      assert.match(out, /<code>const x = 1<\/code>/);
    });

    it('[text](url) → <a href>', () => {
      const out = parseMarkdown('visit [GitHub](https://github.com)');
      assert.match(out, /<a href="https:\/\/github\.com"/);
      assert.match(out, /class="accent"/);
    });
  });

  describe('block formatting', () => {
    it('# heading → bold span', () => {
      const out = parseMarkdown('# Hello World');
      assert.match(out, /<span class="bold">Hello World<\/span>/);
    });

    it('- items → <ul><li>', () => {
      const out = parseMarkdown('- first\n- second\n- third');
      const liCount = (out.match(/<li>/g) || []).length;
      assert.equal(liCount, 3);
      assert.match(out, /<ul>/);
      assert.match(out, /<\/ul>/);
    });

    it('1. items → <ol><li>', () => {
      const out = parseMarkdown('1. first\n2. second');
      const liCount = (out.match(/<li>/g) || []).length;
      assert.equal(liCount, 2);
      assert.match(out, /<ol>/);
      assert.match(out, /<\/ol>/);
    });
  });

  describe('code blocks', () => {
    it('``` fence → pre > code + copy button', () => {
      const out = parseMarkdown('```js\nconsole.log("hi");\n```');
      assert.match(out, /<div class="code-block">/);
      assert.match(out, /<button class="copy-btn"/);
      assert.match(out, /<pre><code>console\.log\("hi"\);/);
    });
  });

  describe('edge cases', () => {
    it('empty string', () => {
      assert.equal(parseMarkdown(''), '');
    });

    it('null / undefined', () => {
      assert.equal(parseMarkdown(null), '');
      assert.equal(parseMarkdown(undefined), '');
    });

    it('plain text passes through', () => {
      const out = parseMarkdown('just plain text');
      assert.ok(out.includes('just plain text'));
    });
  });

});
