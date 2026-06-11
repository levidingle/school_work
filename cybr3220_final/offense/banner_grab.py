# =============================================================================
# Feature: Banner Grabber (Red Team)
# What it is: Connects to a host/port and reads the service banner.
# How it works: Opens a raw TCP socket and reads the first bytes the service sends.
# How tool does it: socket.connect -> recv -> decode -> display.
# Defense: Disable verbose banners in service configs (e.g., ServerTokens Prod in Apache).
# =============================================================================

import socket


def grab_banner(host: str, port: int, timeout: float = 3.0) -> str | None:
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")   # generic probe
            banner = s.recv(1024).decode(errors="replace").strip()
            return banner
    except (ConnectionRefusedError, TimeoutError, OSError):
        return None


def run():
    print("\n[BANNER GRABBER]")
    host = input("  Target host: ").strip()
    port_input = input("  Port (default 80): ").strip()
    port = int(port_input) if port_input.isdigit() else 80

    print(f"\n[*] Connecting to {host}:{port} ...")
    banner = grab_banner(host, port)

    if banner:
        print(f"\n  --- Banner ---\n{banner}\n")
    else:
        print("  [-] No banner received or connection refused.")
