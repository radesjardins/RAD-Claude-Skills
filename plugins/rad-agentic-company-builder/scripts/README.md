# rad-agentic-company-builder scripts

Mechanical validators that turn the plugin's structural and configuration claims into concrete pass/fail checks. Where the previous version asked an LLM agent to "score the structure 1-10," these scripts give a deterministic answer.

All scripts are pure Python 3.8+ stdlib. No `pip install` required.

## audit-structure.py

Audits an agentic company / Claude Code workspace against the structural conventions documented in this plugin.

```bash
python3 scripts/audit-structure.py <company-root>
python3 scripts/audit-structure.py <company-root> --json
python3 scripts/audit-structure.py <company-root> --strict
python3 scripts/audit-structure.py . --skip-hooks --skip-mcp --skip-agents
```

**Catches:**
- Missing CLAUDE.md at company / division / project / repo levels
- Invalid JSON in `.claude/settings.json` or `.mcp.json`
- Missing recommended `.gitignore` entries (`CLAUDE.local.md`, `.env`, etc.)
- Agent files with missing required frontmatter fields
- Hook events that don't exist in Claude Code's documented event list
- MCP server entries with no transport (neither stdio nor http)

**Exit codes:** `0` clean, `1` findings, `2` script error.

## validate-hooks.py

Specifically targets hook configurations against the verified April-2026 list of real Claude Code hook events. Catches the fictional events that earlier versions of this plugin propagated (`PostToolUseFailure`, `SubagentStart`, `Setup`, `InstructionsLoaded`).

```bash
python3 scripts/validate-hooks.py <path-to-settings.json>
python3 scripts/validate-hooks.py <directory> --recursive
python3 scripts/validate-hooks.py <path> --json
```

**Catches:**
- Hook events not in Claude Code's documented event list
- Stop hooks with `exit 2` and no guard logic (potential infinite loop)
- Wrong handler array shape
- Use of experimental Agent Teams events without acknowledging the experimental flag

For each invalid event, the script suggests the most likely intended replacement (e.g., `PostToolUseFailure` → "use PostToolUse and inspect tool result").

## check-mcp-config.py

Validates `.mcp.json` files for syntax + common configuration mistakes.

```bash
python3 scripts/check-mcp-config.py <path-to-.mcp.json>
python3 scripts/check-mcp-config.py <directory>          # finds .mcp.json recursively
python3 scripts/check-mcp-config.py <path> --check-env   # also verify referenced env vars are set
python3 scripts/check-mcp-config.py <path> --json
```

**Catches:**
- Invalid JSON
- Missing top-level `mcpServers` object
- Servers with neither stdio (`command`) nor http (`type: "http"` + `url`)
- Env var references in `$VAR` form (Claude Code expects `${VAR}`)
- Hardcoded secrets (heuristic on long token-shaped strings + literal bearer headers)
- Missing `cmd /c` wrapping for npx-based servers on Windows
- Optionally: env vars referenced but not currently set in the user's shell

## When the skills run these scripts

| Skill | Script | When |
|---|---|---|
| `scaffold-company` | `audit-structure.py --skip-projects` | After scaffolding, to verify what was created |
| `scaffold-project` | `audit-structure.py` (focused on the new project) | After scaffolding |
| `configure-hooks` | `validate-hooks.py` | After writing settings.json |
| `configure-mcp` | `check-mcp-config.py` | After writing .mcp.json |
| `add-function-agent` | both | After adding the agent + MCP entry |
| (existing) `company-auditor` agent | `audit-structure.py --json` | First step of every audit; agent reserves judgment for things scripts can't check |

## What these scripts deliberately do NOT do

- **Do not modify files.** They report; the user (or a downstream skill) decides what to change.
- **Do not judge "good" vs "bad" architecture.** Mechanical checks only.
- **Do not validate the *content* of CLAUDE.md** — they only check it exists and is non-empty.
- **Do not test that hooks actually work** when fired. They check the events are real and the handler shape is sane.
- **Do not validate that an MCP server starts cleanly** — they check the config syntax and obvious mistakes. Use `claude mcp` or `/mcp` in Claude Code to verify connectivity.
