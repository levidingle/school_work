import socket
import time
import threading
from queue import Queue
BRIGHT_MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"
socket.setdefaulttimeout(0.55)
thread_lock = threading.Lock()

def banner1():
    print(BRIGHT_MAGENTA + BOLD + r""" __     __     __     __         _____        __   __     ______     ______      __     __     ______     __     ______     _____        ______   ______     ______     __         ______    
/\ \  _ \ \   /\ \   /\ \       /\  __-.     /\ "-.\ \   /\  __ \   /\__  _\    /\ \  _ \ \   /\  ___\   /\ \   /\  == \   /\  __-.     /\__  _\ /\  __ \   /\  __ \   /\ \       /\  ___\   
\ \ \/ ".\ \  \ \ \  \ \ \____  \ \ \/\ \    \ \ \-.  \  \ \ \/\ \  \/_/\ \/    \ \ \/ ".\ \  \ \  __\   \ \ \  \ \  __<   \ \ \/\ \    \/_/\ \/ \ \ \/\ \  \ \ \/\ \  \ \ \____  \ \___  \  
 \ \__/".~\_\  \ \_\  \ \_____\  \ \____-     \ \_\\"\_\  \ \_____\    \ \_\     \ \__/".~\_\  \ \_____\  \ \_\  \ \_\ \_\  \ \____-       \ \_\  \ \_____\  \ \_____\  \ \_____\  \/\_____\ 
  \/_/   \/_/   \/_/   \/_____/   \/____/      \/_/ \/_/   \/_____/     \/_/      \/_/   \/_/   \/_____/   \/_/   \/_/ /_/   \/____/        \/_/   \/_____/   \/_____/   \/_____/   \/_____/ 
                                                                                                                                                                                             """+ RESET)


banner1()


#Get target IP and port from user input

print('='*50)
print('Advanced Port and Vulnerability Scanner Lab-01')
print('='*50)
target_IP = input('Please enter the target IP address: ')
port_start = eval(input('Please enter the start port number: '))
port_stop = eval(input('Please enter the stop port number: '))
print('-'*50)

print('Scanning Host for selected ports ', target_IP)

#definte our port scan process
def portscan(port):
    # create socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #try to connect
    try:
        #create/open connection
        conx = s.connect((target_IP, port))

        # don't let threat screw up printing
        with thread_lock:
            print(port, 'is open')

        conx.close()
    except:
        pass

def portThreader():
    while True:
        thisPortToScan = q.get()
        # Gets a port from queue

        portscan(thisPortToScan)
        #run the job with available port

        q.task_done()


#create queue
q = Queue()

#start time
startTime = time.time()

#200 threads
for x in range(200):
    #thread id
    t = threading.Thread(target=portThreader)
    #classifying as a daemon, so they will die when the main dies
    t.daemon = True
    #begins, must come after daemon definition
    t.start()
    #ports passed to the queue
for thisPort in range(port_start, port_stop):
    q.put(thisPort)
#wait until thread terminates
q.join()
    #thread ID
# Print final time report
runtime = float("%0.2f" % (time.time() - startTime))
print('-'*50)
print("Run Time: ", runtime, " Seconds")
print('-'*50)