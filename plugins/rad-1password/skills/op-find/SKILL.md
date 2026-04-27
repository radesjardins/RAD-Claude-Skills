---
name: op-find
description: Find 1Password items by name across all accessible vaults. Returns name, vault, category, and ID for each match.
argument-hint: "<query> [--vault <vault>] [--category <category>]"
allowed-tools: Bash(op item list:*), Bash(op vault list:*)
---

# /op-find

Search for 1Password items by name (case-insensitive substring match).

## Inputs

`$ARGUMENTS` is the search query plus optional flags. Treat the first word as the query and pass through any `--vault` or `--category` flags.

## Steps

1. Run a list across all accessible vaults (or scoped if flags are present):
   ```bash
   op item list --format=json [--vault <vault>] [--categories <category>]
   ```

2. Filter the JSON for items whose `title` contains the query string (case-insensitive). Match `tags` too if no title hits.

3. Print a table:
   ```
   TITLE                          VAULT       CATEGORY        ID
   GitHub deploy                  Infra       SSH Key         abc123...
   ```

4. If results > 20, print top 20 sorted by exact-match-first then alphabetical, and note "showing 20 of N".

5. If 0 results: list the vaults searched ("Searched: Personal, Work, Prod (3 vaults)") so the user knows the query was answered, just empty.

## On failure

- If `op item list` fails with auth error: suggest `/op-signin`.
- If a service account is in use and no `--vault` is provided: list vaults the service account can see (`op vault list`), then re-run the search across each of them and merge results.
