# import psutil
# disk = psutil.disk_usage("C:\\")
# print("Total :", round(disk.total / 1024**3, 2), "GB")
# print("used (GB):", round(disk.used / 1024**3, 2), "GB")
# print("free: (GB)", round(disk.free / 1024**3, 2), "GB")
# print("usage (%)", disk.free / disk.total * 100, "%")

# import psutil
# ram = psutil.virtual_memory()
# print("Total : ", round(ram.total /1024**3 ,2), "GB")
# print("Available : ", round(ram.available /1024**3 ,2), "GB")
# print("Used : ", round(ram.used /1024**3 ,2), "GB")
# print("Percent : ",ram.percent, "%")

# import psutil
# import platform
# print("Processor", platform.processor())
# print("Physical cores", psutil.cpu_count(logical=False))
# print("Logical cores", psutil.cpu_count(logical=True))
# print("CPU Usage", psutil.cpu_percent(interval=1) ,"%")

# import platform
# print("OS", platform.system())
# print("Release", platform.release())
# print("Version", platform.version())
# print("Architecture", platform.machine())
# print("Arch", platform.architecture())

# import socket
# import getpass
# print("Computer Name : ", socket.gethostname())
# print("User Name : ", getpass.getuser())

# import socket
# hostname = socket.gethostname()
# ip = socket.gethostbyname(hostname)
# print()
# print("Computer Name:" , hostname)
# print("IP Address: ", ip)

# import psutil
# net_info = psutil.net_if_addrs()
# for interface, address in net_info.items():
#     print("\interface : ", interface)
#     for addr in address:
#         print("Address : ", addr.address)

## Boot Time Info ##
# import psutil
# from datetime import datetime
# boot_time = psutil.boot_time()
# # Convert timestamp to readable date-time
# readable_boot_time = datetime.fromtimestamp(boot_time)
# print(readable_boot_time)
# print("System Boot Time: ", readable_boot_time.strftime('%Y-%m-%d %H:%M:%S'))


## GPU Info ##
# import os
# os.system("wmic path win32_VideoController get name, driverversion")

## BIOS Info ##
# import os
# os.system("wmic bios get manufacturer, name, serialnumber, version")

# ## Motherboard info ##
# import os
# os.system("wmic baseboard get manufacturer")

# import os
# os.system("wmic computersystem get manufacturer, model, systemtype")

## Active network connection ##
import psutil
for conn in psutil.net_connections(kind='inet'):
    print(conn)

