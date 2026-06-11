# =============================================================================
# Feature: Hash Cracker (Red Team)
# What it is: Attempts to recover a plaintext password from a hash via dictionary attack.
# How it works: Hashes each word in a wordlist and compares to the target hash.
# How tool does it: hashlib.md5/sha1/sha256 per word, compare hex digests.
# Defense: Use salted hashing (bcrypt/argon2); slow hashing defeats dictionary attacks.
# =============================================================================

import hashlib
from pathlib import Path

DEFAULT_WORDLIST = Path(__file__).parent.parent / "utils" / "wordlist_passwords.txt"

SUPPORTED = {
    "md5":    hashlib.md5,
    "sha1":   hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}


def crack(target_hash: str, algo: str, wordlist_path: str) -> str | None:
    h_func = SUPPORTED[algo]
    target = target_hash.lower().strip()

    with open(wordlist_path, "r", errors="replace") as f:
        for word in f:
            word = word.strip()
            if not word:
                continue
            candidate = h_func(word.encode()).hexdigest()
            if candidate == target:
                return word
    return None


def run():
    print("\n[HASH CRACKER]")
    target = input("  Target hash: ").strip()
    algorithm = input(f"  Algorithm [{'/'.join(SUPPORTED)}] (default sha256): ").strip().lower() or "sha256"

    if algorithm not in SUPPORTED:
        print(f"  [-] Unsupported algorithm. Choose from: {', '.join(SUPPORTED)}")
        return

    wordlist = input(f"  Wordlist [{DEFAULT_WORDLIST}]: ").strip() or str(DEFAULT_WORDLIST)

    if not Path(wordlist).exists():
        print(f"  [-] Wordlist not found: {wordlist}")
        return

    print(f"\n  [*] Cracking {algorithm.upper()} hash ...")
    result = crack(target, algorithm, wordlist)

    if result:
        print(f"\n  [+] CRACKED: {target} => \"{result}\"")
    else:
        print("\n  [-] Hash not cracked with provided wordlist.")
