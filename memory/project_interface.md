---
name: Sol Interface Approach
description: How the user wants to interact with Sol
type: project
---

User is uncertain about the interface layer. Tried a popular Python TUI library and didn't enjoy it. Given that Claude Code already covers interactive use, the interface module will likely become a simple Click CLI for headless/cron invocation rather than a full TUI.

**Why:** Claude Code is already the primary interactive interface. A TUI would duplicate that.
**How to apply:** Suggest Click + Rich over full TUI frameworks. Don't push TUI solutions.
