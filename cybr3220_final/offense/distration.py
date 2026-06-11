# =============================================================================
# Feature: Distraction - Annoying Beep (Red Team)
# What it is: Plays a series of loud, high-pitched beeps on the target machine.
# How it works: Uses the Windows winsound module to emit system beeps.
# How tool does it: winsound.Beep(frequency, duration) called in a loop.
# Defense: Disable system speaker/audio in BIOS or mute system sounds via policy.
# Platform: Windows only.
# =============================================================================

import winsound
import time


def run():
    print("\n[DISTRACTION - ANNOYING BEEP]")
    print("  Plays high-pitched beeps on this machine.")

    print("  [*] Beeping ...")
    for i in range(5):
        # winsound.Beep(1000, 1000) # This is what Amalan did, but my sound is better.
        winsound.Beep(1000, 1000)
        time.sleep(0.5)

    print("  [+] Done.")
