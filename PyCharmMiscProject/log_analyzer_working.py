import re
from collections import defaultdict
from datetime import datetime

# Path to the log file
LOG_FILE = "mixauth_realistic_1000.log"

# Count failed attempts by IP
failed_attempts = defaultdict(int)

# Count successful logins by IP
success_attempts = defaultdict(int)

# Count failed attempts by username
failed_usernames = defaultdict(int)

# Count successful logins by username
success_usernames = defaultdict(int)

# Count failed attempts by port
failed_ports = defaultdict(int)

# Count successful logins by port
success_ports = defaultdict(int)

# Separate counters for IPv4 and IPv6
ipv4_failed_count = 0
ipv6_failed_count = 0
ipv4_success_count = 0
ipv6_success_count = 0

# Store failed attempt times for each IP
failed_times_by_ip = defaultdict(list)

# Regex patterns
timestamp_pattern = r"^([A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2})"
failed_ip_pattern = r"Failed password for (?:invalid user )?\S+ from ([A-Fa-f0-9:.]+)"
success_ip_pattern = r"Accepted password for \S+ from ([A-Fa-f0-9:.]+)"
failed_username_pattern = r"Failed password for (?:invalid user )?(\S+)"
success_username_pattern = r"Accepted password for (\S+)"
port_pattern = r"port (\d+)"

print("Starting log analysis...\n")

