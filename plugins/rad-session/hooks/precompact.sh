#!/usr/bin/env bash
# rad-session PreCompact hook
#
# Fires just before Claude Code compacts the conversation context.
# Emits a systemMessage instructing Claude to run /wrapup so session
# state (HANDOFF.md, session-log.md, CLAUDE.md) reflects the pre-compaction
# state before it's lost.
#
# Input (stdin JSON): standard hook payload — we ignore it; the action
# is always the same regardless of compaction trigger or matcher.
#
# Output (stdout JSON): a systemMessage that will be shown to Claude in the
# post-compaction context. Exit 0 = non-blocking success.

set -euo pipefail

# Drain stdin so the hook runner doesn't block on pipe buffering.
cat >/dev/null 2>&1 || true

cat <<'JSON'
{
  "systemMessage": "⚠ rad-session PreCompact hook fired. Before continuing with any other work, run the /wrapup skill to capture the current session state. This writes HANDOFF.md, appends the session log, and prunes CLAUDE.md so the pre-compaction state isn't silently lost. After /wrapup completes, resume whatever the user was working on — the /startup skill will read the fresh HANDOFF.md on the next session."
}
JSON
