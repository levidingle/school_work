# Feature: Port Scanner (Defense)
import socket


def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    """Return True if the TCP port is open on host."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (ConnectionRefusedError, TimeoutError, OSError):
        return False


def run():
    print("\n[PORT SCANNER]")
    host = input("  Target host (IP or hostname): ").strip()
    port_range = input("  Port range (e.g. 1-1024): ").strip()

    try:
        start, end = map(int, port_range.split("-"))
    except ValueError:
        print("[-] Invalid range format. Use start-end (e.g. 1-1024).")
        return

    print(f"\n[*] Scanning {host} ports {start}-{end} ...\n")
    open_ports = []
    for port in range(start, end + 1):
        if scan_port(host, port):
            print(f"  [+] Port {port}/tcp  OPEN")
            open_ports.append(port)

    print(f"\n[*] Scan complete. {len(open_ports)} open port(s) found.")
