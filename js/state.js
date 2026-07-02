// ============================================================
//  state.js — Shared mutable state singleton
//
//  All modules import this single object. Mutation happens via
//  direct property assignment — simple and transparent.
// ============================================================

export const state = {
  commandHistory:  [],
  historyIndex:    -1,
  isTyping:        false,
  ghReposCache:    null,    // { originals: [], forks: [] }
  ghProfileCache:  null,    // GitHub user object
  streamAbort:     null,    // AbortController for LLM stream
  streamCancelled: false,   // true when user pressed Esc
};
