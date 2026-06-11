import psutil

connections = psutil.net_connections()

for conn in connections:
    if conn.raddr:
        print("Local:", conn.laddr, "Remote:", conn.raddr, "Status:", conn.status)
        