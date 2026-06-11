# =============================================================================
# Feature: Log Analyzer (Defense)
# What it does: Scans a log file for suspicious patterns (failed logins, etc.).
# Defense value: Early detection of brute-force attempts and anomalous activity.
# =============================================================================

import re
from collections import Counter

# Regex patterns to flag as suspicious
PATTERNS = {
    "Failed login":     re.compile(r"(failed|invalid|incorrect).*(password|login|auth)", re.IGNORECASE),
    "Root login":       re.compile(r"(root|administrator)\s+login", re.IGNORECASE),
    "SQL injection":    re.compile(r"(select|union|insert|drop|--|;)\s", re.IGNORECASE),
    "Path traversal":   re.compile(r"\.\./|\.\.\%2[Ff]"),
    "Port scan noise":  re.compile(r"(syn|ack|rst).*(flood|scan)", re.IGNORECASE),
}


def analyze(log_path: str):
    hits = {name: [] for name in PATTERNS}
    ip_counter = Counter()

    ip_pattern = re.compile(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b")

    with open(log_path, "r", errors="replace") as f:
        for lineno, line in enumerate(f, 1):
            for name, pattern in PATTERNS.items():
                if pattern.search(line):
                    hits[name].append((lineno, line.rstrip()))
            for ip in ip_pattern.findall(line):
                ip_counter[ip] += 1

    return hits, ip_counter


def run():
    print("\n[LOG ANALYZER]")
    log_path = input("  Path to log file: ").strip()

    try:
        hits, ip_counter = analyze(log_path)
    except FileNotFoundError:
        print("[-] File not found.")
        return

    print("\n--- Suspicious Pattern Matches ---")
    total = 0
    for name, lines in hits.items():
        if lines:
            print(f"\n  [{name}] — {len(lines)} hit(s)")
            for lineno, text in lines[:5]:    # show first 5 matches
                print(f"    Line {lineno}: {text[:120]}")
            total += len(lines)

    if total == 0:
        print("  No suspicious patterns found.")

    print("\n--- Top 5 IPs by Frequency ---")
    for ip, count in ip_counter.most_common(5):
        print(f"  {ip:20s}  {count} occurrences")
