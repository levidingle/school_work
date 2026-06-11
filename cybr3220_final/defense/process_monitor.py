# =============================================================================
# Feature: Suspicious Process Monitor (Defense)
# What it does: Lists running processes and flags unusual or high-resource ones.
# Defense value: Detects malware, cryptominers, or unauthorized tools running live.
# Requires: pip install psutil
# =============================================================================

import psutil

# Known-good process names (expand this list for your environment)
WHITELIST = {
    "system", "svchost.exe", "explorer.exe", "python.exe", "pythonw.exe",
    "cmd.exe", "powershell.exe", "taskmgr.exe", "lsass.exe", "services.exe",
    "wininit.exe", "csrss.exe", "smss.exe", "spoolsv.exe", "winlogon.exe",
    "claude.exe", "chrome.exe", "pycharm64.exe", "msedge.exe",
}

CPU_THRESHOLD = 50.0   # percent
MEM_THRESHOLD = 400    # MB


def run():
    print("\n[SUSPICIOUS PROCESS MONITOR]")
    print(f"  Flagging: CPU > {CPU_THRESHOLD}%  |  MEM > {MEM_THRESHOLD} MB\n")

    flagged = []

    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info", "username"]):
        try:
            info = proc.info
            name = info["name"] or "unknown"
            cpu = info["cpu_percent"] or 0.0
            mem_mb = (info["memory_info"].rss / 1024 / 1024) if info["memory_info"] else 0

            reasons = []
            if cpu > CPU_THRESHOLD:
                reasons.append(f"high CPU ({cpu:.1f}%)")
            if mem_mb > MEM_THRESHOLD:
                reasons.append(f"high MEM ({mem_mb:.0f} MB)")

            if reasons:
                flagged.append((info["pid"], name, cpu, mem_mb, ", ".join(reasons)))

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    if flagged:
        print(f"  {'PID':<8} {'Name':<30} {'CPU%':<8} {'MEM(MB)':<10} Reason")
        print("  " + "-" * 70)
        for pid, name, cpu, mem, reason in flagged:
            print(f"  {pid:<8} {name:<30} {cpu:<8.1f} {mem:<10.0f} {reason}")
    else:
        print("  No suspicious processes detected.")
