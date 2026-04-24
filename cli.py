#Client code
from socket import *
import sys, os

if len(sys.argv) != 3:
    print("Usage: python cli.py <server_machine> <port>")
    sys.exit(1)

serverName = sys.argv[1]
serverPort = int(sys.argv[2])

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

def send_msg(sock, msg):
    """Helper to send a message prefixed with a 10-byte size header"""
    if isinstance(msg, str):
        msg = msg.encode()
    size_str = str(len(msg)).zfill(10).encode()
    sock.sendall(size_str + msg)

def recv_msg(sock):
    """Helper to receive a message based on the 10-byte size header"""
    size_buff = b""
    while len(size_buff) < 10:
        chunk = sock.recv(10 - len(size_buff))
        if not chunk:
            return None
        size_buff += chunk

    size = int(size_buff.decode())
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            break
        data += chunk
    return data

def open_data_listener():
    """Create a temporary socket on an ephemeral port for the data channel"""
    dataListenSock = socket(AF_INET, SOCK_STREAM)
    dataListenSock.bind(('', 0))
    ephemeral_port = dataListenSock.getsockname()[1]
    dataListenSock.listen(1)
    return dataListenSock, ephemeral_port

while True:
    client_line = input("ftp> ")
    cmd = client_line.split()
    
    if not cmd:
        continue

    if cmd[0] == "quit":
        send_msg(clientSocket, "quit")
        print("Exiting the client.")
        clientSocket.close()
        break
        
    elif cmd[0] == "ls":
        dataListenSock, eport = open_data_listener()
        send_msg(clientSocket, f"ls {eport}")
        dataSocket, _ = dataListenSock.accept()
        dataListenSock.close()
        res = recv_msg(dataSocket).decode()
        dataSocket.close()
        status = recv_msg(clientSocket).decode()
        print("Listing files on the server:")
        print(res)
        print(status)
        
    elif cmd[0] == "get":
        if len(cmd) == 1:
            print("Please provide a file name...")
        else:
            dataListenSock, eport = open_data_listener()
            send_msg(clientSocket, f"get {cmd[1]} {eport}")
            status = recv_msg(clientSocket).decode()
            
            if status.startswith("FAILURE"):
                dataListenSock.close()
                print("File not found in the server...")
                print(status)
            else:
                filename = f"client/{cmd[1]}"
                dataSocket, _ = dataListenSock.accept()
                dataListenSock.close()
                response = recv_msg(dataSocket)
                dataSocket.close()
                print("Getting file from the server...")
                with open(filename, "wb") as f:
                    f.write(response)
                print(f"Downloaded '{filename}' — {len(response)} bytes transferred.")
                print(status)
                
    elif cmd[0] == "put":
        if len(cmd) == 1:
            print("Please provide a file name...")
        else:
            filename = cmd[1]
            dir = f"{os.getcwd()}/client"
            if not filename in os.listdir(dir):
                print("File not found locally...")
            else:
                print("Putting file in the server...")
                dataListenSock, eport = open_data_listener()
                send_msg(clientSocket, f"put {cmd[1]} {eport}")
                dataSocket, _ = dataListenSock.accept()
                dataListenSock.close()
                with open(f"{dir}/{filename}", "rb") as f:
                    fileData = f.read()
                send_msg(dataSocket, fileData)
                dataSocket.close()
                status = recv_msg(clientSocket).decode()
                print(f"Sent '{cmd[1]}' — {len(fileData)} bytes transferred.")
                print(status)
    else:
        print("Invalid command. Please enter 'ls', 'get', 'put', or 'quit'.")
