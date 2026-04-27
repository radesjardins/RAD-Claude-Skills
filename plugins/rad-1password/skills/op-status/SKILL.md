---
name: op-status
description: Quick 1Password CLI status — current account and accessible vaults.
argument-hint: ""
allowed-tools: Bash(op whoami:*), Bash(op vault list:*), Bash(op account list:*), Bash(op --version:*)
---

# /op-status

Print a concise status report:

1. CLI version:
   ```bash
   op --version
   ```

2. Current auth identity:
   ```bash
   op whoami
   ```
   If this fails, report "Not signed in" and suggest `/op-signin`.

3. Locally configured accounts:
   ```bash
   op account list
   ```

4. Accessible vaults (the most useful "am I in the right account?" check):
   ```bash
   op vault list --format=json
   ```
   Pretty-print as a list with vault name, ID, and item count where available.

5. If `OP_SERVICE_ACCOUNT_TOKEN` is set in the environment, mention that the user is auth'd as a service account (not via desktop app).

Keep the report under 20 lines. No prose summary — just the data.
