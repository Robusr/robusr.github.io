// ============================================================
//  Shared mutable state — single source of truth
//  Imported by all modules that need read/write access.
// ============================================================

export const state = {
  commandHistory:  [],
  historyIndex:    -1,
  isTyping:        false,
  ghReposCache:    null,
  ghProfileCache:  null,
  streamAbort:     null,   // AbortController for cancelling LLM stream
  streamCancelled: false,  // true when user pressed Esc
};
