# =============================================================================
# Feature: Firewall Rule Auditor (Defense)
# What it does: Reads Windows Firewall rules and flags overly permissive entries.
# Defense value: Surfaces rules that allow "Any" source/port — common misconfigs.
# Platform: Windows only (uses netsh via subprocess).
# =============================================================================

import subprocess
import re


def get_firewall_rules() -> list[dict]:
    """Parse 'netsh advfirewall firewall show rule' output into dicts."""
    result = subprocess.run(
        ["netsh", "advfirewall", "firewall", "show", "rule", "name=all", "verbose"],
        capture_output=True, text=True
    )
    rules = []
    current = {}

    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            if current:
                rules.append(current)
                current = {}
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            current[key.strip()] = value.strip()

    if current:
        rules.append(current)

    return rules


def is_permissive(rule: dict) -> bool:
    """Flag rules that allow all remote addresses and/or all ports."""
    enabled = rule.get("Enabled", "No").lower() == "yes"
    action = rule.get("Action", "").lower() == "allow"
    remote_ip = rule.get("RemoteIP", "Any").strip().lower() == "any"
    remote_port = rule.get("RemotePort", "Any").strip().lower() == "any"
    return enabled and action and remote_ip and remote_port


def run():
    print("\n[FIREWALL RULE AUDITOR]")
    print("  Reading Windows Firewall rules (requires admin for full results)...\n")

    try:
        rules = get_firewall_rules()
    except FileNotFoundError:
        print("  [-] 'netsh' not found. This tool requires Windows.")
        return

    flagged = [r for r in rules if is_permissive(r)]

    print(f"  Total rules loaded : {len(rules)}")
    print(f"  Overly permissive  : {len(flagged)}\n")

    if flagged:
        for rule in flagged[:20]:   # cap output at 20
            name = rule.get("Rule Name", "Unnamed")
            profile = rule.get("Profiles", "?")
            direction = rule.get("Direction", "?")
            print(f"  [!] {name}")
            print(f"      Profile: {profile}  |  Direction: {direction}  |  RemoteIP: Any  |  RemotePort: Any")
    else:
        print("  [+] No overly permissive rules found.")
