# =============================================================================
# Feature: DNS Enumerator (Red Team)
# What it is: Discovers subdomains and DNS records for a target domain.
# How it works: Queries A, MX, NS, TXT records via DNS over HTTPS (port 443).
# How tool does it: Uses Cloudflare DoH API + brute-forces common subdomains.
# Defense: Limit DNS zone transfers; don't expose internal hostnames publicly.
# Requires: pip install requests
# =============================================================================

import requests

DOH_URL = "https://cloudflare-dns.com/dns-query"
RECORD_TYPES = ["A", "MX", "NS", "TXT", "CNAME"]

COMMON_SUBS = [
    "www", "mail", "ftp", "webmail", "remote", "vpn", "dev",
    "staging", "api", "admin", "portal", "test", "git", "ssh",
]


def doh_query(domain: str, rtype: str) -> list:
    """Query DNS over HTTPS using Cloudflare's DoH API."""
    try:
        resp = requests.get(
            DOH_URL,
            headers={"accept": "application/dns-json"},
            params={"name": domain, "type": rtype},
            timeout=10
        )
        data = resp.json()
        answers = data.get("Answer", [])
        return [a["data"] for a in answers]
    except Exception:
        return []


def query_records(domain: str):
    for rtype in RECORD_TYPES:
        results = doh_query(domain, rtype)
        for record in results:
            print(f"  [{rtype:6}] {record}")


def brute_subdomains(domain: str):
    print("\n  [*] Brute-forcing common subdomains ...")
    found = []
    for sub in COMMON_SUBS:
        fqdn = f"{sub}.{domain}"
        results = doh_query(fqdn, "A")
        for ip in results:
            print(f"  [+] {fqdn:40s} -> {ip}")
            found.append(fqdn)
    return found


def run():
    print("\n[DNS ENUMERATOR]")
    domain = input("  Target domain (e.g. example.com): ").strip()

    print(f"\n  --- DNS Records for {domain} ---")
    query_records(domain)
    brute_subdomains(domain)
    print("\n[*] DNS enumeration complete.")
