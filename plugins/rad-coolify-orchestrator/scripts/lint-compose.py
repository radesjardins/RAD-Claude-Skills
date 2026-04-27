#!/usr/bin/env python3
"""
lint-compose.py — Coolify-specific docker-compose validator.

Catches the patterns the coolify-reviewer agent currently checks subjectively
on docker-compose files, plus Coolify-specific concerns (port conflicts with
80/443/8000, coolify network reference, etc.).

Used by:
  - coolify-reviewer agent (Step 3 Docker Compose Review)
  - Standalone CLI

Usage:
  python3 lint-compose.py <path-to-compose.yml>
  python3 lint-compose.py <project-root>           # finds compose files recursively
  python3 lint-compose.py <path> --json
  python3 lint-compose.py <path> --strict           # promote SUGGESTION to WARNING

Exit codes:
  0  no issues
  1  issues found
  2  script error

Pure stdlib Python 3.8+. Uses a minimal YAML parser since this is a single-script
distribution (no PyYAML dependency). The parser handles the subset of YAML
docker-compose actually uses (mapping, sequence, scalar). Edge cases that the
parser can't handle fall through with a parse warning rather than crashing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

# Try to use PyYAML if available for robustness; fall back to a minimal parser
try:
    import yaml  # type: ignore
    HAS_PYYAML = True
except ImportError:
    HAS_PYYAML = False


# Coolify reserves these ports on the host
COOLIFY_RESERVED_PORTS = {80, 443, 8000, 6001, 6002}

SECRET_LIKE_NAMES = re.compile(
    r"(?:^|_)(SECRET|TOKEN|KEY|PASSWORD|PASSWD|PWD|API[-_]?KEY|ACCESS[-_]?KEY|"
    r"PRIVATE[-_]?KEY|AUTH|CREDENTIAL|DATABASE_URL)(?:_|$)",
    re.IGNORECASE,
)
SECRET_LIKE_VALUE = re.compile(
    r"\b(?:sk_live_|sk_test_|pk_live_|gh[ousp]_|ghp_|xoxb-|xoxp-|AIza[0-9A-Za-z_-]{35}|"
    r"AKIA[0-9A-Z]{16}|[A-Za-z0-9+/]{40,})",
)


@dataclass
class Finding:
    severity: str
    category: str
    service: str | None
    message: str
    fix: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def minimal_yaml_load(text: str) -> dict:
    """Tiny YAML parser supporting the subset docker-compose uses.
    Handles: mappings, sequences, inline strings, basic scalars.
    Doesn't handle: anchors, complex multi-line strings, complex flow style.
    """
    if HAS_PYYAML:
        try:
            return yaml.safe_load(text) or {}
        except yaml.YAMLError:
            return {}

    # Minimal fallback parser
    lines = text.splitlines()
    root: dict = {}
    stack: list[tuple[int, dict | list]] = [(-1, root)]

    def get_indent(s: str) -> int:
        return len(s) - len(s.lstrip(" "))

    for raw_line in lines:
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = get_indent(line)
        content = line.strip()

        # Pop stack to current indent level
        while stack and stack[-1][0] >= indent:
            stack.pop()
        if not stack:
            stack = [(-1, root)]
        parent = stack[-1][1]

        if content.startswith("- "):
            # Sequence item
            value = content[2:].strip()
            if not isinstance(parent, list):
                # Convert (probably the parent should have been initialized as a list)
                continue
            if ":" in value and not (value.startswith('"') or value.startswith("'")):
                # Inline mapping in list item: "- key: value"
                k, _, v = value.partition(":")
                item = {k.strip(): v.strip() or {}}
                parent.append(item)
                stack.append((indent, item))
            else:
                parent.append(value)
        elif ":" in content:
            key, sep, value = content.partition(":")
            key = key.strip()
            value = value.strip()
            if not value or value.startswith("#"):
                # Block — children come on next lines
                # Look ahead at next non-blank line to decide list vs map
                next_indent = None
                next_starts_dash = False
                for nl in lines[lines.index(raw_line)+1:]:
                    if nl.strip() and not nl.lstrip().startswith("#"):
                        next_indent = get_indent(nl)
                        next_starts_dash = nl.lstrip().startswith("- ")
                        break
                if next_indent is not None and next_indent > indent:
                    new_container: dict | list = [] if next_starts_dash else {}
                    if isinstance(parent, dict):
                        parent[key] = new_container
                    elif isinstance(parent, list):
                        parent.append({key: new_container})
                    stack.append((indent, new_container))
                else:
                    if isinstance(parent, dict):
                        parent[key] = None
            else:
                # Inline value
                # Strip quotes
                if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                if isinstance(parent, dict):
                    parent[key] = value
                elif isinstance(parent, list):
                    parent.append({key: value})
    return root


def lint(data: dict, strict: bool) -> list[Finding]:
    findings: list[Finding] = []

    if not isinstance(data, dict):
        findings.append(Finding(
            severity="WARNING", category="parse", service=None,
            message="Could not parse docker-compose YAML — top-level not a mapping",
            fix="Verify YAML syntax (try `docker compose config`).",
        ))
        return findings

    services = data.get("services", {})
    if not isinstance(services, dict) or not services:
        findings.append(Finding(
            severity="WARNING", category="structure", service=None,
            message="No 'services' block found",
            fix="docker-compose files require a 'services' top-level key with at least one service.",
        ))
        return findings

    networks = data.get("networks", {}) or {}
    has_coolify_network = "coolify" in networks if isinstance(networks, dict) else False

    for service_name, service in services.items():
        if not isinstance(service, dict):
            continue
        check_service(service_name, service, has_coolify_network, strict, findings)

    return findings


def check_service(name: str, service: dict, has_coolify_network: bool, strict: bool, findings: list[Finding]) -> None:
    # restart policy
    restart = service.get("restart")
    if not restart:
        findings.append(Finding(
            severity="WARNING", category="reliability", service=name,
            message=f"Service '{name}' has no restart policy",
            fix=f"Add 'restart: unless-stopped' to '{name}' so it auto-recovers from container crashes "
                "and host reboots. Coolify expects this for production services.",
        ))
    elif restart == "no":
        findings.append(Finding(
            severity="SUGGESTION", category="reliability", service=name,
            message=f"Service '{name}' uses 'restart: no' — won't auto-recover",
            fix="Use 'restart: unless-stopped' unless this is a one-shot job container.",
        ))

    # healthcheck
    healthcheck = service.get("healthcheck")
    if not healthcheck:
        # Only warn if this isn't an obviously stateless one-shot
        image = service.get("image", "")
        if "init" not in name.lower() and "migrate" not in name.lower():
            findings.append(Finding(
                severity="WARNING", category="coolify-compatibility", service=name,
                message=f"Service '{name}' has no healthcheck — Coolify rolling updates need this for zero-downtime",
                fix=f"Add a healthcheck block to '{name}': test command, interval, timeout, retries. "
                    "See coolify-deploy SKILL for the standard pattern.",
            ))

    # ports — check for conflicts and binding patterns
    ports = service.get("ports", [])
    if isinstance(ports, list):
        for port_entry in ports:
            check_port(name, port_entry, findings)

    # environment — check for hardcoded secrets
    env = service.get("environment", {})
    if isinstance(env, dict):
        for k, v in env.items():
            check_env_var(name, str(k), str(v) if v is not None else "", findings)
    elif isinstance(env, list):
        for entry in env:
            if isinstance(entry, str) and "=" in entry:
                k, _, v = entry.partition("=")
                check_env_var(name, k.strip(), v.strip(), findings)

    # privileged mode
    if service.get("privileged") is True or service.get("privileged") == "true":
        findings.append(Finding(
            severity="CRITICAL", category="security", service=name,
            message=f"Service '{name}' runs in --privileged mode — disables container isolation",
            fix="Remove 'privileged: true' unless absolutely necessary. If a specific capability is needed, "
                "use 'cap_add: [SPECIFIC_CAP]' instead.",
        ))

    # cap_add for sensitive caps
    cap_add = service.get("cap_add", [])
    if isinstance(cap_add, list):
        sensitive_caps = {"ALL", "SYS_ADMIN", "NET_ADMIN", "DAC_OVERRIDE"}
        for cap in cap_add:
            if str(cap).upper() in sensitive_caps:
                findings.append(Finding(
                    severity="WARNING", category="security", service=name,
                    message=f"Service '{name}' adds cap '{cap}' — high-privilege capability",
                    fix=f"Verify '{cap}' is actually needed. Consider least-privilege alternatives.",
                ))

    # volume declarations for stateful services
    image = str(service.get("image", "")).lower()
    stateful_signals = ("postgres", "mysql", "mariadb", "mongodb", "mongo", "redis", "clickhouse")
    if any(s in image for s in stateful_signals) or any(s in name.lower() for s in stateful_signals):
        volumes = service.get("volumes", [])
        if not volumes:
            findings.append(Finding(
                severity="CRITICAL", category="data-loss", service=name,
                message=f"Stateful service '{name}' (image: {image}) has no volume mount — data lost on container removal",
                fix=f"Add a named volume: 'volumes: [\"{name}-data:/var/lib/postgresql/data\"]' (adjust path per engine).",
            ))

    # network attachment for coolify-managed services
    nets = service.get("networks", [])
    if has_coolify_network and isinstance(nets, list) and "coolify" not in nets:
        findings.append(Finding(
            severity="SUGGESTION" if not strict else "WARNING",
            category="coolify-compatibility", service=name,
            message=f"Service '{name}' is not on the 'coolify' network — won't be reachable by Traefik",
            fix=f"Add 'coolify' to the networks list for '{name}' if you want Coolify's proxy to route to it.",
        ))


def check_port(service_name: str, entry, findings: list[Finding]) -> None:
    """Validate a port entry. Accepts str ('8080:80'), int (8080), or dict shorthand."""
    if isinstance(entry, dict):
        host = entry.get("published")
        target = entry.get("target")
    elif isinstance(entry, int):
        host = entry
        target = entry
    elif isinstance(entry, str):
        # Handle "host:target" or "ip:host:target" or "target"
        parts = entry.split(":")
        if len(parts) == 1:
            host = target = parts[0]
        elif len(parts) == 2:
            host, target = parts
        elif len(parts) == 3:
            host = parts[1]
            target = parts[2]
        else:
            return
    else:
        return

    try:
        host_port = int(str(host).split("/")[0])
    except (ValueError, AttributeError):
        return

    if host_port in COOLIFY_RESERVED_PORTS:
        findings.append(Finding(
            severity="CRITICAL", category="coolify-compatibility", service=service_name,
            message=f"Service '{service_name}' binds host port {host_port} — collides with Coolify's reserved ports "
                    f"({sorted(COOLIFY_RESERVED_PORTS)})",
            fix="Don't bind host ports for Coolify-managed services. Let Coolify's Traefik route via "
                "domain configured in the UI. If you need a host port, choose one outside the reserved range.",
        ))
    elif host_port < 1024:
        findings.append(Finding(
            severity="WARNING", category="security", service=service_name,
            message=f"Service '{service_name}' binds privileged host port {host_port} (<1024)",
            fix="Use a port ≥1024 unless you specifically need a well-known port. Privileged ports require root.",
        ))


def check_env_var(service_name: str, var_name: str, value: str, findings: list[Finding]) -> None:
    if not value:
        return
    # Skip env interpolation references like ${VAR} or $VAR
    if value.startswith("$") or "${" in value:
        return

    if SECRET_LIKE_NAMES.search(var_name) and value not in ("", "placeholder", "change-me", "TODO"):
        findings.append(Finding(
            severity="CRITICAL", category="security", service=service_name,
            message=f"Service '{service_name}' env var '{var_name}' has a hardcoded value — secret in committed file",
            fix=f"Replace with '${{{var_name}}}' and set the actual value via Coolify UI environment variables, "
                "or via .env file (in .gitignore).",
        ))
    elif SECRET_LIKE_VALUE.search(value):
        findings.append(Finding(
            severity="CRITICAL", category="security", service=service_name,
            message=f"Service '{service_name}' env var '{var_name}' value looks like a secret token",
            fix=f"Replace with '${{{var_name}}}' env var reference; never commit secrets to compose files.",
        ))


def render_text(report: dict) -> str:
    lines: list[str] = []
    lines.append(f"lint-compose: {report['file']}  (parser: {report['parser']})")
    findings = report["findings"]
    if not findings:
        lines.append("OK — no issues.")
        return "\n".join(lines)

    by_severity: dict[str, list[dict]] = {}
    for f in findings:
        by_severity.setdefault(f["severity"], []).append(f)

    lines.append("")
    lines.append(
        f"Issues: {len(findings)} total — "
        + ", ".join(f"{sev}: {len(by_severity[sev])}" for sev in ("CRITICAL", "WARNING", "SUGGESTION") if sev in by_severity)
    )
    for sev in ("CRITICAL", "WARNING", "SUGGESTION"):
        for f in by_severity.get(sev, []):
            label = f"[{f['service']}]" if f.get("service") else "[plan-level]"
            lines.append(f"  {sev:11} {label:20} ({f['category']}) {f['message']}")
            if f["fix"]:
                lines.append(f"      fix: {f['fix']}")
    return "\n".join(lines)


def find_compose_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    if target.is_dir():
        results: list[Path] = []
        for pattern in ("docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml",
                        "docker-compose.*.yml", "docker-compose.*.yaml"):
            results.extend(target.rglob(pattern))
        return [p for p in results if not any(part in {"node_modules", ".git", "vendor"} for part in p.parts)]
    return []


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", help="Path to a docker-compose file or directory")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    p.add_argument("--strict", action="store_true", help="Promote SUGGESTION to WARNING")
    args = p.parse_args(argv)

    target = Path(args.path).resolve()
    if not target.exists():
        print(f"error: not found: {target}", file=sys.stderr)
        return 2

    files = find_compose_files(target)
    if not files:
        print(f"error: no compose files found at {target}", file=sys.stderr)
        return 2

    parser_name = "PyYAML" if HAS_PYYAML else "stdlib-fallback"
    all_reports: list[dict] = []
    any_blocking = False
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        data = minimal_yaml_load(text)
        findings = lint(data, args.strict)
        if any(fd.severity in ("CRITICAL", "WARNING") for fd in findings):
            any_blocking = True
        all_reports.append({"file": str(f), "parser": parser_name, "findings": [fd.to_dict() for fd in findings]})

    if args.json:
        print(json.dumps({"reports": all_reports, "parser": parser_name}, indent=2))
    else:
        for r in all_reports:
            print(render_text(r))
            print()

    return 1 if any_blocking else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
