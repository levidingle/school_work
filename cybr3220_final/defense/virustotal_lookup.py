# =============================================================================
# Feature: VirusTotal File Hash Lookup (Defense)
# What it does: Hashes a local file and queries the VirusTotal API for detections.
# Defense value: Quick triage of suspicious files without uploading them.
# Requires: pip install requests  |  Set VT_API_KEY env var or enter at runtime.
# =============================================================================

import hashlib
import os
import requests


VT_URL = "https://www.virustotal.com/api/v3/files/{}"


def sha256_file(path: str) -> str:
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()


def query_virustotal(file_hash: str, api_key: str) -> dict:
    headers = {"x-apikey": api_key}
    response = requests.get(VT_URL.format(file_hash), headers=headers, timeout=15)
    response.raise_for_status()
    return response.json()


def run():
    print("\n[VIRUSTOTAL FILE HASH LOOKUP]")
    file_path = input("  Path to file: ").strip()

    if not os.path.isfile(file_path):
        print("[-] File not found.")
        return

    api_key = os.environ.get("VT_API_KEY") or input("  VirusTotal API key: ").strip()
    if not api_key:
        print("[-] No API key provided.")
        return

    file_hash = sha256_file(file_path)
    print(f"  SHA-256: {file_hash}")
    print("  Querying VirusTotal ...")

    try:
        data = query_virustotal(file_hash, api_key)
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            print("  [?] File not found in VirusTotal database.")
        else:
            print(f"  [-] API error: {e}")
        return
    except requests.RequestException as e:
        print(f"  [-] Network error: {e}")
        return

    stats = data["data"]["attributes"]["last_analysis_stats"]
    malicious = stats.get("malicious", 0)
    total = sum(stats.values())

    print(f"\n  Detections : {malicious}/{total} engines flagged this file")
    print(f"  Harmless   : {stats.get('harmless', 0)}")
    print(f"  Suspicious : {stats.get('suspicious', 0)}")
    print(f"  Undetected : {stats.get('undetected', 0)}")

    if malicious > 0:
        print(f"\n  [!] WARNING: {malicious} engine(s) detected this as malicious!")
    else:
        print("\n  [+] No detections found.")
