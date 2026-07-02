// ============================================================
//  main.js — Entry point: DOM refs, event listeners, boot sequence
// ============================================================

import { state } from './state.js';
import { initI18n, tStr, setLocale, getLocale } from './i18n.js';
import { fetchGitHubProfile, fetchGitHubRepos } from './github.js';
import { initUI, showStartupScreen, appendSysMsg, scrollToBottom } from './ui.js';
import { executeCommand } from './commands.js';

// ---- DOM References ----
const terminalBody = document.getElementById('terminalBody');
const output       = document.getElementById('output');
const cmdInput     = document.getElementById('cmdInput');
const titleBar     = document.getElementById('titleBar');

// Seed ui.js with DOM refs so it can manipulate the terminal
initUI(terminalBody, output, cmdInput, titleBar);

// ---- Event Listeners ----

cmdInput.addEventListener('keydown', (e) => {
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
    output.innerHTML = '';
    cmdInput.value = '';
    return;
  }

  if (state.isTyping) { e.preventDefault(); return; }

  if (e.key === 'Enter') {
    e.preventDefault();
    const cmd = cmdInput.value;
    cmdInput.value = '';
    executeCommand(cmd);
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    if (state.historyIndex > 0) {
      state.historyIndex--;
      cmdInput.value = state.commandHistory[state.historyIndex];
    }
    cmdInput.setSelectionRange(cmdInput.value.length, cmdInput.value.length);
  } else if (e.key === 'ArrowDown') {
    e.preventDefault();
    if (state.historyIndex < state.commandHistory.length) {
      state.historyIndex++;
      cmdInput.value = state.commandHistory[state.historyIndex];
    } else {
      state.historyIndex = state.commandHistory.length;
      cmdInput.value = '';
    }
    cmdInput.setSelectionRange(cmdInput.value.length, cmdInput.value.length);
  }
});

terminalBody.addEventListener('click', () => {
  if (!state.isTyping) cmdInput.focus();
});

cmdInput.addEventListener('click', (e) => e.stopPropagation());

// ---- Boot Sequence ----

async function init() {
  // Phase 1: instant — terminal shell is already in the DOM
  cmdInput.placeholder = 'Loading...';
  cmdInput.disabled = true;

  const loadDiv = document.createElement('div');
  loadDiv.className = 'response';
  loadDiv.innerHTML = '<span class="spinner"></span> <span class="dim">Loading...</span>';
  output.appendChild(loadDiv);

  // Phase 2: fetch config (network)
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

  // Remove loading indicator
  output.innerHTML = '';

  if (!ok) {
    const errDiv = document.createElement('div');
    errDiv.className = 'response';
    errDiv.innerHTML =
      '<span class="err">[!] Failed to load configuration.</span><br><br>' +
      '<span class="dim">Check your connection and try again.</span><br><br>' +
      '<button onclick="output.innerHTML=\'\';init()" ' +
        'style="font-family:inherit;font-size:13px;padding:4px 14px;' +
        'color:var(--text-primary, #F8F8F2);background:rgba(255,255,255,0.08);' +
        'border:1px solid var(--border-code, rgba(255,255,255,0.08));' +
        'border-radius:4px;cursor:pointer;">Retry</button>';
    output.appendChild(errDiv);
    cmdInput.placeholder = 'Reload page to retry...';
    cmdInput.disabled = false;
    cmdInput.focus();
    return;
  }

  // Phase 3: bootstrap the full UI
  cmdInput.placeholder = tStr('placeholder');
  titleBar.textContent = tStr('titleBar');
  cmdInput.disabled = false;

  showStartupScreen();
  cmdInput.focus();
  scrollToBottom();

  // Pre-fetch GitHub data in background (unauthenticated)
  fetchGitHubProfile();
  fetchGitHubRepos();
}

init();
