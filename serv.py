#Server code
from socket import * 
import sys
import subprocess

#Check if the correct number of command-line arguments is provided
if(len(sys.argv) != 2):
    print("Usage: python serv.py <port>")
    sys.exit(1)

#The port on which to listen - should be passed as a command-line argument (int is used for typecasting)
serverPort = int(sys.argv[1])

#Create a TCP server socket
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))

#Start listening for incoming connections
serverSocket.listen(1)
print("The server is ready to receive")

#Bugger to store the received data
data = ""

#Forever loop to accept and process incoming connections
while True:
    #Accept a connection from the client
    connectionSocket, addr = serverSocket.accept()
    print("Received connection from: ", addr)

    # Inner loop to keep the control channel open 
    while True:
        #Receive the data from the client
        data = connectionSocket.recv(1024).decode()
        if not data:
            break

        print("Received data: ", data)
        parts = data.split()
        command = parts[0]

        if command == "ls" and len(parts) > 1:
            client_data_port = int(parts[1])
            try:
                ls_output = subprocess.getoutput("ls")
                dataSocket = socket(AF_INET, SOCK_STREAM)
                dataSocket.connect((addr[0], client_data_port))
                
                dataSocket.sendall(ls_output.encode())

                dataSocket.close()
                print("SUCCESS")
                connectionSocket.send("SUCCESS".encode()) 
            except Exception as e:
                print(f"FAILURE: {e}")
                connectionSocket.send(f"FAILURE: {e}".encode())
        
        elif command == "quit":
                break

    connectionSocket.close()