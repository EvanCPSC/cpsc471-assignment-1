from socket import *
import sys, os

if len(sys.argv) != 2:
    print("Usage: python cli.py <port>")
    sys.exit(1)

serverName = 'localhost'
serverPort = int(sys.argv[1]) 

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
    size_buff = sock.recv(10)
    if not size_buff:
        return None
    
    size = int(size_buff.decode())
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            break
        data += chunk
    return data

def validFile(input_str):
    return len(input_str.split(".")) >= 2

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
        elif not validFile(cmd[1]):
            print("Please provide a valid file...")
        else:
            send_msg(clientSocket, f"get {cmd[1]}")
            response = recv_msg(clientSocket)
            
            if response == b"ERROR":
                print("File not found in the server...")
            else:
                print("Getting file from the server...")
                with open(cmd[1], "wb") as f:
                    f.write(response)
                print(f"Downloaded {cmd[1]} successfully.")
                
    elif cmd[0] == "put":
        if len(cmd) == 1:
            print("Please provide a file name...")
        elif not validFile(cmd[1]):
            print("Please provide a valid file...")
        else:
            if cmd[1] not in os.listdir(os.getcwd()):
                print("File not found locally...")
            else:
                print("Putting file in the server...")
                send_msg(clientSocket, f"put {cmd[1]}")
                
                ack = recv_msg(clientSocket).decode()
                if ack == "OK":
                    with open(cmd[1], "rb") as f:
                        fileData = f.read()
                    send_msg(clientSocket, fileData)
                    print("Sent " + cmd[1])
    else:
        print("Invalid command. Please enter 'ls', 'get', 'put', or 'quit'.")