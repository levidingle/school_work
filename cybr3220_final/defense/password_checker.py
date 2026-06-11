# =============================================================================
# Feature: Password Strength Checker (Defense)
# What it does: Evaluates password entropy and checks against a common-passwords list.
# Defense value: Helps users and admins enforce strong password policies.
# =============================================================================

import string

# A small built-in list; supplement with rockyou-top1000.txt for real use
COMMON_PASSWORDS = {
    "password", "123456", "password1", "qwerty", "abc123",
    "letmein", "welcome", "monkey", "dragon", "iloveyou",
    "admin", "login", "passw0rd", "master", "sunshine",
}



def score(password: str) -> tuple[int, list[str]]:
    """Return (score 0-5, list of feedback messages)."""
    feedback = []
    pts = 0

    if password.lower() in COMMON_PASSWORDS:
        return 0, ["Password is in the common-passwords list — change it immediately."]

    if len(password) >= 8:
        pts += 1
    else:
        feedback.append("Use at least 8 characters.")

    if len(password) >= 14:
        pts += 1

    if any(c in string.ascii_uppercase for c in password):
        pts += 1
    else:
        feedback.append("Add uppercase letters.")

    if any(c in string.digits for c in password):
        pts += 1
    else:
        feedback.append("Add numbers.")

    if any(c in string.punctuation for c in password):
        pts += 1
    else:
        feedback.append("Add special characters (!@#$...).")

    return pts, feedback


STRENGTH_LABELS = {0: "VERY WEAK, advise changing immediately", 1: "WEAK, advise changing immediately", 2: "FAIR, advise changing", 3: "MODERATE, still advise changing it", 4: "STRONG, good password", 5: "VERY STRONG, great job"}


def run():
    print("\n[PASSWORD STRENGTH CHECKER]")
    password = input("  Enter password: ")

    pts, feedback = score(password)
    label = STRENGTH_LABELS.get(pts, "UNKNOWN")

    print(f"\n  Strength : {label} ({pts}/5)")

    if feedback:
        print("\n  Suggestions:")
        for tip in feedback:
            print(f"    - {tip}")
    else:
        print("  No issues found.")
