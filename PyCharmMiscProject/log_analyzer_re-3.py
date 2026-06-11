import re
# A built-in Python module that provides specialized container data types.
from collections import defaultdict



# Path to the log file
LOG_FILE = "mixauth2.log"

failed_attempts = defaultdict(int)
# Dictionary to count failed login attempts by username
failed_username = defaultdict(int)
# Dictionary to count failed attempts by port number
failed_ports = defaultdict(int)
# Separate counters for IPv4 or 6
ipv4_count = 0
ipv6_count = 0

# Regular Expression to extract IPv4 or 6 address
# ip_pattern = r"((?:\d{1,3}\.){3}\d{1,3}|(?:(?:[A-Fa-f0-9]{1,4}:){1,7}[A-Fa-f0-9]{0,4}|::1|::|[A-Fa-f0-9]{0,4}::[A-Fa-f0-9:]*))"
# ip_pattern = r"\b((?:\d{1,3}\.){3}\d{1,3}|(?:[A-Fa-f0-9]{1,4}:){2,7}[A-Fa-f0-9]{1,4}|::1|::)\b"
# ip_pattern = r"\b((?:\d{1,3}\.){3}\d{1,3}|(?:[A-Fa-f0-9]{1,4}:){1,7}:|:(?::[A-Fa-f0-9]{1,4}){1,7}|(?:[A-Fa-f0-9]{1,4}:){1,6}:[A-Fa-f0-9]{1,4}|::1|::)\b"
ip_pattern = r"from\s+([A-Fa-f0-9:.]+)"
# Regex to extract username after "for" or "For invalid user"
username_pattern = r"Failed password for (?:invalid user )?(\S+)"

# Regex to extract port number
port_pattern = r"port (\d+)"

print("Starting log analysis...\n")
try:
    with open(LOG_FILE, "r") as file: # Open the log file in read mode
        for line in file:
            if "Failed password" in line:
                print("[FAILED LOGIN]", line.strip())

                # Search for IP address
                ip_match = re.search(ip_pattern, line)
                if ip_match:
                    ip = ip_match.group(1)
                    failed_attempts[ip] += 1

                    # Check if IP is IPv4 or 6
                    if "." in ip:
                        ipv4_count += 1
                    elif ":" in ip:
                        ipv6_count += 1
                # Search for attacked username
                username_match = re.search(username_pattern, line)
                if username_match:
                    username = username_match.group(1)
                    failed_username[username] += 1

                # Search for port number
                port_match = re.search(port_pattern, line)
                if port_match:
                    port = port_match.group(1)
                    failed_ports[port] += 1

    print("\n Summary of failed login attempts by IP: \n")
    for ip, count in failed_attempts.items():
        print(f"IP Address: {ip} -> Failed attempts: {count}")
        # Raise alert if attempts are above threshold
        if count >= 5:
            print(f"[ALERT] Possible brute-force attack from IP: {ip}")
    print("\n Summary of attacked usernames: \n")
    for username, count in failed_username.items():
        print(f"Username: {username} -> Failed attempts: {count}")

    print("\n Summary of attacked port numbers: \n")
    for port, count in failed_ports.items():
        print(f"Port: {port} -> Failed attempts: {count}")

    print("\n Separate IP version counts: \n")
    print(f"Total IPv4 failed login entries: {ipv4_count}")
    print(f"Total IPv6 failed login entries: {ipv6_count}")

except FileNotFoundError:
    print(f"File not found: {LOG_FILE}")
except Exception as e:
    print(f"Unexpected error: {e}")















