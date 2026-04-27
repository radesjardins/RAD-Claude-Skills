---
name: op-item-management
description: Use this skill when the user is creating, editing, getting, listing, deleting, archiving, sharing, or moving 1Password items via the CLI — anything involving `op item create`, `op item edit`, `op item get`, `op item list`, `op item delete`, `op item move`, `op item share`, `op item template`, `op document`, item field types, item categories, JSON item templates, assignment statements, or generating passwords with the CLI.
version: 1.0.0
---

# `op item` — item CRUD

## The 20 categories

```
API Credential   Bank Account            Credit Card
Database         Document                Driver License
Email Account    Identity                Login
Membership       Outdoor License         Passport
Password         Reward Program          Secure Note
Server           Social Security Number  Software License
SSH Key          Wireless Router
```

Use exactly these names with `--category` (case-insensitive, whitespace-insensitive). For SSH Keys see the `op-ssh-keys` sub-skill.

## Two ways to set fields: assignment statements vs JSON template

### Assignment statements (quick, but visible to other processes)

Syntax:
```
[<section>.]<field>[<fieldType>]=<value>
```

- Section is optional unless multiple sections share a field name.
- `fieldType` in `[brackets]` for custom fields. Built-in fields don't need it.
- Escape `.`, `=`, `\` in section/field NAMES with backslash. Don't escape values.

Field types that go in brackets:

| `fieldType` | Field |
|---|---|
| `text` | plain string |
| `password` | concealed |
| `email` | email |
| `url` | URL |
| `phone` | phone |
| `date` | `YYYY-MM-DD` |
| `monthyear` | `YYYY/MM` |
| `otp` | `otpauth://...` URI |
| `file` | path to file (attachment) |

**Caveat:** assignment values appear in the parent shell's argv (visible via `ps`, kept in shell history). For sensitive values, use a JSON template instead.

### JSON template (recommended for sensitive values)

```bash
op item template get Login --out-file login.json
# edit login.json — set values for each field
op item create --template login.json
rm login.json
```

The same JSON shape returned by `op item get <item> --format json` works as a template. Use this to clone items between vaults or accounts:

```bash
op item get "My Login" --format json --account work | \
  op item create --account personal --vault Personal -
```

Pipe input replaces `--template`. Don't use both.

### Combining the two

```bash
op item create --template login.json username=actual-user@example.com
```

Assignment statements override the template's values for those keys.

## `op item create`

```
op item create [- | --template <path>] [<assignment>...] [flags]
```

| Flag | Purpose |
|---|---|
| `--category <name>` | Set category. |
| `--title <title>` | Set name. |
| `--vault <vault>` | Target vault (defaults to Private/Personal/Employee). **Required for service accounts.** |
| `--url <url>` | Set URL field (Login/Password/API Credential). |
| `--tags a,b,c` | Comma-separated tags. |
| `--generate-password[=recipe]` | Auto-generate. Default 32 chars w/ letters,digits,symbols. Recipe e.g. `letters,digits,symbols,40` or `letters,digits,20`. Length must be 1–64. |
| `--ssh-generate-key <type>` | `ed25519` (default), `rsa`, `rsa2048`, `rsa3072`, `rsa4096`. |
| `--template <path>` | JSON template. |
| `--favorite` | Mark as favorite. |
| `--reveal` | Print concealed values in output. |
| `--dry-run` | Preview without creating. |

### Examples

Login with generated password:
```bash
op item create --category=Login --title="Acme" --vault=Work \
  --url=https://acme.example.com \
  --generate-password=letters,digits,symbols,40 \
  username=jane@example.com
```

API Credential with custom fields:
```bash
op item create --category="API Credential" --title="Stripe Live" --vault=Prod \
  --tags=production,billing \
  username=acct_123 \
  credential=sk_live_xxx \
  "Notes.Webhook URL[url]=https://hooks.acme.com/stripe"
```

Database with section and OTP:
```bash
op item create --category=Database --title="Postgres prod" --vault=Prod \
  type=postgresql \
  username=app \
  password=hunter2 \
  "Server.host[text]=db.prod.example.com" \
  "Server.port[text]=5432" \
  "Server.database[text]=app_prod" \
  "MFA.totp[otp]=otpauth://totp/Postgres?secret=JBSWY3DPEBLW64TMMQ&issuer=Acme"
```

Login with file attachment:
```bash
op item create --category=Login --title="VPN" --vault=Work \
  username=jane \
  "config[file]=/etc/openvpn/client.ovpn"
```

