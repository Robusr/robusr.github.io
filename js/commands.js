// ============================================================
//  commands.js — Natural-language matching, command dispatch,
//                LLM chat pipeline, response helpers.
// ============================================================

import { state } from './state.js';
import { tStr, getLocale, setLocale, getPersonal } from './i18n.js';
import { fetchGitHubProfile, fetchGitHubRepos, formatProjects, formatStats } from './github.js';
import {
  appendCommandLine, appendSysMsg, switchLanguageUI,
  typeHTML, typeText, bufferStream, scrollToBottom,
} from './ui.js';
import { parseMarkdown } from './markdown.js';

// ---- Natural Language Matching ----

export function matchNaturalLanguage(input) {
  const lower = input.toLowerCase();

  // English
  if (/who (are|is) (you|this)|your name|what.*name/.test(lower)) return 'about';
  if (/what (can|do) you do|skill|ability|tech stack/.test(lower)) return 'skills';
  if (/contact|email|reach|find you|wechat|how.*(contact|reach)/.test(lower)) return 'contact';
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

async function respondAbout(respDiv) {
  const personal = getPersonal();
  return typeText(respDiv, tStr('about', {
    name: personal?.name ?? '',
    bio: personal?.bio?.[getLocale()] ?? '',
  }));
}

async function respondSkills(respDiv) {
  const personal = getPersonal();
  const title = tStr('skillsTitle');
  const list = (personal?.skills?.[getLocale()] ?? [])
    .map((s, i) => `  ${String(i + 1).padStart(2, ' ')}. ${s}`)
    .join('\n');
  return typeText(respDiv, `${title}\n${'-'.repeat(24)}\n${list}`);
}

async function respondContact(respDiv) {
  return typeText(respDiv, [
    tStr('contactTitle'),
    '-'.repeat(24),
    tStr('contact', getPersonal()?.contact ?? {}),
  ].join('\n'));
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
          `<span class="warn">${escapeHTMLDirect('[!] 太快啦，请等几秒再试 — Too fast, wait a moment.')}</span>`;
      } else {
        respDiv.innerHTML =
          `<span class="err">${escapeHTMLDirect('[!] 出了点问题 — Something went wrong. Try again later.')}</span>`;
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
          `<span class="dim">${escapeHTMLDirect('[!] Empty response — try rephrasing.')}</span>`;
      }
    }
  } catch (err) {
    if (state.streamCancelled || err.name === 'AbortError') {
      respDiv.innerHTML = '<span class="dim">--- Cancelled ---</span>';
    } else {
      respDiv.innerHTML =
        `<span class="dim">${escapeHTMLDirect('[!] 网络连接失败 — Network error. Check your connection.')}</span>`;
    }
  } finally {
    state.streamAbort = null;
    state.streamCancelled = false;
  }
}

// Tiny inline escaper so this module doesn't need ui.js just for
// static error strings (avoids coupling for simple literal use).
function escapeHTMLDirect(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ---- Command Execution ----

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

  // ---- Exact commands ----

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
    if (!state.ghReposCache) {
      respDiv.innerHTML = `<span class="spinner"></span> ${escapeHTMLDirect(tStr('projectsLoading'))}`;
      scrollToBottom();
      await fetchGitHubRepos();
    }
    respDiv.innerHTML = '';
    await typeHTML(respDiv, formatProjects(), 8);
    return;
  }

  if (lower === 'stats' || lower === 'status') {
    if (!state.ghProfileCache) {
      respDiv.innerHTML = `<span class="spinner"></span> ${escapeHTMLDirect(tStr('statsLoading'))}`;
      scrollToBottom();
      await fetchGitHubProfile();
    }
    respDiv.innerHTML = '';
    await typeHTML(respDiv, formatStats(), 8);
    return;
  }

  if (lower === 'lang' || lower === 'locale') {
    const next = getLocale() === 'en' ? 'zh' : 'en';
    setLocale(next);
    switchLanguageUI(next);
    respDiv.remove();
    return;
  }
  if (lower === 'zh' || lower === 'cn') {
    setLocale('zh');
    switchLanguageUI('zh');
    respDiv.remove();
    return;
  }
  if (lower === 'en') {
    setLocale('en');
    switchLanguageUI('en');
    respDiv.remove();
    return;
  }

  if (lower === 'clear' || lower === 'cls') {
    const output = document.getElementById('output');
    const cmdInput = document.getElementById('cmdInput');
    output.innerHTML = '';
    cmdInput.value = '';
    cmdInput.focus();
    return;
  }

  // ---- Natural language / LLM Chat ----
  const intent = matchNaturalLanguage(cmd);
  respDiv.innerHTML = '';

  if (intent === 'help') {
    await typeHTML(respDiv, tStr('help'));
  } else if (intent === 'about') {
    await respondAbout(respDiv);
  } else if (intent === 'skills') {
    await respondSkills(respDiv);
  } else if (intent === 'contact') {
    await respondContact(respDiv);
  } else if (intent === 'projects') {
    if (!state.ghReposCache) {
      respDiv.innerHTML = `<span class="spinner"></span> ${escapeHTMLDirect(tStr('projectsLoading'))}`;
      scrollToBottom();
      await fetchGitHubRepos();
    }
    respDiv.innerHTML = '';
    await typeHTML(respDiv, formatProjects(), 8);
  } else if (intent === 'stats') {
    if (!state.ghProfileCache) {
      respDiv.innerHTML = `<span class="spinner"></span> ${escapeHTMLDirect(tStr('statsLoading'))}`;
      scrollToBottom();
      await fetchGitHubProfile();
    }
    respDiv.innerHTML = '';
    await typeHTML(respDiv, formatStats(), 8);
  } else {
    await handleLLMChat(respDiv, cmd);
  }
}
