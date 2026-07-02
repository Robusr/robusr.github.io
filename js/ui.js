// ============================================================
//  UI — DOM helpers, typewriter effect, startup screen
// ============================================================

import { state } from './state.js';
import { escapeHTML } from './markdown.js';
import { tStr, getPersonal, getLocale } from './i18n.js';

// ---- DOM refs (lazy, resolved at call time) ----
const $ = (id) => document.getElementById(id);

// ---- ASCII Pixel-Art Logo (pre-computed by scripts/ascii_gen.py) ----

const LOGO_UP = [
'########                 ##                                            ',
'#########                ##                                            ',
'###   ###                ##                                            ',
'###    ###               ##                                            ',
'###    ###    ######     ## ####     ##    ##     ######      ### #### ',
'###   ###    ########    ########    ##    ##    ########     #########',
'########     ###  ###    ###  ####   ##    ##    ###   ##     ####   # ',
'#######     ###    ###   ##    ###   ##    ##    ##           ###      ',
'###  ###    ###    ###   ##     ##   ##    ##    ####         ###      ',
'###   ###   ##      ##   ##     ##   ##    ##     ######      ###      ',
'###    ##   ###    ###   ##     ##   ##    ##         ###     ###      ',
'###    ###  ###    ###   ##    ###   ##    ##          ##     ###      ',
'###     ##   ###  ###    ###  ####   ###  ###    ##   ###     ###      ',
];
const LOGO_UP_SPLITS = [11, 23, 35, 47, 59];
const LOGO_UP_WIDTH  = 71;
const LOGO_COLORS    = ['#FF6188','#FC9867','#FFD866','#A9DC76','#78DCE8','#AB9DF2'];
const LOGO_SLANT      = 1;
const LOGO_DIR        = 'reverse';
const LOGO_ROWS       = LOGO_UP.length;
const LOGO_TOTAL_W    = LOGO_UP_WIDTH + LOGO_SLANT * (LOGO_ROWS - 1);

// ---- Helpers ----

export function scrollToBottom() {
  const el = $('terminalBody');
  if (el) el.scrollTop = el.scrollHeight;
}

export function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export function appendCommandLine(cmd) {
  const output = $('output');
  const line = document.createElement('div');
  line.className = 'cmd-line';
  line.innerHTML =
    `<span class="prompt-arrow">$</span> <span class="prompt-path">~</span> <span class="cmd-text">${escapeHTML(cmd)}</span>`;
  output.appendChild(line);

  const resp = document.createElement('div');
  resp.className = 'response';
  output.appendChild(resp);
  return resp;
}

export function appendSysMsg(text) {
  const output = $('output');
  const div = document.createElement('div');
  div.className = 'response';
  div.innerHTML = `<span class="dim">${escapeHTML(text)}</span>`;
  output.appendChild(div);
  return div;
}

export function clearTerminal() {
  const output = $('output');
  const input = $('cmdInput');
  output.innerHTML = '';
  if (input) { input.value = ''; input.focus(); }
}

// ---- Typewriter Effect (HTML-aware, renders tags correctly) ----

export async function typeHTML(element, html, speed = 16) {
  state.isTyping = true;
  const input = $('cmdInput');
  if (input) input.disabled = true;

  // Respect accessibility preference — instant output, no animation
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    element.innerHTML = html;
    state.isTyping = false;
    if (input) { input.disabled = false; input.focus(); }
    scrollToBottom();
    return;
  }

  let out = '';
  let i = 0;

  while (i < html.length) {
    const remaining = html.slice(i);
    const tagMatch = remaining.match(/^<[^>]*>/);
    if (tagMatch) {
      out += tagMatch[0];
      i += tagMatch[0].length;
      element.innerHTML = out;
      scrollToBottom();
      continue;
    }

    out += html[i];
    element.innerHTML = out;
    scrollToBottom();
    i++;

    const ch = html[i - 1];
    const pause =
      (ch === '.' || ch === '。') ? speed * 5 :
      (ch === ',' || ch === '，') ? speed * 3 :
      speed;
    await delay(pause);
  }

  state.isTyping = false;
  if (input) { input.disabled = false; input.focus(); }
  scrollToBottom();
}

export async function typeText(element, text, speed = 16) {
  await typeHTML(element, escapeHTML(text).replace(/\n/g, '<br>'), speed);
}

// ---- Buffer LLM stream (SSE → full text) ----

export async function bufferStream(reader) {
  const decoder = new TextDecoder();
  let buffer = '';
  let fullText = '';
  let timeout;

  try {
    timeout = setTimeout(() => reader.cancel(), 30_000);

    while (true) {
      const { done, value } = await reader.read();
      clearTimeout(timeout);
      if (done) break;
      timeout = setTimeout(() => reader.cancel(), 30_000);

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const data = line.slice(6);
        if (data === '[DONE]') continue;

        try {
          const json = JSON.parse(data);
          const content = json.choices?.[0]?.delta?.content;
          if (content) fullText += content;
        } catch {}
      }
    }
  } catch {
    // Aborted or network error — caller checks streamCancelled
  }

  clearTimeout(timeout);
  return fullText;
}

// ---- Startup: pixel logo + system info + hint ----

export function showStartupScreen() {
  const output = $('output');
  const personal  = getPersonal();
  const locale    = getLocale();

  // Step 1: "Robusr" logo — upright colouring + row-shift slant
  const logoDiv = document.createElement('div');
  logoDiv.className = 'ascii-logo';
  for (let r = 0; r < LOGO_ROWS; r++) {
    const line = LOGO_UP[r];
    const leftPad  = LOGO_DIR === 'reverse'
      ? LOGO_SLANT * (LOGO_ROWS - 1 - r)
      : LOGO_SLANT * r;
    const rightPad = LOGO_TOTAL_W - leftPad - LOGO_UP_WIDTH;

    const rowDiv = document.createElement('div');
    rowDiv.style.whiteSpace = 'pre';

    let html = ' '.repeat(leftPad);
    let cursor = 0;
    for (let i = 0; i < LOGO_COLORS.length; i++) {
      const end = (i < LOGO_UP_SPLITS.length) ? LOGO_UP_SPLITS[i] : LOGO_UP_WIDTH;
      const seg = line.slice(cursor, end);
      html += `<span style="color:${LOGO_COLORS[i]};">${escapeHTML(seg)}</span>`;
      cursor = end;
    }
    html += ' '.repeat(rightPad);

    rowDiv.innerHTML = html;
    logoDiv.appendChild(rowDiv);
  }
  output.appendChild(logoDiv);

  // Step 2: System info
  const sysDiv = document.createElement('div');
  sysDiv.className = 'sysinfo';
  sysDiv.textContent = tStr('sysinfo', {
    name: 'guest',
    tagline: personal?.tagline?.[locale] ?? '',
  });
  output.appendChild(sysDiv);

  // Step 3: Short hint
  const hintDiv = document.createElement('div');
  hintDiv.className = 'response';
  hintDiv.innerHTML = `<span class="dim">${escapeHTML(tStr('placeholder'))}</span>`;
  output.appendChild(hintDiv);

  scrollToBottom();
}