Secure Note:
```bash
op item create --category="Secure Note" --title="Recovery codes" --vault=Personal \
  notesPlain="$(cat recovery.txt)"
rm recovery.txt
```

## `op item edit`

```
op item edit { <name> | <id> | <shareLink> } [<assignment>...] [flags]
```

Same flags as `create` minus `--category` and `--ssh-generate-key`. Plus a few specifics:

- **Update a field's value:** `field=newvalue`
- **Change field type without value:** `field[password]`
- **Change both:** `field[monthyear]=2026/04`
- **Delete a custom field:** `section.field[delete]`. If a section ends up empty, the section is removed.
- **Built-in fields can't be deleted, only emptied:** `username=`

Examples:
```bash
op item edit "Acme" --generate-password=letters,digits,symbols,32
op item edit "Acme" --tags=production,external,reviewed
op item edit "Acme" --title="Acme (rotated 2026-04)"
op item edit "Stripe Live" "Notes.Old Key[delete]"
```

## `op item get`

```
op item get [{ <name> | <id> | <shareLink> | - }] [flags]
```

| Flag | Purpose |
|---|---|
| `--vault <vault>` | Limit search scope. Required for service accounts unless piping. |
| `--fields label=a,label=b` | Return specific fields. Supports `label=`, `type=`. Comma-separated. |
| `--otp` | Print primary OTP (no secret reference needed). |
| `--share-link` | Print a shareable link for the item. |
| `--include-archive` | Include archived items. |
| `--reveal` | Show concealed values. |

Examples:
```bash
op item get "Acme" --fields label=username,label=password --reveal --format=json
op item get Google --otp                     # current 6-digit code
op item get "Acme" --share-link              # shareable URL
op item list --tags work --format=json | op item get -   # bulk get from list
```

## `op item list` (alias `ls`)

```
op item list [flags]
```

| Flag | Purpose |
|---|---|
| `--vault <vault>` | Filter to one vault. |
| `--categories Login,Database` | **Plural**, comma-separated. |
| `--tags work/client-a` | Tag filter; nested tags include children. |
| `--favorite` | Favorites only. |
| `--include-archive` | Include archived. |
| `--long` | More detailed output. |
| `--format json\|csv` | Machine-readable. |

```bash
op item list --vault Prod --categories Login,Database --format=json
op item list --tags onboarding --format=csv
```

## `op item delete` (aliases `remove`, `rm`)

```
op item delete <item> [--archive] [--vault <vault>]
```

- Default: soft delete (recoverable from "Recently Deleted" for 30 days).
- `--archive`: move to Archive instead.

## `op item move`

```
op item move <item> --vault <source> --to-vault <dest>
```

Creates a copy in the destination vault and deletes the original. Permissions on both vaults required.

## `op item share`

```
op item share <item> [flags]
```

| Flag | Purpose |
|---|---|
| `--emails a@x.com,b@y.com` | Restrict to these recipients (else anyone with the link). |
| `--expires-in 7d` | Lifetime — `s`/`m`/`h`/`d`/`w`. Default `7d`. |
| `--view-once` | Expire after first view. |
| `--vault <vault>` | Source vault. |

```bash
op item share "Customer credentials" --emails=customer@example.com --expires-in=24h --view-once
```

**Limitations:** file attachments and `Document` items can't be shared. Subsequent edits to the item are not reflected in already-shared links.

## `op item template`

```bash
op item template list                          # all categories
op item template get Login                     # JSON template for Login
op item template get Login --out-file l.json
```

Use the template as a starting point for `--template` or as documentation of available built-in fields per category.

## `op document` — files as items

Documents are file attachments stored as their own items. Different from a `file` field on another item.

```bash
op document create ./report.pdf --vault Work --tags 2026,Q1
op document get "report" --vault Work --out-file ./report-from-1pw.pdf
op document edit "report" --file-path ./report-v2.pdf
op document delete "report" --archive
op document list
```

`op document create -` reads from stdin (use `--file-name` to set the saved name).

## Common gotchas

1. **Service accounts must specify `--vault`** for `op item get` (or pipe the item). They can't search across vaults like an interactive user.
2. **Assignment values land in shell history.** For real secrets use a JSON template + `rm` after.
3. **`--categories` (plural) for `list`, `--category` (singular) for `create`/`get`.**
4. **JSON templates don't carry passkeys.** Editing a passkey-bearing item via `--template` overwrites the passkey.
5. **`op item delete` is reversible for 30 days** via the desktop app's Recently Deleted view. `--archive` is permanent until manually restored.
