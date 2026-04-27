---
name: op-provisioning
description: Use this skill when the user is provisioning, suspending, deleting, or recovering 1Password users; managing groups; granting or revoking vault permissions for users or groups; performing bulk onboarding/offboarding; or auditing access. Triggers include `op user`, `op group`, `op vault user`, `op vault group`, "invite a user", "remove a user from 1Password", "onboarding", "offboarding", "vault permissions".
version: 1.0.0
---

# Provisioning, groups, and vault permissions

Requires a 1Password Business or Teams account. Some operations (CLI provisioning) require enabling **Settings > Provisioning > CLI Provisioning** at <https://start.1password.com>, and the calling user must be in the **Provision Managers** group (or a custom group with the relevant permissions).

## User states

| State | Meaning | How you got here |
|---|---|---|
| `ACTIVE` | Normal active user. | Confirmed after accepting invite. |
| `TRANSFER_STARTED` | Provisioned, hasn't accepted invite yet. | After `op user provision`. |
| `TRANSFER_SUSPENDED` | Provisioned but didn't accept and was deprovisioned. | Auto-deprovision of pending. |
| `RECOVERY_STARTED` | Admin started account recovery. | After `op user recovery begin`. |
| `RECOVERY_ACCEPTED` | User created new password; awaiting admin completion. | After user follows recovery email. |
| `SUSPENDED` | Active user temporarily blocked. | After `op user suspend`. |

`op user list` and `op user get` show the state.

## `op user`

```
op user provision --name "Wendy Appleseed" --email wendy@example.com [--language en]
op user confirm   "Wendy Appleseed"        # or --all
op user get       "Wendy Appleseed"        # by name, email, or ID
op user list      [--group <id>] [--vault <id>]
op user edit      "Wendy Appleseed" --name "Wendy A. Appleseed"   # or --travel-mode-on/off
op user suspend   "Wendy Appleseed" [--deauthorize-devices-after 10m]   # max 24h
op user reactivate "Wendy Appleseed"
op user delete    "Wendy Appleseed"        # PERMANENT
op user recovery begin <user-id> [<user-id>...]   # up to 10 at once
```

### Onboarding workflow

```bash
# 1. Provision (sends invite email)
op user provision --name "New Hire" --email new.hire@example.com

# 2. They accept the email invitation in their browser.

# 3. Confirm — completes provisioning. Until confirmed, the user has no access.
op user confirm "New Hire"
# Or batch:
op user confirm --all

# 4. Add to relevant groups (this is what actually grants vault access).
op group user grant --group Engineering --user new.hire@example.com

# 5. (Optional) Direct vault permission, if not group-managed.
op vault user grant --vault "Engineering Shared" --user new.hire@example.com \
  --permissions allow_viewing,allow_editing
```

### Offboarding workflow

```bash
# Immediate: suspend (revokes access, keeps data, doesn't bill).
op user suspend "Departing User" --deauthorize-devices-after 1h

# After data review:
op user delete "Departing User"   # destroys their data; cannot be undone
```

`suspend` is reversible (`reactivate`); `delete` is not. Always `suspend` first, audit, then `delete`.

### Recovery workflow

When a user can't access their account (lost device + secret key):

```bash
# Admin: start recovery
op user recovery begin <user-id>

# User receives email, clicks "Recover my account", chooses a new password.
# State -> RECOVERY_ACCEPTED.

# Admin: complete in the 1Password app (no CLI command for completion as of v2.34.0)
# or, on accounts where supported, op user recovery complete <user-id>.
```

Recovery resets MFA. The user must re-authenticate on every device.

## `op group`

```
op group create "Engineering" [--description "Backend team"]
op group get    "Engineering"
op group edit   "Engineering" --name "Backend Engineering"
op group list   [--user <id>] [--vault <id>]
op group delete "Engineering"

op group user grant  --group "Engineering" --user new.hire@example.com [--role member|manager]
op group user revoke --group "Engineering" --user new.hire@example.com
op group user list   --group "Engineering"
```

The **Provision Managers** built-in group is required to run `op user provision/confirm`. Add yourself or your service account to it once:

```bash
op group user grant --group "Provision Managers" --user me@example.com
```

## Vault permissions

### The model

- **1Password Teams / Families**: three permissions — `allow_viewing`, `allow_editing`, `allow_managing`.
- **1Password Business**: granular set, with the three "allow_*" being aliases.

### Granular permissions (Business)

