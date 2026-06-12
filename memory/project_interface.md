---
name: Sol Interface Approach
description: How the user wants to interact with Sol
type: project
---

User previously built a TUI that rendered markdown from Qwen's output (lost when home directory was wiped). Decided not to rebuild it after learning that `Rich.Live` + `Rich.Markdown` can render streaming markdown in-place in the terminal without a full TUI framework.

**Why:** Claude Code is already the primary interactive interface. A TUI would duplicate that. Rich's Live context manager re-renders a Markdown block in place as chunks arrive, giving a streaming feel with rendered output.
**How to apply:** Suggest `Rich.Live` + `Rich.Markdown` for streaming output rendering. Don't push TUI frameworks.
