import psutil

print("Detect Too Many SYN_SENT - Possible Scanning")
count = 0

for conn in psutil.net_connections(kind="inet"):
    if conn.status == "SYN_SENT":
        count += 1
        print("SYN_SENT To :", conn.raddr)

    if count > 5 :
        print("Possible scanning activity detected.")