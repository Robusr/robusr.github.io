// ============================================================
//  Commands — dispatch, natural-language matching, LLM chat
// ============================================================

import { state } from './state.js';
import { tStr, getLocale, setLocale, getPersonal } from './i18n.js';
import { fetchGitHubProfile, fetchGitHubRepos, formatProjects, formatStats } from './github.js';
import { parseMarkdown, escapeHTML } from './markdown.js';
import {
  typeHTML, typeText, appendCommandLine, appendSysMsg,
  bufferStream, scrollToBottom, clearTerminal,
} from './ui.js';

// ---- DOM refs ----
const $ = (id) => document.getElementById(id);

// ---- Natural Language Matching ----

export function matchNaturalLanguage(input) {
  const lower = input.toLowerCase();

  // English
  if (/who (are|is) (you|this)|your name|what.*name/.test(lower)) return 'about';
  if (/what (can|do) you do|skill|ability|tech stack/.test(lower)) return 'skills';
  if (/contact|email|reach|find you|github|wechat|how.*(contact|reach)/.test(lower)) return 'contact';
  if (/project|repo|github|code|work|portfolio|show.*(project|repo)/.test(lower)) return 'projects';
  if (/about|bio|intro|tell me about|describe|whoami/.test(lower)) return 'about';
  if (/stat|profile|overview|account/.test(lower)) return 'stats';
  if (/help|command|what.*available/.test(lower)) return 'help';

  // Chinese
  if (/名字|叫什么|是谁|称呼|姓名|你是谁/.test(lower)) return 'about';
  if (/技能|会什么|能力|技术|擅长|懂什么|你会/.test(lower)) return 'skills';
  if (/联系|邮箱|微信|电话|找到你|联系你|怎么联系/.test(lower)) return 'contact';
  if (/项目|作品|做过|写过|仓库|github/.test(lower)) return 'projects';
  if (/简介|介绍|about|关于|背景/.test(lower)) return 'about';
  if (/统计|数据|概览|状态|账号/.test(lower)) return 'stats';

  return null;
}

// ---- Response helpers ----

function respondAbout(respDiv) {
  return typeText(respDiv, tStr('about', {
    name: getPersonal()?.name ?? '',
    bio: getPersonal()?.bio?.[getLocale()] ?? '',
  }));
}

function respondSkills(respDiv) {
  const title = tStr('skillsTitle');
  const list = (getPersonal()?.skills?.[getLocale()] ?? [])
    .map((s, i) => `  ${String(i + 1).padStart(2, ' ')}. ${s}`)
    .join('\n');
  return typeText(respDiv, `${title}\n${'-'.repeat(24)}\n${list}`);
}

function respondContact(respDiv) {
  return typeText(respDiv, [
    tStr('contactTitle'),
    '-'.repeat(24),
    tStr('contact', getPersonal()?.contact ?? {}),
  ].join('\n'));
}

// ---- Language switch ----

function doSwitchLanguage(lang) {
  if (lang === getLocale()) return;
  setLocale(lang);

  const input = $('cmdInput');
  const title = $('titleBar');
  if (input) input.placeholder = tStr('placeholder');
  if (title) title.textContent = tStr('titleBar');
  appendSysMsg(lang === 'en' ? tStr('langEN') : tStr('langZH'));
  scrollToBottom();
}

// ---- Projects / Stats helper (used by both exact + NL paths) ----

async function handleProjects(respDiv) {
  if (!state.ghReposCache) {
    respDiv.innerHTML = `<span class="spinner"></span> ${escapeHTML(tStr('projectsLoading'))}`;
    scrollToBottom();
    await fetchGitHubRepos();
  }
  respDiv.innerHTML = '';
  await typeHTML(respDiv, formatProjects(), 8);
}

async function handleStats(respDiv) {
  if (!state.ghProfileCache) {
    respDiv.innerHTML = `<span class="spinner"></span> ${escapeHTML(tStr('statsLoading'))}`;
    scrollToBottom();
    await fetchGitHubProfile();
  }
  respDiv.innerHTML = '';
  await typeHTML(respDiv, formatStats(), 8);
}