| Permission | Grants | Requires |
|---|---|---|
| `view_items` | View items in vault. | (base) |
| `view_and_copy_passwords` | View concealed values + copy. | `view_items` |
| `view_item_history` | See and restore previous versions. | `view_and_copy_passwords`, `view_items` |
| `create_items` | Create new items. | `view_items` |
| `edit_items` | Modify items. | `view_and_copy_passwords`, `view_items` |
| `archive_items` | Archive items. | `edit_items`, `view_and_copy_passwords`, `view_items` |
| `delete_items` | Delete items. | `edit_items`, `view_and_copy_passwords`, `view_items` |
| `import_items` | Move/copy items into vault. | `create_items`, `view_items` |
| `export_items` | Export items to unencrypted file. | `view_item_history`, `view_and_copy_passwords`, `view_items` |
| `copy_and_share_items` | Copy between vaults / share externally. | `view_item_history`, `view_and_copy_passwords`, `view_items` |
| `print_items` | Print contents. | `view_item_history`, `view_and_copy_passwords`, `view_items` |
| `manage_vault` | Grant/revoke access, delete vault. | (always granted to vault owners) |

### Aliases

- `allow_viewing` = `view_items + view_and_copy_passwords + view_item_history`
- `allow_editing` = `create_items + edit_items + archive_items + delete_items + import_items + export_items + copy_and_share_items + print_items`
- `allow_managing` = `manage_vault`

### Granting

```bash
# Teams / Families syntax
op vault user grant  --vault "Prod Secrets" --user me@example.com \
  --permissions allow_viewing,allow_editing

op vault group grant --vault "Prod Secrets" --group "Engineering" \
  --permissions allow_viewing
```

```bash
# Business — granular
op vault user grant --vault "Prod Secrets" --user me@example.com \
  --permissions view_items,view_and_copy_passwords,view_item_history,export_items \
  --no-input
```

`--no-input` is required in non-interactive shells (CI). When you pass dependent permissions, list **all** of them — the CLI rejects half-specified sets.

### Revoking

```bash
# Revoke specific permissions
op vault user revoke --vault "Prod Secrets" --user me@example.com \
  --permissions edit_items,delete_items

# Revoke all access
op vault user revoke --vault "Prod Secrets" --user me@example.com

# Same for groups
op vault group revoke --vault "Prod Secrets" --group "Engineering"
```

### Listing access

```bash
op vault user list  --vault "Prod Secrets"
op vault group list --vault "Prod Secrets"
op user list  --vault "Prod Secrets"          # users with any access
op group list --vault "Prod Secrets"
```

## Vaults

```bash
op vault create "App Prod" \
  --description "Production app secrets" \
  --icon vault-door \
  [--allow-admins-to-manage true|false]

op vault edit   "App Prod" --name "Application — Production" --icon castle
op vault get    "App Prod"
op vault list   [--user <id>] [--group <id>]
op vault delete "App Prod"
```

Valid icon keywords (from `op vault create --help`):
```
airplane, application, art-supplies, bankers-box, brown-briefcase, brown-gate,
buildings, cabin, castle, circle-of-dots, coffee, color-wheel, curtained-window,
document, doughnut, fence, galaxy, gears, globe, green-backpack, green-gem,
handshake, heart-with-monitor, house, id-card, jet, large-ship, luggage, plant,
porthole, puzzle, rainbow, record, round-door, sandals, scales, screwdriver,
shop, tall-window, treasure-chest, vault-door, vehicle, wallet, wrench
```

## Bulk operations

### Bulk onboard from a CSV

```bash
# new_users.csv:  name,email
while IFS=, read -r name email; do
  op user provision --name "$name" --email "$email"
done < new_users.csv

# Confirm them all once they've accepted
op user confirm --all
```

### Audit who has access to a vault

```bash
op vault user list  --vault "Prod Secrets" --format=json | jq '.[] | {name, email, permissions}'
op vault group list --vault "Prod Secrets" --format=json | jq '.[] | {name, permissions}'
```

### Audit a user's access

```bash
op vault list --user user@example.com --format=json | jq '.[].name'
op group list --user user@example.com --format=json | jq '.[].name'
```

## Gotchas

1. **Provisioned ≠ confirmed.** A user who's been `provisioned` has zero access until you `confirm` them.
2. **`delete` is permanent.** Always `suspend` first to give yourself a recovery window.
3. **Group membership is the right unit for vault access.** Granting to individual users scales poorly; grant to a group, change membership.
4. **Dependent permissions must be listed together.** The CLI rejects partial sets.
5. **`Provision Managers` is required for `op user provision/confirm`** — your service account or admin user needs to be in it.
6. **You can't use service accounts to provision users** as of CLI v2.x — use a real admin signed in via desktop app for provisioning operations.
