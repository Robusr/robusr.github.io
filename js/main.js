// ============================================================
//  Robusr's Utopia — Entry point
//  Boots the terminal: loads config → renders UI → wires events
// ============================================================

import { state } from './state.js';
import { initI18n, getLocale, tStr } from './i18n.js';
import { fetchGitHubProfile, fetchGitHubRepos } from './github.js';
import { executeCommand } from './commands.js';
import { showStartupScreen, scrollToBottom, clearTerminal } from './ui.js';

// ---- DOM refs ----
const $ = (id) => document.getElementById(id);

// ---- Event listeners ----

function setupEvents() {
  const input  = $('cmdInput');
  const body   = $('terminalBody');

  input.addEventListener('keydown', (e) => {
    // Esc — cancel in-progress LLM stream
    if (e.key === 'Escape' && state.streamAbort) {
      e.preventDefault();
      state.streamCancelled = true;
      state.streamAbort.abort();
      return;
    }

    // Ctrl+L / Cmd+L — clear terminal
    if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
      e.preventDefault();
      clearTerminal();
      return;
    }

    if (state.isTyping) { e.preventDefault(); return; }

    if (e.key === 'Enter') {
      e.preventDefault();
      const cmd = input.value;
      input.value = '';
      executeCommand(cmd);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (state.historyIndex > 0) {
        state.historyIndex--;
        input.value = state.commandHistory[state.historyIndex];
      }
      input.setSelectionRange(input.value.length, input.value.length);
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (state.historyIndex < state.commandHistory.length) {
        state.historyIndex++;
        input.value = state.commandHistory[state.historyIndex];
      } else {
        state.historyIndex = state.commandHistory.length;
        input.value = '';
      }
      input.setSelectionRange(input.value.length, input.value.length);
    }
  });

  body.addEventListener('click', () => {
    if (!state.isTyping) input.focus();
  });

  input.addEventListener('click', (e) => e.stopPropagation());
}

// ---- Bootstrap ----

async function init() {
  const input  = $('cmdInput');

  // Phase 1: instant — terminal shell is already in the DOM
  input.placeholder = 'Loading...';
  input.disabled = true;

  const output = $('output');
  const loadDiv = document.createElement('div');
  loadDiv.className = 'response';
  loadDiv.innerHTML = '<span class="spinner"></span> <span class="dim">Loading...</span>';
  output.appendChild(loadDiv);

  // Phase 2: fetch config
  let ok = true;
  try {
    const [pRes, iRes] = await Promise.all([
      fetch('./data/personal.json'),
      fetch('./data/i18n.json'),
    ]);
    if (!pRes.ok || !iRes.ok) throw new Error('Failed to load config');
    initI18n(await pRes.json(), await iRes.json());
  } catch (e) {
    ok = false;
  }

  output.innerHTML = '';

  if (!ok) {
    const errDiv = document.createElement('div');
    errDiv.className = 'response';
    errDiv.innerHTML =
      '<span class="err">[!] Failed to load configuration.</span><br><br>' +
      '<span class="dim">Check your connection and try again.</span><br><br>' +
      '<button onclick="import(\'./js/main.js\').then(m=>m.reinit())" ' +
        'style="font-family:inherit;font-size:13px;padding:4px 14px;' +
        'color:var(--text-primary,#F8F8F2);background:rgba(255,255,255,0.08);' +
        'border:1px solid var(--border-code,rgba(255,255,255,0.08));' +
        'border-radius:4px;cursor:pointer;">Retry</button>';
    output.appendChild(errDiv);
    input.placeholder = 'Reload page to retry...';
    input.disabled = false;
    input.focus();
    return;
  }

  // Phase 3: bootstrap
  const title = $('titleBar');
  input.placeholder = tStr('placeholder');
  if (title) title.textContent = tStr('titleBar');
  input.disabled = false;

  showStartupScreen();
  input.focus();
  scrollToBottom();

  // Pre-fetch GitHub data in background
  fetchGitHubProfile();
  fetchGitHubRepos();
}

// Exported for the Retry button
export function reinit() {
  const output = $('output');
  if (output) output.innerHTML = '';
  init();
}

// ---- Go ----
setupEvents();
init();
