// ============================================================
//  Lightweight Markdown → HTML parser
//  Zero dependencies.  Matches the terminal's CSS class system.
//
//  Supported syntax:
//    # Heading 1-3        → <span class="bold">
//    **bold**              → <span class="bold">
//    *italic*              → <span class="dim">
//    `inline code`         → <code>
//    [text](url)           → <a href="url" target="_blank" class="accent">
//    - unordered list      → <ul><li>…</li></ul>
//    1. ordered list       → <ol><li>…</li></ol>
//    ```code block```      → <pre><code>…</code></pre>
// ============================================================

function escapeHTML(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function parseMarkdown(text) {
  if (!text) return '';

  // ---- Step 0: guard — extract & protect fenced code blocks ----
  const fences = [];
  let html = text.replace(/```(\w*)\n?([\s\S]*?)```/g, (_, lang, code) => {
    const i = fences.push(`<pre><code>${escapeHTML(code.trim())}</code></pre>`);
    return `\x00FENCE${i - 1}\x00`;
  });

  // ---- Step 1: escape remaining HTML ----
  html = escapeHTML(html);

  // ---- Step 2: process line by line (block-level) ----
  const lines = html.split('\n');
  const out = [];
  let i = 0;

  while (i < lines.length) {
    const raw = lines[i];

    // Fenced-code placeholder — pass through untouched
    if (raw.startsWith('\x00FENCE')) {
      // Close any open list before the fence
      flushList(out);
      out.push(raw);
      i++;
      continue;
    }

    // Blank line — paragraph break, close lists
    if (raw.trim() === '') {
      flushList(out);
      out.push('<br>');
      i++;
      continue;
    }

    // Heading  (### / ## / #)
    const hMatch = raw.match(/^(#{1,3})\s+(.+)/);
    if (hMatch) {
      flushList(out);
      out.push(`<span class="bold">${parseInline(hMatch[2])}</span>`);
      i++;
      continue;
    }

    // Unordered list  (-  or  *)
    const ulMatch = raw.match(/^[\-\*]\s+(.+)/);
    if (ulMatch) {
      openList(out, '<ul>');
      out.push(`<li>${parseInline(ulMatch[1])}</li>`);
      i++;
      continue;
    }

    // Ordered list  (1.  2.  etc.)
    const olMatch = raw.match(/^\d+\.\s+(.+)/);
    if (olMatch) {
      openList(out, '<ol>');
      out.push(`<li>${parseInline(olMatch[1])}</li>`);
      i++;
      continue;
    }

    // Regular paragraph line
    flushList(out);
    out.push(parseInline(raw));
    i++;
  }

  flushList(out);  // close any trailing list

  // ---- Step 3: join lines ----
  let result = out.join('\n');

  // Collapse consecutive <br> tags
  result = result.replace(/(<br>\n){3,}/g, '<br>\n<br>\n');

  // ---- Step 4: restore fenced code blocks ----
  result = result.replace(/\x00FENCE(\d+)\x00/g, (_, idx) => fences[+idx]);

  return result;
}

// ---- Inline parser (bold, italic, code, links) ----
function parseInline(text) {
  let out = text;

  // Inline code  `…`  (before bold/italic so backticks inside don't leak)
  out = out.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Bold  **…**
  out = out.replace(/\*\*(.+?)\*\*/g, '<span class="bold">$1</span>');

  // Italic  *…*  (single asterisk, not matching **)
  out = out.replace(/(?<!\*)\*([^*\n]+)\*(?!\*)/g, '<span class="dim">$1</span>');

  // Links  [text](url)
  out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g,
    '<a href="$2" target="_blank" rel="noopener" class="accent">$1</a>');

  return out;
}

// ---- List-builder helpers ----
let _listKind = null;

function openList(buf, tag) {
  if (_listKind === tag) return;        // already open, same kind
  if (_listKind !== null) closeList(buf); // different kind → close first
  buf.push(tag);
  _listKind = tag;
}

function closeList(buf) {
  if (_listKind === null) return;
  buf.push(_listKind === '<ul>' ? '</ul>' : '</ol>');
  _listKind = null;
}

function flushList(buf) {
  closeList(buf);
}