// ---- LLM Chat ----

async function handleLLMChat(respDiv, cmd) {
  respDiv.innerHTML = '<span class="spinner"></span>';
  state.streamAbort = new AbortController();

  try {
    const resp = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: cmd }),
      signal: state.streamAbort.signal,
    });

    if (!resp.ok) {
      if (resp.status === 429) {
        respDiv.innerHTML =
          `<span class="warn">${escapeHTML('[!] 太快啦，请等几秒再试 — Too fast, wait a moment.')}</span>`;
      } else {
        respDiv.innerHTML =
          `<span class="err">${escapeHTML('[!] 出了点问题 — Something went wrong. Try again later.')}</span>`;
      }
    } else {
      const reader = resp.body.getReader();
      const fullText = await bufferStream(reader);

      if (state.streamCancelled) {
        respDiv.innerHTML = '<span class="dim">--- Cancelled ---</span>';
      } else if (fullText) {
        respDiv.innerHTML = '';
        await typeHTML(respDiv, parseMarkdown(fullText));
      } else {
        respDiv.innerHTML =
          `<span class="dim">${escapeHTML('[!] Empty response — try rephrasing.')}</span>`;
      }
    }
  } catch (err) {
    if (state.streamCancelled || err.name === 'AbortError') {
      respDiv.innerHTML = '<span class="dim">--- Cancelled ---</span>';
    } else {
      respDiv.innerHTML =
        `<span class="dim">${escapeHTML('[!] 网络连接失败 — Network error. Check your connection.')}</span>`;
    }
  } finally {
    state.streamAbort = null;
    state.streamCancelled = false;
  }
}

// ---- Main command dispatcher ----

export async function executeCommand(raw) {
  const cmd = raw.trim();
  if (!cmd) return;

  // History
  if (state.commandHistory.length === 0 ||
      state.commandHistory[state.commandHistory.length - 1] !== cmd) {
    state.commandHistory.push(cmd);
  }
  state.historyIndex = state.commandHistory.length;

  const respDiv = appendCommandLine(cmd);
  scrollToBottom();

  const lower = cmd.toLowerCase();

  // === Exact commands ===

  if (lower === 'help' || lower === 'h' || lower === '?') {
    await typeHTML(respDiv, tStr('help'));
    return;
  }

  if (lower === 'about' || lower === 'whoami') {
    await respondAbout(respDiv);
    return;
  }

  if (lower === 'skills' || lower === 'skill') {
    await respondSkills(respDiv);
    return;
  }

  if (lower === 'contact') {
    await respondContact(respDiv);
    return;
  }

  if (lower === 'projects' || lower === 'project' || lower === 'portfolio') {
    await handleProjects(respDiv);
    return;
  }

  if (lower === 'stats' || lower === 'status') {
    await handleStats(respDiv);
    return;
  }

  if (lower === 'lang' || lower === 'locale') {
    doSwitchLanguage(getLocale() === 'en' ? 'zh' : 'en');
    respDiv.remove();
    return;
  }
  if (lower === 'zh' || lower === 'cn') {
    doSwitchLanguage('zh');
    respDiv.remove();
    return;
  }
  if (lower === 'en') {
    doSwitchLanguage('en');
    respDiv.remove();
    return;
  }

  if (lower === 'clear' || lower === 'cls') {
    clearTerminal();
    return;
  }

  // === Natural language / LLM Chat ===

  const intent = matchNaturalLanguage(cmd);
  respDiv.innerHTML = '';

  if (intent === 'help')     { await typeHTML(respDiv, tStr('help')); return; }
  if (intent === 'about')    { await respondAbout(respDiv); return; }
  if (intent === 'skills')   { await respondSkills(respDiv); return; }
  if (intent === 'contact')  { await respondContact(respDiv); return; }
  if (intent === 'projects') { await handleProjects(respDiv); return; }
  if (intent === 'stats')    { await handleStats(respDiv); return; }

  // Fall through → LLM
  await handleLLMChat(respDiv, cmd);
}
