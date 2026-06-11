# Import module to validate both IPv4 and IPv6 addresses
import ipaddress

# Import defaultdict to automatically initialize dictionary values
from collections import defaultdict

# Path to the log file
log_file = "log_file.log"

# Dictionary to store count of failed login attempts per IP
# defaultdict(int) automatically sets default value = 0
failed_attempts = defaultdict(int)
print("Starting log analysis...\n")

try:
    with open(log_file, "r", encoding = "utf-8") as file: # Open the log file in read mode
        for line in file: # Read the file line by line

            if "Failed password" in line: # Check if line contains failed login attempt
                print("FAILED LOGIN ATTEMPT", line.strip()) # Print the failed login attempt
                words = line.split() # Split the line into words (Tokens)

                for word in words: # Loop through each word to find an IP address
                    cleaned_word = word.strip("[](),") # Clean unwanted characters (Like brackets, commas and parenthesis)
                    try:
                        ip = str(ipaddress.ip_address(cleaned_word)) # Validate if the word is a valid IPv4 or 6 address
                        failed_attempts[ip] += 1 # If valid, increase the failed attempt count
                        # Stop checking further woreds once IP is found
                        break
                    except ValueError:
                        continue # If not a valid IP, ignore and continue

    # Print summary
    print("\n Summary of failed login attempts by IP: \n")
    # Check if any failed attempts were recorded
    if failed_attempts:
        for ip, count in failed_attempts.items(): # Loop through each IP and its count
            print(f"IP Address: {ip} -> Failed attempts: {count}")
            # Alert if attempts exceed threshold (e.g. brute force attacks)
            if count >= 5:
                print(f"[ALERT] Possible brute-force attack from IP: {ip}")
    else:
        print("No failed login attempts found")
# Handle case where log file does not exist
except FileNotFoundError:
    print("[ERROR] Log File Not Found")
except Exception as e:
    print(f"Unexpected error: {e}")




