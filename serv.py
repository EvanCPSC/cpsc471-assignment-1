#Server code
from socket import * 
import sys
import os

if len(sys.argv) != 2:
    print("Usage: python serv.py <port>")
    sys.exit(1)

serverPort = int(sys.argv[1])

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))

serverSocket.listen(1)
print("The server is ready to receive")

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

def open_data_connection(client_ip, data_port):
    """Connect to the client's ephemeral data port"""
    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.connect((client_ip, data_port))
    return dataSocket

while True:
    connectionSocket, addr = serverSocket.accept()
    client_ip = addr[0]
    print("Received connection from: ", addr)

    while True:
        request = recv_msg(connectionSocket)
        if not request:
            print("Client disconnected.")
            break
        
        req_str = request.decode()
        cmd = req_str.split()

        if cmd[0] == "quit":
            print("Client requested to quit.")
            break
            
        elif cmd[0] == "ls":
            data_port = int(cmd[1])
            print("Executing 'ls' command...")
            ls = os.listdir(os.getcwd())
            res = "  ".join(ls)
            dataSocket = open_data_connection(client_ip, data_port)
            send_msg(dataSocket, res)
            dataSocket.close()
            send_msg(connectionSocket, "SUCCESS: ls complete.")
            
        elif cmd[0] == "get":
            filename = cmd[1]
            data_port = int(cmd[2])
            print(f"Client requested to get: {filename}")
            if filename in os.listdir(os.getcwd()):
                with open(filename, "rb") as f:
                    fileData = f.read()
                dataSocket = open_data_connection(client_ip, data_port)
                send_msg(dataSocket, fileData)
                dataSocket.close()
                send_msg(connectionSocket, f"SUCCESS: {filename} {len(fileData)} bytes transferred.")
            else:
                send_msg(connectionSocket, f"FAILURE: File '{filename}' not found.")
                
        elif cmd[0] == "put":
            filename = cmd[1]
            data_port = int(cmd[2])
            print(f"Client putting file: {filename}")
            dataSocket = open_data_connection(client_ip, data_port)
            fileData = recv_msg(dataSocket)
            dataSocket.close()
            with open(filename, "wb") as f:
                f.write(fileData)
            print(f"Successfully received and saved {filename}")
            send_msg(connectionSocket, f"SUCCESS: {filename} {len(fileData)} bytes received.")

    connectionSocket.close()