try:
    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # -----------------------------
            # FAILED PASSWORD LOGS
            # -----------------------------
            if "Failed password" in line:
                print("[FAILED LOGIN]", line)

                # Extract timestamp
                time_match = re.search(timestamp_pattern, line)
                if time_match:
                    timestamp_text = time_match.group(1)
                    # Year is not in auth logs, so we add one manually
                    log_time = datetime.strptime("2026 " + timestamp_text, "%Y %b %d %H:%M:%S")
                else:
                    log_time = None

                # Extract IP
                ip_match = re.search(failed_ip_pattern, line)
                if ip_match:
                    ip = ip_match.group(1)
                    failed_attempts[ip] += 1

                    # Save timestamp for time-based attack detection
                    if log_time:
                        failed_times_by_ip[ip].append(log_time)

                    # Count IPv4 vs IPv6
                    if "." in ip and ":" not in ip:
                        ipv4_failed_count += 1
                    else:
                        ipv6_failed_count += 1

                # Extract username
                username_match = re.search(failed_username_pattern, line)
                if username_match:
                    username = username_match.group(1)
                    failed_usernames[username] += 1

                # Extract port
                port_match = re.search(port_pattern, line)
                if port_match:
                    port = port_match.group(1)
                    failed_ports[port] += 1

            # -----------------------------
            # ACCEPTED PASSWORD LOGS
            # -----------------------------
            elif "Accepted password" in line:
                print("[SUCCESS LOGIN]", line)

                # Extract IP
                ip_match = re.search(success_ip_pattern, line)
                if ip_match:
                    ip = ip_match.group(1)
                    success_attempts[ip] += 1

                    # Count IPv4 vs IPv6
                    if "." in ip and ":" not in ip:
                        ipv4_success_count += 1
                    else:
                        ipv6_success_count += 1

                # Extract username
                username_match = re.search(success_username_pattern, line)
                if username_match:
                    username = username_match.group(1)
                    success_usernames[username] += 1

                # Extract port
                port_match = re.search(port_pattern, line)
                if port_match:
                    port = port_match.group(1)
                    success_ports[port] += 1

                count_failed = sum(failed_attempts.values())
                count_success = sum(success_attempts.values())

    # ----------------------------------------
    # SUMMARY 1: Failed attempts by IP
    # ----------------------------------------
    print("\n======================================")
    print("SUMMARY OF FAILED LOGIN ATTEMPTS BY IP")
    print("======================================\n")

    for ip, count in failed_attempts.items():
        print(f"IP Address: {ip} -> Failed Attempts: {count}")

        # Alert if brute-force threshold reached
        # if count >= 5:
        if count >= 3:
            print(f"[ALERT] Possible brute-force attack from IP: {ip}")

    # ----------------------------------------
    # SUMMARY 2: Success attempts by IP
    # ----------------------------------------
    print("\n======================================")
    print("SUMMARY OF SUCCESSFUL LOGIN ATTEMPTS BY IP")
    print("======================================\n")

    for ip, count in success_attempts.items():
        print(f"IP Address: {ip} -> Successful Logins: {count}")

    # ----------------------------------------
    # SUMMARY 3: Attacked usernames
    # ----------------------------------------
    print("\n======================================")
    print("SUMMARY OF ATTACKED USERNAMES")
    print("======================================\n")

    for username, count in failed_usernames.items():
        print(f"Username: {username} -> Failed Attempts: {count}")

    # ----------------------------------------
    # SUMMARY 4: Successful usernames
    # ----------------------------------------
    print("\n======================================")
    print("SUMMARY OF SUCCESSFUL USERNAMES")
    print("======================================\n")

    for username, count in success_usernames.items():
        print(f"Username: {username} -> Successful Logins: {count}")

    # ----------------------------------------
    # SUMMARY 5: Failed ports
    # ----------------------------------------
    print("\n======================================")
    print("SUMMARY OF TARGETED PORT NUMBERS (FAILED)")
    print("======================================\n")

    for port, count in failed_ports.items():
        print(f"Port: {port} -> Failed Attempts: {count}")
        print(f"IP Address: {ip} -> Failed Logins: {count}\n")


    # ----------------------------------------
    # SUMMARY 6: Success ports
    # ----------------------------------------
    print("\n======================================")
    print("SUMMARY OF PORT NUMBERS (SUCCESS)")
    print("======================================\n")

    for port, count in success_ports.items():
        print(f"Port: {port} -> Successful Logins: {count}")

    # ----------------------------------------
    # SUMMARY 7: IPv4 and IPv6 counts
    # ----------------------------------------
    print("\n======================================")
    print("SEPARATE IPv4 AND IPv6 COUNTS")
    print("======================================\n")

    print(f"Total IPv4 failed login entries: {ipv4_failed_count}")
    print(f"Total IPv6 failed login entries: {ipv6_failed_count}")
    print(f"Total IPv4 successful login entries: {ipv4_success_count}")
    print(f"Total IPv6 successful login entries: {ipv6_success_count}")

    # ----------------------------------------
    # SUMMARY 8: Time-based attack detection
    # Rule: 5 failed attempts in 10 seconds
    # ----------------------------------------
    print("\n======================================")
    print("TIME-BASED ATTACK DETECTION")
    print("======================================\n")

    found_time_attack = False

    for ip, times in failed_times_by_ip.items():
        times.sort()

        for i in range(len(times) - 4):
            first_time = times[i]
            fifth_time = times[i + 4]

            time_difference = (fifth_time - first_time).total_seconds()

            if time_difference <= 10:
                print(f"[TIME ALERT] IP {ip} made 5 failed attempts within {int(time_difference)} seconds")
                print(f"    Start Time: {first_time}")
                print(f"    End Time  : {fifth_time}")
                found_time_attack = True
                break

    if not found_time_attack:
        print("No IP made 3 failed attempts within 10 seconds.")

    # ----------------------------------------
    # SUMMARY 9: Mixed behavior detection
    # IPs with both failed and successful logins
    # ----------------------------------------
    print("\n======================================")
    print("MIXED SUCCESS + FAILURE DETECTION")
    print("======================================\n")
    print(f"\n Failed Logins = {count_failed}")
    print(f"\n Successful Logins = {count_success}")
    mixed_found = False

    all_ips = set(list(failed_attempts.keys()) + list(success_attempts.keys()))

    for ip in all_ips:
        if ip in failed_attempts and ip in success_attempts:
            print(f"[MIXED ACTIVITY] IP {ip} has both failed and successful logins")
            print(f"    Failed Attempts    : {failed_attempts[ip]}")
            print(f"    Successful Logins  : {success_attempts[ip]}")
            mixed_found = True

    if not mixed_found:
        print("No IPs were found with both failed and successful logins.")

except FileNotFoundError:
    print(f"Error: the file '{LOG_FILE}' was not found.")
except Exception as e:
    print(f"Unexpected error: {e}")




# Task 1: Count failed logins
# Hint sum(failed_attempts.values())
# Task 2: Count Total successful Logins
# Hint sum(success_attempts.values())
# Task 3: Display attacking IPs
# Hint sorted(failed_attempts.items(), key=lamda x: x[1], reverse=True)
# Task 4: Detect suspicious Ports

# DONE
# Task 5: Modify brute force threshold current >= 5 new : >=3














