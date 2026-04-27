---
name: op-ssh-keys
description: Use this skill when the user is generating, retrieving, importing, or using SSH keys stored in 1Password — anything involving the `SSH Key` item category, the `--ssh-generate-key` flag, the `?ssh-format=openssh` query parameter, the 1Password SSH agent, signing git commits with a 1Password key, or using a 1Password-stored key for `ssh`/`scp`/`rsync`/`git`.
version: 1.0.0
---

# SSH keys in 1Password

Two distinct use cases:

1. **1Password SSH agent** — keys live in 1Password; the desktop app exposes them via the SSH agent protocol. `ssh` / `git` use them transparently. Best for daily work. **No CLI needed for daily use** once configured.
2. **CLI export** — extract a key to a file or stdout via `op read`. Best for CI/CD, server provisioning, or one-off uses where the agent isn't available.

Requires CLI v2.20.0+.

## Generating a key

```bash
op item create --category="SSH Key" --title="GitHub deploy" --vault=Infra \
  --ssh-generate-key=ed25519
```

Supported types: `ed25519` (default), `rsa`, `rsa2048`, `rsa3072`, `rsa4096`. The CLI:
- Generates the key.
- Stores it as a new item in the named vault (or Personal/Private/Employee if `--vault` omitted).
- Prints the **public key** to stdout (private key is redacted).

Want the public key into a file:
```bash
op item create --category="SSH Key" --title="GitHub deploy" --vault=Infra \
  --ssh-generate-key=ed25519 --format=json | jq -r '.fields[] | select(.id=="public_key") | .value' > deploy.pub
```

## Importing an existing key

The CLI doesn't import existing keys — use the 1Password desktop app (drag-and-drop or paste). Once stored, all the read/use patterns below work the same.

## Retrieving a key

### Public key only

```bash
op read "op://Infra/GitHub deploy/public key"
```

### Private key in OpenSSH format (for `ssh`/`git`/etc.)

```bash
op read "op://Infra/GitHub deploy/private key?ssh-format=openssh"
```

The `?ssh-format=openssh` query parameter is required — without it, you get the raw key in 1Password's storage format which most tools can't use.

### Private key to a file with correct mode

```bash
op read --out-file ~/.ssh/id_deploy "op://Infra/GitHub deploy/private key?ssh-format=openssh"
# op already sets file-mode 0600 by default
ssh -i ~/.ssh/id_deploy git@github.com
```

`--file-mode 0600` is the default for `op read --out-file` — don't override unless you have a reason.

## Using the 1Password SSH agent (recommended for local dev)

Setup once:

1. In the 1Password app: **Settings > Developer** → enable "Use the SSH agent".
2. Configure your shell to use the 1Password agent socket. On macOS:
   ```bash
   export SSH_AUTH_SOCK=~/Library/Group\ Containers/2BUA8C4S2C.com.1password/t/agent.sock
   ```
   On Windows: agent runs on a named pipe; configure OpenSSH-for-Windows to use it (see 1Password docs).
   On Linux: agent socket lives at `~/.1password/agent.sock`.

3. Add to `~/.ssh/config`:
   ```
   Host *
     IdentityAgent ~/.1password/agent.sock
   ```

After this, `ssh`, `git`, `rsync`, `scp` all use 1Password keys with biometric approval per use. **No CLI commands at runtime.**

## Signing git commits

```bash
git config --global gpg.format ssh
git config --global user.signingkey "$(op read 'op://Personal/Git Signing/public key')"
git config --global commit.gpgsign true
git commit -S -m "signed commit"
```

For verification, add the public key to GitHub/GitLab as a "Signing key" (separate from "Authentication key").

## CI / one-shot deploy server access

Service account + `op read --out-file`:

```bash
export OP_SERVICE_ACCOUNT_TOKEN="ops_..."
op read --out-file deploy_key "op://CI/deploy-bot/private key?ssh-format=openssh"
trap 'shred -u deploy_key 2>/dev/null || rm -f deploy_key' EXIT
ssh -i deploy_key -o IdentitiesOnly=yes deploy@server.example.com 'systemctl restart app'
```

Or stream the key into `ssh-add` for the duration of a job (no file on disk):

```bash
eval "$(ssh-agent -s)"
op read "op://CI/deploy-bot/private key?ssh-format=openssh" | ssh-add -
ssh -o IdentitiesOnly=yes deploy@server.example.com 'systemctl restart app'
ssh-agent -k
```

## Patterns for common tools

### Ansible
```bash
op read --out-file /tmp/ansible_key "op://Infra/Ansible/private key?ssh-format=openssh"
ANSIBLE_PRIVATE_KEY_FILE=/tmp/ansible_key ansible-playbook site.yml
shred -u /tmp/ansible_key
```

### Terraform (remote-exec)
```hcl
provisioner "remote-exec" {
  connection {
    host        = self.public_ip
    user        = "ubuntu"
    private_key = file("${path.module}/.terraform_key")
  }
}
```
```bash
op read --out-file .terraform_key "op://Infra/Terraform/private key?ssh-format=openssh"
trap 'rm -f .terraform_key' EXIT
terraform apply
```

### rsync
```bash
rsync -e "ssh -i <(op read 'op://Infra/Backup/private key?ssh-format=openssh')" \
  -av ./build/ deploy@server:/var/www/
```
(Process substitution `<(...)` works on bash/zsh; not on POSIX `sh`.)

## Gotchas

1. **Always include `?ssh-format=openssh`** when reading a private key for use with OpenSSH tools. Without it the format is unusable.
2. **Don't `chmod 600` after `op read --out-file`** — the file is already 0600. `chmod 644` would break SSH.
3. **The CLI can't import existing keys.** Use the desktop app.
4. **`op item edit` doesn't work on SSH Key items.** Edit them in the desktop app, or delete + recreate via CLI.
5. **`SSH_AUTH_SOCK` is per-shell.** Add the export to your shell rc file or use systemd user services on Linux.
6. **Public-key-only access for verification:** `op read 'op://.../public key'` — no `?ssh-format=` needed.
7. **Service accounts can use SSH Key items** if the items are in vaults the service account has read access to. Personal vaults are off-limits.
