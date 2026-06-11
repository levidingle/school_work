import re
#A built-in Python module that provides specialized container data types.
from collections import defaultdict
## Path to the log file
LOG_FILE = "log_file.log"
# Dictionary to count failed login attempts by IP address
failed_attempts = defaultdict(int)
## Regular expression to extract IP addresses
ip_pattern = r"((?:\d{1,3}\.){3}\d{1,3}|(?:[a-fA-F0-9:]+:+)+[a-fA-F0-9]+)"
print("Starting log analysis...\n")
try:
    with open(LOG_FILE, "r") as file: # Open the log file in read mode
        for line in file: # Check if the line contains a failed password attempt
            if "Failed password" in line:
                print("[FAILED LOGIN]", line.strip())

                ip_match = re.search(ip_pattern, line)  # Search for an IP address in the line
                if ip_match:
                    ip = ip_match.group(1)
                    failed_attempts[ip] += 1
    print("\n Summary of failed login attempts by IP: \n")

    # Print counts for each IP
    for ip, count in failed_attempts.items():
        print(f"IP Address: {ip} -> Failed Attempts: {count}")

        # Raise alert if attempts are above threshold
        if count >=5:
            print(f"[ALERT] Possible brute-force attack from IP: {ip}")
except FileNotFoundError:
    print(f"Error: the file '{LOG_FILE}' was not found.")
except Exception as e:
    print(f"Unexpected error: {e}")