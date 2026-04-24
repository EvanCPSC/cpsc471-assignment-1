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
        send_msg(clientSocket, "ls")
        res = recv_msg(clientSocket).decode()
        print("Listing files on the server:")
        print(res)
        
    elif cmd[0] == "get":
        if len(cmd) == 1:
            print("Please provide a file name...")
        else:
            send_msg(clientSocket, f"get {cmd[1]}")
            response = recv_msg(clientSocket)
            
            if response == b"ERROR":
                print("File not found in the server...")
            else:
                print("Getting file from the server...")
                with open(cmd[1], "wb") as f:
                    f.write(response)
                print(f"Downloaded '{cmd[1]}' successfully.")
                
    elif cmd[0] == "put":
        if len(cmd) == 1:
            print("Please provide a file name...")
        else:
            if not os.path.isfile(cmd[1]):
                print("File not found locally...")
            else:
                print("Putting file in the server...")
                send_msg(clientSocket, f"put {cmd[1]}")
                
                ack = recv_msg(clientSocket).decode()
                if ack == "OK":
                    with open(cmd[1], "rb") as f:
                        fileData = f.read()
                    send_msg(clientSocket, fileData)
                    print(f"Sent '{cmd[1]}'.")
    else:
        print("Invalid command. Please enter 'ls', 'get', 'put', or 'quit'.")
