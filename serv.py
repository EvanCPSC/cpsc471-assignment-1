#Server code
from socket import * 
import sys

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

    #Receive the data from the client
    data = connectionSocket.recv(1024).decode()
    print("Received data: ", data)

    #Send the same data back to the client (echo)
    connectionSocket.send(data.encode())
    print("Sent data back to client")

    #Close the connection socket
    connectionSocket.close()

