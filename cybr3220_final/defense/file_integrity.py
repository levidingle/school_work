# =============================================================================
# Feature: File Integrity Monitor (Defense)
# What it does: Hashes files in a directory and detects changes over time.
# Defense value: Detects unauthorized modification of critical files (FIM).
# =============================================================================

import hashlib
import json
import os
from pathlib import Path

BASELINE_FILE = "fim_baseline.json"


def hash_file(path: str) -> str:
    """Return the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def build_baseline(directory: str) -> dict:
    """Walk directory and hash every file; return {path: hash} mapping."""
    baseline = {}
    for root, _, files in os.walk(directory):
        for name in files:
            full_path = os.path.join(root, name)
            try:
                baseline[full_path] = hash_file(full_path)
            except (PermissionError, OSError):
                pass
    return baseline


def run():
    print("\n[FILE INTEGRITY MONITOR]")
    print("  [1] Create baseline")
    print("  [2] Check against baseline")
    choice = input("  Select: ").strip()

    directory = input("  Directory to monitor: ").strip()

    if choice == "1":
        baseline = build_baseline(directory)
        with open(BASELINE_FILE, "w") as f:
            json.dump(baseline, f, indent=2)
        print(f"[+] Baseline saved to {BASELINE_FILE} ({len(baseline)} files hashed).")

    elif choice == "2":
        if not Path(BASELINE_FILE).exists():
            print("[-] No baseline found. Create one first.")
            return
        with open(BASELINE_FILE) as f:
            baseline = json.load(f)

        current = build_baseline(directory)
        changed, added, removed = [], [], []

        for path, old_hash in baseline.items():
            if path not in current:
                removed.append(path)
            elif current[path] != old_hash:
                changed.append(path)

        for path in current:
            if path not in baseline:
                added.append(path)

        for p in changed:
            print(f"  [!] MODIFIED : {p}")
        for p in added:
            print(f"  [+] ADDED    : {p}")
        for p in removed:
            print(f"  [-] REMOVED  : {p}")

        if not any([changed, added, removed]):
            print("[+] No changes detected.")
    else:
        print("[-] Invalid option.")
