# =============================================================================
# Feature: Directory Brute Forcer (Red Team)
# What it is: Discovers hidden web directories by guessing common path names.
# How it works: Sends HTTP GET requests for each word in a wordlist; 200/301 = found.
# How tool does it: requests.get per word, checks status code.
# Defense: Use a WAF with rate limiting; return 404 for all non-existent paths uniformly.
# Requires: pip install requests
# =============================================================================

import requests
from pathlib import Path

DEFAULT_WORDLIST = Path(__file__).parent.parent / "utils" / "wordlist_dirs.txt"


def brute(base_url: str, wordlist_path: str, timeout: float = 5.0) -> list[str]:
    found = []
    with open(wordlist_path, "r", errors="replace") as wl:
        words = [w.strip() for w in wl if w.strip() and not w.startswith("#")]

    print(f"  [*] Loaded {len(words)} words. Scanning ...\n")

    for word in words:
        url = f"{base_url.rstrip('/')}/{word}"
        try:
            resp = requests.get(url, timeout=timeout, allow_redirects=False)
            if resp.status_code in (200, 201, 301, 302, 403):
                print(f"  [+] {resp.status_code}  {url}")
                found.append(url)
        except requests.RequestException:
            pass

    return found


def run():
    print("\n[DIRECTORY BRUTE FORCER]")
    base_url = input("  Target URL (e.g. http://10.0.0.1): ").strip()
    wordlist = input(f"  Wordlist path [{DEFAULT_WORDLIST}]: ").strip() or str(DEFAULT_WORDLIST)

    if not Path(wordlist).exists():
        print(f"  [-] Wordlist not found: {wordlist}")
        return

    found = brute(base_url, wordlist)
    print(f"\n[*] Done. {len(found)} path(s) discovered.")
